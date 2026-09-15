"""评估向量检索效果的简单示例。"""

import importlib

vector_retrieval = importlib.import_module("11_vector_retrieval")
VectorStore = vector_retrieval.VectorStore


def evaluate_retrieval(vector_store, test_queries, expected_docs):
    """评估检索结果的 Top-1 准确率。

    Args:
        vector_store: 已经添加文档的向量存储对象。
        test_queries: 测试查询列表。
        expected_docs: 每个查询对应的正确文档下标，按 0 开始计数。

    Returns:
        准确率（0 到 1 之间的浮点数）。
    """
    if len(test_queries) != len(expected_docs):
        raise ValueError("test_queries 和 expected_docs 的长度必须一致")
    if not test_queries:
        raise ValueError("至少需要一个测试查询")

    correct = 0

    for query, expected_idx in zip(test_queries, expected_docs):
        results = vector_store.query(query, n_results=3)
        top_ids = results.get("ids", [[]])[0]
        if not top_ids:
            raise ValueError(f"查询没有返回结果: {query}")

        # 11_vector_retrieval.py 使用 doc_0、doc_1 这样的 ID。
        retrieved_idx = int(top_ids[0].split("_", 1)[1])
        is_correct = (retrieved_idx == expected_idx)
        correct += int(is_correct)

        mark = "[OK]" if is_correct else "[MISS]"
        print(f"查询: {query}")
        print(f"  期望文档: doc_{expected_idx}")
        print(f"  实际文档: doc_{retrieved_idx} {mark}")
        print()

    accuracy = correct / len(test_queries)
    print(f"Top-1 准确率: {accuracy:.2%} ({correct}/{len(test_queries)})")
    return accuracy


if __name__ == "__main__":
    documents = [
        "Python是一种高级编程语言，由Guido创建",
        "JavaScript主要用于Web前端开发",
        "Rust注重内存安全和性能",
        "Go语言适合并发编程",
        "Java是企业级开发的常用语言",
    ]

    metadatas = [
        {"category": "编程语言", "name": "Python"},
        {"category": "编程语言", "name": "JavaScript"},
        {"category": "编程语言", "name": "Rust"},
        {"category": "编程语言", "name": "Go"},
        {"category": "编程语言", "name": "Java"},
    ]

    print("=" * 60)
    print("向量检索评估示例")
    print("=" * 60 + "\n")

    vector_store = VectorStore("evaluation_bge_collection")

    # PersistentClient 会保留上次运行的数据，避免重复添加相同 ID。
    if vector_store.collection.count() == 0:
        vector_store.add_documents(documents, metadatas)
    else:
        print("复用已有的 evaluation_bge_collection 集合")

    test_queries = [
        "哪种语言主要用于Web前端开发？",
        "哪种语言注重内存安全？",
        "哪种语言适合并发编程？",
        "哪种语言常用于企业级开发？",
    ]
    expected_docs = [1, 2, 3, 4]

    evaluate_retrieval(vector_store, test_queries, expected_docs)
    print("\n[OK] 检索评估示例完成！")
