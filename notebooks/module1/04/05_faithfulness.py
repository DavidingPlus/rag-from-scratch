# 文件名：05_faithfulness.py
"""使用项目配置的 DeepSeek API 评估 RAG 答案的忠实度。"""

from __future__ import annotations

import re
from typing import Any

from utils.client import buildClient
from utils.config import Settings


def evaluate_faithfulness(
    answer: str,
    context_documents: list[str],
    llm_client: Any | None = None,
    llm_model: str | None = None,
) -> float:
    """
    评估答案的忠实度

    Args:
        answer: RAG生成的答案
        context_documents: 检索到的上下文文档
        llm_client: 可选的 OpenAI-compatible 客户端。未传入时使用项目配置创建。
        llm_model: 可选的模型名称。未传入时使用 DEEPSEEK_MODEL。

    Returns:
        faithfulness_score: 忠实度分数 (0-1)
    """
    if llm_client is None or llm_model is None:
        settings = Settings.fromEnv()
        if llm_client is None:
            llm_client = buildClient(settings)
        if llm_model is None:
            llm_model = settings.model

    # 构建评估提示词
    context = "\n\n".join([
        f"文档{i+1}: {doc}"
        for i, doc in enumerate(context_documents)
    ])

    prompt = f"""
请评估以下答案是否基于提供的参考文档。

参考文档：
{context}

答案：
{answer}

请评估：
1. 答案中的所有声明是否都能在参考文档中找到支持？
2. 答案是否没有添加文档中不存在的信息？

评分标准：
- 1.0: 完全基于文档，无编造
- 0.7-0.9: 大部分基于文档，有少量合理推断
- 0.4-0.6: 部分基于文档，有明显添加信息
- 0.1-0.3: 大量编造信息
- 0.0: 完全不基于文档

请只返回一个0-1之间的分数，保留两位小数。
"""

    response = llm_client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": "你是一个专业的评估助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=20,
    )

    # 提取分数
    score_text = response.choices[0].message.content.strip()
    print("DeepSeek 原始返回：", repr(score_text))
    try:
        score = float(score_text)
        return max(0, min(1, score))  # 确保在0-1之间
    except ValueError:
        # 如果返回的不是纯数字，尝试提取
        import re
        numbers = re.findall(r'0\.\d+', score_text)
        if numbers:
            return float(numbers[0])
        return 0.5  # 默认分数


# 示例
if __name__ == "__main__":
    # 按项目统一配置创建一次客户端，供多个测试用例复用。
    settings = Settings.fromEnv()
    client = buildClient(settings)

    # 示例文档
    context = [
        "Python是一种高级编程语言，由Guido van Rossum于1991年创建。",
        "Python的特点是语法简洁、易学易用，适合初学者。"
    ]

    # 测试不同质量的答案
    test_cases = [
        {
            "name": "完全忠实",
            "answer": "Python由Guido van Rossum于1991年创建，它的特点是语法简洁、易学易用。"
        },
        {
            "name": "大部分忠实",
            "answer": "Python是一种高级编程语言，由Guido创建，它非常适合数据科学和Web开发。"
        },
        {
            "name": "部分编造",
            "answer": "Python是Google开发的编程语言，发布于2000年，主要用于人工智能领域。"
        },
        {
            "name": "完全编造",
            "answer": "Java是一种脚本语言，主要用于前端开发，语法非常复杂难学。"
        }
    ]

    print("Faithfulness评估示例")
    print("="*60 + "\n")

    for test in test_cases:
        score = evaluate_faithfulness(
            test["answer"],
            context,
            llm_client=client,
            llm_model=settings.model,
        )
        print(f"{test['name']:15s}: {score:.2f}")
        print(f"  答案: {test['answer']}")
        print()
