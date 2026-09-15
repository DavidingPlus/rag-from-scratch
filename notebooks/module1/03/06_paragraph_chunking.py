"""按段落分块示例。

使用空行作为主要分隔符，将文档切分为带重叠的文本块。
"""

from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


def load_documents(data_dir: Path):
    """从目录中加载文本和 Markdown 文档。"""
    if not data_dir.is_dir():
        raise FileNotFoundError(f"文档目录不存在: {data_dir}")

    reader = SimpleDirectoryReader(
        input_dir=str(data_dir),
        required_exts=[".txt", ".md"],
        recursive=True,
    )
    return reader.load_data()


def split_by_paragraph(documents, chunk_size=1000, chunk_overlap=100):
    """按段落优先分块，并保留原文档的元数据。

    Args:
        documents: LlamaIndex 文档列表。
        chunk_size: 每个分块的大小，单位为 tokenizer token。
        chunk_overlap: 相邻分块的重叠大小，单位为 tokenizer token。

    Returns:
        LlamaIndex TextNode 列表。
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须大于等于 0 且小于 chunk_size")

    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n\n",  # 优先按段落切分
    )
    return splitter.get_nodes_from_documents(documents)


def print_chunks(nodes, preview_length=120):
    """打印分块结果，便于观察分块大小和来源。"""
    print(f"原文档按段落分块后共得到 {len(nodes)} 个文本块\n")

    for index, node in enumerate(nodes, start=1):
        text = node.get_content().replace("\n", " ")
        print(f"文本块 {index}:")
        print(f"  - 字符数: {len(text)}")
        print(f"  - 元数据: {node.metadata}")
        print(f"  - 内容预览: {text[:preview_length]}...")
        print()


if __name__ == "__main__":
    # 从当前脚本位置向上定位项目根目录，避免依赖终端当前目录。
    project_root = Path(__file__).resolve().parents[3]
    data_dir = project_root / "data" / "processed"

    documents = load_documents(data_dir)
    print(f"加载了 {len(documents)} 个文档: {data_dir}\n")

    # 使用示例参数方便观察按段落切分的效果。
    nodes = split_by_paragraph(
        documents,
        chunk_size=100,
        chunk_overlap=20,
    )
    print_chunks(nodes)
    print("[OK] 按段落分块测试完成！")
