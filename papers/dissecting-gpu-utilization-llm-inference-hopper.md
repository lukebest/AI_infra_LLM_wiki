---
type: Paper
title: "Dissecting GPU Utilization for LLM Inference on Nvidia Hopper"
description: KTH — H100 NVL 上 vLLM/FA3 八视图利用率；decode GMMA 64-row fill 1.6–12.5%，SOL 冷 92% vs decode 7.9%
tags:
- gpu
- nvidia
- inference
- decode
- prefill
- attention
- kernel
- llm
- throughput
- latency
- batching
- serving
- architecture
- benchmark
- memory-bandwidth
- moe
timestamp: '2026-09-15T00:00:00Z'
created: 2026-09-15
updated: 2026-09-15
sources:
- raw/papers/Dissecting_GPU_Utilization_LLM_Inference_Hopper_2026.pdf
- raw/papers/dissecting-gpu-utilization-llm-inference-hopper.md
---

# Dissecting GPU Utilization for LLM Inference on Nvidia Hopper

**Authors:** Mohammad Siavashi, Gerald Q. Maguire Jr., Dejan Kostić, Marco Chiesa
**Affiliation:** KTH Royal Institute of Technology
**arXiv:** [2609.12923](https://arxiv.org/abs/2609.12923)（2026-09-11，cs.PF / cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.12923)

相对 [FlashAttention-3](/concepts/flashattention-3.md) 的 kernel 设计论文，本文是 **serving 现场测量学**：同一 FA3/cuBLASLt 栈上，把「SM 利用率」拆成可对账的机制。相对 [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) 的 Roofline 直觉，给出 Hopper **GMMA m64 fragment** 的硬上限数字。

## 动机

Nsight 的单一 `sm__throughput`（俗称 SM utilization / sm_busy_pct）是 elapsed-cycle 管道吞吐代理，不是「有用 matmul」也不是 occupancy。Decode 时每请求一行 token，稠密投影变成小-M GEMM；Hopper BF16 **GMMA（wgmma.mma_async）固定 64 行 M 轴 fragment**，小 batch 只能填满一小部分真实 token 行——利用率数字可以看起来「忙」，有用工作却很少。

## 方案

**平台：** H100 NVL（文内 **94 GB** HBM3）；**栈：** vLLM + FlashAttention-3 + cuBLASLt（CUDA Graphs on）。**模型：** Llama-3-8B、Qwen3-14B、Qwen3-32B、Qwen3-30B-A3B（MoE）。**三相：** 冷 prefill（关 prefix cache）、暖 prefill（高命中 prefix）、decode；扫描 context S 与 batch B；按层角色（QKV / o_proj / gate-up / down / FA3 / MoE fused）聚合。

**八视图：** 各锚定 NCU 计数器或显式公式——含 SM time-util、per-active-SM SOL、两种 occupancy 分母（架构 64-warp vs kernel 资源上限）、**GMMA M-fragment fill** η_M = M_actual / (ceil(M/64)·64)、stall 签名、wave quantization / SM coverage 等。

## 效果（仅论文数字）

**SM busy（热力图归纳）。** 冷 prefill 稠密 GEMM **73–97%**（均值 **92%**，峰值 **97.4%** 在 Llama-3-8B down_proj）；暖 prefill 稠密塌到 **8–11%**（部分 FA3 **14–73%** 均值 **33%**）；decode 稠密 **6.5–12.7%**（均值 **9.4%**），FA3 **3.4–23.9%**，MoE **16–23%**。同模型同 (S,B) 下冷 prefill 可 ~**97%**、暖 prefill 仅 ~**9%**。

**Fragment fill 天花板。** Decode 稠密 GEMM η_M 均值 **5.86%**（范围 **1.6–12.5%**）；文称 per-kernel compute-throughput 可读数会把有用 matmul **高估 8–64×**。B=32 时 GEMM 报 ≈**72%** sm_busy，但每个 m64 fragment 大约只有一半行是真实 token（引言例）。设备级 compute SOL：冷 **92.0%** vs decode **7.9%**（**11.7×**）；暖 **22.6%**。

**Occupancy 分母陷阱。** Llama-3-8B decode 典例 ~**9.0–9.4** warps/SM → 相对 64-warp 架构上限 **12–15%**，但相对 kernel 自身寄存器/SMEM 上限常 **75–95%**（约 **5×** 分母差）。Decode 主 stall：**long_scoreboard 70–84%**；冷 prefill 则更多 barrier/gmma。

**B=32 验证臂。** 稠密 GEMM SM-busy 从 B=1 ~**12%** 升到 **71.9%**；FA3-fwd 达 decode iteration 的 **49.5%**。文论处方：抬高 M（persistent decode / 跨请求 token packing），**不是** 靠 cuBLASLt 换 tile 绕过 m64 地板。

**口径：** 单卡 H100 NVL + 指定 vLLM/FA3 版本；绝对值不保证跨 SKU 平移；仿真/分析混合，主结果来自 NCU 实测报告。

## 与 wiki 的关系

- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — Warp/occupancy/Tensor Core；本文量化 Hopper decode 的分母陷阱
- [FlashAttention-3](/concepts/flashattention-3.md) — 被测 attention 内核；本文补 stall 签名与 decode 份额
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 小-M decode = fragment fill 地板的实测版
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 文内把抬高 M / PD 解耦列为杠杆之一（测量侧）
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 冷→暖→decode 利用率塌缩的计数器证据

## 开放问题

1. 单 SKU（H100 NVL）；Blackwell / 其他 FA 后端未测。
2. FA3 与稠密 GEMM 分角色报告；端到端 tok/s 不是主指标。
3. m64 是 BF16 GMMA 指令属性；其他精度/指令路径的地板可能不同。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.12923) — Siavashi et al., arXiv:2609.12923
[2] [raw/papers/dissecting-gpu-utilization-llm-inference-hopper.md](raw/papers/dissecting-gpu-utilization-llm-inference-hopper.md) — 结构化摘录
