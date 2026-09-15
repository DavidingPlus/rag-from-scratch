"""
完整RAG生成示例
"""

import importlib

from utils.client import buildClient
from utils.config import Settings

vector_retrieval = importlib.import_module("11_vector_retrieval")
VectorStore = vector_retrieval.VectorStore


class RAGSystem:
    """简单的RAG系统"""

    def __init__(self, collection_name="rag_documents"):
        """
        初始化RAG系统

        Args:
            collection_name: 向量集合名称
        """
        self.settings = Settings.fromEnv()
        self.llm_client = buildClient(self.settings)
        self.llm_model = self.settings.model

        # BGE 负责生成向量，DeepSeek 负责生成最终答案。
        self.VectorStore = VectorStore(collection_name)

    def add_documents(self, documents: list):
        """
        添加文档到知识库

        Args:
            documents: 文档列表
        """
        self.VectorStore.add_documents(documents)

    def query(self, question: str, n_results: int = 3):
        """
        查询RAG系统

        Args:
            question: 用户问题
            n_results: 检索文档数量

        Returns:
            答案和来源
        """
        # 1. 检索相关文档
        print(f"\n步骤1: 检索相关文档")
        retrieval_results = self.VectorStore.query(question, n_results)

        if not retrieval_results['documents'][0]:
            return "抱歉，知识库中没有找到相关信息。", []

        context_docs = retrieval_results['documents'][0]
        print(f"检索到 {len(context_docs)} 个相关文档")

        # 2. 构建提示词
        print(f"步骤2: 构建提示词")
        context = "\n\n".join([
            f"【文档{i+1}】\n{doc}"
            for i, doc in enumerate(context_docs)
        ])

        prompt = f"""
你是一个专业的问答助手。请基于以下参考文档回答用户问题。

参考文档：
{context}

用户问题：{question}

要求：
1. 基于文档内容回答
2. 如果文档中没有相关信息，明确说明
3. 回答要准确、简洁
4. 引用参考的文档编号

回答：
"""

        # 3. 生成答案
        print(f"步骤3: 生成答案")
        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "你是一个专业的问答助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        return answer, context_docs


# 完整示例
if __name__ == "__main__":
    print("="*70)
    print("完整RAG系统示例")
    print("="*70)

    # 1. 创建RAG系统
    print("\n初始化RAG系统...")
    rag = RAGSystem("demo_rag")

    # 2. 添加知识库
    print("\n添加知识库...")
    knowledge_base = [
        {
            "text": "Python是一种高级编程语言，由Guido van Rossum于1991年创建。"
            "Python的特点是语法简洁、易学易用、应用广泛。",
            "metadata": {"topic": "Python介绍"}
        },
        {
            "text": "Python可用于Web开发（Django、Flask）、数据分析（Pandas、NumPy）、"
            "人工智能（TensorFlow、PyTorch）等多个领域。",
            "metadata": {"topic": "Python应用"}
        },
        {
            "text": "JavaScript是一种脚本语言，主要用于Web前端开发。"
            "它可以创建动态的网页内容，与HTML和CSS一起构成Web的三大核心技术。",
            "metadata": {"topic": "JavaScript介绍"}
        },
        {
            "text": "Rust是一种系统编程语言，注重内存安全、并发和性能。"
            "它没有垃圾回收，而是通过所有权系统在编译时保证内存安全。",
            "metadata": {"topic": "Rust介绍"}
        }
    ]

    documents = [item["text"] for item in knowledge_base]
    rag.add_documents(documents)

    # 3. 测试查询
    test_questions = [
        "Python有什么特点？",
        "JavaScript主要用于什么？",
        "Rust如何保证内存安全？",
        "Python可以用来做什么？"  # 需要综合多个文档
    ]

    for question in test_questions:
        print("\n" + "="*70)
        print(f"用户问题: {question}")
        print("="*70)

        answer, sources = rag.query(question)

        print("\n【答案】")
        print(answer)

        print("\n【参考来源】")
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source[:100]}...")

    print("\n" + "="*70)
    print("[OK] RAG系统演示完成！")
    print("="*70)
