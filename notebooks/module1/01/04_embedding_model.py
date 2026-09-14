# 示例：使用不同的嵌入模型
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# 1. OpenAI嵌入（推荐生产环境）
def embed_with_openai(texts, model="text-embedding-3-small"):
    """
    使用OpenAI嵌入模型

    Args:
        texts: 文本列表
        model: 模型名称

    Returns:
        嵌入向量列表
    """
    from openai import OpenAI

    client = OpenAI()  # 需要设置API key

    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            model=model,
            input=text
        )
        embeddings.append(response.data[0].embedding)

    return embeddings


# 2. 开源模型（推荐私有部署）
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


# 3. 计算相似度
def compute_similarity(query, documents, embeddings):
    """
    计算查询和文档的相似度

    Args:
        query: 查询文本
        documents: 文档列表
        embeddings: 文档的嵌入向量

    Returns:
        相似度分数列表
    """
    # 生成查询的嵌入
    query_embedding = embed_with_sentence_transformer([query])[0]

    # 计算余弦相似度
    similarities = cosine_similarity(
        [query_embedding],
        embeddings
    )[0]

    # 返回排序后的结果
    results = list(zip(documents, similarities))
    results.sort(key=lambda x: x[1], reverse=True)

    return results


# 使用示例
if __name__ == "__main__":
    # 示例文档
    docs = [
        "Python是一种编程语言",
        "Java也是一种编程语言",
        "今天天气很好",
        "我喜欢吃苹果"
    ]

    print("生成嵌入向量...")
    embeddings = embed_with_sentence_transformer(docs)

    # 查询相似文档
    query = "编程语言有哪些？"
    results = compute_similarity(query, docs, np.array(embeddings))

    print(f"\n查询: {query}\n")
    for doc, score in results[:3]:
        print(f"相似度 {score:.3f}: {doc}")
