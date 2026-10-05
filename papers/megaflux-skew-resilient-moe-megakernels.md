---
type: Paper
title: "MegaFlux: Skew-Resilient MoE Megakernels via Pipelined Expert Replication"
description: "Princeton+NVIDIA — MoE megakernel 内运行时热专家复制并流水化权重/梯度传输；8×B200 前向/反向几何均值 1.45×/1.28×（峰值 2.14×/2.64×）；vLLM DeepSeek-V4-Pro prefill 中位 1.13–1.26×"
tags:
- architecture
- llm
- moe
- training
- inference
- expert-parallelism
- kernel
- gpu
- nvidia
- communication
- scheduling
- throughput
created: 2026-10-05
updated: 2026-10-05
timestamp: '2026-10-05T00:00:00Z'
paper_author: [Jianzhu Yao, Siva Kumar Sastry Hari, Vignesh Balaji, Sana Damani, Insu Jang, Pramod Viswanath, Christos Kozyrakis]
year: 2026
arxiv: '2610.00671'
sources:
  - raw/papers/MegaFlux_Skew_Resilient_MoE_Megakernels_2026.pdf
  - raw/papers/megaflux-skew-resilient-moe-megakernels.md
---

# MegaFlux：在 megakernel 里做运行时热专家复制

## 一句话结论

MoE megakernel 把 EP 通信与专家计算融合后，**路由倾斜**仍让过载 GPU 决定层延迟。MegaFlux 把"复制热专家"变成 **运行时决策**，并把复制带来的 **权重下发（前向）与副本梯度归约（反向）** 流水进持久 kernel；8×B200 上相对同一 megakernel 固定放置，前向/反向几何均值 **1.45× / 1.28×**（峰值 **2.14× / 2.64×**）。

## 动机

- 固定专家放置下，skew → straggler GPU；其余 GPU 空等。
- 复制热专家能分流，但副本需先收到权重；训练时副本的部分梯度还要归约回 owner——额外通信若串行执行会吃掉收益。
- 现有 megakernel（[MegaMoE](/concepts/megamoe-kernel.md)、[Mixture-of-Kittens](/papers/mixture-of-kittens-moe-megakernel-nvl72.md)）假设放置固定。

## 方案

1. **设备端 planner**：在每 GPU 副本预算下联合选副本位置、按 tile 对齐分配 token block；**不改 router 输出**。
2. **前向流水复制**：副本在所需权重到达后即开算。
3. **反向 megakernel（新增）**：副本梯度归约与持续专家计算重叠。
4. 基于 TensorRT-LLM 的 CuTeDSL MegaMoE 前向 kernel 扩展；集成 vLLM。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 前向 / 反向 vs 固定放置（147 配置/方向，8×B200，几何均值） | **1.45× / 1.28×** |
| 峰值 | **2.14× / 2.64×** |
| 流水隐藏副本权重传输（前向） | **56–76%** |
| 流水隐藏权重传输+副本梯度归约（反向） | **91–100%** |
| 相对同一复制计划但串行执行的额外层延迟下降 | 最高 **13.2%**（前向）/ **26.7%**（反向） |
| vLLM DeepSeek-V4-Pro prefill e2e | 中位 **1.13–1.26×** |

## 与 wiki 的关系

- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — 直接基座；MegaFlux 补上 **负载倾斜** 这一维
- [Mixture-of-Kittens](/papers/mixture-of-kittens-moe-megakernel-nvl72.md) — 同为 MoE megakernel；MoK 偏 NVL72 训练融合，MegaFlux 偏动态复制
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) / [Weave](/papers/weave-dynamic-sm-moe-overlap.md) — EP 通信计算重叠的其它路线
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP All-to-All 与梯度归约

## 开放问题

- 单 NVLink 域 8 卡；跨节点（RDMA）下副本权重下发代价与预算如何变化？
- 副本预算占用 HBM，与 KV/激活争容量的取舍。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.00671) — Yao et al., arXiv:2610.00671
[2] [raw stub](raw/papers/megaflux-skew-resilient-moe-megakernels.md)
