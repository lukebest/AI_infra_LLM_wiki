---
type: Concept
title: LPU Architecture
description: Groq LPU 推理专用架构：SRAM-first、显式数据搬运、编译器调度
tags:
- lpu
- accelerator
- architecture
- deterministic
- inference
timestamp: '2026-05-08T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
---

# LPU Architecture（Language Processing Unit）

LPU 是 Groq（现 NVIDIA）设计的推理专用加速器架构。核心思想：不追求峰值算力，而是追求可预测的低延迟。

## 设计哲学
- **SRAM-first**：片上 SRAM 作为主要工作存储，不用硬件缓存
- **向量为主**：320-byte 固定向量作为计算/内存/通信的统一工作单元
- **编译器控制**：显式调度一切，无运行时决策
- **确定性互联**：C2C 链路 + plesiosynchronous 协议

## Slice 架构（ISCA 2020 原始设计）

LPU 将架构重组为**单功能单元组 "slice"**，slice 间通过 streaming registers 和 scratchpad SRAM 传递数据：

| Slice | 功能 |
|-------|------|
| MXM (Matrix) | 密集 MAC，矩阵乘法 |
| VXM (Vector) | 逐元素运算、类型转换、激活函数 |
| SXM (Switch) | 排列、旋转、分发、转置 |
| MEM | 片上 SRAM 存储 |

- Slice **水平排布**：数据水平流
- Slice 内指令**垂直 pump**：指令垂直穿越功能单元
- 概念上类似 systolic array：指令垂直流、数据水平流

## SRAM 与内存层次

| 层级 | GPU | LPU |
|------|-----|-----|
| L1 | Hardware-managed cache | Streaming registers |
| L2 | Hardware-managed cache | Scratchpad SRAM（编译器管理） |
| HBM | 高带宽外部内存 | 无（SRAM-only，LP30 为 500 MB） |
| DDR5 | Host DRAM | FPGA 附加 DRAM（LPX 中最多 256 GB/FPGA） |

**关键权衡**：SRAM 极快（低延迟、高带宽）但密度低、成本高 → LPU 的 TTFT 和 tokens/sec/user 极快，但总吞吐受 SRAM 容量限制（weight 占满后 KV cache 空间不足）。

## 芯片世代对比

| 世代 | 制程 | SRAM | 算力 | 状态 |
|------|------|------|------|------|
| LPU Gen 1 | GF 14nm | 230 MB | 750 TFLOPs (INT8) | 量产（2020） |
| LPU Gen 2 | Samsung SF4X | — | — | 失败（112G SerDes 问题） |
| LP30 (Gen 3) | Samsung SF4 | 500 MB | 1.2 PFLOPs (FP8) | NVIDIA 产品化中 |
| LP35 | Samsung SF4 | 500 MB | — | 规划中（+NVFP4） |
| LP40 | TSMC N3P + CoWoS-R | Hybrid bonded DRAM | — | Feynman 世代，NVLink 协议 |

## 与 GPU 的核心区别

| 维度 | GPU | LPU |
|------|-----|-----|
| 内存层次 | HBM + 缓存（硬件管理） | SRAM（编译器管理） |
| 调度 | 硬件 warp scheduler | 编译器静态调度 |
| 数据搬运 | 隐式（缓存一致性） | 显式（编译器编排） |
| 优化目标 | 峰值吞吐 | 可预测延迟 |
| 通信 | NVLink（自适应路由） | C2C（确定性） |
| 适用负载 | Prefill、attention（stateful） | FFN/MoE expert（stateless） |

## 相关页面
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — Groq 3 LPX 实体（含 rack 级架构）
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行概念
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — GPU+LPU 异构推理
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — Attention/FFN 解耦推理

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
