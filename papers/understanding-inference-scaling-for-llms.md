---
title: Understanding Inference Scaling for LLMs
created: 2026-06-15
updated: 2026-06-15
type: summary
tags: [inference, reasoning, parallelism, kv-cache, decode, prefill, latency, throughput, serving, benchmark]
sources: [raw/papers/Understanding_Inference_Scaling_for_LLMs.pdf]
---

# Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles

**arXiv:** [2605.19775](https://arxiv.org/abs/2605.19775) | **Authors:** Moiz Arif, Avinash Maurya, Sudharshan Vazhkudai, Bogdan Nicolae | **Affiliations:** Micron Technology + Argonne National Laboratory

## 一句话总结

Reasoning-centric LLM 推理从 compute-bound prefill 转向 **capacity-bound decode**：长推理链（OSL ≫ 10k tokens）产生的 KV cache 使 HBM 容量成为首要约束，标准的 DP/TP 缩放启发式在 reasoning workload 下系统性失效。

## 核心贡献

论文在 8× H200 集群上系统评估 8B-671B 参数模型的推理行为，提出 9 个 key observations：

1. **Capacity Trap**（[[inference-capacity-trap]]）：增加 concurrency 只在 KV 饱和前有效
2. **TTFT-TPOT Tradeoff**：最优 batch size 凸点
3. **DP 内存不池化**：每个 replica 独立面对 capacity wall
4. **DP tail latency** 由最先饱和的 replica 决定
5. **Parallelism Transition Point**（[[parallelism-transition-point]]）：32B 是 DP→TP inflection
6. **Dense vs MoE 分歧**：Dense (405B) 需 high TP；MoE (671B) 需 hybrid PP+TP
7. **Decode dominance**：>99% wall-clock 在 decode，arithmetic intensity 极低
8. **Reasoning Cliff**（[[reasoning-cliff]]）：KV 增长使饱和提前到 prefill
9. **Scheduler = traffic shaping**：capacity bounds throughput, bandwidth bounds latency

## 核心概念

### [[inference-capacity-trap]] — 容量陷阱
DP 下每个 GPU 复制全部 weights + 独立管理 KV cache → 长推理链导致 KV 饱和 → preemption → recomputation → throughput 崩溃。

### [[reasoning-cliff]] — 推理悬崖
KV cache 线性增长（8B: 20M tokens → 2 TB）→ 饱和后 scheduler 进入 convoy mode，新请求仅在旧请求释放 KV 后才能 admission。

### [[parallelism-transition-point]] — 并行度切换点
- **<32B**：DP optimal（weights fit in HBM, TP 通信不值得）
- **32B**：inflection point（sharding weights releases KV space → TP wins）
- **32B hybrid**：DP=4+TP=2 optimal（最小化 TP degree + 最大化 DP concurrency）

### [[prefill-decode-divergence]] — Prefill vs Decode 资源分歧
- Prefill: compute-bound（high SM, low HBM BW util）
- Decode: bandwidth-bound（high HBM BW saturation, low SM）
- Reasoning >99% 时间在 decode → 硬件应物理解耦两个阶段

### Dense vs MoE 前沿规模分歧

| Model | Architecture | Optimal | E2E Time | Bottleneck |
|-------|-------------|---------|----------|------------|
| Llama-405B | Dense, GQA | TP=8 | 986s | HBM BW + KV footprint |
| DeepSeek-R1-671B | MoE, MLA | PP=4+TP=2 | 1663s | Sync latency + routing |

关键：MoE 的低 compute-to-communication ratio 使 high-degree TP 的 all-reduce 成瓶颈；MLA 压缩 KV 使 PP bubbles 可填满。

## 对推理基础设施的启示

1. **硬件解耦 Prefill/Decode**（→ [[disaggregated-inference]], [[heterogeneous-inference]]）
2. **Tiered Memory**: HBM → DDR → CXL → NVMe 显式 KV placement
3. **HBF (High-Bandwidth Flash)**: 增容但有 read/write asymmetry + power 挑战
4. **Agentic AI 乘数效应**: fan-out × branching × tools → 系统级内存压力（HBM + DRAM 同时受压）
5. **NVLink + optical interconnect** 跨 tier 低延迟

## 与现有 wiki 的交叉引用

- [[disaggregated-inference]] — 论文为 prefill/decode 物理解耦提供实证基础
- [[heterogeneous-inference]] — compute-bound prefill + bandwidth-bound decode 对异构硬件的需求
- [[deepseek-v4]] — MLA 架构在此论文中验证为 critical for long-context reasoning
- [[csa-hca]] — DeepSeek 的注意力压缩机制（MLA 是 CSA/HCA 的前身）
- [[kv-cache]] — 本文系统刻画了 KV cache 作为推理首要瓶颈
- [[noc-router-microarchitecture]] — NoC 层面的流控机制与 HBM tier 管理共通
