"""
文档加载示例
演示如何加载各种格式的文档
"""

from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader


# 1. 加载整个目录
def load_directory(directory_path: str):
    """
    从目录加载所有文档

    Args:
        directory_path: 目录路径

    Returns:
        文档列表
    """
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        required_exts=[".txt", ".md", ".pdf"],  # 只加载这些格式
        recursive=True  # 递归加载子目录
    )

    documents = reader.load_data()
    return documents


# 2. 加载单个PDF文件
def load_single_pdf(file_path: str):
    """
    加载单个PDF文件

    Args:
        file_path: PDF文件路径

    Returns:
        文档列表
    """
    loader = PDFReader()
    documents = loader.load_data(file_path)
    return documents


# 3. 加载多个文件
def load_specific_files(file_paths: list):
    """
    加载指定的文件列表

    Args:
        file_paths: 文件路径列表

    Returns:
        文档列表
    """
    reader = SimpleDirectoryReader(
        input_files=file_paths
    )
    documents = reader.load_data()
    return documents


# 4. 查看文档信息
def inspect_documents(documents):
    """
    查看文档的详细信息

    Args:
        documents: 文档列表
    """
    print(f"总文档数: {len(documents)}\n")

    for i, doc in enumerate(documents, 1):
        print(f"文档 {i}:")
        print(f"  - 元数据: {doc.metadata}")
        print(f"  - 字符数: {len(doc.text)}")
        print(f"  - 预览: {doc.text[:100]}...")
        print()


# 使用示例
if __name__ == "__main__":
    # 准备测试数据
    import os
    os.makedirs("data/test_docs", exist_ok=True)

    # 创建测试文件
    test_files = {
        "data/test_docs/doc1.txt": "这是第一个测试文档。\n包含两行内容。",
        "data/test_docs/doc2.txt": "这是第二个测试文档。\n用于测试批量加载功能。"
    }

    for filepath, content in test_files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"创建测试文件: {filepath}")

    print("\n" + "="*60)
    print("测试1: 加载目录")
    print("="*60 + "\n")

    # 测试1：加载目录
    docs = load_directory("data/test_docs")
    inspect_documents(docs)

    print("="*60)
    print("测试2: 加载指定文件")
    print("="*60 + "\n")

    # 测试2：加载指定文件
    specific_docs = load_specific_files([
        "data/test_docs/doc1.txt",
        "data/test_docs/doc2.txt"
    ])
    inspect_documents(specific_docs)

    print("\n[OK] 文档加载测试完成！")
