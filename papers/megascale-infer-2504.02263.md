---
type: Paper
title: MegaScale-Infer
description: MegaScale-Infer：MoE disaggregated attention/FFN serving，ping-pong pipeline
  + M2N 通信库，1.90× 吞吐提升
tags:
- moe
- disaggregated-inference
- expert-parallelism
- serving-system
- bytedance
timestamp: '2026-04-16T00:00:00Z'
created: 2026-04-16
sources:
- arXiv:2504.02263
- raw/papers/megascale-infer-2504.02263.pdf
---

# MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism

**arXiv**: [2504.02263](https://arxiv.org/abs/2504.02263) | **v4** (2025-07-26)
**Authors**: Ruidong Zhu, Ziheng Jiang, Chao Jin, Peng Wu, et al. (ByteDance Seed + PKU)
**Key metric**: 1.90× per-GPU throughput, 1.5–2× cost reduction in production

---

## 一句话总结

> MoE 的稀疏激活使 FFN 从 compute-intensive 变为 memory-intensive → GPU 利用率低；MegaScale-Infer 通过 **disaggregated expert parallelism**（attention/FFN 分 GPU 部署）+ **ping-pong pipeline** + **M2N 通信库**解决。

---

## 核心问题

MoE 在推理时遇到 **sparsity 导致 GPU 利用率低**的问题：

- Attention 在 decode 阶段是 **memory-intensive**（必须访问所有历史 KV cache）
- FFN 在 dense model 时因 batching 可以 reuse weights，compute-intensive
- **MoE 的 sparse activation**（top-k routing）使每个 expert 只处理 batch 中少量 token
  - 以 Mixtral 8×22B 为例：batch=156 tokens，每个 expert 平均只处理 39 tokens
  - 理论 FFN MFU = top-k/#expert = 2/8 = **25%**
- 增大 batch size 可以缓解，但受限于：
  - 在线推理的低延迟要求
  - KV cache 的 GPU 内存限制
  - 增大 parallelism 引入更多通信开销

---

## 核心贡献

### 1. Disaggregated Expert Parallelism（解耦专家并行）

把 attention 和 FFN 模块**部署在不同的 GPU 组**：

- **Attention nodes**：replicate attention 模块（存储 KV cache），用 data parallelism 扩展
- **Expert nodes**：每个节点 1-8 GPUs，每个 GPU 存一个 expert，用 expert parallelism 扩展
- **独立扩展**：attention 和 FFN 可以独立选择 parallelism 策略
- **异构部署**：attention 用内存带宽大的 GPU（如 HBM），FFN 用算力强的 GPU

**核心洞察**：通过在多个 attention replicas 上聚合请求，**每个 expert 的 effective batch size 增大**，FFN 重新变成 compute-intensive。

### 2. Ping-Pong Pipeline Parallelism（乒乓流水线）

 disaggregation 引入的 idle time 问题：每个 token 必须**顺序**经过 attention → FFN → attention → FFN...

解法：把一批请求分成 **m 个 micro-batches**，在 attention nodes 和 expert nodes 之间"乒乓"传递：

- Micro-batch i → attention → expert → attention → expert → ... → output
- 当 expert 处理 micro-batch i 时，attention 可以处理 micro-batch i+1
- **目标**：让通信时间被计算时间覆盖

**必要条件**（公式）：
1. Ta ≈ Te（attention 和 expert 的计算时间要接近）
2. Tc < Tf（单 micro-batch 通信时间 < 计算时间）
3. m × Tf ≥ 2 × (Tf + Tc)（总时间覆盖两跳通信）

最小 micro-batch 数：m ≥ 2 × (1 + Tc/Tf)

### 3. M2N Communication Library

Disaggregation 后，原来 MoE layer 内的 All-to-All 通信变成了 **M 个 attention GPU → N 个 expert GPU 的 M2N 通信**。

现有 NCCL 等库在 M2N 场景下性能差（大量小消息、频繁 group init、GPU-CPU 不必要的数据拷贝）。

MegaScale-Infer 的 M2N 库优化：
- 消除不必要的 GPU→CPU→GPU 数据拷贝
- 消除 group initialization overhead
- 减少 GPU 同步
- Traffic-oriented 优化

**结果**：M2N 通信比 NCCL **4.2× 吞吐更高，延迟降低 68.2%**

### 4. Performance Model for Deployment Planning

给定 MoE 模型 + workload + 硬件 + 延迟要求，自动确定：
- Attention 和 Expert 的 parallelism 策略
- Ping-pong pipeline 的 micro-batch 数量
- 最大 batch size
- 硬件配置

目标是 **throughput per dollar** 最大。

---

## 评估结果

- **测试规模**：MoE 模型 132B–317B 参数
- **per-GPU throughput**：比 SOTA **1.90×** 提升
- **异构集群**：比 SOTA **1.86×** per-cost 提升
- **生产部署**：节省 **1.5–2×** 服务成本

---

## 与 Luke 研究的关联

- **AI infra / 推理系统**：disaggregation 是 scale-up fabric 的重要场景
- **Scale-up fabric**：M2N 通信库的优化对跨节点通信有意义
- **Heterogeneous inference**：attention（memory-bound）用 HBM GPU，FFN（compute-bound）用算力 GPU → Vera Rubin + LPX 的异构方案也是类似思路
- **可重构网络**：disaggregation 意味着动态的资源分配和调度

---

## 关键洞察

1. **MoE sparsity 是 memory-intensity 的根源**：不是计算变少了，而是每个 expert 的有效 batch 变小了
2. **Disaggregation 的本质是聚合**：通过多个 attention replica 聚合请求，增大 expert 的 effective batch
3. **Ping-pong pipeline 是时序上的聚合**：micro-batch 在 attention 和 expert 之间 shuttle，让通信被计算覆盖
4. **M2N vs All-to-All**：disaggregation 改变了通信模式，从 All-to-All 变成 M2N/N2M，这需要专门的通信库优化

---

## 相关页面
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 解耦推理：attention/FFN 分离部署的架构范式
- [M2N Communication](/concepts/m2n-communication.md) — M2N 通信模式及其优化
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构推理（GPU + LPU）vs attention/FFN disaggregation
- [Lpu Architecture](/concepts/lpu-architecture.md) — LPU 处理 FFN/MoE 的角色
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — Groq LPU 用于 FFN/decode

# Citations

[1] [arXiv:2504.02263](https://arxiv.org/abs/2504.02263)
[2] [raw/papers/megascale-infer-2504.02263.pdf](raw/papers/megascale-infer-2504.02263.pdf)
