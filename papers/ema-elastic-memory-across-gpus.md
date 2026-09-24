---
type: Paper
title: "EMA: Elastic Transparent Memory Across GPUs"
description: "伯克利 — 机内 GPU 互借 HBM；吞吐最高 +52%，达 2× 容量静态配置的 96%；预取透明 + 可回收"
tags:
- architecture
- gpu
- hbm
- memory
- llm
- inference
- serving
- kv-cache
- interconnect
- throughput
- latency
created: 2026-09-24
updated: 2026-09-24
timestamp: '2026-09-24T00:00:00Z'
paper_author: [Yi Xu, Tian Xia, Ion Stoica]
year: 2026
arxiv: '2609.27040'
sources:
  - raw/papers/EMA_Elastic_Memory_Across_GPUs_2026.pdf
  - raw/papers/ema-elastic-memory-across-gpus.md
---

# EMA: Elastic and Performance Transparent Memory Across GPUs

## 一句话结论

同机 GPU 通过 **Elastic Address Space** 互借/回收 HBM：借方预取使远端接近本地；贷方可即时收回。相对静态分区吞吐最高 **+52%**，并达到 **2×** 物理容量静态供给吞吐的 **96%**，延迟接近本地基线。

## 动机

- LLM 推理 KV/权重使单卡 HBM 突发打满，邻卡却可能空闲；云实例绑定后容量搁浅。
- 需要同时满足：**借方透明**（远端≈本地）与 **贷方安全**（回收后不低于静态分区）。

## 方案

1. **EAS**：把可借容量并入统一地址抽象；容量不保证永久，但访问路径统一。
2. **预取**：按 layer-group / slab 提前拉远端数据，掩盖 NVLink 延迟。
3. **回收**：贷方按需 reclaim，借方释放对应份额。
4. **评测**：A100 等多卡；LLaMA/OPT；NVLink 双向最高约 **600 GB/s**（文中 A100 设定）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 吞吐 vs 静态分区 | 最高 **+52%** |
| vs 2× 容量静态供给 | 达到其吞吐的 **96%** |
| 延迟 | 与静态本地基线相近（摘要） |
| 地址空间 | EAS 可将可用空间扩至约 **2×** 本地 HBM |

## 与 wiki 的关系

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 机内远端 HBM 作为近层扩展
- [GPU SIMT](/concepts/gpu-simt-architecture.md) — 多 GPU 内存池化
- [BOOST](/papers/boost-concurrent-host-hbm-llm-inference.md) — host↔HBM 并发；本文是 **peer-HBM**
- [Composable CXL](/papers/composable-cxl-memory-k8s-llm-serving.md) — 跨节点 CXL；本文是 **节点内 NVLink**

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.27040) — Xu, Xia, Stoica, arXiv:2609.27040
[2] [raw stub](raw/papers/ema-elastic-memory-across-gpus.md)
