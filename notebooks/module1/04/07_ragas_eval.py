# 文件名：07_ragas_eval.py
"""
使用RAGAS框架评估
"""

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision
)
from datasets import Dataset


def evaluate_with_ragas(questions, answers, contexts, ground_truths=None):
    """
    使用RAGAS评估

    Args:
        questions: 问题列表
        answers: RAG生成的答案列表
        contexts: 检索到的上下文列表
        ground_truths: 真实答案列表（可选）

    Returns:
        评估结果
    """
    # 准备数据
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    }

    if ground_truths:
        data["ground_truth"] = ground_truths

    dataset = Dataset.from_dict(data)

    # 选择评估指标
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision
    ]

    # 运行评估
    results = evaluate(
        dataset=dataset,
        metrics=metrics
    )

    return results


# 示例
if __name__ == "__main__":
    # 示例数据
    questions = [
        "Python是什么时候创建的？",
        "Python有什么特点？"
    ]

    answers = [
        "Python由Guido van Rossum于1991年创建。",
        "Python的特点是语法简洁、易学易用。"
    ]

    contexts = [
        ["Python是一种高级编程语言，由Guido van Rossum于1991年创建。"],
        ["Python的特点是语法简洁、易学易用，适合初学者。"]
    ]

    # 评估
    print("使用RAGAS评估")
    print("="*60 + "\n")

    results = evaluate_with_ragas(questions, answers, contexts)

    # 打印结果
    print(results.to_pandas())
