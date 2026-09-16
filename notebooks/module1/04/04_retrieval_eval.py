# 文件名：04_02_retrieval_eval.py
"""
完整的检索评估框架
"""


class RetrievalEvaluator:
    """检索质量评估器"""

    def __init__(self):
        self.metrics = {}

    def evaluate(self, queries, retrieved_docs, relevant_docs):
        """
        全面评估检索质量

        Args:
            queries: 查询列表
            retrieved_docs: 检索结果
            relevant_docs: 真实相关文档

        Returns:
            评估指标字典
        """
        results = {
            "hit_rate": self.calculate_hit_rate(retrieved_docs, relevant_docs),
            "mrr": self.calculate_mrr(retrieved_docs, relevant_docs),
            "precision_at_1": self.calculate_precision_at_k(retrieved_docs, relevant_docs, k=1),
            "precision_at_3": self.calculate_precision_at_k(retrieved_docs, relevant_docs, k=3),
            "precision_at_5": self.calculate_precision_at_k(retrieved_docs, relevant_docs, k=5),
        }

        self.metrics = results
        return results

    def calculate_hit_rate(self, retrieved_docs, relevant_docs):
        """计算Hit Rate"""
        hits = sum(
            1 for retrieved, relevant in zip(retrieved_docs, relevant_docs)
            if any(doc in relevant for doc in retrieved)
        )
        return hits / len(retrieved_docs)

    def calculate_mrr(self, retrieved_docs, relevant_docs):
        """计算MRR"""
        reciprocal_ranks = []
        for retrieved, relevant in zip(retrieved_docs, relevant_docs):
            for rank, doc in enumerate(retrieved, 1):
                if doc in relevant:
                    reciprocal_ranks.append(1 / rank)
                    break
            else:
                reciprocal_ranks.append(0)
        return sum(reciprocal_ranks) / len(reciprocal_ranks)

    def calculate_precision_at_k(self, retrieved_docs, relevant_docs, k):
        """计算Precision@K"""
        precisions = []
        for retrieved, relevant in zip(retrieved_docs, relevant_docs):
            top_k = retrieved[:k]
            relevant_count = sum(1 for doc in top_k if doc in relevant)
            precisions.append(relevant_count / k)
        return sum(precisions) / len(precisions)

    def print_report(self):
        """打印评估报告"""
        print("\n" + "="*60)
        print("检索质量评估报告")
        print("="*60)

        for metric, value in self.metrics.items():
            # 格式化指标名称
            metric_name = metric.replace("_", " ").title()
            # 格式化值
            if isinstance(value, float):
                print(f"{metric_name:20s}: {value:.3f}")
            else:
                print(f"{metric_name:20s}: {value}")

        print("="*60)

        # 评级
        hit_rate = self.metrics.get("hit_rate", 0)
        mrr = self.metrics.get("mrr", 0)

        if hit_rate > 0.85 and mrr > 0.7:
            rating = "优秀 ⭐⭐⭐⭐⭐"
        elif hit_rate > 0.7 and mrr > 0.5:
            rating = "良好 ⭐⭐⭐⭐"
        elif hit_rate > 0.5 and mrr > 0.3:
            rating = "中等 ⭐⭐⭐"
        else:
            rating = "需要改进 ⭐⭐"

        print(f"综合评级: {rating}")


# 使用示例
if __name__ == "__main__":
    # 示例数据
    queries = [f"Q{i}" for i in range(1, 11)]

    # 模拟检索结果（文档ID）
    retrieved_docs = [
        [1, 5, 8, 12, 15],
        [2, 6, 9, 13, 16],
        [3, 7, 10, 14, 17],
        [4, 8, 11, 15, 18],
        [5, 9, 12, 16, 19],
        [1, 6, 11, 16, 20],
        [2, 7, 12, 17, 21],
        [3, 8, 13, 18, 22],
        [4, 9, 14, 19, 23],
        [5, 10, 15, 20, 24]
    ]

    # 真实相关文档
    relevant_docs = [
        {1, 8},
        {6, 13},
        {3},
        {15},
        {9},
        {1, 11},
        {2, 17},
        {8, 13},
        {14},
        {20}
    ]

    # 评估
    evaluator = RetrievalEvaluator()
    metrics = evaluator.evaluate(queries, retrieved_docs, relevant_docs)

    # 打印报告
    evaluator.print_report()
