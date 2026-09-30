---
type: Paper
title: "RR-Evict: Round-Robin Prefix Cache Eviction for Agentic Serving"
description: "UCSD — SGLang@H100；vs LRU P99 TTFT 最高 −75.4%、P99 未缓存 prompt token 最高 −65.7%；vs completion-aware LRU 最高 −46.9%/−30.6%"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- kv-cache
- agentic-ai
- ai-agent
- cache
- memory
- scheduling
- disaggregated-inference
- throughput
- latency
- gpu
created: 2026-09-30
updated: 2026-09-30
timestamp: '2026-09-30T00:00:00Z'
paper_author: [Zaifeng Pan, Chris Wu, Zhengding Hu, Xinwei Qiang, Zhongkai Yu, Yufei Ding]
year: 2026
arxiv: '2609.32278'
sources:
  - raw/papers/RREvict_Prefix_Cache_Eviction_Agentic_2026.pdf
  - raw/papers/rrevict-prefix-cache-eviction-agentic.md
---

# RR-Evict: Agentic 前缀缓存的细粒度轮转淘汰

## 一句话结论

Agent 多轮会 **同步刷新** 整条私有历史的 recency，使节点级 LRU 退化为「整智能体清空」；**RR-Evict** 对空闲轨迹 round-robin 淘汰尾块，保留更多可复用前缀。相对 LRU，P99 TTFT 最高 **−75.4%**，P99 未缓存 prompt token 最高 **−65.7%**（SGLang @ H100）。

## 动机

- 长程 agent：工具/用户等待期间保留 prefix KV；并发升高后必须淘汰。
- **Recency synchronization**：一次前缀匹配刷新整条路径节点，LRU 连续抽中最老空闲 agent 的几乎全部历史 → 回归时冷预填，**尾部 TTFT** 爆。
- [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) 显示生产轨迹上花哨策略难超 LRU；本文指出 **agentic 访问节拍** 让 LRU 自身失效，需要换分布目标而非更复杂预测。

对照 [Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md)、[Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md)、[Disaggregated Inference](/concepts/disaggregated-inference.md)。

## 方案

1. 按 agent 轨迹分组；容量不足时 **轮转访问** 各空闲轨迹，每次淘汰一个 **尾块**（保连续有效前缀）。
2. 无需预测到达或工具时延；可与 completion 生命周期信号分层（文中主结果不依赖预测）。
3. **评测**：SGLang；H100 NVLink。对话：Qwen3-Coder-30B-A3B @ τ²-bench（共置）。编码：Qwen3-8B @ SWE-bench，**1P3D** PD 解耦。基线 LRU 与 completion-aware LRU。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| vs LRU（τ²-bench，摘要/正文） | P99 TTFT 最高 **−75.4%**；P99 uncached prompt tokens 最高 **−65.7%** |
| vs LRU + Completion Signals | P99 TTFT 最高 **−46.9%**；P99 uncached 最高 **−30.6%** |
| 场景 | 共置对话 + PD 解耦编码（Fig.6 等，相对 LRU 归一化） |

## 与 wiki 的关系

- [Fancy Eviction](/papers/fancy-eviction-llm-prefix-cache.md) — 「难超 LRU」的生产结论；本文给 **agentic 反例与轮转分布**
- [Ask the Tool](/papers/ask-tool-progress-agent-kv-serving.md) — 工具等待期 keep/evict 信号；本文是 **无预测的分布式淘汰**
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 1P3D 下同样生效

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.32278) — Pan et al., arXiv:2609.32278
[2] [raw stub](raw/papers/rrevict-prefix-cache-eviction-agentic.md)
