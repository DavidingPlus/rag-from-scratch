"""
最简RAG系统演示
仅用于理解概念，非生产代码
"""

# 步骤1：准备知识库（简化版，实际从文件加载）
knowledge_base = [
    {
        "id": 1,
        "content": "Python是一种高级编程语言，由Guido van Rossum于1991年创建。"
    },
    {
        "id": 2,
        "content": "JavaScript主要用于Web开发，可以在浏览器中运行。"
    },
    {
        "id": 3,
        "content": "Rust是一种系统编程语言，注重内存安全和性能。"
    }
]


# 步骤2：简单的检索函数（基于关键词匹配）
def retrieve_documents(query, kb, top_k=2):
    """
    检索相关文档

    Args:
        query: 用户问题
        kb: 知识库
        top_k: 返回前K个结果

    Returns:
        相关文档列表
    """
    # 简单的关键词匹配（实际应该使用向量相似度）
    query_lower = query.lower()

    # 计算每个文档的相关性分数
    scores = []
    for doc in kb:
        content_lower = doc["content"].lower()
        # 简单计算：统计问题中出现在文档中的词数
        score = sum(1 for word in query_lower.split() if word in content_lower)
        scores.append((doc, score))

    # 按分数排序，返回top_k
    scores.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scores[:top_k] if score > 0]


# 步骤3：构建提示词
def build_prompt(query, retrieved_docs):
    """
    构建包含检索文档的提示词

    Args:
        query: 用户问题
        retrieved_docs: 检索到的文档

    Returns:
        完整提示词
    """
    context = "\n".join([
        f"文档{i+1}: {doc['content']}"
        for i, doc in enumerate(retrieved_docs)
    ])

    prompt = f"""
基于以下文档回答用户问题。如果文档中没有相关信息，请明确说明。

【参考文档】
{context}

【用户问题】
{query}

【回答】
"""
    return prompt


# 步骤4：模拟LLM生成（实际应调用真实LLM）
def generate_response(prompt):
    """
    生成回答

    实际应用中，这里应该调用OpenAI API或其他LLM
    这里简化为返回提示词本身
    """
    print("=== 发送给LLM的提示词 ===")
    print(prompt)
    print("\n=== LLM会基于上述信息生成回答 ===\n")
    return "[这里应该是LLM生成的回答]"


# 步骤5：完整的RAG流程
def simple_rag_pipeline(query):
    """
    完整的RAG流程

    Args:
        query: 用户问题

    Returns:
        回答和参考文档
    """
    print(f"用户问题: {query}\n")

    # 1. 检索相关文档
    print("步骤1: 检索相关文档")
    retrieved_docs = retrieve_documents(query, knowledge_base)
    print(f"检索到 {len(retrieved_docs)} 个相关文档\n")

    if not retrieved_docs:
        return "抱歉，知识库中没有找到相关信息。", []

    # 2. 构建提示词
    print("步骤2: 构建提示词")
    prompt = build_prompt(query, retrieved_docs)

    # 3. 生成回答
    print("步骤3: 生成回答\n")
    answer = generate_response(prompt)

    # 4. 返回结果和来源
    return answer, retrieved_docs


# 运行示例
if __name__ == "__main__":
    # 测试问题
    test_queries = [
        "Python是什么时候创建的？",
        "Rust语言的特点是什么？",
        "如何学习Go语言？"  # 知识库中没有的信息
    ]

    print("=" * 60)
    print("简单RAG系统演示")
    print("=" * 60)
    print()

    for query in test_queries:
        print("\n" + "=" * 60)
        answer, sources = simple_rag_pipeline(query)

        if sources:
            print("=== 最终答案 ===")
            print(answer)
            print("\n=== 参考来源 ===")
            for doc in sources:
                print(f"- 文档ID: {doc['id']}")
                print(f"  内容: {doc['content']}")
