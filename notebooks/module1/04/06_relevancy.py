# 文件名：06_relevancy.py
"""使用项目配置的 DeepSeek API 评估答案与问题的相关性。"""

from __future__ import annotations

import importlib
from typing import Any

from utils.client import buildClient
from utils.config import Settings

faithfulness_model = importlib.import_module("05_faithfulness")
_parse_score = faithfulness_model._parse_score


def evaluate_relevancy(
    question: str,
    answer: str,
    llm_client: Any | None = None,
    llm_model: str | None = None,
) -> float:
    """
    评估答案是否真正回答了用户的问题。

    Args:
        question: 用户问题
        answer: RAG 生成的答案
        llm_client: 可选的 OpenAI-compatible 客户端。未传入时使用项目配置创建。
        llm_model: 可选的模型名称。未传入时使用 DEEPSEEK_MODEL。

    Returns:
        relevancy_score: 相关性分数 (0-1)

    Raises:
        ValueError: 模型返回的 JSON 或 score 字段不符合要求。
    """
    if not question.strip():
        raise ValueError("question 不能为空")
    if not answer.strip():
        raise ValueError("answer 不能为空")

    if llm_client is None or llm_model is None:
        settings = Settings.fromEnv()
        if llm_client is None:
            llm_client = buildClient(settings)
        if llm_model is None:
            llm_model = settings.model

    prompt = f"""
请评估以下答案是否真正回答了用户的问题。

用户问题：
{question}

答案：
{answer}

评估标准：
- 1.0: 完全回答了问题，信息充分准确
- 0.7-0.9: 很好地回答了问题，略有不足
- 0.4-0.6: 部分回答了问题，信息不完整
- 0.1-0.3: 基本没有回答问题
- 0.0: 完全不相关

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
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    score_text = response.choices[0].message.content or ""
    return _parse_score(score_text)


if __name__ == "__main__":
    settings = Settings.fromEnv()
    client = buildClient(settings)

    question = "Python 有什么特点？"
    test_cases = [
        {
            "name": "完全相关",
            "answer": "Python 语法简洁、易学易用，适合初学者。",
        },
        {
            "name": "部分相关",
            "answer": "Python 是一种高级编程语言。",
        },
        {
            "name": "完全不相关",
            "answer": "JavaScript 主要用于 Web 前端开发。",
        },
    ]

    print("Relevancy 评估示例")
    print("=" * 60 + "\n")

    for test in test_cases:
        score = evaluate_relevancy(
            question,
            test["answer"],
            llm_client=client,
            llm_model=settings.model,
        )
        print(f"{test['name']:15s}: {score:.2f}")
        print(f"  问题: {question}")
        print(f"  答案: {test['answer']}\n")
