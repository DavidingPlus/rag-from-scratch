"""同步 notebooks 下的 Python 任务和项目依赖。

用法：
    python scripts/sync.py
    python scripts/sync.py --dry-run

脚本只会新增缺失的 Poe 任务和 requirements 条目，不会删除用户已有的配置。
"""

from __future__ import annotations

import argparse
import ast
import importlib.metadata
import re
import sys
from pathlib import Path


# import 名称和 PyPI 发行包名称并不总是一致。这里放项目中已经用到的包，以及几个常见的名称映射；其余包会优先从当前环境查询，最后才按 import_name -> import-name 推断。
REQUIREMENT_OVERRIDES = {
    "llama_index.readers.file": "llama-index-readers-file~=0.1.0",
    "llama_index.readers.web": "llama-index-readers-web~=0.1.0",
    "llama_index.text_splitter": "llama-index~=0.9.0",
    "llama_index": "llama-index-core~=0.10.0",
    "langchain.text_splitter": "langchain",
    "dotenv": "python-dotenv",
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "dateutil": "python-dateutil",
    "sklearn": "scikit-learn",
}

FALLBACK_STDLIB_MODULES = {
    "argparse",
    "ast",
    "asyncio",
    "collections",
    "contextlib",
    "dataclasses",
    "datetime",
    "functools",
    "glob",
    "hashlib",
    "importlib",
    "inspect",
    "io",
    "itertools",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "platform",
    "re",
    "shutil",
    "statistics",
    "string",
    "subprocess",
    "sys",
    "tempfile",
    "textwrap",
    "time",
    "traceback",
    "typing",
    "unittest",
    "urllib",
    "uuid",
    "warnings",
    "xml",
}

TASK_SECTION = "[tool.poe.tasks]"
SECTION_PATTERN = re.compile(r"(?m)^[ \t]*\[[^\]\r\n]+\][ \t]*\r?$")
TASK_NAME_PATTERN = re.compile(
    r'(?m)^[ \t]*(?:"([^"]+)"|([A-Za-z_][A-Za-z0-9_-]*))[ \t]*='
)
REQUIREMENT_NAME_PATTERN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)")


def read_text(path: Path) -> str:
    """读取文本并保留原始换行符。"""
    with path.open("r", encoding="utf-8", newline="") as file:
        return file.read()


def write_text(path: Path, content: str) -> None:
    """写入 UTF-8 文本，不额外转换换行符。"""
    with path.open("w", encoding="utf-8", newline="") as file:
        file.write(content)


def newline_for(content: str) -> str:
    return "\r\n" if "\r\n" in content else "\n"


def python_files(scan_dir: Path) -> list[Path]:
    """找出可作为 Poe 任务的 Python 文件。"""
    return sorted(
        path
        for path in scan_dir.rglob("*.py")
        if path.is_file() and path.name != "__init__.py"
    )


def normalise_task_part(part: str) -> str:
    part = re.sub(r"[^A-Za-z0-9]+", "_", part)
    return part.strip("_").lower()


def task_name_for(path: Path, scan_dir: Path) -> str:
    """按项目约定将 notebooks/module1/01/example.py 转成任务名。"""
    relative = path.relative_to(scan_dir)
    parts = list(relative.parts)
    parts[-1] = Path(parts[-1]).stem

    if parts and (match := re.fullmatch(r"module(\d+)", parts[0], re.IGNORECASE)):
        parts[0] = f"m{match.group(1)}"

    normalised_parts = [normalise_task_part(part) for part in parts]
    normalised_parts = [part for part in normalised_parts if part]
    if not normalised_parts:
        raise ValueError(f"无法为文件生成任务名：{path}")
    return "n_" + "_".join(normalised_parts)


def task_command_for(path: Path, project_root: Path) -> str:
    return f'{{cmd = "python {path.relative_to(project_root).as_posix()}"}}'


def task_section_bounds(content: str) -> tuple[int, int] | None:
    """返回 [tool.poe.tasks] 内容区间，不含 section 标题。"""
    section_match = re.search(
        r"(?m)^[ \t]*\[tool\.poe\.tasks\][ \t]*\r?$", content
    )
    if section_match is None:
        return None

    body_start = section_match.end()
    if content.startswith("\n", body_start):
        body_start += 1
    next_section = SECTION_PATTERN.search(content, body_start)
    body_end = next_section.start() if next_section else len(content)
    return body_start, body_end


def existing_task_names(content: str) -> set[str]:
    bounds = task_section_bounds(content)
    if bounds is None:
        return set()

    body = content[bounds[0]: bounds[1]]
    names = set()
    for match in TASK_NAME_PATTERN.finditer(body):
        names.add(match.group(1) or match.group(2))
    return names


def add_tasks(content: str, tasks: dict[str, str]) -> tuple[str, list[str]]:
    """向 Poe 任务区追加缺失任务，保留已有内容和任务。"""
    if not tasks:
        return content, []

    newline = newline_for(content)
    task_lines = newline.join(
        f"{name} = {command}" for name, command in sorted(tasks.items())
    )
    bounds = task_section_bounds(content)

    if bounds is None:
        suffix = "" if not content or content.endswith(
            ("\n", "\r")) else newline
        updated = (
            content
            + suffix
            + TASK_SECTION
            + newline
            + newline
            + task_lines
            + newline
        )
        return updated, list(sorted(tasks))

    body_start, body_end = bounds
    prefix = content[:body_end]
    suffix = content[body_end:]
    if prefix and not prefix.endswith(("\n", "\r")):
        prefix += newline

    updated = prefix + task_lines + newline + suffix
    return updated, list(sorted(tasks))


def local_module_names(project_root: Path) -> set[str]:
    """收集项目内模块名，避免把本地模块误写进 requirements。"""
    names = set()
    for path in project_root.rglob("*.py"):
        names.add(path.stem)
        if (path.parent / "__init__.py").exists():
            names.add(path.parent.name)
    return names


def stdlib_module_names() -> set[str]:
    names = set(getattr(sys, "stdlib_module_names", ()))
    names.update(name.strip() for name in FALLBACK_STDLIB_MODULES)
    names.add("__future__")
    return names


def imported_modules(files: list[Path]) -> tuple[set[str], list[str]]:
    modules = set()
    parse_errors = []
    for path in files:
        try:
            tree = ast.parse(read_text(path), filename=str(path))
        except (OSError, SyntaxError) as error:
            parse_errors.append(f"{path}: {error}")
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules.add(node.module)
    return modules, parse_errors


def installed_distribution_map() -> dict[str, str]:
    """将当前环境中的 import 名称映射到发行包名称。"""
    result = {}
    try:
        distributions = importlib.metadata.packages_distributions()
    except Exception:  # 某些精简 Python 环境可能无法读取 metadata
        return result

    for import_name, package_names in distributions.items():
        if package_names:
            result[import_name] = sorted(package_names)[0]
    return result


def installed_distribution_versions() -> dict[str, str]:
    """读取当前环境中已安装发行包的版本。"""
    result = {}
    try:
        distributions = importlib.metadata.packages_distributions()
    except Exception:  # 某些精简 Python 环境可能无法读取 metadata
        return result

    package_names = {
        package_name
        for names in distributions.values()
        for package_name in names
    }
    for package_name in package_names:
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            continue
        result[normalise_requirement_name(package_name)] = version
    return result


def has_version_specifier(requirement: str) -> bool:
    return bool(re.search(r"(?:===|==|~=|>=|<=|!=|>|<)", requirement))


def add_compatible_version(requirement: str, versions: dict[str, str]) -> str:
    """按已安装版本生成同一 minor 版本范围，例如 ~=2.32.0。

    三段式 ~=2.32.0 等价于 >=2.32.0,<2.33.0。
    """
    if has_version_specifier(requirement):
        return requirement

    package_name = requirement_name(requirement)
    if package_name is None:
        return requirement
    version = versions.get(normalise_requirement_name(package_name))
    if version is None:
        return requirement

    match = re.match(r"^(\d+)\.(\d+)", version)
    if match is None:
        return requirement
    return f"{package_name}~={match.group(1)}.{match.group(2)}.0"


def requirement_for(
    module: str,
    installed: dict[str, str],
    versions: dict[str, str] | None = None,
) -> str:
    override_names = sorted(
        REQUIREMENT_OVERRIDES,
        key=len,
        reverse=True,
    )
    requirement = None
    for import_name in override_names:
        if module == import_name or module.startswith(import_name + "."):
            requirement = REQUIREMENT_OVERRIDES[import_name]
            break

    if requirement is None:
        root_name = module.split(".", 1)[0]
        package_name = installed.get(root_name, root_name.replace("_", "-"))
        requirement = package_name

    if versions is not None:
        return add_compatible_version(requirement, versions)
    return requirement


def requirement_name(line: str) -> str | None:
    """提取 requirements 行中的发行包名，用于去重。"""
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("-"):
        return None
    match = REQUIREMENT_NAME_PATTERN.match(line)
    return match.group(1) if match else None


def normalise_requirement_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def add_requirements(content: str, requirements: set[str]) -> tuple[str, list[str]]:
    """向 requirements.txt 追加缺失依赖，不删除或重排已有依赖。"""
    existing = {
        normalise_requirement_name(name)
        for line in content.splitlines()
        if (name := requirement_name(line)) is not None
    }
    missing = sorted(
        (requirement for requirement in requirements
         if normalise_requirement_name(requirement_name(requirement) or requirement)
         not in existing),
        key=normalise_requirement_name,
    )

    if not missing:
        return content, []

    newline = newline_for(content)
    updated = content
    for requirement in missing:
        if updated and not updated.endswith(("\n", "\r")):
            updated += newline
        updated += requirement + newline
    return updated, missing


def sync(project_root: Path, scan_dir: Path, dry_run: bool = False) -> int:
    project_root = project_root.resolve()
    scan_dir = scan_dir.resolve()
    pyproject_path = project_root / "pyproject.toml"
    requirements_path = project_root / "requirements.txt"

    files = python_files(scan_dir)
    print(f"扫描目录：{scan_dir.relative_to(project_root)}")
    print(f"发现 Python 文件：{len(files)} 个")

    tasks_by_name = {}
    for path in files:
        name = task_name_for(path, scan_dir)
        command = task_command_for(path, project_root)
        previous = tasks_by_name.get(name)
        if previous is not None and previous != command:
            raise ValueError(f"任务名冲突：{name}")
        tasks_by_name[name] = command

    pyproject = read_text(pyproject_path) if pyproject_path.exists() else ""
    missing_tasks = {
        name: command
        for name, command in tasks_by_name.items()
        if name not in existing_task_names(pyproject)
    }
    updated_pyproject, added_tasks = add_tasks(pyproject, missing_tasks)

    modules, parse_errors = imported_modules(files)
    local_names = local_module_names(project_root)
    third_party_modules = {
        module
        for module in modules
        if module.split(".", 1)[0] not in stdlib_module_names()
        and module.split(".", 1)[0] not in local_names
        and not module.split(".", 1)[0].startswith("_")
    }
    installed = installed_distribution_map()
    versions = installed_distribution_versions()
    discovered_requirements = {
        requirement_for(module, installed, versions)
        for module in third_party_modules
    }
    requirements = (
        read_text(requirements_path) if requirements_path.exists() else ""
    )
    updated_requirements, added_requirements = add_requirements(
        requirements,
        discovered_requirements,
    )

    if added_tasks:
        print("新增 Poe 任务：")
        for name in added_tasks:
            print(f"  + {name}")
    else:
        print("Poe 任务：无需更新")

    if added_requirements:
        print("新增依赖：")
        for requirement in added_requirements:
            print(f"  + {requirement}")
    else:
        print("requirements.txt：无需更新")

    unbounded_requirements = sorted(
        requirement
        for requirement in added_requirements
        if not has_version_specifier(requirement)
    )
    if unbounded_requirements:
        print("以下新增依赖无法自动确定版本上限，请补充 REQUIREMENT_OVERRIDES：")
        for requirement in unbounded_requirements:
            print(f"  ! {requirement}")

    if discovered_requirements:
        print("识别到的第三方依赖：")
        for requirement in sorted(discovered_requirements):
            print(f"  = {requirement}")

    if dry_run:
        print("试运行完成，未写入文件。")
    else:
        if updated_pyproject != pyproject:
            write_text(pyproject_path, updated_pyproject)
        if updated_requirements != requirements:
            write_text(requirements_path, updated_requirements)
        print("同步完成。")

    if parse_errors:
        print("解析 Python 文件时遇到问题：", file=sys.stderr)
        for error in parse_errors:
            print(f"  ! {error}", file=sys.stderr)
        return 1
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="同步 notebooks 下的 Poe 任务和 requirements.txt 依赖。"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="项目根目录，默认是当前仓库根目录。",
    )
    parser.add_argument(
        "--scan-dir",
        type=Path,
        default=Path("notebooks"),
        help="相对于项目根目录的 Python 扫描目录，默认是 notebooks。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示将要新增的内容，不修改文件。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = args.root.resolve()
    scan_dir = args.scan_dir
    if not scan_dir.is_absolute():
        scan_dir = project_root / scan_dir
    if not scan_dir.is_dir():
        raise SystemExit(f"扫描目录不存在：{scan_dir}")
    return sync(project_root, scan_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
