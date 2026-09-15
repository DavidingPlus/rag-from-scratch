# 为文档添加自定义元数据
from llama_index.core import Document


def load_with_metadata(file_path: str, metadata: dict):
    """
    加载文档并添加自定义元数据

    Args:
        file_path: 文件路径
        metadata: 元数据字典

    Returns:
        带元数据的文档
    """
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建文档对象
    doc = Document(
        text=content,
        metadata=metadata
    )

    return doc


# 使用示例
doc = load_with_metadata(
    "data/test_docs/doc1.txt",
    metadata={
        "title": "测试文档1",
        "category": "技术文档",
        "author": "教程作者",
        "date": "2024-01-01"
    }
)


print(f"文档元数据: {doc.metadata}")
