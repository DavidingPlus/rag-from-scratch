# 文件名：preprocess_data.py
"""
数据预处理脚本
"""

import os
import re
from typing import List, Dict


def clean_text(text: str) -> str:
    """
    清洗文本

    Args:
        text: 原始文本

    Returns:
        清洗后的文本
    """
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)

    # 移除特殊字符（保留中文、英文、数字、标点）
    text = re.sub(
        r'[^\w\s\u4e00-\u9fff\u3000-\u303f\uff00-\uffef.,!?;:()“”‘’"【】\[\]]',
        '',
        text,
    )

    # 移除过短的行
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if len(line) > 10]

    return '\n'.join(lines)


def read_text_file(filepath: str) -> str:
    """
    读取文本文件

    Args:
        filepath: 文件路径

    Returns:
        文件内容
    """
    encodings = ['utf-8', 'gbk', 'gb2312']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    raise ValueError(f"无法解码文件: {filepath}")


def process_text_files(input_dir: str, output_dir: str):
    """
    批量处理文本文件

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)

    # 统计
    processed = 0
    total_chars = 0

    # 遍历文件
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue

        try:
            # 读取
            filepath = os.path.join(input_dir, filename)
            text = read_text_file(filepath)

            # 清洗
            cleaned = clean_text(text)

            # 保存
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            # 统计
            processed += 1
            total_chars += len(cleaned)

            print(f"✓ 处理: {filename} ({len(cleaned)} 字符)")

        except Exception as e:
            print(f"✗ 失败: {filename} - {e}")

    print(f"\n总计: {processed} 个文件, {total_chars} 字符")
    return processed > 0


def main():
    """主函数"""
    input_dir = "data/raw"
    output_dir = "data/processed"

    print("开始处理文本文件...")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}\n")

    success = process_text_files(input_dir, output_dir)

    if success:
        print("\n✓ 处理完成！")
    else:
        print("\n✗ 处理失败")


if __name__ == "__main__":
    main()
