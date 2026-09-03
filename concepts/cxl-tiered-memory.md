---
type: Concept
title: CXL Tiered Memory
description: CXL 扩展内存分层 — 页迁移（M5）、解耦内存数据通路（CosMoS）、fabric（Aurelia）；把冷页/容量迁出本机 DRAM
tags:
- cxl
- memory
- memory-bandwidth
- interconnect
- fabric
- storage
- infrastructure
- latency
timestamp: '2026-09-03T00:00:00Z'
created: 2026-07-17
updated: 2026-09-03
sources:
- raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf
- raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf
- raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf
- raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf
---

# CXL Tiered Memory

## 定义

**CXL（Compute Express Link）** 把远端/扩展内存挂到 CPU 一致性域附近，形成 **本机 DRAM ↔ CXL 内存** 的分层容量。LLM serving / 训练常受 **KV cache、激活、权重副本** 容量挤压；CXL 分层用页迁移与数据通路优化，在可接受延迟下扩大有效内存。

## 三条研究线

| 方向 | 代表 | 核心问题 |
|------|------|----------|
| **页迁移策略** | [M5](/papers/m5-cxl-tiered-memory-page-migration.md) | 何时、迁哪些页；避免 thrashing 与错误层级 |
| **解耦内存数据移动** | [CosMoS](/papers/cosmos-disaggregated-memory-data-movement.md) | 解耦内存池上的 cost-effective 搬运/访问支持 |
| **CXL fabric** | [Aurelia](/papers/aurelia-cxl-fabric-tentacle.md) | 多主机共享 CXL 内存的 fabric / tentacle 拓扑 |

## 与 LLM 系统的交汇

- **KV / 会话状态**：长上下文与多轮对话放大容量需求；分层内存与 [HCache](/papers/hcache-fast-state-restoration.md)、[FlexInfer](/papers/flexinfer-on-device-llm-offloading.md) 的 offload/prefetch 正交但目标相近（把冷状态移出热路径）。
- **训练激活/检查点**：大 batch 与长序列可把中间张量放到 CXL 层，代价是带宽与延迟。
- **MoE expert 近数据执行**：[DynaNDE](/papers/dynande-near-data-expert-scheduling.md) 在 CXL-NDP 上做 AMove 专家计算，与纯页迁移正交；vs MoNDE prefill/decode 平均 2.6×/2.2×。
- **超芯片 / C2C**：[SuperInfer](/papers/superinfer-slo-aware-rotary-scheduling.md) 在 GH200 上利用 NVLink-C2C 的统一内存视图——与 CXL 同属「扩大可寻址内存」，介质与一致性模型不同。
- **Hot Chips 2026（未单列论文）**：Intel Diamond Rapids MVF 写 **CXL 3.0 1LM / Flat2LM** + CXL 3 I/O（每 hub 4×16 Flexbus，可 PCIe Gen6 / CXL 3 / UPI 3）；不是 GPU scale-up。[Vera](/papers/hc2026-nvidia-vera.md) 带 **CXL 3.1**。

## 开放问题

1. LLM serving 的访问模式（顺序扫 KV vs 随机 KV）是否匹配通用 OS 页迁移启发式？
2. CXL 带宽/延迟相对 HBM：何时该用软件 prefetch/异步 DMA，而非被动缺页？
3. Fabric 规模化后的 QoS：多租户训练/推理如何隔离？

## 相关页面

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — CPU↔内存通路全景
- [DRAM and Memory System](/concepts/dram-memory-system.md) — DRAM 层次
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 计算/状态解耦
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构内存/加速器栈
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — 更冷一层（存储）对照

# Citations

[1] [raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf](raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf)
[2] [raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf](raw/papers/CosMoS_Disaggregated_Memory_Data_Movement_2025.pdf)
[3] [raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf](raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf)
[4] [raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf](raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf) — DynaNDE CXL-NDP MoE
