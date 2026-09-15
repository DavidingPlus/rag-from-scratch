"""使用本地 BGE 模型生成文本嵌入并计算相似度。"""

from sentence_transformers import SentenceTransformer
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "BAAI/bge-small-zh-v1.5"
_model = None


def load_bge_model():
    """加载 BGE 模型，并在当前进程中复用模型实例。"""
    global _model

    if _model is None:
        # 首次调用会从 Hugging Face 下载模型，之后使用本地缓存。
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def get_embedding(text: str) -> np.ndarray:
    """获取单条文本的嵌入向量。"""
    model = load_bge_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return np.asarray(embedding)


def batch_get_embeddings(texts: list) -> np.ndarray:
    """批量获取文本嵌入向量。"""
    model = load_bge_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return np.asarray(embeddings)


def compute_similarity(query: str, documents: list):
    """计算查询文本和文档的余弦相似度并排序。"""
    query_embedding = get_embedding(query)
    doc_embeddings = batch_get_embeddings(documents)

    similarities = cosine_similarity(
        [query_embedding],
        doc_embeddings,
    )[0]

    results = list(zip(documents, similarities))
    results.sort(key=lambda item: item[1], reverse=True)
    return results


if __name__ == "__main__":
    documents = [
        "Python是一种高级编程语言",
        "Java也是一种编程语言",
        "今天天气很好",
        "我喜欢吃苹果",
    ]

    print("=" * 60)
    print("BGE 文本嵌入示例")
    print("=" * 60 + "\n")

    # 1. 生成嵌入
    print("步骤1: 生成嵌入向量")
    embeddings = batch_get_embeddings(documents)
    print(f"嵌入模型: {MODEL_NAME}")
    print(f"嵌入维度: {embeddings.shape[1]}")
    print(f"向量数量: {embeddings.shape[0]}")

    print("\n第一个向量的前10个值:")
    print(embeddings[0][:10])
    print()

    # 2. 计算相似度
    print("步骤2: 计算文档相似度\n")
    query = "编程语言有哪些？"
    results = compute_similarity(query, documents)

    print(f"查询: {query}\n")
    print("最相关的文档:")
    for index, (document, score) in enumerate(results[:3], start=1):
        print(f"{index}. 相似度 {score:.3f}: {document}")

    # 3. 可视化（简化版）
    print("\n步骤3: 相似度可视化")
    print("=" * 60)

    for document, score in results:
        bar = "#" * max(0, int(score * 50))
        print(f"{score:.3f} {bar} {document[:30]}...")

    print("\n[OK] BGE 嵌入示例完成！")
