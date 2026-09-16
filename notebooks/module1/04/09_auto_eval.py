# 文件名：09_auto_eval.py
"""自动化 RAG 评估流程。"""

import importlib
import sys
from pathlib import Path


golden_dataset = importlib.import_module("08_golden_dataset")
GoldenDatasetBuilder = golden_dataset.GoldenDatasetBuilder

retrieval_eval = importlib.import_module("04_retrieval_eval")
RetrievalEvaluator = retrieval_eval.RetrievalEvaluator

ragas_eval = importlib.import_module("07_ragas_eval")
evaluate_with_ragas = ragas_eval.evaluate_with_ragas

# 13_rag_system.py 位于相邻的 module1/03 目录。
module3_dir = Path(__file__).resolve().parents[1] / "03"
if str(module3_dir) not in sys.path:
    sys.path.insert(0, str(module3_dir))

rag_system = importlib.import_module("13_rag_system")
SimpleRAG = rag_system.RAGSystem


class AutoEvaluator:
    """自动化评估器"""

    def __init__(self, rag_system, golden_dataset_path):
        """
        初始化评估器

        Args:
            rag_system: RAG系统实例
            golden_dataset_path: 黄金数据集路径
        """
        self.rag = rag_system
        self.dataset = self.load_dataset(golden_dataset_path)

    def load_dataset(self, path):
        """加载黄金数据集"""
        builder = GoldenDatasetBuilder(path)
        return builder.load()

    def run_evaluation(self):
        """运行完整评估"""
        print("="*70)
        print("自动化RAG评估")
        print("="*70 + "\n")

        # 1. 准备数据
        questions = [item["question"] for item in self.dataset]
        ground_truths = [item["answer"] for item in self.dataset]

        # 2. 运行RAG系统
        print("步骤1: 运行RAG系统生成答案\n")
        rag_answers = []
        retrieved_contexts = []

        for question in questions:
            response = self.rag.query(question)
            rag_answers.append(str(response))
            # 假设response包含检索到的上下文
            retrieved_contexts.append([response.source_nodes[0].text])

        # 3. 评估生成质量
        print("步骤2: 评估生成质量（使用RAGAS）\n")
        generation_scores = evaluate_with_ragas(
            questions,
            rag_answers,
            retrieved_contexts,
            ground_truths
        )

        # 4. 评估检索质量
        print("步骤3: 评估检索质量\n")
        # 这里需要额外的真实相关文档标注
        # 简化示例：假设第一个检索到的文档是相关的
        retrieval_evaluator = RetrievalEvaluator()
        retrieval_scores = retrieval_evaluator.evaluate(
            questions,
            [[0] for _ in questions],  # 简化
            [set() for _ in questions]  # 简化
        )

        # 5. 综合报告
        self.print_report(generation_scores, retrieval_scores)

    def print_report(self, generation_scores, retrieval_scores):
        """打印综合报告"""
        print("\n" + "="*70)
        print("评估报告")
        print("="*70 + "\n")

        print("生成质量:")
        for metric, value in generation_scores.items():
            print(f"  {metric}: {value:.3f}")

        print("\n检索质量:")
        for metric, value in retrieval_scores.items():
            print(f"  {metric}: {value:.3f}")

        print("\n" + "="*70)


# 使用示例
if __name__ == "__main__":
    # 创建RAG系统
    rag = SimpleRAG()
    documents = rag.load_documents()
    rag.build_index(documents)

    # 运行评估
    evaluator = AutoEvaluator(rag, "data/eval/golden_dataset.json")
    evaluator.run_evaluation()
