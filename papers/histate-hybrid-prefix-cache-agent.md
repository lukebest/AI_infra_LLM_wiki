---
type: Paper
title: "HiState: Hierarchical Prefix Cache Management for Hybrid LLM Serving in Agentic Workloads"
description: "UCSD — 混合 LLM（全注意+循环）agent 前缀缓存；历史循环 checkpoint 落 SSD、KV 占快存；真实 coding-agent 轨迹 p99 TTFT 相对 vLLM-Marconi 最高 5.73×、SGLang-HiCache 5.44×"
tags:
- inference
- serving-system
- prefix-cache
- kv-cache
- hybrid-llm
- agentic-ai
- storage
- ssd
- latency
- llm
created: 2026-11-04
updated: 2026-11-04
timestamp: '2026-11-04T00:00:00Z'
paper_author: [Zaifeng Pan, Lucas Wang, Xinwei Qiang, Yanbo Zhou, Chang Chen, Zhengding Hu, Yue Guan, Yufei Ding]
year: 2026
venue: arXiv
arxiv: '2610.41508'
sources:
  - raw/papers/HiState_Hybrid_Prefix_Cache_Agent_2026.pdf
  - raw/papers/histate-hybrid-prefix-cache-agent.md
---

# HiState：混合模型上面向 agent 的分层前缀缓存

## 一句话结论
混合 LLM（全注意层 + 循环线性层）里，循环 checkpoint **无法**从较短前缀反推更早状态；agent 会改写并回访旧上下文，现有边界 checkpoint 常未保存或已驱逐。HiState 观察到命中时需要**全部匹配 KV**，但只需**一个**循环 checkpoint——把历史 checkpoint 留在 **SSD**，快存优先给 KV；配合自适应间隔与统一驱逐。基于 vLLM，在真实 coding-agent 轨迹上 **p99 TTFT** 相对 vLLM-Marconi 最高 **5.73×**、相对 SGLang-HiCache **5.44×**。

## 动机
- 前缀缓存能跨请求省计算，但循环层状态不可像 KV 一样任意截断复用。
- 对话场景的边界 checkpoint 对「改写/回访更早前缀」的 agent 轨迹不够用。
- 多留 checkpoint 会挤占其它会话的可复用前缀，引发连锁 miss。

## 方案
1. **非对称分层**：快存优先保留 KV；历史循环 checkpoint 落 SSD；每次命中只取**一个**与长度无关的 checkpoint。
2. **自适应间隔**：在 checkpoint 存储开销与重算之间调间隔密度。
3. **统一驱逐**：checkpoint 稀疏化与陈旧轨迹回收联动，避免单侧占满。
4. **实现与评测**：叠在 vLLM；Qwen3.5-9B；Weka + TraceLab 公开 coding-agent 轨迹与微基准；对照 vLLM-Marconi、SGLang-HiCache。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 真实 agent 轨迹 p99 TTFT vs vLLM-Marconi | 最高 **5.73×** |
| 真实 agent 轨迹 p99 TTFT vs SGLang-HiCache | 最高 **5.44×** |
| 正文另报相对 Marconi（p95 / p99） | 最高 **7.40× / 5.73×** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 前缀页式共享；HiState 补混合模型循环 checkpoint 的分层与 agent 回访
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — SSD 上的历史 checkpoint 与快存 KV 的非对称路径
- [SSD / NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — checkpoint I/O 与前缀复用协同
- [FlatCake](/papers/flatcake-flat-kvcache-storage.md) — 同属 DRAM/SSD KV 路径；FlatCake 扁平放置，HiState 专攻混合层 checkpoint

## 开放问题
- 评测以 coding-agent 轨迹与 Qwen3.5-9B 为主；更大混合模型族与多租户干扰下的间隔策略仍待展开。
- SSD checkpoint 取回与调度重叠的极限延迟分布依赖具体存储栈。

# Citations
- [arXiv:2610.41508](https://arxiv.org/abs/2610.41508) — Pan et al., UCSD, 2026
- [raw stub](/raw/papers/histate-hybrid-prefix-cache-agent.md)
