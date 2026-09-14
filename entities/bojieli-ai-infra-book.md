---
type: Entity
title: 深入理解 AI Infra（李博杰）
description: 开源教材《深入理解 AI Infra：量化分析与系统设计》— 从约束推导设计，五个数据搬移问题贯穿十二章
tags:
- book
- methodology
- infrastructure
- architecture
- llm
- training
- inference
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# 《深入理解 AI Infra：量化分析与系统设计》

李博杰开源教材（Apache-2.0）。定位是 AI Infra 的量化体系结构书：对照 H&P《量化研究方法》，从硬件约束和模型架构推导系统设计，而不是罗列框架 API。

源 stub：[raw/articles/bojieli-ai-infra-book.md](/raw/articles/bojieli-ai-infra-book.md)。章节摘要在 [analyses/ai-infra-book/](/analyses/ai-infra-book/ch01-intro.md)。

## 方法：「从约束推导设计」

先明确任务与质量，再列出计算、存储、通信和依赖；检查容量是否装得下、带宽是否供得上、哪些等待无法消除。估算不必一开始精确，但必须知道算进了什么、漏了什么。方法专页：[Constraint-Driven AI Infra Design](/concepts/constraint-driven-ai-infra-design.md)。

贯穿五问：**搬什么、搬多少、搬几次、经过哪里、谁必须等它。**

利用率：峰值下界是物理极限。计算侧 \(F/(\Pi T)\) 为 **MFU**，带宽侧 \(R/(\beta T)\) 为 **MBU**。下界与实测之差要么是模型漏项，要么是可去掉的系统开销。

## 阅读地图

| 部分 | 章 | 本 wiki 主要对接 |
|------|----|------------------|
| 模型与负载 | [Ch.1](/analyses/ai-infra-book/ch01-intro.md)–[Ch.3](/analyses/ai-infra-book/ch03-workloads.md) | [Quantitative Architecture](/concepts/quantitative-architecture-fundamentals.md)、[Prefill/Decode](/concepts/prefill-decode-divergence.md) |
| 芯片与系统 | [Ch.4](/analyses/ai-infra-book/ch04-accelerators.md)–[Ch.7](/analyses/ai-infra-book/ch07-datacenter-network.md) | [GPU SIMT](/concepts/gpu-simt-architecture.md)、[超节点](/concepts/ai-infra-supernode.md)、[NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)、[Clos](/concepts/clos-fat-tree-topology.md)、[UB](/entities/unifiedbus-ub.md) |
| 推理与训练 | [Ch.8](/analyses/ai-infra-book/ch08-inference-optimization.md)–[Ch.12](/analyses/ai-infra-book/ch12-edge-cloud.md) | [Disaggregated Inference](/concepts/disaggregated-inference.md)、[Collectives](/concepts/llm-distributed-training-collectives.md) |

作者建议：模型/应用侧重 8–9、11–12；系统/网络侧重 5–7、9–10；芯片侧重 4–7。先自己估，再对书。

## 作者线索（为何这本书对 UB / 超节点有一手数字）

- MSRA / 中科大系统研究；Bing DNN 的 FPGA 模型并行（2016）。
- MindSpore **AKG** 算子生成；在线 softmax → 后来 FlashAttention 同族思路。
- 2020 起 **Unified Bus**：万卡互联；书中 OpenURMA 仿真给出 Load/Store vs PCIe NIC 的 μs 级分解。
- KV-Direct（可编程 NIC KV）；创业后实时语音管线（5 s → ~500–600 ms）。

## 贯穿算例（工作层只保留量级）

- **Qwen3-8B / 32B / 235B-A22B**：容量、TP、EP、PD 配比。
- **DeepSeek V4 / V4.1 Flash**：CED、SWA、Engram 表、200K decode。
- **HGX H100 八卡**：NVLink 450 GB/s/dir，ConnectX-7 50 GB/s/dir。
- **CloudMatrix384**：384×910C + 192 CPU，UB 交换。

数字一律来自书中手稿；未在书中出现的规格不补。

# Citations

[1] [GitHub manuscripts](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/00-前言.md) — 前言与目录
[2] [AI-Infra-Book.pdf](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [Online](https://bojieli.github.io/ai-infra-book/)
[4] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
