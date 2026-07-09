---
type: Concept
title: WaferLLM System
description: Edinburgh/MSR 晶圆级 LLM 推理：PLMR 设备模型、MeshGEMM/MeshGEMV、KV shift、prefill/decode 百万 core parallelism；WSE-2 上 10–20× SGLang/A100 集群
tags:
- cerebras
- wse
- llm
- inference
- gemm
- gemv
- mesh
- noc
- plmr
- kv-cache
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf
---

# WaferLLM System

**WaferLLM**（He et al., arXiv 2502.04563, 2025）是首个面向 **晶圆级 mesh NoC 加速器**（实证平台 [Cerebras WSE-2](/entities/cerebras-wse.md)）的 **端到端 LLM 推理系统**。相对 GPU shared-memory 栈（SGLang/vLLM、Ladder 编译器）与 IPU 分布式栈（T10），它用 **PLMR 设备模型**统一约束 parallelism、通信与内存，并实现 **MeshGEMM / MeshGEMV** 与 **KV cache shift**。

**Authors:** Congjie He, Yeqi Huang, Pei Mu (Edinburgh); Ziming Miao, Jilong Xue, Lingxiao Ma, Fan Yang (MSR) | **Code:** https://github.com/MeshInfra/WaferLLM

## 为何 GPU 栈不够用

| 架构 | 内存抽象 | LLM 痛点 |
|------|----------|----------|
| GPU / TPU pod | Shared / NUMA 层次 | AllGather GEMM、PagedAttention concat KV |
| GraphCore IPU (T10) | 片上 crossbar，**常延迟** | 仅千级 core，忽略 mesh **L** |
| **WSE-2 mesh** | 百万 local SRAM + 2-D NoC | 远端延迟 **~1000×**、每 core **48 KB**、**≤25 路由路径** |

LLM 推理两阶段（见 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)）：**prefill → GEMM**；**decode → GEMV + 反复读权重/KV**，在 mesh 上若沿用 AllGather/SUMMA 或 concat KV，会违反 PLMR 的 **L/M/R/P**。

## PLMR 设备模型

| 属性 | 含义 | 系统设计含义 |
|------|------|--------------|
| **P** Parallelism | 百万 core | 双维 partition（prefill）/ replicate（decode） |
| **L** Latency | α·hops + β·routing stages | 最小化关键路径 hop；two-hop GEMM；K-tree reduce |
| **M** Memory | tens of KB / core | O(1/N²) 分块；KV **shift** 非 concat |
| **R** Routing | 有限路径数（WSE-2 ≤25） | 避免 AllGather 的 O(N) paths；K-tree 可调 K |

延迟模型：mesh Nw×Nh 上最坏 **α(Nw+Nh)+βr**；WSE 上 **α < β** → 软件 relay 极贵。**R** 与 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) / [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) 的静态路径预算一致。

## Wafer-scale LLM parallelism

### Prefill（Figure 3）

- 激活 **BLyEx**：L 沿 Y、E 沿 X partition → **百万 core** dist-GEMM
- **dist-GEMM-T**：Q@K^T 无 mesh 对角 **transpose**（L 违反）
- 自注意力/FFN 权重 W 双维分布

### Decode（Figure 4）

- **BEyLx**：E 沿 Y partition、L（=1）沿 X **replicate**
- 权重预优化布局 → decode dist-GEMV **无 transpose**
- Prefill↔decode：**NoC reshuffle** KV/权重（片上 PB/s 级，免 off-chip）

### KV cache shift（Figure 5）

GPU **concat** 新 token KV → 仅末行 core 膨胀 → **M/P 违反**。WaferLLM **向上 shift** 最老 KV 到邻行，并行 NoC 链路，保持各行均衡；相对 GPU PagedAttention 可扩展性最高 **~400×** token capacity。

## MeshGEMM（Section 5）

分布式 GEMM 对比（Figure 6）：

| 算法 | 路径/core | 关键路径延迟 | 内存/core |
|------|-----------|--------------|-----------|
| AllGather | O(N) | O[(α+β)N] | O(1/N) 膨胀 |
| SUMMA (Cerebras 默认) | O(N) | O[(α+β)N] | O(1/N²) |
| Cannon | O(1) | O(αN) | O(1/N²) |
| **MeshGEMM** | O(1) | **O(α)** 2-hop | O(1/N²) |

**机制：** (1) **Cyclic shift** 保证正确性 + 邻接通信；(2) **INTERLEAVE**（Algorithm 1）把逻辑环映射为物理 **two-hop** 邻接；(3) 支持 **dist-GEMM-T**（B 沿 Y shift + ReduceAdd）。

## MeshGEMV（Section 6）

Decode 瓶颈在 **局部 GEMV + 全局聚合**：

| Allreduce 风格 | 关键路径 | R |
|----------------|----------|---|
| Pipeline | O(2N) hops, N stages | O(1) paths |
| Ring | O[(2α+β)N] | O(1) |
| **K-tree (K=2)** | O(√N) 分组 + 有限 pass-through | O(K) at root |

**MeshGEMV**：partition B 为 N×N tiles；A 向量分片 + replicate；**K-tree allreduce** 拼接各 root 的 Csub。相对 Cerebras demo GEMV **4–8×**；相对 **单 A100 606×**（带宽 bound decode 主战场）。

## 实现与 autotune

- **~7k CSL** + **~2k Python**；支持 MHA/MQA/GQA
- 离线 autotune：按模型/seq len 选 prefill vs decode **core grid**（LLaMA3-8B：660×660 / 360×360）
- 全模型：**LLaMA3-8B、LLaMA2-13B**；34B/72B 子层（超 40 GB 片上容量）

## 作者承认的未解瓶颈（compiler 视角的机会）

论文 §7.5、§8 明确承认以下瓶颈**未解**，是 Direction 2（compiler-aware decode on mesh-NoC）的入口：

1. **48KB SRAM 限制** → pipeline parallelism 替代 tensor parallel → **5× underutilization**
2. **edge cores underutilization** → mesh 几何 + 算子 partition 假设未考虑
3. **K=2 K-tree allreduce 硬编码** → 没做 cost-model 驱动的 K 搜索

**完整 6 个 gap**（含作者没提的 3 个）见 [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md)。

## 评测要点（WSE-2 vs A100 7nm）

- **TPR** = 1/TPOT；vs **T10 ~160×**、**Ladder ~625×**（同 WSE-2）
- **E2E**：vs SGLang **2×8 A100**（NVLink+IB）**10–20×**、**2.5×** 能效；vs 单卡 **30–40×**
- **MeshGEMM** vs SUMMA/Cannon **2–3×** prefill throughput

## 与 SpaDA / TileLoom 区分

| | WaferLLM | [SpaDA](/concepts/spada-programming-language.md) | [TileLoom](/concepts/tileloom-compiler.md) |
|--|----------|-------------------|-------------------------------------------|
| **层次** | LLM 推理系统 + CSL 算子 | 通用 spatial DSL → CSL | Triton → Tenstorrent dataflow |
| **Target** | WSE LLM serving | WSE stencil/collective/GEMV | Tenstorrent 2-D mesh |
| **核心** | PLMR + MeshGEMM/V | place/dataflow/compute | spatiotemporal tile mapping |

SpaDA 报告 WSE-2 **82× GEMV vs A100**（HPDC'24 手写 CSL baseline）；WaferLLM 在 **全模型 E2E** 与 **KV 管理** 上进一步系统化为 PLMR-compliant 栈。

## 相关概念

- [Cerebras WSE](/entities/cerebras-wse.md) — WSE-2 硬件与 color 路由
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — GEMM/GEMV 阶段分工
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — massive mesh memory
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — 有限路由与 DOR
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — mesh 上 collective 设计空间
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 编程抽象
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 无 DRAM、编译器承担复杂性
- [paper/waferllm-wafer-scale-llm-inference.md](/papers/waferllm-wafer-scale-llm-inference.md) — 论文摘要页
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — 算子基础（AI、Roofline、Prefill/Decode）
- [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md) — 606× GEMV 的带宽边界与 Amdahl（Day 26）

# Citations

[1] [raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf) — He et al. (2025)
