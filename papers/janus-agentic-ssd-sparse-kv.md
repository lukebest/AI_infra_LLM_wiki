---
type: Paper
title: "Janus: Agentic Serving with SSD-Centric Sparse KV"
description: "上交大等 — 稀疏注意力×SSD KV；TTFT 最高 1.57–3.69×（均值 1.22–1.85×）；关键路径 SSD I/O <6.5%"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- kv-cache
- agentic-ai
- storage
- memory
- sparse
- attention
- latency
- prefill
- gpu
created: 2026-10-01
updated: 2026-10-01
timestamp: '2026-10-01T00:00:00Z'
paper_author: [Wenhao He, Ping Zhang, Xiaohe Hu, Chutian Wang, Jinlong Hou, Yuan Cheng, Peng Sun, Fangcheng Fu]
year: 2026
arxiv: '2609.36938'
sources:
  - raw/papers/Janus_Agentic_SSD_Sparse_KV_2026.pdf
  - raw/papers/janus-agentic-ssd-sparse-kv.md
---

# Janus: 面向 Agent 的 SSD 中心稀疏 KV 服务

## 一句话结论

在 **稀疏注意力**（DeepSeek-V4 / GLM-5 系）与 **SSD 中心 KV** 下，用模型自身 indexer 提前预测 KV 需求并与计算重叠，辅以合并读/写打包/相感知写限流；三模型×三 agent 轨迹上 TTFT 相对既有工作最高 **1.57–3.69×**（均值 **1.22–1.85×**），关键路径 SSD I/O **<6.5%** append-prefill 延迟。

## 动机

- Agentic 会话多轮 append、上下文极长；稀疏注意力使「读哪些 KV」依赖当轮中间态，SSD 读易落到关键路径（文中可占 append-prefill **>30%**）。
- DRAM 容量贵（文中公开报价量级：256 GB DDR5 vs 30.72 TB NVMe 单价差约两个数量级）；SSD 中心设计必需，但碎片读与读写干扰（并发写可令读带宽降约 **60%**）未充分优化。
- Agent 工况下约 **99%** 历史 KV 读发生在 **append prefill**，decode 多复用已加载历史——与 decode 步间相似预测假设不同。

对照 [Memory Hierarchy](/concepts/memory-hierarchy-cache.md)、[End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)、[Fathom](/papers/fathom-sparse-decoding-offloaded-kv.md)、[Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md)、[RR-Evict](/papers/rrevict-prefix-cache-eviction-agentic.md)。

## 方案

1. **训练无关预测**：对 indexer 喂更早中间态（DeepSeek-V4 取 d=2、GLM-5.2 取 d=4），预测读与主计算重叠；精确选择后只补 **corrective reads**，输出无损。
2. **多 GPU 切分预测**：历史分片并行跑 indexer，准确率影响可忽略，避免预测拖慢管线。
3. **SSD I/O**：相邻块 best-effort 合并读；CPU 辅助把散落 GPU page 打成顺序写；相感知写限流保护读带宽（约保 **90%** prefetch 读带宽）。
4. **评测**：DeepSeek-V4-Flash / V4-Pro、GLM-5.2；多轮 agent 轨迹。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| TTFT vs 既有工作 | 最高 **1.57–3.69×**；均值 **1.22–1.85×** |
| 关键路径 SSD I/O 占比 | append prefill **<6.5%** |
| 预测冗余读 | DeepSeek-V4 **<5%**；GLM-5.2 **<10%**（选定 d） |

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM→DRAM→**SSD** 层级在 agent 稀疏读下的关键路径
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 与 RR-Evict/Fancy 的前缀策略互补（本文偏 **介质+稀疏选择时机**）
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — agentic 长会话存储侧扩展

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.36938) — He et al., arXiv:2609.36938
[2] [raw stub](raw/papers/janus-agentic-ssd-sparse-kv.md)
