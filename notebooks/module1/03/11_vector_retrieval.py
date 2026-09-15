"""
向量检索示例
"""

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-zh-v1.5"


class VectorStore:
    """向量存储类"""

    def __init__(self, collection_name="rag_bge_documents"):
        """
        初始化向量存储

        Args:
            collection_name: 集合名称
        """
        # 创建持久化客户端
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
        )

        # BGE 模型（首次运行会自动下载，当前进程内复用）
        self.embedding_model = SentenceTransformer(MODEL_NAME)

    def add_documents(self, texts: list, metadatas: list = None):
        """
        添加文档到向量库

        Args:
            texts: 文本列表
            metadatas: 元数据列表
        """
        # 生成嵌入
        embeddings = self._get_embeddings(texts)

        # 生成ID
        ids = [f"doc_{i}" for i in range(len(texts))]

        # 添加到集合
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✓ 添加了 {len(texts)} 个文档")

    def query(self, query_text: str, n_results: int = 3):
        """
        查询相似文档

        Args:
            query_text: 查询文本
            n_results: 返回结果数量

        Returns:
            查询结果
        """
        # 生成查询嵌入
        query_embedding = self._get_embeddings([query_text])[0]

        # 查询
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def _get_embeddings(self, texts: list):
        """使用 BGE 模型获取归一化嵌入向量"""
        embeddings = self.embedding_model.encode(
            texts,
            normalize_embeddings=True,
        )
        # Chroma 接收 Python 列表，避免直接依赖 numpy 类型。
        return embeddings.tolist()


# 使用示例
if __name__ == "__main__":
    print("="*60)
    print("向量检索示例")
    print("="*60 + "\n")

    # 1. 创建向量存储
    print("步骤1: 创建向量存储")
    vector_store = VectorStore("demo_bge_collection")
    print()

    # 2. 添加文档
    print("步骤2: 添加文档")
    documents = [
        "Python是一种高级编程语言，由Guido创建",
        "JavaScript主要用于Web前端开发",
        "Rust注重内存安全和性能",
        "Go语言适合并发编程",
        "Java是企业级开发的常用语言"
    ]

    metadatas = [
        {"category": "编程语言", "name": "Python"},
        {"category": "编程语言", "name": "JavaScript"},
        {"category": "编程语言", "name": "Rust"},
        {"category": "编程语言", "name": "Go"},
        {"category": "编程语言", "name": "Java"}
    ]

    vector_store.add_documents(documents, metadatas)
    print()

    # 3. 查询
    print("步骤3: 查询相似文档\n")

    queries = [
        "什么语言性能最好？",
        "如何做Web开发？",
        "适合系统的语言"
    ]

    for query in queries:
        print(f"查询: {query}")
        results = vector_store.query(query, n_results=2)

        print("最相关的文档:")
        for i, (doc, distance, metadata) in enumerate(zip(
            results['documents'][0],
            results['distances'][0],
            results['metadatas'][0]
        ), 1):
            similarity = 1 - distance  # 转换为相似度
            print(f"  {i}. {doc}")
            print(f"     相似度: {similarity:.3f}")
            print(f"     元数据: {metadata}")
        print()

    print("="*60)
    print("[OK] 向量检索示例完成！")
    print("="*60)
