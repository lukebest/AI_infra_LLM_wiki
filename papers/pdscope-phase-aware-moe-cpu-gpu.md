---
type: Paper
title: "PDScope: Phase-Aware MoE Inference on CPU–GPU"
description: "国防科大 — 相位感知专家预测/预取/放置 + 静态图零拷贝异步 I/O；相对现有系统 prefill 吞吐 2.5–10.3×、decode 2.1–6.1×"
tags:
- inference
- moe
- prefill
- decode
- memory
- cpu
- gpu
- throughput
- llm
- serving-system
- expert-parallelism
- scheduling
created: 2026-11-03
updated: 2026-11-03
timestamp: '2026-11-03T00:00:00Z'
paper_author: [Enda Yu, Dezun Dong, Zhaoning Zhang, Xiaojian Yang, Weiling Yang, Shaonan Ma, Dongsheng Li, Yongwei Wu, Xiangke Liao]
year: 2026
venue: arXiv
arxiv: '2610.39216'
sources:
  - raw/papers/PDScope_Phase_Aware_MoE_CPU_GPU_2026.pdf
  - raw/papers/pdscope-phase-aware-moe-cpu-gpu.md
---

# PDScope：打破内存受限 MoE 的 Prefill–Decode 跷跷板

## 一句话结论
本地 CPU–GPU 部署 MoE 时，多数专家落在 CPU：prefill 偏算力、想激进装 GPU；decode 偏 PCIe，要保守传。相位无关调度陷入跷跷板。PDScope 用**相位感知专家预测/预取/放置**（PhasePer + AdaptSched）+ **静态计算图 / cache 预取 / 零拷贝异步 I/O**，在主流 MoE 上相对现有系统 prefill 吞吐 **2.5–10.3×**、decode **2.1–6.1×**。

## 动机
- 低 batch（本地助手/文档工具）无法用请求间并行掩盖相位冲突。
- 静态驻留（如 kTransformers）稳住 decode I/O 却饿 prefill GPU；按需加载（如 Fate）抬 prefill 却在 decode 打出 PCIe 气泡；动态层调度仍偏「看当前层」而非前瞻。

## 方案
1. **PhasePer**：把专家激活预测做成相位相关排序；利用层组效应，DeepSeek-V2-Lite / Qwen3-30B-A3B 上 Top-6 约 **94%**。
2. **AdaptSched**：跨层代价建模，联合当前层放置与下层预取；prefill 偏激进、decode 偏保守。
3. **开销无关执行引擎**：静态计算图 + cache 预取 + 零拷贝异步 I/O，避免运行时调度开销吃掉相位感知收益。
4. **评测**：相对 Fate / KTransformers / Fiddler / HybriMoE / MoE-APEX 等；A100 + Intel 6230R 平台。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Prefill 吞吐 vs 现有系统 | **2.5–10.3×** |
| Decode 吞吐 vs 现有系统 | **2.1–6.1×** |
| PhasePer Top-6（DS-V2-Lite / Qwen3-30B-A3B） | 约 **94%** |

## 与 wiki 的关系
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 把 PD 分歧推到 MoE 专家卸载的 PCIe/算力跷跷板
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — CPU–GPU 异构执行与相位策略共设计
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 专家权重在 CPU↔GPU 之间的预取与零拷贝路径
- [DualPace](/papers/dualpace-decoupled-gpu-cpu-decoding.md) — 同属 CPU–GPU 分工；DualPace 侧重 decode 引擎解耦，PDScope 侧重 MoE 专家相位调度

## 开放问题
- 低 batch 最坏情形优化后向多 batch 外推有讨论，跨更大 MoE（如 DeepSeek-V3 级）与多卡 EP 叠加未系统展开。
- 预测误差在路由突变负载下的尾部行为需更多刻画。

# Citations
- [arXiv:2610.39216](https://arxiv.org/abs/2610.39216) — Yu et al., NUDT / Qiyuan Lab, 2026
- [raw stub](/raw/papers/pdscope-phase-aware-moe-cpu-gpu.md)
