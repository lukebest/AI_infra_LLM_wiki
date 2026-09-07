---
type: Paper
title: "CREDIT: Cost-guided Reduction-reuse with Efficient DSMEM Inter-CTA Tiling"
description: UW–Madison — Hopper/Blackwell DSMEM 何时划算；reduction-reuse 变换 + 成本模型 91.7%；5090/H100 几何均值 1.466×/1.318×
tags:
- gpu
- nvidia
- architecture
- memory
- kernel
- optimization
- communication
- interconnect
- noc
- throughput
timestamp: '2026-09-07T00:00:00Z'
created: 2026-09-07
updated: 2026-09-07
sources:
- raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf
- raw/papers/credit-dsmem-inter-cta-tiling.md
---

# CREDIT: Cost-guided Reduction-reuse with Efficient DSMEM Inter-CTA Tiling

**Authors:** Zhengxiong Li, Tsung-Wei Huang, Umit Ogras
**Affiliation:** University of Wisconsin–Madison
**arXiv:** [2609.01864](https://arxiv.org/abs/2609.01864)（2026-09-02，cs.DC）
**Venue:** 预印本
**PDF:** [raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf](raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf)

Hopper 起 CUDA **thread block cluster** 允许 CTA 经 **DSMEM** 直接访问 peer SMEM。CREDIT 不把 DSMEM 当通用融合织物，而是筛 **reduction-reuse** 模式：宽行归约出紧凑统计量后再逐元素复用，用 cluster 内交换标量 partial **换掉第二次 HBM 重读**。对照 [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) 的内存层次：这是 **GPC 内 inter-SM** 一层，不是 NVLink scale-up。

## 动机

- Roofline ridge：V100 ~139 → H100 ~295 FLOPs/byte，算力相对带宽继续拉开。
- DSMEM 不免费：远程 load 延迟约 **6.4×** 本地，吞吐约 **4.4–5.4×** 更低；cluster barrier 在 H100 上 **851 cycle** vs 5090 **404 cycle**。
- 需要：**哪些算子/形状该开 DSMEM**，而不是一律 cluster 化。

## 方案

1. **微基准刻画** local/remote load-store 与 sync（双 CTA 强制不同 SM）。
2. **Reduction-reuse 变换：** 行切成 P 片，owner 留在本地 SMEM；每 stage 压成 \(q_\ell\) 个标量 partial，replicated push 到 peer slot 后本地归约（远程读字节=0）。
3. **成本模型：** 用匹配非 DSMEM CUDA 的 \(T_B\) 估节省的重读时间，再减 control/replay/DSMEM store；预测盈利对 **55/60**（**91.7%**）。
4. **工作负载：** LayerNorm、weighted-variance / Pearson / softmax-logits backward、LARS、row-wise int8 quant；相对 torch.compile / Triton / 优化非 DSMEM CUDA。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 几何均值 vs 最快 baseline（N=64K） | RTX 5090 **1.466×**；H100 **1.318×** |
| N=4K | 几何均值 **0.738× / 0.815×**（常输给单 CTA） |
| DRAM 流量（5090，N=64K） | 降 **33–60%** |
| 盈利对准确率 | **91.7%**（55/60） |

**实测** RTX 5090 + H100 SXM；CUDA 13 / PyTorch 2.11 / Triton 3.6。源码公开。

## 与 wiki 的关系

- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — SMEM/GPC 之上的 DSMEM 合作域
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 用 on-chip 协作压 HBM 重读
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 机柜级互联对照；本文是片内 inter-SM
- [FlashAttention IO-aware](/papers/flashattention-io-aware-exact-attention.md) — 同属「避免物化/重读」谱系，但 FlashAttn 不依赖 DSMEM
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 集体 barrier 税；本文是 cluster barrier 进成本模型

## 开放问题

1. 更复杂图级融合（FlashFuse/ClusterFusion）如何与 CREDIT 的形状筛共用？
2. Blackwell 数据中心 GPU（非 5090）上 barrier/远程 store 曲线是否同形？

# Citations

[1] [raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf](raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf) — Li, Huang, Ogras, arXiv:2609.01864
[2] [raw/papers/credit-dsmem-inter-cta-tiling.md](raw/papers/credit-dsmem-inter-cta-tiling.md) — ingest stub
