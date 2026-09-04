"""基础环境检查。

用于检查 rag-from-scratch 的 Python、核心依赖、项目目录和环境变量。
"""

import os
import platform
import sys
from importlib.util import find_spec
from pathlib import Path


def configure_output() -> None:
    """在 Windows 控制台中使用 UTF-8 输出，避免检查图标导致编码错误。"""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check_python() -> None:
    """检查 Python 版本和运行平台。"""
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")

    if sys.version_info >= (3, 9):
        print("✅ Python version is supported (>= 3.9)")
    else:
        print("❌ Python version is too old; Python 3.9+ is required")


def check_packages() -> None:
    """检查 Jupyter 和 RAG 基础依赖是否可以导入。"""
    packages = {
        "jupyter": "Jupyter",
        "ipykernel": "Jupyter Kernel",
        "llama_index": "LlamaIndex",
        "chromadb": "ChromaDB",
        "openai": "OpenAI",
        "dotenv": "python-dotenv",
    }

    missing = []
    for import_name, display_name in packages.items():
        if find_spec(import_name) is None:
            missing.append(display_name)
        else:
            print(f"✅ {display_name}")

    if missing:
        print("\n⚠️ Missing packages:")
        for package in missing:
            print(f"- {package}")
    else:
        print("\n✅ All checked packages are available")


def find_project_root() -> Path:
    """从当前目录或脚本位置查找项目根目录。"""
    script_root = Path(__file__).resolve().parents[2]
    candidates = [Path.cwd(), script_root, *Path.cwd().parents]
    return next(
        (
            path
            for path in dict.fromkeys(candidates)
            if (path / "reference").is_dir() and (path / "docs").is_dir()
        ),
        script_root,
    )


def check_project() -> None:
    """检查项目目录和 OpenAI API Key 配置。"""
    project_root = find_project_root()
    print(f"Project root: {project_root}")

    expected_paths = [
        project_root / "docs",
        project_root / "reference",
        project_root / "notebooks",
        project_root / "notebooks" / "tests",
    ]

    for path in expected_paths:
        mark = "✅" if path.exists() else "⚠️"
        print(f"{mark} {path.relative_to(project_root)}")

    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY is configured")
    else:
        print("⚠️ OPENAI_API_KEY is not configured; API examples may not run")


def main() -> None:
    """运行全部环境检查。"""
    configure_output()
    check_python()
    print()
    check_packages()
    print()
    check_project()
    print("\n基础环境检查完成。")


if __name__ == "__main__":
    main()
