---
type: Paper
title: "HiNa-MoE: High-Performance, Non-Intrusive MoE Inference on CPUs with Matrix Engines"
description: "国防科大（PACT'26）— Intel AMX 上 MoE CPU 算子库：不改权重布局、页交错下 NUMA-aware 切分、decode MV→MM；FFN kernel 最高 3.37×、端到端 decode 最高 2.09×，可插拔到 IPEX/KTransformers"
tags:
- moe
- inference
- decode
- cpu
- kernel
- memory-bandwidth
- memory
- intel
- hardware
created: 2026-10-07
updated: 2026-10-07
timestamp: '2026-10-07T00:00:00Z'
paper_author: [Weiling Yang, Junwen Zhang, Dezun Dong, Jianbin Fang, Enda Yu, Zhe Bai, Xiaopeng Deng]
year: 2026
arxiv: '2610.05123'
venue: "PACT '26"
sources:
  - raw/papers/HiNa_MoE_CPU_AMX_MoE_Inference_2026.pdf
  - raw/papers/hina-moe-cpu-amx-moe-inference.md
---

# HiNa-MoE：多路 CPU + AMX 上的非侵入式 MoE 推理

## 一句话结论

本地/私有部署的 MoE 专家放不下 GPU 时，低并发下每个专家只处理少量 token，把权重搬上 GPU 不划算，**CPU 上的专家 FFN** 就在关键路径上。现有 AMX 加速（KTransformers、IPEX）靠预转换 AMX 专用权重布局和手工 NUMA 分片，和 GPU 库不兼容、侵入框架。HiNa-MoE 改为"**变换中间矩阵，不变换权重**"，在页交错策略下做 NUMA-aware 任务切分，decode 把 MV 变 MM 用上 AMX：FFN kernel 最高 **3.37×**，端到端最高 **2.09×**，替换少量算子即可接入。

## 动机

- Mixtral-8x7B 在 Xeon Gold 6430 vs A6000 上，CPU（AMX）FFN 在小/中批次下吞吐仍有竞争力，大批次才轮到 GPU（Fig. 1）。
- 两个约束：每专家 token 少导致小而不规则的 GEMM；专家权重在 CPU DRAM 中造成跨 socket 流量。

## 方案

1. **通用布局 AMX micro-kernel**：权重保持行/列主序，把轻量布局变换融合进 token gather 和结果 store。
2. **非侵入 NUMA 切分**：利用专家维度通常是 128 的倍数，在 `numactl --interleave=all` 页交错下按页周期切任务，避免远端权重访问，不改分配器。
3. **decode 注意力 MV→MM**：把访存密集的矩阵-向量运算转成小矩阵乘，喂给 AMX。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 平台 | 双路 Xeon Gold 6430（+RTX A6000）、四路 Xeon Gold 6448H、双路 Xeon Max 9462（HBM-only） |
| FFN kernel（6430/6448H，平均） | vs IPEX **1.73×**、vs KTransformers **1.68×**；最高 **3.37×** / **2.16×** |
| 带宽利用 | 6430 上达实测本地峰值带宽 **96%** |
| 端到端 decode（6430+A6000，batch 1，128/128 token） | 平均 vs vLLM-CPU **1.99×**、IPEX **1.70×**、KTransformers **1.22×**；最高 **2.87× / 2.09× / 1.25×** |
| Xeon Max 9462（HBM-only，FFN） | vs oneDNN **9.65×**、IPEX **3.41×**（平均）；本地/远端带宽比 ~5×（425 vs 89 GB/s），6430 约 2.3× |

## 与 wiki 的关系

- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — CPU–GPU MoE 卸载里 CPU 侧执行引擎；与 [RapidMoE](/papers/rapidmoe-residual-offloading-moe-inference.md) 的比特级卸载互补（一个改切分，一个改 CPU 算子）
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — decode MV→MM 是同一问题在矩阵引擎上的解法
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 多路 NUMA 本地/远端带宽比决定收益；HBM 版 Xeon 上远端惩罚更大

## 局限与开放问题

- 只覆盖 Intel AMX；ARM SME / AMD 矩阵扩展未验证。端到端主要是 batch 1 低并发。
- 硬件启示：CPU 矩阵引擎的 tile 布局约束是 MoE 卸载的兼容性痛点；若硬件支持更灵活的 tile 装载（或带 gather），软件可省掉布局融合。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.05123) — Yang et al., arXiv:2610.05123（PACT '26）
[2] [raw stub](raw/papers/hina-moe-cpu-amx-moe-inference.md)
