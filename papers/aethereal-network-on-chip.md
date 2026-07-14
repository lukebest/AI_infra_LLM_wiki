---
type: Summary
title: Æthereal Network on Chip
description: Philips Æthereal NoC（IEEE MDT 2005）— contention-free TDM 电路交换提供 GS；GS+BES 组合；分布式/集中编程；四种路由器面积对比
tags:
- noc
- aethereal
- guaranteed-service
- tdm
- circuit-switching
- qos
- flow-control
- philips
timestamp: '2026-07-14T00:00:00Z'
created: 2026-07-14
sources:
- raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf
---

# Æthereal Network on Chip

**IEEE Design & Test of Computers, Sept.–Oct. 2005** | DOI [10.1109/MDT.2005.99](https://doi.org/10.1109/MDT.2005.99)  
Goossens, Dielissen, Rădulescu（Philips Research）

早期 SoC NoC 经典：用 **contention-free routing（流水线 TDM 电路交换）** 提供硬 **Guaranteed Services（GS）**，并用并行 **Best-Effort（BES）** 吃掉未用带宽。概念页：[Æthereal NoC](/concepts/aethereal-noc.md)。

## 核心贡献

1. **Contention-free GS**：时隙表预约 → 无争用、最小缓冲、GS 块可无 header  
2. **GS + BES**：BES 虫孔吃空闲/未用时隙，提高利用率  
3. **两种编程模型**：分布式 SetUp/TearDown（可扩展）vs 集中/MMIO（低成本）  
4. **四种硅实现**（0.13 µm）：从 0.24 mm² GS-BE 分布式到 **0.033 mm² / 1 GHz** GS-only

## 关键数字

| 实现 | Area | Freq | 每端口原始带宽 |
|------|------|------|----------------|
| GS-BE distributed | 0.24 mm² | 500 MHz | 2 GB/s |
| GS-BE centralized (N×N) | 0.13 mm² | 500 MHz | — |
| GS-only centralized | **0.033 mm²** | **1 GHz** | **4 GB/s** |

GS-only ≈ **2× 性能、~1/4 面积**（相对 GS-BE）；代价是缺少“软”流量通道时可能要更多全局线/路由器。

## 与 wiki 交叉

- [Æthereal NoC](/concepts/aethereal-noc.md) — 机制展开
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) — 电路/虫孔对照
- [Switching Principles](/concepts/switching-principles.md) — TDM / 电路交换
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性通信谱系
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — 预配置确定性通道（对照）
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — BES 虫孔侧

# Citations

[1] [raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf](raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf)
[2] [raw/papers/aethereal-network-on-chip.md](raw/papers/aethereal-network-on-chip.md) — 结构化摘录
