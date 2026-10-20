---
type: Paper
title: "Understanding KV Residency in Production-Scale Agentic LLM Workloads"
description: "Microsoft M365/IISc — 4 条生产 trace、>1.21 亿次模型调用；Deep Research 一个 P99 会话 81.6 GiB 超 H100 HBM，全驻留峰值约 501.8 TB；1 小时空闲上限降 3.6×；10% 预算下 LRU/FNU/int4 MRR 重算率 63%/31%/13.6%；跨部署复用 89%→29%"
tags:
- agentic-ai
- kv-cache
- inference
- serving-system
- memory
- hbm
- quantization
- workload-characterization
- microsoft
created: 2026-10-20
updated: 2026-10-20
timestamp: '2026-10-20T00:00:00Z'
paper_author: [Mayank Arya, Agrim Bari, Anjaly Parayil, Yogesh Simmhan, Renee St. Amant, Victor Rühle, Saravan Rajmohan]
year: 2026
arxiv: '2610.22863'
sources:
  - raw/papers/Agentic_KV_Residency_M365_Production_2026.pdf
  - raw/papers/agentic-kv-residency-m365-production.md
---

# 生产级 agentic 负载的 KV 驻留刻画

## 一句话结论
agentic 应用把一次用户请求拆成一串「模型调用 + 工具调用」，上下文越滚越长；要靠前缀缓存省掉重算，就得把会话 KV 长期留在 HBM，在机群规模上这是一个几百 TB 级的容量问题。光靠淘汰策略扛不住，论文给出两条出路：改变 KV 的表示（降精度保留），以及按部署亲和路由或迁移 KV。

## 动机
- 数据：Microsoft M365 四条生产 trace（Deep Research、Enterprise Assistant、Coding Agent、Enterprise Chat），合计 **>1.21 亿**次模型调用。
- Deep Research 里 **89%** 的模型调用由应用自身发起；中位上下文从约 **10K** token 涨到第 30 次调用时约 **68K**；约 **80%** 上下文 token 命中前缀缓存。
- 用公开的 Llama-2-70B（GQA）KV 布局代替保密模型：一个 P99 Research 会话需 **81.6 GiB**，超过 H100 的 80 GB HBM；所有活跃会话按峰值驻留约需 **501.8 TB** HBM，而推理只占驻留时间的 **5.6%**，其余是工具执行与空闲间隙。
- Research 中承载长上下文的重模型类（Spine）占调用上下文 KV 字节 **67%**，只占未缓存 token **32%**，自转移概率 **0.97**，可预测性强。

## 方案（刻画 + 回放）
1. 按会话/调用统计上下文增长、复用与空闲间隔（四个负载的中位空闲间隔落在 6–10 s 带内）。
2. 用 trace 驱动的驻留回放比较策略：空闲上限、LRU、clairvoyant 最远下次使用（FNU，Belady）、多分辨率保留（MRR：把 LRU 受害会话的 KV 降为 int4 留在 HBM，而非丢弃）。
3. 单独建模「KV 只在本部署可用」带来的放置约束。
4. 计划开源参数化 trace 生成器 AgenticTraceSim 与驻留回放框架（生产 trace 本身不公开）。

## 效果（论文数字）
| 场景 | 结果 |
|---|---|
| 1 小时空闲上限 | 全驻留上限 501.8 → **140.8 TB**（**3.6×**），需重算的调用占比 4.07% → **4.53%** |
| 预算 = 最忙小时需求的 1/10 | 需重算的 Research 调用：LRU **62.9%**，FNU **31.1%**，int4 MRR **13.6%**（比 FNU 低 **2.3×**） |
| 计入 int4 分组量化元数据 | HBM 内 MRR 重算率升到 **14.99%–19.25%** |
| 放置 | 同部署连续调用复用 **88.9%**，同区域换部署后 **29.0%**；KV 视作部署本地时，无限内存下的首触重算下限 **5.4% → 20.2%** |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 会话级 KV 驻留与跨部署放置是 PD 分离之外的另一层调度问题
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 500 TB 级驻留需求直接推动 HBM 之外的容量层（HBF、host DRAM、CXL）
- [Lachesis](/papers/lachesis-lifetime-aware-kv-hbm-hbf.md)、[Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md) — 同样从 agent 会话寿命出发做 KV 分层；本文给出生产侧的规模与空闲占比
- [RREvict](/papers/rrevict-prefix-cache-eviction-agentic.md) — agentic 前缀缓存淘汰策略，本文说明仅靠淘汰在紧预算下不够
- [HBFSim (MBZUAI)](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md) — HBF 作为容量层时 KV 写入决定寿命

## 开放问题
- 回放没有测量 int4 KV 对回答质量的影响，只引用已发表的开源模型评测（70B 以内最多掉 1.03 分）。
- 用 Llama-2-70B 布局代替保密模型；MLA 等压缩 KV 的模型会改变 TB 级结论的绝对值。
- MRR 降级副本放到 host DRAM 层时，回放未计传输与反量化开销。
- 对硬件的含义：会话级 KV 的「推理 5.6%、空闲 94%」占比，意味着容量层的带宽要求可以远低于 HBM，但需要按会话粒度快速提升；这是 wiki 侧推论，需要后续论文验证。

# Citations
- Arya et al., "Understanding KV Residency in Production-Scale Agentic LLM Workloads", arXiv:2610.22863. [raw](/raw/papers/agentic-kv-residency-m365-production.md) · [PDF](/raw/papers/Agentic_KV_Residency_M365_Production_2026.pdf)
