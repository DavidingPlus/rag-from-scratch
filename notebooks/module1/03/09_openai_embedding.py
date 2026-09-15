"""
文本嵌入示例
"""

from openai import OpenAI
import numpy as np

# 初始化OpenAI客户端
client = OpenAI()  # 自动读取 OPENAI_API_KEY 环境变量


def get_embedding(text: str, model="text-embedding-3-small"):
    """
    获取文本的嵌入向量

    Args:
        text: 输入文本
        model: 嵌入模型名称

    Returns:
        嵌入向量（numpy数组）
    """
    response = client.embeddings.create(
        model=model,
        input=text
    )

    embedding = response.data[0].embedding
    return np.array(embedding)


def batch_get_embeddings(texts: list, model="text-embedding-3-small"):
    """
    批量获取嵌入向量（更高效）

    Args:
        texts: 文本列表
        model: 模型名称

    Returns:
        嵌入向量列表
    """
    response = client.embeddings.create(
        model=model,
        input=texts
    )

    embeddings = [item.embedding for item in response.data]
    return np.array(embeddings)


def compute_similarity(query: str, documents: list):
    """
    计算查询和文档的相似度

    Args:
        query: 查询文本
        documents: 文档列表

    Returns:
        排序后的(文档, 相似度)列表
    """
    # 生成嵌入
    query_embedding = get_embedding(query)
    doc_embeddings = batch_get_embeddings(documents)

    # 计算余弦相似度
    from sklearn.metrics.pairwise import cosine_similarity

    similarities = cosine_similarity(
        [query_embedding],
        doc_embeddings
    )[0]

    # 排序
    results = list(zip(documents, similarities))
    results.sort(key=lambda x: x[1], reverse=True)

    return results


# 使用示例
if __name__ == "__main__":
    # 示例文档
    documents = [
        "Python是一种高级编程语言",
        "Java也是一种编程语言",
        "今天天气很好",
        "我喜欢吃苹果"
    ]

    print("="*60)
    print("文本嵌入示例")
    print("="*60 + "\n")

    # 1. 生成嵌入
    print("步骤1: 生成嵌入向量")
    embeddings = batch_get_embeddings(documents)
    print(f"嵌入维度: {embeddings.shape[1]}")
    print(f"向量数量: {embeddings.shape[0]}")

    # 显示第一个向量的一部分
    print(f"\n第一个向量的前10个值:")
    print(embeddings[0][:10])
    print()

    # 2. 计算相似度
    print("步骤2: 计算文档相似度\n")

    query = "编程语言有哪些？"
    results = compute_similarity(query, documents)

    print(f"查询: {query}\n")
    print("最相关的文档:")
    for i, (doc, score) in enumerate(results[:3], 1):
        print(f"{i}. 相似度 {score:.3f}: {doc}")

    # 3. 可视化（简化版）
    print("\n步骤3: 相似度可视化")
    print("="*60)

    for doc, score in results:
        bar = "█" * int(score * 50)
        print(f"{score:.3f} {bar} {doc[:30]}...")

    print("\n✓ 嵌入示例完成！")
