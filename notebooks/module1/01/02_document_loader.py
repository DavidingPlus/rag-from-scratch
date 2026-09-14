# 示例：加载多种类型的文档
from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader


# 1. 加载本地文件或目录中的文档
def load_local_documents(path):
    """
    从本地文件或目录加载文档

    Args:
        path: 单个文档路径或文档目录路径

    Returns:
        文档列表
    """
    path = Path(path)

    if path.is_file():
        # input_files 用于加载单个或多个明确指定的文件。
        reader = SimpleDirectoryReader(
            input_files=[str(path)],
            required_exts=[".pdf", ".txt", ".md"]
        )
    else:
        # input_dir 用于加载目录；recursive=True 表示递归读取子目录。
        reader = SimpleDirectoryReader(
            input_dir=str(path),
            required_exts=[".pdf", ".txt", ".md"],
            recursive=True
        )

    documents = reader.load_data()
    return documents


# 2. 加载网页内容
def load_web_pages(urls):
    """
    从URL加载网页内容

    Args:
        urls: URL列表

    Returns:
        文档列表
    """
    documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
    return documents


# 3. 加载单个PDF文件
def load_single_pdf(file_path):
    """
    加载单个PDF文件

    Args:
        file_path: PDF文件路径

    Returns:
        文档对象
    """
    # LlamaIndex 当前文件读取器使用 PDFReader。
    from llama_index.readers.file import PDFReader

    loader = PDFReader()
    documents = loader.load_data(file_path)
    return documents


# 使用示例
if __name__ == "__main__":
    # 从当前脚本位置向上定位项目根目录，避免依赖终端当前工作目录。
    project_root = Path(__file__).resolve().parents[3]

    # 加载本地文档。
    docs = load_local_documents(project_root / "README.md")
    print(f"加载了 {len(docs)} 个文档")

    # 加载网页。
    urls = ["https://baidu.com"]
    web_docs = load_web_pages(urls)
    print(f"从网页加载了 {len(web_docs)} 个文档")
