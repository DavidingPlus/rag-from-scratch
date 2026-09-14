# rag-from-scratch

从零开始学习构建并理解 RAG（检索增强生成）。

## 环境与常用命令

使用 Conda 创建并进入项目环境：

```bash
conda create -n rag-from-scratch python=3.11
conda activate rag-from-scratch
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

项目使用 `poethepoet` 管理常用任务。任务定义在根目录的 `pyproject.toml` 中：

```bash
poe n_m1_01_01_simple_rag_demo  # 运行 notebooks/module1/01/01_simple_rag_demo.py
poe n_tests_environment_check   # 运行 notebooks/tests/environment_check.py
```

Python 示例任务遵循以下命名规则：

```text
notebooks/module1/01/01_simple_rag_demo.py
└─> n_m1_01_01_simple_rag_demo
```

任务类型使用短前缀区分：`n_` 表示 Notebook，`e_` 表示 Exercise，`p_` 表示 Project。模块使用 `m1`、`m2` 等形式表示，后续新增任务时，按 `类型前缀_模块_章节目录编号_文件名` 命名。

在 VSCode 中选择 `Python (rag-from-scratch)` Kernel，即可运行 `notebooks/` 下的 Notebook。

## 自动同步任务和依赖

新增或复制 Python 文件后，运行：

```bash
python scripts/sync.py
# 或
poe sync
```

脚本会递归扫描 `notebooks/**/*.py`（包括函数体内部的静态 import），为缺少的文件新增 Poe 任务，并根据文件中的 import 语句把缺少的第三方依赖追加到 `requirements.txt`。已有任务和依赖不会删除或重排，重复运行也是安全的。修改前可以先用 `--dry-run` 查看结果：

```bash
python scripts/sync.py --dry-run
# 或
poe sync--dry-run
```

依赖名称通常可以从 import 名称推断；对于名称不一致的包，脚本内置了常见映射。已安装的包会按当前主版本和次版本生成兼容范围（例如 `~=2.32.0`，等价于 `>=2.32.0,<2.33.0`）；未安装且没有固定映射的包无法安全推断版本上限，脚本会提示补充规则。动态导入、代码注释或某个第三方包的间接依赖无法仅通过静态扫描确定，仍需要手动检查。
