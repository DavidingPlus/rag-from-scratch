# 文件名：01_hit_rate.py
"""
Hit Rate计算示例
"""


def calculate_hit_rate(queries, retrieved_docs, relevant_docs):
    """
    计算Hit Rate

    Args:
        queries: 查询列表
        retrieved_docs: 检索到的文档列表（每个查询的top-k结果）
        relevant_docs: 真实相关文档列表

    Returns:
        hit_rate: 命中率
    """
    hits = 0

    for query_id, retrieved in enumerate(retrieved_docs):
        # 获取该查询的真实相关文档
        relevant = set(relevant_docs[query_id])

        # 检查检索结果中是否有至少一个相关文档
        if any(doc_id in relevant for doc_id in retrieved):
            hits += 1

    hit_rate = hits / len(queries)
    return hit_rate


# 示例
if __name__ == "__main__":
    # 示例数据
    queries = ["Q1", "Q2", "Q3", "Q4", "Q5"]

    # 检索结果（每个查询的top-3文档ID）
    retrieved_docs = [
        [1, 5, 8],    # Q1的结果
        [2, 6, 9],    # Q2的结果
        [3, 7, 10],   # Q3的结果
        [4, 8, 12],   # Q4的结果
        [5, 9, 13]    # Q5的结果
    ]

    # 真实相关文档
    relevant_docs = [
        {1, 8},      # Q1的相关文档
        {6},         # Q2的相关文档
        {11, 12},    # Q3的相关文档
        {4, 15},     # Q4的相关文档
        {9, 13}      # Q5的相关文档
    ]

    # 计算Hit Rate
    hit_rate = calculate_hit_rate(queries, retrieved_docs, relevant_docs)

    print("Hit Rate计算示例")
    print("="*50)
    for i, (retrieved, relevant) in enumerate(zip(retrieved_docs, relevant_docs), 1):
        hit = any(doc in relevant for doc in retrieved)
        status = "✓" if hit else "✗"
        print(f"Q{i}: {status} 检索={retrieved}, 相关={relevant}")

    print(f"\nHit Rate: {hit_rate:.2%}")
    print(f"解释: {hit_rate:.0%}的查询至少检索到一个相关文档")
