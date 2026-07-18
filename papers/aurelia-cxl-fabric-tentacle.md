---
type: Summary
title: 'Aurelia: CXL Fabric with Tentacle'
description: WORDS 2023 — 将寻址/路由/传输层 networking 化扩展 CXL fabric；解决 PBR 单路径与 PCIe 拥塞（RDMA 延迟可 spike 3×）
tags:
- fabric
- transport
- routing
- flow-control
- congestion-control
- memory
- infrastructure
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf
---

# Aurelia: CXL Fabric with Tentacle

**WORDS 2023** | DOI [10.1145/3605181.3626287](https://doi.org/10.1145/3605181.3626287)  
Shu-Ting Wang, Weitao Wang（UCSD, Rice）

为 **CXL disaggregated fabric** 引入 host networking 式**寻址 / 路由 / 传输**分层（含 Tentacle 机制），克服 CXL 现有多级交换的扩展性与延迟瓶颈。

## 核心贡献

1. **问题诊断**：12-bit Port ID 单路径路由；集中 fabric manager；PCIe 点对点 credit 无法防 switch 端口拥塞
2. **Aurelia**：用 CXL 现有机制实现 networking-layer 功能，支持未来千级 endpoint 解耦负载
3. **Workload 分析**：ML/HPC/KV 对 fabric-attached memory 的容量、带宽、**同步 load/store 低延迟**需求

## 关键数字

| 指标 | 值 |
|------|-----|
| CXL endpoint 规模 | 最多 **4096** |
| CXL vs RDMA (64B read) | **8.3×** 更低延迟（DirectCXL 下界） |
| PCIe 5.0 / 6.0 带宽 | **63** / **121 GB/s** |
| PCIe 拥塞下 RDMA 延迟 | **~3×** spike |

## 与 wiki 交叉

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — CXL 内存语义数据路径
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — fabric 路由/传输设计空间

# Citations

[1] [raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf](raw/papers/Aurelia_CXL_Fabric_Tentacle_2023.pdf)
[2] [raw/papers/aurelia-cxl-fabric-tentacle.md](raw/papers/aurelia-cxl-fabric-tentacle.md) — 结构化摘录
