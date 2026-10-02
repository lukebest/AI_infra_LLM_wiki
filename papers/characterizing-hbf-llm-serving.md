---
type: Paper
title: "Characterizing High Bandwidth Flash for LLM Serving"
description: "Berkeley/Furiosa — HBM–HBF–host 分层 + buffered 调度；完成时间相对 HBM-only 最高 −36.1–87.0%；能效最高 −55.8%；寿命 4.77→14.82 年"
tags:
- architecture
- llm
- inference
- serving
- serving-system
- kv-cache
- hbf
- hbm
- memory
- memory-bandwidth
- agentic-ai
- throughput
- gpu
created: 2026-10-02
updated: 2026-10-02
timestamp: '2026-10-02T00:00:00Z'
paper_author: [Zack Yu, Chloe Wong, Coleman Hooper, Minjae Lee, Wonjun Kang, Youngjin Cho, Michael W. Mahoney, Yakun Sophia Shao, Kurt Keutzer, Amir Gholami]
year: 2026
arxiv: '2609.39131'
sources:
  - raw/papers/Characterizing_HBF_LLM_Serving_2026.pdf
  - raw/papers/characterizing-hbf-llm-serving.md
---

# Characterizing HBF for LLM Serving：容量必须配调度

## 一句话结论

面向 **高吞吐 agentic serving**，用 **HBM–HBF–host** 分层存放 + **buffered cache-aware** 准入；最快 HBF 配置相对 HBM-only 完成时间 **−36.1–87.0%**，建模能耗最高 **−55.8%**；预留 **10%** 准入余量把估计写寿命从 **4.77→14.82 年**（HBF KV 写 **−69%**）。

## 动机

- 权重 + 活跃 KV + 可复用前缀争同一块加速器内存；agentic 多轮共享上下文使「保容量」与「加大 batch」同等重要。
- HBF 扩容近端存储，但读能耗更高、写更慢、有有限 P/E；简单加容量不等于好用。
- 对照 Sandisk **shared-site**（HBM/HBF 争站点）与 **H3**（HBM 占满站点、HBF 串在后）。

对照 [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md)、[HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md)、[SPLASH HBF](/papers/splash-sparse-attention-hbf.md)、[HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md)、[Janus](/papers/janus-agentic-ssd-sparse-kv.md)、[End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)。

## 方案

1. **分层存放**：新 KV / 重载前缀进 HBM；冷缓存下沉 HBF → host DRAM → SSD；权重可驻 HBM 或下沉。
2. **Buffered cache-aware 调度**：准入缓冲为 decode 增长留余量，减少可复用前缀被挤出与写放大。
3. **评测设定**：高吞吐（合成数据、异步 agent、RL rollout）；LLMServingSim 类轨迹驱动；模型含 Llama-3.1-405B / GLM-5.2 / Qwen3-32B 等。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 最快 HBF 配置 vs HBM-only 完成时间 | **−36.1–87.0%**（摘要跨负载） |
| 建模能耗节省（摘要峰值） | 最高 **55.8%**（轻负载上 HBF 可能更费能） |
| HBM 权重配置 vs HBM-only（1× 轨迹，405B/GLM-5.2） | 完成时间 **−46–56%**；能耗 **−14–24%** |
| GLM-5.2 5× 轨迹（HBM 权重） | 完成 **6.7×** 加速；能耗 **−56%** |
| 10% 准入余量 | HBF KV 写 **−69%**；寿命 **4.77→14.82 年**；完成时间再 **−4.7%**（相对无缓冲 cache-aware） |

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) / [Memory Hierarchy](/concepts/memory-hierarchy-cache.md) — HBF 作近端扩容时的放置×调度共设计
- [Hot–Cold](/papers/hotcold-hbm-hbf-agentic-llm.md) / [HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md) / [SPLASH](/papers/splash-sparse-attention-hbf.md) — 同介质族；本文强调 **写寿命与准入缓冲** 的量化
- [HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md) — 仿真器底座；本文是 serving 策略表征
- [Janus](/papers/janus-agentic-ssd-sparse-kv.md) — SSD 中心稀疏 KV；本文主攻 **近端 HBF 层级**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.39131) — Yu et al., arXiv:2609.39131
[2] [raw stub](raw/papers/characterizing-hbf-llm-serving.md)
