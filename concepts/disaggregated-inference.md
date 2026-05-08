---
title: Disaggregated Inference
created: 2026-04-17
updated: 2026-05-08
type: concept
tags: [inference, serving-system, moe, disaggregated-inference]
sources: [arXiv:2504.02263, raw/articles/GTC 2026 – The Inference Kingdom Expands.md]
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

NVIDIA 在 [[nvidia-groq-3-lpx]] 中将 AFD（Attention FFN Disaggregation）产品化：
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
见 [[m2n-communication]]

### 3. 部署规划
给定模型 + workload + SLO → 自动确定 parallelism 策略、micro-batch 数、硬件配置。优化目标：throughput per dollar。

## 与其他解耦方案的关系

| 方案 | 解耦维度 | 通信模式 | 目标 |
|------|----------|----------|------|
| **Disaggregated Attn/FFN** | 模块层 | M2N/N2M | MoE 推理效率 |
| **Disaggregated Prefill/Decode** | 阶段层 | KV transfer | 降低 TTFT/TPOT |
| **Pool-based KV** | 内存层 | KV routing | KV cache 管理 |

## 与 Luke 研究的关联

- **Scale-up fabric**：disaggregation 意味着跨节点的高频通信，是 scale-up fabric 的核心场景
- **可重构网络**：不同模型、不同 expert 数量 → M:N 比例变化 → 需要动态适配
- **MoE 路由**：expert 的稀疏激活 + disaggregation = 通信模式高度动态

## 开放问题

1. Attention/FFN 解耦是否适用于 dense model？还是仅限 MoE？
2. Prefill/Decode 解耦 + Attn/FFN 解耦能否叠加？
3. 光交换/可重构网络能否简化 M2N 的复杂性？

## 相关页面

- [[megascale-infer-2504.02263]] — 首个大规模 disaggregated expert parallelism 系统
- [[m2n-communication]] — disaggregation 产生的通信模式
- [[heterogeneous-inference]] — GPU + LPU 异构推理
- [[nvidia-groq-3-lpx]] — LPX 产品化 AFD
