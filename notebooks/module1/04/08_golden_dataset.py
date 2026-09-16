# 文件名：08_golden_dataset.py
"""
创建黄金数据集
"""

import json
from typing import List, Dict


class GoldenDatasetBuilder:
    """黄金数据集构建器"""

    def __init__(self, output_path="data/eval/golden_dataset.json"):
        self.output_path = output_path
        self.dataset = []

    def add_example(self, question: str, answer: str, context: str, metadata: dict = None):
        """
        添加一个示例

        Args:
            question: 问题
            answer: 标准答案
            context: 相关上下文
            metadata: 元数据
        """
        example = {
            "question": question,
            "answer": answer,
            "context": context,
            "metadata": metadata or {}
        }
        self.dataset.append(example)

    def save(self):
        """保存数据集"""
        import os
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, ensure_ascii=False, indent=2)

        print(f"✓ 保存了 {len(self.dataset)} 个示例到 {self.output_path}")

    def load(self):
        """加载数据集"""
        with open(self.output_path, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
        return self.dataset


# 创建示例数据集
if __name__ == "__main__":
    builder = GoldenDatasetBuilder()

    # 添加示例（基于我们的测试文档）
    examples = [
        {
            "question": "Python是什么时候创建的？",
            "answer": "Python由Guido van Rossum于1991年创建。",
            "context": "Python是一种高级编程语言，由Guido van Rossum于1991年创建。",
            "metadata": {"topic": "Python历史", "difficulty": "easy"}
        },
        {
            "question": "Python有哪些特点？",
            "answer": "Python的特点是语法简洁、易学易用，适合初学者。",
            "context": "Python的特点是语法简洁、易学易用，适合初学者。",
            "metadata": {"topic": "Python特点", "difficulty": "easy"}
        },
        {
            "question": "JavaScript主要用于什么？",
            "answer": "JavaScript主要用于Web前端开发。",
            "context": "JavaScript是一种脚本语言，主要用于Web前端开发。",
            "metadata": {"topic": "JavaScript", "difficulty": "easy"}
        },
        {
            "question": "Rust如何保证内存安全？",
            "answer": "Rust通过所有权系统在编译时保证内存安全，不需要垃圾回收。",
            "context": "Rust是一种系统编程语言，注重内存安全、并发和性能。它没有垃圾回收，而是通过所有权系统在编译时保证内存安全。",
            "metadata": {"topic": "Rust", "difficulty": "medium"}
        }
    ]

    for example in examples:
        builder.add_example(**example)

    # 保存
    builder.save()

    print("\n黄金数据集创建完成！")
    print(f"包含 {len(builder.dataset)} 个问答对")
