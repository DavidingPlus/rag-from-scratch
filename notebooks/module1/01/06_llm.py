# 示例：使用LLM生成答案
from openai import OpenAI


def generate_answer_with_llm(query, context_documents, model="gpt-3.5-turbo"):
    """
    使用LLM生成答案

    Args:
        query: 用户问题
        context_documents: 检索到的相关文档
        model: LLM模型名称

    Returns:
        生成的答案
    """
    client = OpenAI()  # 需要设置API key

    # 构建上下文
    context = "\n\n".join([
        f"【文档{i+1}}}\n{doc}"
        for i, doc in enumerate(context_documents)
    ])

    # 构建提示词
    prompt = f"""
你是一个专业的助手。请基于以下参考文档回答用户问题。

参考文档：
{context}

用户问题：{query}

要求：
1. 基于文档内容回答
2. 如果文档中没有相关信息，明确说明
3. 回答要准确、简洁

回答：
"""

    # 调用LLM
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个专业的问答助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # 控制随机性
        max_tokens=500    # 限制回答长度
    )

    answer = response.choices[0].message.content
    return answer


# 使用示例
if __name__ == "__main__":
    query = "Python有什么特点？"

    context_docs = [
        "Python是一种高级编程语言，由Guido van Rossum创建。",
        "Python的特点是语法简洁、易学易用、应用广泛。",
        "Python可用于Web开发、数据分析、人工智能等领域。"
    ]

    answer = generate_answer_with_llm(query, context_docs)

    print(f"问题: {query}\n")
    print(f"回答: {answer}")
