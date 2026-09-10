---
type: Paper
title: "CIERA: Cross-Iteration Exponent Reuse for Lossless Allgather in Sharded MoE Training"
description: UVA/Anyscale — 跨 iter 复用 BF16/FP16 指数做无损 MoE Allgather；OLMoE@16GPU vs ZeRO-3 3.70×、vs ZeRO++ 3.68×（实测）
tags:
- llm
- training
- moe
- collective
- communication
- parallelism
- gpu
- nvidia
- training-system
- quantization
timestamp: '2026-09-08T00:00:00Z'
created: 2026-09-08
updated: 2026-09-08
sources:
- raw/papers/CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf
- raw/papers/ciera-cross-iteration-exponent-reuse-allgather.md
---

# CIERA: Cross-Iteration Exponent Reuse for Lossless Allgather in Sharded MoE Training

**Authors:** Ali Zafar Sadiq, Haiying Shen, Masahiro Tanaka
**Affiliation:** University of Virginia; Anyscale
**arXiv:** [2609.04609](https://arxiv.org/abs/2609.04609)（2026-09-04，cs.DC）
**Venue:** 预印本
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.04609)

ZeRO-3 类分片把 expert 权重切开后，每层前的 **Allgather** 可占通信 **51.8–69.0%**。CIERA 抓住「warmup 后 ≥99% 指数跨 iter 不变」：缓存指数、只传 sign+mantissa，接收端拼回 **bitwise-exact** 权重。对照 wiki [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)：这是 **AllGather 载荷压缩**（无损、系统感知门控），不是新集体拓扑。

## 动机

- 有损 int8 Allgather（如 ZeRO++）换带宽牺牲数值保真。
- 已有无损压缩未用跨 iteration 指数稳定性。
- 指数检查本身可吃 **25–30%** 关键路径——必须与通信/计算重叠并稀疏检查。

## 方案

1. **指数缓存 + 条件传输**：未变指数只发 sign/mantissa；变了再发全量含指数。
2. **收益门控**：按层矩阵形状决定是否压缩（净省墙钟才开）。
3. **重叠调度**：压缩与 NCCL Allgather、计算流水重叠；检查间隔可调（每 10 iter → 开销约 3–4%）。
4. **叠 ZeRO-3**；BF16/FP16 MoE。

## 效果（仅论文数字）

**平台：** A100 + NVLink/NVSwitch；16 GPU 跨两节点时外加 200 Gbps IB。

| 设定 | 相对基线 |
|------|----------|
| OLMoE-1B-7B @16 GPU vs ZeRO-3 | **3.70×**⋆ |
| 同设定 vs ZeRO++ | **3.68×**⋆ |
| 投影 @128 GPU vs ZeRO-3 / ZeRO++ | **4.28× / 4.42×** |
| MiniCPM-8×2B @16 vs ZeRO-3 | **2.12×**⋆ |
| 通信受限模型族 vs ZeRO-3（含更小规模） | **1.16–2.89×** |
| OLMoE vs FSDP | 最高 **3.38×** |

⋆=实测；大世界规模多为 trace 驱动模拟（全模型匹配误差 ≤4%）。**Bitwise-exact** 重建在评估 run 中成立。

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — MoE/ZeRO AllGather 载荷侧
- [BASP](/papers/basp-batch-aware-sequence-parallelism.md) — 对照：拓扑子组 vs 载荷压缩
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 集体墙钟另一轴（barrier τ）
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — MoE 训练通信另一路线（放置压 A2A）
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 实验域仍是 NVLink 内 + IB 跨节点

## 开放问题

1. 更高 LR / 更大 batch 时指数稳定窗口是否塌缩（文中 B↑ 复用率下降）？
2. 与梯度压缩、ZeRO++ 有损路径如何混合而仍可证明数值界？
3. 跨更多 IB hop 时，压缩 CPU/GPU 开销是否重新上关键路径？

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.04609) — Sadiq et al., arXiv:2609.04609
[2] [raw/papers/ciera-cross-iteration-exponent-reuse-allgather.md](raw/papers/ciera-cross-iteration-exponent-reuse-allgather.md) — ingest stub
