# 示例：不同的分块策略
from llama_index.text_splitter import (
    SentenceSplitter,
    TokenTextSplitter,
)


# 1. 固定长度分块（按字符）
def chunk_by_char(text, chunk_size=500, chunk_overlap=50):
    """
    按字符数分块

    Args:
        text: 输入文本
        chunk_size: 每块大小（字符数）
        chunk_overlap: 块之间重叠大小

    Returns:
        分块列表
    """
    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n\n"  # 优先按段落分割
    )
    chunks = splitter.split_text(text)
    return chunks


# 2. 按Token分块
def chunk_by_token(text, chunk_size=1000, chunk_overlap=100):
    """
    按Token数分块（更符合LLM处理方式）

    Args:
        text: 输入文本
        chunk_size: 每块大小（Token数）
        chunk_overlap: 块之间重叠大小

    Returns:
        分块列表
    """
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        encoding_name="cl100k_base"  # OpenAI的编码方式
    )
    chunks = splitter.split_text(text)
    return chunks


# 3. 递归分块（推荐）
def chunk_recursive(documents, chunk_size=1000, chunk_overlap=200):
    """
    递归分块：尝试多种分隔符

    分隔符优先级：段落 > 句子 > 词 > 字符

    Args:
        documents: 文档列表
        chunk_size: 每块大小
        chunk_overlap: 重叠大小

    Returns:
        分块列表
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    return chunks


# 使用示例
if __name__ == "__main__":
    sample_text = """
    人工智能（AI）是计算机科学的一个分支。
    它致力于创建能够执行通常需要人类智能的任务的系统。

    机器学习是AI的一个子集。
    它使计算机能够从数据中学习，而不是被明确编程。

    深度学习是机器学习的一种方法。
    它使用多层神经网络来模拟人脑的工作方式。
    """

    # 固定长度分块
    chunks_char = chunk_by_char(sample_text, chunk_size=50)
    print(f"字符分块: {len(chunks_char)} 个块")

    # Token分块
    chunks_token = chunk_by_token(sample_text, chunk_size=20)
    print(f"Token分块: {len(chunks_token)} 个块")
