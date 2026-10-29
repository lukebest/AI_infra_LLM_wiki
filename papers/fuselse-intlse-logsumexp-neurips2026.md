---
type: Paper
title: "FuseLSE / IntLSE: Speeding up Log-Sum-Exp at Memory and Compute Walls"
description: "NeurIPS'26 — 单遍融合 FuseLSE（GPU SFU）与整数近似 IntLSE（CPU）；GPU 上相对 torch.logsumexp 小负载 ~10–11×、大负载 ~6×，HBM 流量约 6×→1×；CPU 上 IntLSE 比 FuseLSE 再快 3–6×"
tags:
- nonlinear
- kernel
- gpu
- cpu
- memory-bandwidth
- inference
- llm
- optimization
- activation
- numeric-format
created: 2026-10-29
updated: 2026-10-29
timestamp: '2026-10-29T00:00:00Z'
paper_author: [Lingyun Yao, Martin Andraud, Niki Loppi, Andrea Pilzer, Anji Liu, Guy Van den Broeck, Martin Trapp]
year: 2026
venue: NeurIPS 2026
arxiv: '2610.33647'
sources:
  - raw/papers/FuseLSE_IntLSE_LogSumExp_NeurIPS2026.pdf
  - raw/papers/fuselse-intlse-logsumexp-neurips2026.md
---

# FuseLSE / IntLSE：在内存墙与算力墙加速 Log-Sum-Exp

## 一句话结论
`torch.logsumexp` 默认拆成约九个子 kernel，同规模归约可比 `torch.sum` 慢约 **6×**（例 **1.95 ms vs 0.31 ms**），并带来约 **6×** 输入体积的 HBM 往返。FuseLSE 用结合律 pairwise LSE 做成单遍融合 kernel（SFU `__expf`/`__logf`），把流量压到约 **1×**；IntLSE 在同骨架上把 pair 函数换成 Mitchell 风格整数近似。GPU 上两者相对 PyTorch 小负载约 **10–11×**、大负载约 **6×**；无 SFU 的 CPU 上 IntLSE 再比 FuseLSE 快 **3–6×**（粒子滤波应用相对 torch **2.8–5.2×**）。

## 动机
- LSE 是稳定 log 域计算的基础原语：LLM RL 每 token 的 vocab 维 log-prob、softmax、粒子滤波等都反复调用。
- GPU 上瓶颈是 **launch + HBM 冗余读写**（amax / sub / exp / sum 链），不是算术细节。
- CPU / 微控 / FPGA 等无快速 SFU 平台上，exp/log 本身变成算力墙，需要整数友好近似。

## 方案
1. **FuseLSE**：按 pairwise `LSE(x,y)=max + log(1+exp(−|x−y|))` 流式归约；每行一个 block，向量化加载；HBM 约读一遍输入、写标量结果。
2. **IntLSE**：保留同一归约骨架，把 `log2(1+2^z)` 换成移位/加法（可选 LUT）的 Mitchell 近似。
3. **对照维度**：跨 workload 尺寸、多 GPU HBM 带宽、多种输入分布；另有降精度 FuseLSE16 / IntLSE-Q10.6（未并入应用基准）。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| GPU vs torch.logsumexp | 小负载 **~10–11×**，大负载 **~6×** |
| 例：与 torch.sum 对齐 | FuseLSE **312 µs** / IntLSE **315 µs** vs sum **311 µs**（原 logsumexp **1.95 ms**） |
| HBM 流量 | 约 **6× → 1×** 输入体积 |
| CPU IntLSE vs FuseLSE | **~3–6×** |
| 粒子滤波 vs torch | IntLSE **2.8–5.2×** |
| 全文结论区间 | 微基准 + 三应用合计约 **6–12×** |

## 与 wiki 的关系
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 把「融合降 HBM」与「无 SFU 时整数近似」两条路线补进 LSE/softmax 族
- [FlashAttention](/concepts/flashattention.md) / [FlashAttention-3](/concepts/flashattention-3.md) — online softmax 已在 attention 内融合 LSE；本文针对独立 `logsumexp` 原语与 vocab 维 RL 路径
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 降精度变体与误差–带宽权衡
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — SFU 吞吐决定 FuseLSE 在 GPU 上几乎不被算术卡住

## 开放问题
- IntLSE 累积误差对精度极敏感训练/推理路径的可接受区间未系统标定。
- 与 FlashAttention / CCE 等「LSE 已融进更大算子」路径如何共享实现未讨论。
- 降精度变体尚未进入应用基准，端到端收益未知。

# Citations
- [arXiv:2610.33647](https://arxiv.org/abs/2610.33647) — Yao et al., NeurIPS 2026
- [raw stub](/raw/papers/fuselse-intlse-logsumexp-neurips2026.md)
