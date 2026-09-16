def calculate_mrr(retrieved_docs, relevant_docs):
    """
    计算MRR

    Args:
        retrieved_docs: 检索结果
        relevant_docs: 真实相关文档

    Returns:
        mrr: 平均倒数排名
    """
    reciprocal_ranks = []

    for retrieved, relevant in zip(retrieved_docs, relevant_docs):
        # 找到第一个相关文档的位置
        for rank, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                reciprocal_ranks.append(1 / rank)
                break
        else:
            # 没有找到相关文档
            reciprocal_ranks.append(0)

    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    return mrr


# 示例
if __name__ == "__main__":
    retrieved_docs = [
        [1, 5, 8],    # Q1：相关文档是1，排第1
        [2, 6, 9],    # Q2：相关文档是6，排第2
        [3, 7, 10],   # Q3：相关文档是11，不在结果中
        [4, 8, 12],   # Q4：相关文档是4，排第1
        [5, 9, 13]    # Q5：相关文档是13，排第3
    ]

    relevant_docs = [
        {1},         # Q1
        {6},         # Q2
        {11},        # Q3
        {4},         # Q4
        {13}         # Q5
    ]

    mrr = calculate_mrr(retrieved_docs, relevant_docs)

    print("\nMRR计算示例")
    print("="*50)
    print(f"Q1: 相关文档排第1 → 1/1 = 1.000")
    print(f"Q2: 相关文档排第2 → 1/2 = 0.500")
    print(f"Q3: 相关文档未检索到 → 0.000")
    print(f"Q4: 相关文档排第1 → 1/1 = 1.000")
    print(f"Q5: 相关文档排第3 → 1/3 = 0.333")
    print(f"\nMRR: (1.0 + 0.5 + 0.0 + 1.0 + 0.333) / 5 = {mrr:.3f}")
