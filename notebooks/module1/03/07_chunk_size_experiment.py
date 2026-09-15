"""实验不同 chunk_size 对分块结果的影响。"""

from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


def load_documents(data_dir: Path):
    """从目录中加载文本、Markdown 和 PDF 文档。"""
    if not data_dir.is_dir():
        raise FileNotFoundError(f"文档目录不存在: {data_dir}")

    reader = SimpleDirectoryReader(
        input_dir=str(data_dir),
        required_exts=[".txt", ".md", ".pdf"],
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


def test_chunk_sizes(documents, sizes=(200, 500, 1000, 2000), chunk_overlap=100):
    """测试不同 chunk_size 对分块数量和首块长度的影响。"""
    for size in sizes:
        nodes = split_by_paragraph(
            documents,
            chunk_size=size,
            chunk_overlap=chunk_overlap,
        )
        print(f"chunk_size={size}: {len(nodes)} 个块")

        if nodes:
            first_text = nodes[0].get_content().replace("\n", " ")
            print(f"  第1块长度: {len(first_text)} 个字符")
            print(f"  第1块预览: {first_text[:100]}...")
        print()


if __name__ == "__main__":
    # 从当前脚本位置向上定位项目根目录，避免依赖终端当前目录。
    project_root = Path(__file__).resolve().parents[3]
    data_dir = project_root / "data" / "raw"

    documents = load_documents(data_dir)
    print(f"加载了 {len(documents)} 个文档: {data_dir}\n")
    test_chunk_sizes(documents)
    print("[OK] chunk_size 对比实验完成！")
