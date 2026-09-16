from typing import List, Set, Any


def calculate_precision_at_k(
    retrieved_docs: List[List[Any]],
    relevant_docs: List[Set[Any]],
    k: int = 5
) -> float:
    """
    计算 Precision@K（前 K 个检索结果中的相关文档比例）。

    Args:
        retrieved_docs: 每个查询对应的检索结果，例如：
                        [["文档1", "文档2"], ["文档3", "文档4"]]
        relevant_docs: 每个查询对应的真实相关文档集合，例如：
                       [{"文档1"}, {"文档4"}]
        k: 只评估前 K 个结果。

    Returns:
        所有查询的平均 Precision@K。
    """
    if k <= 0:
        raise ValueError("k 必须是大于 0 的整数")

    if len(retrieved_docs) != len(relevant_docs):
        raise ValueError("retrieved_docs 和 relevant_docs 的长度必须一致")

    if not retrieved_docs:
        return 0.0

    precisions = []

    for retrieved, relevant in zip(retrieved_docs, relevant_docs):
        # 取前 K 个结果
        top_k = retrieved[:k]

        # 统计前 K 个结果中的相关文档数量
        relevant_count = sum(
            1 for doc in top_k if doc in relevant
        )

        # 按照 K 计算精确率
        precision = relevant_count / k
        precisions.append(precision)

    # 计算所有查询的平均精确率
    return sum(precisions) / len(precisions)


def main():
    # 示例：两个查询的检索结果
    retrieved_docs = [
        ["文档A", "文档B", "文档C", "文档D", "文档E"],
        ["文档F", "文档G", "文档H", "文档I", "文档J"]
    ]

    # 每个查询对应的真实相关文档
    relevant_docs = [
        {"文档A", "文档C", "文档F"},
        {"文档G", "文档I"}
    ]

    # 计算 Precision@3
    k = 3
    result = calculate_precision_at_k(
        retrieved_docs,
        relevant_docs,
        k
    )

    print(f"Precision@{k}: {result:.4f}")


if __name__ == "__main__":
    main()
