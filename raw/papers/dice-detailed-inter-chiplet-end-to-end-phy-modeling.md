---
type: Raw Source
title: DICE Detailed Inter-Chiplet End-to-End PHY Modeling
source_url: https://arxiv.org/abs/2607.24221
arxiv: '2607.24221'
ingested: 2026-08-20
sha256: 51b4500eacf8b0183f528ebd0ce3b18a1510472c892548f51944459883862992
---

# DICE: Detailed Inter-Chiplet End-to-End PHY Modeling for Accurate Chiplet Simulation

**Authors:** Rashid Aligholipour, Stefanos Kaxiras, Yuan Yao（Uppsala）
**PDF:** [DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf](DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf)
**arXiv:** [2607.24221](https://arxiv.org/abs/2607.24221)
**Venue:** PDF 页眉写 ISCA 2026 Submission Confidential Draft；artifact 仓自称 ISCA 2026。未独立核实会议程序册。
**Code:** https://github.com/RashidAGP/DICE-Simulator

## 问题

Chiplet 短距链路逼近信号完整性极限，需要 FEC；gem5 HeteroGarnet 等仍用固定延迟/带宽节流近似 PHY。固定延迟抹掉 FEC 迭代、重传与信道噪声带来的长尾，IPC 相对真实硅可偏乐观或悲观。

## 方法要点

- gem5 运行时 PHY：QC-LDPC 编解码、PAM4、AWGN+jitter+crosstalk、LLR 解调、自适应重传、PHY 流控。
- 默认 R≈0.88（128-bit flit + 2-byte parity）、32 GT/s、SNR_base 35 dB。
- CCD 2.0 GHz 2×4 mesh / IOD 1.0 GHz 2×2；解码迭代预算 N=4，时延 2N+1 cycle。
- 对照 HeteroGarnet 与 AMD EPYC 9454P / ThreadRipper 3960X / EPYC 7R13 的 C2C 延迟。

## 摘录数字（仅论文给出）

- IPC 相对 HeteroGarnet 平均偏移 **6.8%**、最高 **27.6%**（方向因负载而异，非单向加速）。
- 9454P 跨 die 最大 C2C RMSE：HG **141.2** cycle（304.6 的 46.4%），DICE **89.5**（29.4%）；尾部保真相对 HG 高 **17.0%**。
- 平均 C2C RMSE：3960X 36.6→17.1（19.1%→8.9%）；7R13 39.9→24.9（18.9%→11.8%）；9454P 100.4→73.9（40.5%→29.8%）；相对 RMSE 降 **7.1%–10.7%**。
- FEC 纠正 **97.8%** 错误，**2.2%** 走重传。
- gem5 开销 0.3–26.1%，平均 **9.2%**。
- 多线程 XSBench 相对 monolithic：DICE **9.53×**，HG **1.74×**。
