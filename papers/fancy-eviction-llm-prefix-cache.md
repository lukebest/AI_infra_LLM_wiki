---
type: Paper
title: "When Fancy Eviction Fails: LLM Prefix Cache 淘汰重思"
description: "Harvard 生产轨迹×14 算法；LRU 难被击败；partial-node compute-aware vs LRU TTFT −19.9%、prefill +18.8%。"
tags:
- architecture
- inference
- serving
- kv-cache
- agentic-ai
- llm
- cache
- memory
- scheduling
- throughput
- latency
created: 2026-09-28
updated: 2026-09-28
timestamp: '2026-09-28T00:00:00Z'
paper_author: [Yiyu Liu, Minlan Yu, Juncheng Yang]
year: 2026
arxiv: '2609.28870'
sources:
  - raw/papers/Fancy_Eviction_LLM_Prefix_Cache_2026.pdf
  - raw/papers/fancy-eviction-llm-prefix-cache.md
---

# When Fancy Eviction Fails：Prefix Cache 淘汰

## 一句话结论

对两条含 agentic 流量的生产 prefix-cache 轨迹评估 **14** 种在线淘汰算法：传统「花哨」策略在命中率上几乎打不过 **LRU**，同时离 Belady 仍远；原因是前缀复用由活跃会话的规则节拍主导、会话寿命短。作者提出以 **compute-savings** 为目标的 compute-aware 淘汰，并在 vLLM + Qwen3-Coder-30B @48 GiB 上用 partial-node 实现相对 LRU 平均 TTFT **−19.9%**、prefill 吞吐 **+18.8%**。

## 动机：命中率优化与 TTFT 脱节

长会话与自治 agent 把上下文推到数十万 token；prefix cache 是降 prefill / TTFT 的关键。Web/块存储时代的频率、学习型淘汰被大量移植，但 agentic 前缀访问模式缺少生产级刻画。同一命中率下，驱逐「浅前缀」与「深前缀」的重算代价可差几个数量级——**hit ratio 不能直接预测 TTFT**。

## 方案

### 1. 生产轨迹 + 忠实仿真器

FreeInference：**327.5K** 请求、**10.5B** tokens、7 天；Chutes：**515.8K** / **9.7B** / 130.9 天。仿真器尊重请求级驻留与块粒度，相对 vLLM Python 评估最高约 **160×**。

### 2. 为何 LRU 难被击败

多轮会话历史约占 distinct blocks 的 **37.6%**，却贡献 **70.2%** 访问；单轮块大量 one-hit（文中 **84.9%** 仅访问一次）。会话内复用间隔短、跨会话全局热核弱 → **recency** 几乎捕获全部可预测性；频率类策略常更差。

### 3. Compute-aware 原则与 PartialNode

引入 compute-savings ratio 与 BeladyCompute 等 offline 界。在线 RandomCompute 按 \(\mathrm{Score}=\mathrm{ComputeIntensity}/\mathrm{TimeSinceLastAccess}\) 采样淘汰廉价浅块；为避免「洞」打碎前缀、拖垮并行 attention，生产可用形态改为 **partial-node** 连续块驱逐。容量紧时 HBM 用块级、大池可用会话级粒度。

## 量化结果

- **命中率（Figure 2）**：多容量下 ARC/Sieve/S3-FIFO/LIRS/LHD/LeCaR/3LCache/LRB 等均无法稳定超过 LRU；Belady 仍显著更高。
- **vLLM 实测（48 GiB，Qwen3-Coder-30B）**：partial-node compute-aware vs LRU — 平均 TTFT **1.04 vs 1.29 s（−19.9%）**；prefill **65.6K vs 55.2K tok/s（+18.8%）**；p99 TTFT **26.0 → 16.8 s**。块级 RandomCompute 因碎片化：TTFT **4.0×↑**、吞吐 **3.9×↓**。
- **偏斜**：top 10% 会话囤积 **76.2%** KV 字节（top 1% **20.3%**）。
- **24 GiB 成本模型**：RandomCompute compute-savings **0.638**，较 LRU **+10.4** points，甚至超过标准 hit-optimal Belady。

## 局限与解读

- 轨迹来自两家组织，agentic 占比不同；结论强调「以 LRU 为底座再叠加 compute-aware」，非宣称 LRU 全局最优。
- Offline Belady 界不可在线实现；partial-node 是工程折中。
- 与 [Ask the Tool](../papers/ask-tool-progress-agent-kv-serving.md)（工具 progress 感知）、[Hot–Cold HBM/HBF](../papers/hotcold-hbm-hbf-agentic-llm.md)（热冷分层）、[EMA](../papers/ema-elastic-memory-across-gpus.md)（跨 GPU 弹性容量）同属 agentic serving 内存管理；概念锚点见 [Memory Hierarchy and Cache](../concepts/memory-hierarchy-cache.md) 与 [End-to-End Memory Data Path](../concepts/end-to-end-memory-data-path.md)。

# Citations

1. Liu, Y., Yu, M., Yang, J. “When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse.” arXiv:2609.28870, 2026. [arXiv](https://arxiv.org/abs/2609.28870)
2. [本地原文 PDF](../raw/papers/Fancy_Eviction_LLM_Prefix_Cache_2026.pdf)；[原始来源记录](../raw/papers/fancy-eviction-llm-prefix-cache.md)
