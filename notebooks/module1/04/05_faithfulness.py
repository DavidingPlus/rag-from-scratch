# 文件名：05_faithfulness.py
"""使用项目配置的 DeepSeek API 评估 RAG 答案的忠实度。"""

from __future__ import annotations

import json
from typing import Any

from utils.client import buildClient
from utils.config import Settings


def _parse_score(score_text: str) -> float:
    """从 JSON 输出中读取并校验忠实度分数。"""
    if not score_text.strip():
        raise ValueError("DeepSeek 返回了空内容，无法读取忠实度分数")

    try:
        result = json.loads(score_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"DeepSeek 返回的不是合法 JSON：{score_text!r}") from exc

    if not isinstance(result, dict) or "score" not in result:
        raise ValueError(
            "DeepSeek JSON 必须包含 score 字段，"
            f"实际返回：{score_text!r}"
        )

    score = result["score"]
    if isinstance(score, bool):
        raise ValueError("JSON 中的 score 必须是 0-1 之间的数字")

    try:
        score = float(score)
    except (TypeError, ValueError) as exc:
        raise ValueError("JSON 中的 score 必须是 0-1 之间的数字") from exc

    if not 0 <= score <= 1:
        raise ValueError(f"JSON 中的 score 超出范围 [0, 1]：{score}")

    return score


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

    Raises:
        ValueError: 模型返回的 JSON 或 score 字段不符合要求。
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

请只返回合法 JSON，不要返回 Markdown 代码块或额外解释。
JSON 格式必须是：{{"score": 0.85}}
其中 score 必须是 0 到 1 之间的数字，并保留两位小数。
"""

    response = llm_client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个专业的评估助手。"
                    "请严格按照用户要求输出 JSON。"
                ),
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
    )

    score_text = response.choices[0].message.content or ""
    return _parse_score(score_text)


# 示例
if __name__ == "__main__":
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
