# 文件名：create_sample_data.py
"""
创建示例文本数据
"""

import os


def create_sample_documents():
    """创建示例文档"""

    # 确保目录存在
    os.makedirs("data/raw", exist_ok=True)

    # 文档1：Python介绍
    doc1 = """
Python是一种高级编程语言

Python是一种解释型、高级、通用的编程语言。它的设计哲学强调代码的可读性，
使用大量的缩进。Python是动态类型的，并且提供垃圾回收功能。

Python支持多种编程范式，包括结构化、面向对象和函数式编程。
"""

    # 文档2：机器学习介绍
    doc2 = """
机器学习基础

机器学习是人工智能的一个分支。它使计算机能够从数据中学习，
而不是被明确编程。

常见的机器学习类型包括：
1. 监督学习：使用标记的数据训练
2. 无监督学习：发现数据中的模式
3. 强化学习：通过奖励和惩罚学习
"""

    # 文档3：RAG介绍
    doc3 = """
RAG技术概述

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合了
信息检索和文本生成的AI技术。

RAG的核心步骤：
1. 检索：从知识库中查找相关文档
2. 增强：将检索到的文档加入提示词
3. 生成：LLM基于增强的提示词生成答案
"""

    # 保存文档
    documents = {
        "python_intro.txt": doc1,
        "ml_intro.txt": doc2,
        "rag_intro.txt": doc3
    }

    for filename, content in documents.items():
        filepath = os.path.join("data/raw", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✓ 创建文档: {filepath}")

    print("\n✓ 示例文档创建完成！")
    return True


if __name__ == "__main__":
    create_sample_documents()
