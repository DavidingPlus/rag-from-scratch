# 示例：使用Chroma向量数据库
import chromadb
from chromadb.config import Settings


# 开源模型（推荐私有部署）
def embed_with_sentence_transformer(texts, model_name="BAAI/bge-small-zh-v1.5"):
    """
    使用Sentence Transformers嵌入模型

    Args:
        texts: 文本列表
        model_name: 模型名称

    Returns:
        嵌入向量列表
    """
    from sentence_transformers import SentenceTransformer

    # 加载模型（首次会下载）
    model = SentenceTransformer(model_name)

    # 生成嵌入
    embeddings = model.encode(texts)

    return embeddings


# 1. 初始化Chroma
def init_chroma(persist_directory="./chroma_db"):
    """
    初始化Chroma客户端

    Args:
        persist_directory: 数据持久化目录

    Returns:
        Chroma客户端
    """
    client = chromadb.PersistentClient(path=persist_directory)
    return client


# 2. 创建集合
def create_collection(client, name="my_documents"):
    """
    创建向量集合

    Args:
        client: Chroma客户端
        name: 集合名称

    Returns:
        集合对象
    """
    # 如果集合已存在，获取它；否则创建新的
    collection = client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
    )
    return collection


# 3. 添加文档
def add_documents(collection, documents, embeddings, metadatas=None):
    """
    添加文档到集合

    Args:
        collection: 集合对象
        documents: 文本列表
        embeddings: 嵌入向量列表
        metadatas: 元数据列表（可选）

    Returns:
        添加的文档数量
    """
    # 生成唯一ID
    ids = [f"doc_{i}" for i in range(len(documents))]

    # 添加到集合
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    return len(documents)


# 4. 查询相似文档
def query_similar(collection, query_embedding, n_results=3):
    """
    查询最相似的文档

    Args:
        collection: 集合对象
        query_embedding: 查询向量
        n_results: 返回结果数量

    Returns:
        查询结果
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


# 5. 完整示例
def vector_db_example():
    """
    完整的向量数据库使用示例
    """
    # 初始化
    client = init_chroma()
    collection = create_collection(client, "demo_docs")

    # 准备数据
    documents = [
        "Python是一种高级编程语言",
        "JavaScript主要用于Web开发",
        "Rust注重内存安全和性能",
        "Go语言适合并发编程"
    ]

    # 生成嵌入（使用前面定义的函数）
    embeddings = embed_with_sentence_transformer(documents)

    # 添加到数据库
    add_documents(collection, documents, embeddings)
    print(f"添加了 {len(documents)} 个文档\n")

    # 查询
    query = "什么语言适合系统编程？"
    query_embedding = embed_with_sentence_transformer([query])[0]

    results = query_similar(collection, query_embedding, n_results=2)

    print(f"查询: {query}\n")
    print("最相关的文档:")
    for i, (doc, distance) in enumerate(zip(
        results['documents'][0],
        results['distances'][0]
    ), 1):
        print(f"{i}. {doc}")
        print(f"   相似度: {1 - distance:.3f}\n")


# 运行示例
if __name__ == "__main__":
    vector_db_example()
