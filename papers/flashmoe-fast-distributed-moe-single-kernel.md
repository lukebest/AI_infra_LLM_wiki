---
type: Summary
title: 'FlashMoE: Fast Distributed MoE in a Single Kernel'
description: NeurIPS 2025：单 persistent GPU kernel 融合 MoE 计算与 NVSHMEM RDMA；actor 调度 + payload-efficient dispatch；8×H100 最高 6× 延迟、5.7× 吞吐、93% SM（FP32 vs FP16 基线）
tags:
- moe
- gpu
- kernel
- expert-parallelism
- communication
- neurips
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf
---

# FlashMoE: Fast Distributed MoE in a Single Kernel

**Authors:** Osayamen Jonathan Aimuyo, Byungsoo Oh, Rachee Singh (Cornell) | **Venue:** NeurIPS 2025 | **arXiv:** [2506.04667](https://arxiv.org/abs/2506.04667) | **PDF:** [raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf](raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf)

## 一句话总结

FlashMoE 用 **一个 persistent GPU megakernel** 融合 gate、dispatch、expert FFN、combine 与 **设备端 NVSHMEM RDMA**，以 **Processor/Scheduler/Subscriber actor 模型** 做 tile 级流水线，消除 CPU 调度与 **33–550×** kernel launch；在 8× H100 上相对 SOTA 达 **6×** 更低延迟、**5.7×** 吞吐、**93%** SM 利用率（FlashMoE 用 **FP32**，基线 **FP16**）。

## 核心贡献

1. **单 kernel 分布式 MoE**：整层仅 **1** 次 launch（vs DeepSpeedMoE **550**）
2. **Actor 并发模型**：OS block 内 Scheduler + Subscriber；其余 block 为 Processor（CUTLASS GEMM）
3. **Payload-efficient 通信**：对称 tensor layout + in-place padding；不用集体 API 零填充上链
4. **设备发起 one-sided RDMA**：替代 bulk-synchronous AlltoAll，减轻 straggler

## 关键数字

| 指标 | 值 |
|------|-----|
| Kernel launches / layer (2×A100, 32 experts/GPU) | FlashMoE **1** vs Megatron+DeepEP **432** |
| SM utilization (2×A100) | **93.17%** vs FasterMoE **9.67%** |
| Throughput @ 8×H100 | **17.7 MTokens/s** (**5.7×** FasterMoE) |
| Latency @ 8 GPU, 16K tokens | up to **6.4×** vs Megatron-TE |
| Overlap efficiency | **4×** |
| Layout memory overhead | ~**4×** token buffer, **≤2%** model memory |

## 与 wiki 交叉引用

- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — 机制与栈位置
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepSeek wave EP overlap（互补）
- [M2N Communication](/concepts/m2n-communication.md) — 解耦 serving 通信模式
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — attention/expert 分 GPU
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — MoE EP/TP 策略
- [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — 生产 disaggregated MoE serving

# Citations

[1] [raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf](raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf) — Aimuyo et al. (2025)
