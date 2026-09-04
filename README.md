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

