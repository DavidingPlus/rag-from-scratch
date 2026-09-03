# RAG Learning Roadmap

> 本文是项目的 RAG 学习主线。后续推进学习时，按本文的顺序，结合 `reference/rag-tutorial/` 中的对应资料学习和实践。

## 1. 总体路线

```text
环境确认
   ↓
模块1：基础 RAG + 评估
   ↓
案例1：智能客服 RAG
   ↓
模块2：检索、排序和性能优化
   ↓
案例2：技术文档问答
   ↓
模块3：Agentic RAG / GraphRAG / 多模态 RAG
   ├─ 案例3：AI 研究助手 Agent
   ├─ 案例4：知识图谱问答
   └─ 案例5：多模态产品问答
   ↓
模块4：生产部署与运维
   ↓
案例6：企业级 RAG 平台
```

推荐完整学习量约为 **60～80 小时**。如果每天学习 1～2 小时，可以按 6～10 周推进；不建议只阅读文档，每个阶段都要运行 Notebook、完成练习，并把结果合并到自己的 RAG 项目中。

## 2. 阶段一：模块1——基础入门

目标：能够从零实现一个基础文档问答系统，并建立可重复的评估基线。

参考入口：[模块1 README](../reference/rag-tutorial/docs/01-基础入门/README.md)

| 步骤 | 学习内容 | 参考资料 | 完成标准 |
|---|---|---|---|
| M1-01 | RAG 是什么、为什么需要 RAG；RAG 与 Fine-tuning、Prompt Engineering 的区别；RAG 五大组件 | [第1章](../reference/rag-tutorial/docs/01-基础入门/01-RAG技术概述.md)；[概念 Notebook](../reference/rag-tutorial/notebooks/module1/01_rag_concepts.ipynb) | 能画出并解释 RAG 流程，知道检索和生成各自解决什么问题 |
| M1-02 | Python 虚拟环境、Jupyter、LlamaIndex、Chroma 和示例数据 | [第2章](../reference/rag-tutorial/docs/01-基础入门/02-环境搭建与工具准备.md)；[环境 Notebook](../reference/rag-tutorial/notebooks/module1/02_environment_setup.ipynb) | Notebook 可以运行，依赖和 API 配置可用 |
| M1-03 | 文档加载、文本分块、Embedding、向量数据库、相似度检索、LLM 生成 | [第3章](../reference/rag-tutorial/docs/01-基础入门/03-基础RAG实现.md)；[基础实现 Notebook](../reference/rag-tutorial/notebooks/module1/03_basic_rag_implementation.ipynb) | 不完全照抄代码，也能说清并实现端到端基础 RAG |
| M1-04 | 检索评估：Hit Rate、MRR、Precision@K；生成评估：Faithfulness、Relevancy；RAGAS | [第4章](../reference/rag-tutorial/docs/01-基础入门/04-RAG评估基础.md)；[评估 Notebook](../reference/rag-tutorial/notebooks/module1/04_rag_evaluation.ipynb) | 准备自己的测试问题集，记录基础 RAG 的评估结果 |
| M1-05 | 复习和项目整合，完成 InteliKB-Lite | [第5章](../reference/rag-tutorial/docs/01-基础入门/05-模块1总结与项目.md)；[模块1练习](../reference/rag-tutorial/exercises/module1/module1_exercises.md) | 得到一个可运行的文档问答项目和一份基础评估记录 |

### 模块1里程碑

完成以下内容后再进入模块2：

- 可以解释 `文档 → 分块 → 向量化 → 检索 → 生成` 的完整链路。
- 可以加载自己的 Markdown、TXT 或 PDF 文档。
- 有至少一组人工整理的测试问题和预期答案。
- 能用 Hit Rate、MRR 等指标判断检索效果。

### 配套案例：案例1

[案例1课程说明](../reference/rag-tutorial/docs/projects/case1-customer-service.md)；[案例1源码说明](../reference/rag-tutorial/projects/case1-customer-service/README.md)

重点不是把界面做得复杂，而是把基础 RAG 从 Notebook 整理成一个可以交互使用的应用，理解知识库管理、多轮对话和 Streamlit 入口。

## 3. 阶段二：模块2——核心优化

目标：知道基础 RAG 为什么检索不准、排序不合理、上下文太长或响应太慢，并能用实验验证优化效果。

参考入口：[模块2 README](../reference/rag-tutorial/docs/02-核心优化/README.md)

| 步骤 | 学习内容 | 参考资料 | 完成标准 |
|---|---|---|---|
| M2-01 | Embedding 原理、主流模型对比、中文模型选择、微调和评估 | [第6章](../reference/rag-tutorial/docs/02-核心优化/06-嵌入模型深入.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/06_embedding_models.ipynb) | 能根据语言、成本、部署方式和质量要求选择 Embedding 模型 |
| M2-02 | 语义分块、上下文分块头、递归分块、父文档检索、代码分块 | [第7章](../reference/rag-tutorial/docs/02-核心优化/07-高级分块策略.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/07_advanced_chunking.ipynb) | 在自己的数据上比较至少两种分块策略和参数 |
| M2-03 | HyDE、查询重写、多查询、查询分解 | [第8章](../reference/rag-tutorial/docs/02-核心优化/08-查询增强技术.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/08_query_enhancement.ipynb) | 能解释原始问题为什么需要改写，并比较增强前后的召回效果 |
| M2-04 | 向量检索、BM25、混合检索、RRF、CrossEncoder 重排序 | [第9章](../reference/rag-tutorial/docs/02-核心优化/09-混合检索与重排序.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/09_hybrid_retrieval.ipynb) | 完成一个向量 + 关键词 + 重排序的检索链路 |
| M2-05 | 迭代检索、自适应检索、Skip Reading、元数据过滤 | [第10章](../reference/rag-tutorial/docs/02-核心优化/10-高级RAG模式.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/10_advanced_rag_patterns.ipynb) | 能判断简单问题和复杂问题是否应该使用不同检索流程 |
| M2-06 | 缓存、批处理、并发、异步、内存和响应时间优化 | [第11章](../reference/rag-tutorial/docs/02-核心优化/11-性能优化.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/11_performance_optimization.ipynb) | 记录优化前后的延迟、吞吐量和成本变化 |
| M2-07 | 上下文压缩、相关片段提取、减少无关上下文 | [第13章](../reference/rag-tutorial/docs/02-核心优化/13-检索压缩优化.md)；[Notebook](../reference/rag-tutorial/notebooks/module2/13_retrieval_compression.ipynb) | 能在不明显损失答案质量的情况下减少上下文长度 |
| M2-08 | 把前面的优化组合到 InteliKB v2.0，进行 A/B 测试和结果分析 | [第12章](../reference/rag-tutorial/docs/02-核心优化/12-综合项目优化.md)；[综合 Notebook](../reference/rag-tutorial/notebooks/module2/12_comprehensive_optimization.ipynb)；[模块2完整代码说明](../reference/rag-tutorial/docs/02-核心优化/code/README.md)；[模块2练习](../reference/rag-tutorial/exercises/module2/module2_exercises.md) | 得到优化前后对比表和一套可解释的优化方案 |

### 模块2里程碑

完成后应该有：

- 一个基础 RAG 与优化 RAG 的对比版本。
- 一份包含召回率、MRR、答案质量、延迟和成本的实验记录。
- 能区分“召回不到”“排位靠后”“上下文污染”和“生成错误”。
- 能根据数据特点选择分块、查询增强、混合检索或重排序，而不是盲目叠加技术。

### 配套案例：案例2

[案例2课程说明](../reference/rag-tutorial/docs/projects/case2-doc-qa.md)；[案例2源码说明](../reference/rag-tutorial/projects/case2-doc-qa/README.md)

重点理解混合检索、BM25、CrossEncoder 重排序，以及代码和技术文档场景为什么不能只依赖向量检索。

## 4. 阶段三：模块3——高级架构

目标：处理需要多步决策、复杂关系推理或图文联合理解的问题。

参考入口：[模块3 README](../reference/rag-tutorial/docs/03-高级架构/README.md)；[模块3练习](../reference/rag-tutorial/exercises/module3/module3_exercises.md)；[模块3练习参考答案](../reference/rag-tutorial/exercises/module3/参考答案.md)

| 步骤 | 学习内容 | 参考资料 | 完成标准 |
|---|---|---|---|
| M3-01 | Agent、Tool、ReAct、动态检索和工具调用 | [第13章](../reference/rag-tutorial/docs/03-高级架构/13-Agentic-RAG基础.md)；[Notebook](../reference/rag-tutorial/notebooks/module3/13_react_agent.ipynb) | 能构建一个会判断是否检索、并调用工具的 Agent |
| M3-02 | Plan-and-Execute、多 Agent、自我反思、Deep Research | [第14章](../reference/rag-tutorial/docs/03-高级架构/14-高级Agent模式.md)；[高级 Agent Notebook](../reference/rag-tutorial/notebooks/module3/14_advanced_agents.ipynb)；[Deep Research Notebook](../reference/rag-tutorial/notebooks/module3/14_deep_research_agent.ipynb) | 能将复杂任务拆分为计划、执行、验证和汇总 |
| M3-03 | 实体、关系、图嵌入、图检索、多跳推理、GraphRAG | [第15章](../reference/rag-tutorial/docs/03-高级架构/15-知识图谱RAG.md)；[Notebook](../reference/rag-tutorial/notebooks/module3/15_graph_rag.ipynb) | 能判断什么时候需要图谱，并完成一个简单多跳问答 |
| M3-04 | CLIP、图像检索、图文跨模态检索、多模态生成 | [第16章](../reference/rag-tutorial/docs/03-高级架构/16-多模态RAG.md)；[Notebook](../reference/rag-tutorial/notebooks/module3/16_multimodal_rag.ipynb) | 能完成以图搜图、以文搜图或图文问答中的至少一种 |

### 模块3的选择建议

- 普通企业知识库：优先 M3-01、M3-02，再按业务需要学习 M3-03。
- 关系复杂、需要多跳推理：重点学习 M3-03。
- 电商、工业、图片资料场景：重点学习 M3-04。
- 不要为了“高级”而强行使用 Agent、GraphRAG 或多模态；先确认基础 RAG 和模块2优化已经解决不了问题。

### 配套案例：案例3～5

- [案例3课程说明](../reference/rag-tutorial/docs/projects/case3-research-agent.md)；[案例3源码说明](../reference/rag-tutorial/projects/case3-research-agent/README.md)
- [案例4课程说明](../reference/rag-tutorial/docs/projects/case4-knowledge-graph.md)；[案例4源码说明](../reference/rag-tutorial/projects/case4-knowledge-graph/README.md)
- [案例5课程说明](../reference/rag-tutorial/docs/projects/case5-multimodal.md)；[案例5源码说明](../reference/rag-tutorial/projects/case5-multimodal/README.md)

## 5. 阶段四：模块4——生产部署

目标：将一个能运行的 RAG Demo 整理成可部署、可监控、可扩展和更安全的服务。

参考入口：[模块4 README](../reference/rag-tutorial/docs/04-生产部署/README.md)；[模块4练习](../reference/rag-tutorial/exercises/module4/module4_exercises.md)；[模块4练习参考答案](../reference/rag-tutorial/exercises/module4/参考答案.md)

| 步骤 | 学习内容 | 参考资料 | 完成标准 |
|---|---|---|---|
| M4-01 | Dockerfile、多阶段构建、Docker Compose、容器网络和存储 | [第17章](../reference/rag-tutorial/docs/04-生产部署/17-Docker容器化.md) | 可以用 Docker Compose 启动 RAG 服务及其依赖 |
| M4-02 | Kubernetes、Deployment、Service、Ingress、Secret、扩缩容和滚动更新 | [第18章](../reference/rag-tutorial/docs/04-生产部署/18-Kubernetes部署.md) | 能完成一次本地或测试环境的 K8s 部署 |
| M4-03 | Prometheus、Grafana、ELK、Jaeger、告警 | [第19章](../reference/rag-tutorial/docs/04-生产部署/19-监控和日志.md) | 能查看请求量、延迟、错误率、Token 使用和检索耗时 |
| M4-04 | GitHub Actions、自动测试、镜像构建、多环境发布 | [第20章](../reference/rag-tutorial/docs/04-生产部署/20-CI-CD流程.md) | 提交代码后可以自动测试并构建部署产物 |
| M4-05 | 多层缓存、数据库和向量检索优化、并发、压力测试 | [第21章](../reference/rag-tutorial/docs/04-生产部署/21-性能优化.md) | 有性能基线、瓶颈定位过程和压力测试结果 |
| M4-06 | JWT、RBAC、数据加密、输入验证、提示词注入防护、限流 | [第22章](../reference/rag-tutorial/docs/04-生产部署/22-安全实践.md) | 关键 API 有认证、授权、输入校验和基本审计能力 |
| M4-07 | 生产架构、故障排查、容量规划、灾备和运维流程 | [第23章](../reference/rag-tutorial/docs/04-生产部署/23-最佳实践和案例分析.md) | 能写出部署说明、监控说明和故障处理预案 |

### 配套案例：案例6

[案例6课程说明](../reference/rag-tutorial/docs/projects/case6-enterprise-platform.md)；[案例6源码说明](../reference/rag-tutorial/projects/case6-enterprise-platform/README.md)

重点理解 FastAPI、JWT、Redis、权限管理、服务拆分和生产运维之间的关系。案例中的性能数字是示例目标，实际结果要以自己的压测数据为准。

### 模块4的 Notebook 说明

参考仓库提供了[模块4 Notebook说明](../reference/rag-tutorial/notebooks/module4/README.md)，但当前实际文件清单中没有 `17_deployment_practice.ipynb` 文件。因此模块4以章节文档、练习题和案例源码为主，不把不存在的 Notebook 当作必需依赖。

## 6. 实战案例源码索引

案例课程文档介绍目标和架构，案例 README 介绍运行方式，下面列出实际源码中的主要入口，便于学习时对照阅读。

| 案例 | 主要源码 | 学习重点 |
|---|---|---|
| 案例1：智能客服 RAG | [`main.py`](../reference/rag-tutorial/projects/case1-customer-service/main.py)、[`rag_system.py`](../reference/rag-tutorial/projects/case1-customer-service/rag_system.py)、[`knowledge_base.py`](../reference/rag-tutorial/projects/case1-customer-service/knowledge_base.py) | 基础 RAG、知识库、Streamlit、多轮对话 |
| 案例2：技术文档问答 | [`main.py`](../reference/rag-tutorial/projects/case2-doc-qa/main.py)、[`doc_qa_system.py`](../reference/rag-tutorial/projects/case2-doc-qa/doc_qa_system.py)、[`hybrid_retriever.py`](../reference/rag-tutorial/projects/case2-doc-qa/hybrid_retriever.py)、[`reranker.py`](../reference/rag-tutorial/projects/case2-doc-qa/reranker.py) | 混合检索、BM25、重排序 |
| 案例3：AI 研究助手 Agent | [`main.py`](../reference/rag-tutorial/projects/case3-research-agent/main.py)、[`research_agent.py`](../reference/rag-tutorial/projects/case3-research-agent/research_agent.py)、[`tools.py`](../reference/rag-tutorial/projects/case3-research-agent/tools.py) | ReAct、工具调用、研究流程 |
| 案例4：企业知识图谱问答 | [`main.py`](../reference/rag-tutorial/projects/case4-knowledge-graph/main.py)、[`knowledge_graph.py`](../reference/rag-tutorial/projects/case4-knowledge-graph/knowledge_graph.py)、[`graph_rag.py`](../reference/rag-tutorial/projects/case4-knowledge-graph/graph_rag.py) | 实体关系、图检索、多跳推理 |
| 案例5：多模态产品问答 | [`main.py`](../reference/rag-tutorial/projects/case5-multimodal/main.py)、[`multimodal_rag.py`](../reference/rag-tutorial/projects/case5-multimodal/multimodal_rag.py) | CLIP、图文检索、视觉问答 |
| 案例6：企业级 RAG 平台 | [`main.py`](../reference/rag-tutorial/projects/case6-enterprise-platform/main.py)、[`rag_engine.py`](../reference/rag-tutorial/projects/case6-enterprise-platform/rag_engine.py)、[`auth.py`](../reference/rag-tutorial/projects/case6-enterprise-platform/auth.py)、[`cache.py`](../reference/rag-tutorial/projects/case6-enterprise-platform/cache.py) | FastAPI、认证、缓存、企业服务化 |

完整案例说明见[实战案例索引](../reference/rag-tutorial/docs/projects/index.md)。

## 7. 每一步的固定学习方法

每个步骤按以下顺序执行：

```text
1. 阅读对应章节，先理解问题和概念
2. 运行对应 Notebook，确认代码能工作
3. 修改一个关键参数或替换一种策略
4. 完成对应练习题，不先看参考答案
5. 把结果接入自己的 RAG 项目
6. 记录指标、问题和结论
```

建议每个阶段都保留一个可运行版本：

```text
baseline/       基础 RAG 基线
optimized/      模块2优化版本
agentic/        模块3高级架构版本
production/     模块4生产化版本
```

## 8. 阶段检查点

### 进入模块2前

- 能独立实现基础 RAG。
- 有自己的文档数据和测试问题集。
- 已记录基础 Hit Rate、MRR、延迟等指标。

### 进入模块3前

- 至少完成一种分块优化。
- 至少完成一种查询增强或混合检索。
- 完成重排序或上下文压缩中的至少一项。
- 有优化前后的实验对比。

### 进入模块4前

- 基础 RAG 服务功能稳定。
- 检索和生成链路有基本日志。
- 已知系统的主要质量、延迟和成本瓶颈。
- 明确是否真的需要 Agent、GraphRAG 或多模态能力。

## 9. 参考仓库索引

- 课程总览：[reference/rag-tutorial/README.md](../reference/rag-tutorial/README.md)
- 文档站点首页：[docs/index.md](../reference/rag-tutorial/docs/index.md)
- 原教程导航：[00-教程导航.md](../reference/rag-tutorial/docs/01-基础入门/00-教程导航.md)
- 总依赖：[requirements.txt](../reference/rag-tutorial/requirements.txt)
- 顶层 Notebook：[reference/rag-tutorial/notebooks/](../reference/rag-tutorial/notebooks/)
- 练习题：[reference/rag-tutorial/exercises/](../reference/rag-tutorial/exercises/)，包含模块1～4练习和参考答案
- 实战案例索引：[projects/index.md](../reference/rag-tutorial/docs/projects/index.md)
- 图表资源：[assets/images/README.md](../reference/rag-tutorial/assets/images/README.md)

练习题的具体入口：

- [模块1练习](../reference/rag-tutorial/exercises/module1/module1_exercises.md)；[模块1学习总结](../reference/rag-tutorial/exercises/module1/learning_summary.md)；[模块1参考答案](../reference/rag-tutorial/exercises/module1/参考答案.md)
- [模块2练习](../reference/rag-tutorial/exercises/module2/module2_exercises.md)；[模块2参考答案](../reference/rag-tutorial/exercises/module2/参考答案.md)
- [模块3练习](../reference/rag-tutorial/exercises/module3/module3_exercises.md)；[模块3参考答案](../reference/rag-tutorial/exercises/module3/参考答案.md)
- [模块4练习](../reference/rag-tutorial/exercises/module4/module4_exercises.md)；[模块4参考答案](../reference/rag-tutorial/exercises/module4/参考答案.md)

说明：参考仓库的部分 README 对章节总数描述不完全一致。当前路线以实际目录为准：模块1为第1～5章，模块2为第6～13章，模块3为第13～16章，模块4为第17～23章。模块2和模块3都出现“第13章”，这是两个模块各自的编号。顶层 `notebooks/` 与 `docs/*/notebooks/` 中存在对应副本，路线图统一使用顶层 Notebook；`04-生产部署/notebooks/README.md` 描述了一个部署 Notebook，但该 `.ipynb` 当前不在实际文件清单中。

`SKILL_GUIDE.md`、`CONTRIBUTING.md`、`mkdocs.yml`、`LICENSE` 等属于教程项目开发、站点配置或许可证资料，不是 RAG 学习步骤，因此没有作为单独路线节点列入。

## 10. 后续协作约定

当用户要求“继续学习”“开始下一步”或“按路线推进”时：

1. 先读取本文，确认用户指定的阶段或步骤。
2. 打开该步骤列出的参考章节、Notebook、练习题和案例源码。
3. 用“概念讲解 → 代码实践 → 练习 → 小结”的顺序推进。
4. 不在本文记录动态进度；动态进度以项目代码、运行结果和提交记录为准。
