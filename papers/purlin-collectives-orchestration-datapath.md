---
type: Paper
title: "Purlin: Separating Orchestration from the Datapath of Collectives"
description: "Stanford/NVIDIA — 集体语义/SNAC/Atom 解耦；延迟最高 5.14×、带宽 4.50×；SGLang 离线均值 1.13×、在线交互最高 2.85×"
tags:
- architecture
- llm
- inference
- serving
- collective
- interconnect
- scale-up
- gpu
- nvidia
- communication
- serving-system
- throughput
- latency
- distributed
created: 2026-10-01
updated: 2026-10-01
timestamp: '2026-10-01T00:00:00Z'
paper_author: [Osayamen Jonathan Aimuyo, Swapnil Gandhi, Christos Kozyrakis]
year: 2026
arxiv: '2609.36954'
sources:
  - raw/papers/Purlin_Collectives_Orchestration_Datapath_2026.pdf
  - raw/papers/purlin-collectives-orchestration-datapath.md
---

# Purlin: 集体通信的编排与数据通路解耦

## 一句话结论

把 scale-up 集体拆成 **语义/布局 → SNAC 编排 → Atom 数据通路（copy/reduce）**；七类集体上延迟最高 **5.14×**、带宽最高 **4.50×**；接入 SGLang 后离线吞吐/交互均值 **1.13×**（最高 **1.37×**），在线交互均值 **1.26×**（过载最高 **2.85×**）。

## 动机

- 推理依赖 NVLink 域内集体，但 NCCL/NVSHMEM/MSCCL++/ParallelKittens 等常把语义、编排与 datapath **绑死**，难同时保留跨代兼容与对新硬件机制（如 TMA）的快速演进。
- Prefill（吞吐）与 decode（延迟）需要不同执行策略；应用侧还要可定制原语。

对照 [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)、[NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md)、[Entwine](/papers/entwine-tiled-computation-fine-grained-gpu-comm.md)。

## 方案

1. **顶层**：集体 = 输入/输出布局命名 + copy 或 reduction。
2. **中层 SNAC**（Stage, Notify, And Consume）：从规格推导协调，无需手写完整通信日程。
3. **底层 Atom**：代际相关的 copy/reduce；可换 datapath 而复用编排。
4. **评测**：A100 / H200 / B200；七集体微基准 + SGLang LLM 服务 + 扩散生成。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 集体延迟 / 带宽 vs 基线 | 最高 **5.14×** / **4.50×** |
| SGLang 离线（45 配置，三代 GPU） | 交互均值 **1.13×**，最高 **1.37×** |
| 在线交互 | 均值 **1.26×**，过载最高 **2.85×** |
| 扩散 e2e 延迟 | 最高 **1.13×** |
| 示例：换 NCCL→Purlin 请求延迟 | **1.23–1.25×**；TTFT **1.10×**（文中 Qwen3.5 分解） |

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把「集体实现可演进」轴补到推理 scale-up
- [NVLink/NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 域内通信软件栈
- [Mixture-of-Kittens](/papers/mixture-of-kittens-moe-megakernel-nvl72.md) — 同日 scale-up 软件；MoK 融 MoE 算通，Purlin 通解耦集体层

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.36954) — Aimuyo et al., arXiv:2609.36954
[2] [raw stub](raw/papers/purlin-collectives-orchestration-datapath.md)
