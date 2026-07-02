---
type: Concept
title: MegaMoE Kernel (Expert Parallelism Overlap)
description: MoE 专家并行 mega-kernel，wave-based 通信计算全重叠
tags:
- communication
- kernel
- parallelism
- moe
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
---

# MegaMoE Kernel: Fine-Grained EP Communication-Computation Overlap

DeepSeek-V4 的 MoE 专家并行方案，将通信完全隐藏在计算之下。开源为 MegaMoE（DeepGEMM 的一部分）。

## Core Insight

MoE 层的通信时间 < 计算时间 → 融合成 pipeline 后，通信可被计算完全掩盖。

## Wave-Based Scheduling

将专家分成多个 wave（每个 wave 包含少量专家）：
- 当前 wave 的计算
- 下一 wave 的 token 传输
- 已完成 wave 的结果发送

**三者在稳态并行执行**，形成 fine-grained pipeline。

对比：
- **Naive**: 无重叠，串行
- **Comet**: Dispatch||Linear-1, Linear-2||Combine（部分重叠），理论加速 1.42×
- **MegaMoE**: Wave-level 全重叠，理论加速 **1.92×**
- **[FlashMoE](/concepts/flashmoe-kernel.md)**: 单 persistent kernel + 设备端 RDMA（NeurIPS 2025 研究栈；与 MegaMoE 正交）

## 性能

- 通用推理：**1.50 ~ 1.73×** 加速
- RL Rollout / 低延迟场景：最高 **1.96×**

## 对硬件设计的建议

### 计算通信比
只要 C/B ≤ 2d = 6144 FLOPs/Byte（V4-Pro），带宽不是瓶颈。
→ 不应无条件堆带宽，应瞄准平衡点。

### Power Budget
极端 kernel fusion 让 compute/memory/network 同时高负载，功耗限制成为瓶颈。

### Communication Primitives
采用 pull-based（每个 GPU 主动从远端读取），避免 push 模式的高通知延迟。

### Activation Function
建议用低成本 element-wise activation 替代 SwiGLU（无指数/除法），去掉 gate projection 后可增大中间维度 d。

## Relations
- Used in: [Deepseek V4](#DeepSeek-V4)
- Related: [Tilelang](#TileLang), [Csa Hca](#CSA-HCA), [FlashMoE Kernel](/concepts/flashmoe-kernel.md)

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
