from llama_index.core import Document
from pathlib import Path


# 创建可复用的文档加载器类
class DocumentLoader:
    """文档加载器类"""

    def __init__(self, base_path: str = "data"):
        """
        初始化加载器

        Args:
            base_path: 基础路径
        """
        self.base_path = Path(base_path)

    def load_txt(self, filename: str) -> Document:
        """加载文本文件"""
        filepath = self.base_path / "test_docs" / filename

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return Document(
            text=content,
            metadata={"source": filename}
        )

    def load_multiple_txt(self, filenames: list) -> list:
        """批量加载文本文件"""
        documents = []
        for filename in filenames:
            try:
                doc = self.load_txt(filename)
                documents.append(doc)
            except Exception as e:
                print(f"加载失败 {filename}: {e}")

        return documents


# 使用示例
loader = DocumentLoader(base_path="data")
docs = loader.load_multiple_txt(["doc1.txt", "doc2.txt"])
print(f"加载了 {len(docs)} 个文档")
