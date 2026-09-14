# 文件名：prepare_data_pipeline.py
"""
完整的数据准备流程
"""

import os
import shutil
import importlib

# 教程文件名带有编号，不能用普通的 from 03_preprocess_data import ... 语法。
preprocess_data = importlib.import_module("03_preprocess_data")
create_sample_data = importlib.import_module("01_create_sample_data")

process_text_files = preprocess_data.process_text_files
create_sample_documents = create_sample_data.create_sample_documents


def full_data_pipeline():
    """完整的数据准备流程"""

    print("="*60)
    print("RAG教程 - 数据准备流程")
    print("="*60 + "\n")

    # 1. 创建目录结构
    print("步骤1: 创建目录结构")
    directories = [
        "data/raw",
        "data/processed",
        "data/eval"  # 评估数据
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}")

    # 2. 创建示例数据
    print("\n步骤2: 创建示例数据")
    create_sample_documents()

    # 3. 预处理数据
    print("\n步骤3: 预处理数据")
    process_text_files("data/raw", "data/processed")

    # 4. 创建评估数据集
    print("\n步骤4: 创建评估数据集")
    create_evaluation_dataset()

    print("\n" + "="*60)
    print("✓ 数据准备完成！")
    print("="*60)

    # 显示数据统计
    show_data_statistics()

    return True


def create_evaluation_dataset():
    """创建评估数据集（问答对）"""

    eval_data = [
        {
            "question": "Python是什么？",
            "answer": "Python是一种高级编程语言",
            "source": "python_intro.txt"
        },
        {
            "question": "机器学习的类型有哪些？",
            "answer": "监督学习、无监督学习、强化学习",
            "source": "ml_intro.txt"
        },
        {
            "question": "RAG的核心步骤是什么？",
            "answer": "检索、增强、生成",
            "source": "rag_intro.txt"
        }
    ]

    import json

    with open("data/eval/eval_qa.json", "w", encoding="utf-8") as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2)

    print("  ✓ 评估数据集: data/eval/eval_qa.json")
    return True


def show_data_statistics():
    """显示数据统计"""
    print("\n数据统计:")

    # 统计文件数量
    for directory in ["data/raw", "data/processed"]:
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"  {directory}: {len(files)} 个文件")

    # 显示示例
    print("\n示例文档:")
    if os.path.exists("data/processed"):
        for filename in os.listdir("data/processed")[:3]:
            filepath = os.path.join("data/processed", filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                preview = content[:100] + \
                    "..." if len(content) > 100 else content
                print(f"\n  {filename}:")
                print(f"    {preview}")


if __name__ == "__main__":
    full_data_pipeline()
