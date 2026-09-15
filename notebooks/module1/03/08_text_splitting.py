"""
文本分块完整示例
"""

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter


def load_and_split():
    """加载文档并分块"""

    # 1. 加载文档
    print("步骤1: 加载文档")
    reader = SimpleDirectoryReader(
        input_dir="data/processed",
        required_exts=[".txt", ".md"]
    )
    documents = reader.load_data()
    print(f"加载了 {len(documents)} 个文档\n")

    # 2. 测试不同分块策略
    print("步骤2: 测试分块策略\n")

    strategies = [
        ("固定长度(500字)", 500, 50),
        ("段落优先(1000字)", 1000, 100),
        ("大块(2000字)", 2000, 200)
    ]

    results = []

    for name, chunk_size, overlap in strategies:
        print(f"策略: {name}")
        print(f"  chunk_size={chunk_size}, overlap={overlap}")

        # 分块
        splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separator="\n\n"
        )
        nodes = splitter.get_nodes_from_documents(documents)

        # 统计
        print(f"  生成块数: {len(nodes)}")

        # 计算平均长度
        avg_length = sum(len(node.text) for node in nodes) / len(nodes)
        print(f"  平均长度: {avg_length:.0f} 字符")

        # 显示示例
        if nodes:
            print(f"  第1块预览:")
            preview = nodes[0].text[:150]
            print(f"    {preview}...")

        print()
        results.append((name, nodes))

    # 3. 返回最佳策略的结果
    # 通常段落优先是最佳选择
    best_nodes = results[1][1]  # 段落优先策略

    print("="*60)
    print(f"选择策略: {results[1][0]}")
    print(f"生成块数: {len(best_nodes)}")
    print("="*60)

    return best_nodes


def visualize_chunks(nodes):
    """可视化分块结果"""

    print("\n分块可视化:")
    print("="*60)

    for i, node in enumerate(nodes[:5], 1):  # 只显示前5个
        print(f"\n块 {i}:")
        print(f"  长度: {len(node.text)} 字符")
        print(f"  内容预览: {node.text[:100]}...")
        print(f"  元数据: {node.metadata}")


if __name__ == "__main__":
    # 分块
    nodes = load_and_split()

    # 可视化
    visualize_chunks(nodes)

    print("\n✓ 分块完成！")
