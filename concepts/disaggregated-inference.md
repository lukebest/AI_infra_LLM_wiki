---
type: Concept
title: Disaggregated Inference
description: 解耦推理：attention/FFN 分离部署，独立扩展，batch 聚合
tags:
- inference
- serving-system
- moe
- disaggregated-inference
timestamp: '2026-08-21T00:00:00Z'
created: 2026-04-17
updated: 2026-08-21
sources:
- arXiv:2504.02263
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
- raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf
- raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf
- raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf
---

# Disaggregated Inference（解耦推理）

## 定义

将 Transformer 的不同模块（attention、FFN/MoE）部署在**不同硬件/节点**上，各自独立扩展和优化。核心思想：不同模块的资源瓶颈不同，解耦后可以针对性分配硬件。

## 动机

传统部署中，attention 和 FFN 共享同一 GPU，导致：
- **Attention（decode 阶段）**：memory-bound（需读全部 KV cache），但计算量低 → GPU 算力浪费
- **FFN（dense）**：compute-bound，batch 大时算力利用率高
- **FFN（MoE）**：sparse activation → 每个 expert 的 effective batch 小 → 变成 memory-bound

**矛盾**：同一 GPU 上，attention 需要内存带宽，MoE FFN 需要聚合 batch 提升算力利用率，两者互相牵制。

## 核心架构

```
Attention Nodes (M个)          Expert Nodes (N个)
┌──────────┐                  ┌──────────┐
│ Attn + KV│ ── M2N ──→      │ Expert 0 │
│ Cache    │                  │ Expert 1 │
│ (replica)│ ←── N2M ──      │ ...      │
└──────────┘                  └──────────┘
  Data Parallel                Expert Parallel
  独立扩展                     独立扩展
```

- **Attention nodes**：存储 KV cache，用 data parallelism 复制多份
- **Expert nodes**：每个 GPU 存一个 expert，用 expert parallelism 扩展
- **通信**：M2N（dispatch tokens）+ N2M（collect results）

## NVIDIA LPX 产品化（AFD）

NVIDIA 在 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) 中将 AFD（Attention FFN Disaggregation）产品化：
- **GPU 运行 attention**（stateful，需要 HBM 存 KV cache）
- **LPU 运行 FFN/MoE expert**（stateless，确定性架构适配静态工作负载）
- Token routing 通过 Spectrum-X Ethernet scale-out fabric
- Ping-pong pipeline 掩盖通信延迟
- 这是 M2N 通信模式在 GPU+LPU 异构场景的具体实现

## 关键优势

1. **独立扩展**：attention 和 expert 各自选择 parallelism 策略
2. **异构部署**：attention 用 HBM 大的 GPU，expert 用 SRAM 快的 LPU
3. **Batch 聚合**：多个 attention replica 聚合请求 → expert 的 effective batch 增大 → MoE FFN 回到 compute-intensive
4. **资源利用率**：每种硬件只做自己擅长的事

## 核心技术挑战

### 1. Ping-Pong Pipeline
disaggregation 引入额外通信 → 需要用 pipeline 并行掩盖延迟。将 batch 分成 m 个 micro-batch，在 attention 和 expert 之间"乒乓"传递。

必要条件：
- Ta ≈ Te（计算时间匹配）
- Tc < Tf（通信 < 计算）
- m ≥ 2 × (1 + Tc/Tf)

### 2. M2N 通信
见 [M2N Communication](/concepts/m2n-communication.md)

### 3. 部署规划
给定模型 + workload + SLO → 自动确定 parallelism 策略、micro-batch 数、硬件配置。优化目标：throughput per dollar。

## 与其他解耦方案的关系

| 方案 | 解耦维度 | 通信模式 | 目标 |
|------|----------|----------|------|
| **Disaggregated Attn/FFN** | 模块层 | M2N/N2M | MoE 推理效率 |
| **Disaggregated Prefill/Decode** | 阶段层 | KV transfer | 降低 TTFT/TPOT |
| **Pool-based KV** | 内存层 | KV routing | KV cache 管理 |
| **3DLS 物理隔离** | 封装垂直维 | 垂直 KVT + 侧向 AR | 去掉共享 D2D 争用 |

## 与 Luke 研究的关联

- **Scale-up fabric**：disaggregation 意味着跨节点的高频通信，是 scale-up fabric 的核心场景
- **可重构网络**：不同模型、不同 expert 数量 → M:N 比例变化 → 需要动态适配
- **MoE 路由**：expert 的稀疏激活 + disaggregation = 通信模式高度动态

## 开放问题

1. Attention/FFN 解耦是否适用于 dense model？还是仅限 MoE？
2. Prefill/Decode 解耦 + Attn/FFN 解耦能否叠加？
3. 光交换/可重构网络能否简化 M2N 的复杂性？

## 实证支持

[Understanding Inference Scaling For Llms](/papers/understanding-inference-scaling-for-llms.md) 通过 8B-671B 模型的系统实验为 prefill/decode 解耦提供了实证基础：
- Prefill 是 compute-bound（低 HBM BW util），Decode 是 bandwidth-bound（高 HBM BW saturation）
- Reasoning >99% wall-clock 在 decode → 硬件应物理解耦
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) 量化了两阶段的正交资源需求

## 相关页面

- [Megascale Infer 2504.02263](/papers/megascale-infer-2504.02263.md) — 首个大规模 disaggregated expert parallelism 系统
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — 单节点 EP megakernel（与 disagg 正交，可叠在 expert 侧）
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — DeepSeek wave EP overlap
- [M2N Communication](/concepts/m2n-communication.md) — disaggregation 产生的通信模式
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — GPU + LPU 异构推理
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX 产品化 AFD
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — Prefill vs Decode 的资源特性分歧
- [Understanding Inference Scaling For Llms](/papers/understanding-inference-scaling-for-llms.md) — 系统性推理 scaling 瓶颈分析
- [PRESERVE Prefetch](/papers/preserve-prefetch-weights-kv-cache.md) — 分布式 serving 中权重/KV HBM→L2 prefetch
- [HCache State Restoration](/papers/hcache-fast-state-restoration.md) — 会话状态快速恢复（隐藏激活）
- [FlexInfer Offloading](/papers/flexinfer-on-device-llm-offloading.md) — 端侧预算自适应 offload
- [SuperInfer Superchips](/papers/superinfer-slo-aware-rotary-scheduling.md) — GH200 NVLink-C2C 上 SLO-aware KV 调度
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — chiplet 上 PD+TP 的 KVT/AR 物理隔离（IEEE CAL 2026）
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 驻留 ReRAM FFN 池 + 有界组播；iso-compute vs H20 **9.5×** FFN 延迟
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — 不拆模块池，拆 HBF→GPU 的 Direct/Relay 投递
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 同包内 host / DRAM-PNM attn / FeFET expert

# Citations

[1] [arXiv:2504.02263](arXiv:2504.02263)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
[3] [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf](raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf)
[4] [raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf](raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf) — 3DLS 物理隔离
[5] [raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf](raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf) — ReXpert 驻留 FFN 池
[6] [raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf](raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf) — DASH HBF 双路径
