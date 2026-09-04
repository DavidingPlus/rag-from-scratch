# Notebooks

本目录存放本项目的学习和实验 Notebook。

> 注意：本目录存放的笔记尽可能不是复制粘贴原参考文档中的内容，因此只记录原文档中可能没提到的点，或者做的衍生思考。

环境检查脚本可以直接运行，也可以通过 Poe 执行：

```bash
python notebooks/tests/environment_check.py
poe n_tests_environment_check
```

建议直接用 VSCode 打开项目根目录，然后安装并启用以下扩展：

- Python
- Jupyter

本项目不要求安装 JupyterLab；只要虚拟环境中有 `ipykernel`，VSCode 就可以运行 Notebook。若 VSCode 提示安装 Jupyter 相关依赖，按提示安装到当前虚拟环境即可。

