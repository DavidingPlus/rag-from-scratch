# 文件名：prepare_custom_data.py
"""
准备自定义数据集
"""

import os
import shutil


def organize_documents(source_dir, target_dir="data/raw"):
    """
    整理文档到项目目录

    Args:
        source_dir: 源文档目录
        target_dir: 目标目录
    """
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 支持的文件格式
    supported_formats = {'.pdf', '.txt', '.md', '.docx', '.html'}

    # 统计
    total_files = 0
    copied_files = 0

    # 遍历源目录
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            total_files += 1

            # 检查文件格式
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in supported_formats:
                # 复制文件
                src_path = os.path.join(root, file)
                dst_path = os.path.join(target_dir, file)

                # 避免覆盖
                if os.path.exists(dst_path):
                    base, ext = os.path.splitext(file)
                    dst_path = os.path.join(
                        target_dir,
                        f"{base}_{copied_files}{ext}"
                    )

                shutil.copy2(src_path, dst_path)
                copied_files += 1
                print(f"✓ 复制: {file}")

    print(f"\n总计: {copied_files}/{total_files} 个文件")
    return copied_files > 0


if __name__ == "__main__":
    source = input("输入文档目录路径: ").strip()

    if os.path.isdir(source):
        organize_documents(source)
    else:
        print("错误：目录不存在")
