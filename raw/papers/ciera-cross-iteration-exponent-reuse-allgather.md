---
type: Raw Source
title: CIERA — Cross-Iteration Exponent Reuse for Lossless Allgather in Sharded MoE Training
source_url: https://arxiv.org/abs/2609.04609
arxiv: '2609.04609'
ingested: 2026-09-08
sha256: 394f9a15677339447abb4878cfa2b729eea191099fb57c3051e2406cddbfa718
---

# CIERA: Cross-Iteration Exponent Reuse for Lossless Allgather in Sharded MoE Training

**Authors:** Ali Zafar Sadiq, Haiying Shen, Masahiro Tanaka
**Affiliations:** University of Virginia; Anyscale
**PDF:** [CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf](CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf)
**arXiv:** [2609.04609](https://arxiv.org/abs/2609.04609)（2026-09-04，cs.DC）

## 问题

Sharded data parallelism（如 ZeRO-3）把每个 expert 权重切到多 GPU，每层前需要 Allgather 拼回完整矩阵；文中观测 Allgather 可占通信时间 **51.8–69.0%**，关键路径可达 iteration 的 **25–30%**。已有有损压缩牺牲数值保真；已有无损方法未利用跨 iteration 指数稳定性。

## 方法要点

- 观测：warmup 约 30 iter 后，至少 **99%** 权重指数跨 iteration 不变（BF16/FP16）。
- 本地缓存指数；未变时只传 sign+mantissa，接收端与缓存指数拼回，**bitwise-exact**。
- 按层形状做收益门控：只在压缩净省时间时启用；压缩与 Allgather/计算重叠。
- 叠在 ZeRO-3 上；指数检查间隔可调（每 iter 25–30% 开销 vs 每 10 iter 3–4%）。

## 摘录数字（仅论文给出）

- 平台：A100 NVLink 3.0 + NVSwitch（600 GB/s bi-dir/GPU）；多节点 8×A100-80GB + 200 Gbps IB（~8 GB/s）；CUDA 12.4 / PyTorch 2.7。
- OLMoE-1B-7B @16 GPU：**3.70×** vs ZeRO-3（无损）、**3.68×** vs ZeRO++（有损）；⋆ 实测。
- 投影 128 GPU：相对 ZeRO-3 **4.28×**、相对 ZeRO++ **4.42×**。
- 其它模型（表 1，⋆=实测）：MiniCPM-8×2B @16 **2.12×**；通信受限模型族相对 ZeRO-3 **1.16–2.89×**；相对 FSDP 最高 **3.38×**（OLMoE）。
- 模拟器对全模型 iteration 时间匹配实测误差 **≤4%**（OLMoE/MiniCPM @8/16 GPU）。
