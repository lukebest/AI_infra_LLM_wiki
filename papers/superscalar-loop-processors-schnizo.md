---
type: Paper
title: "Superscalar Loop Processors (Schnizo)"
description: "ETH Zurich MICRO'26 — 面向规则循环核的轻量多发射 SLP；Schnizo（Snitch RV32I+FP）相对标量 LA 几何均值 4.4×、面积效率 +72%；多样微核最大问题上可达理想 IPC/FPU 几何均值 92%"
tags:
- superscalar
- microarchitecture
- risc-v
- accelerator
- cpu
- pipeline
- architecture
created: 2026-11-04
updated: 2026-11-04
timestamp: '2026-11-04T00:00:00Z'
paper_author: [Luca Colagrande, Pascal Etterli, Luca Benini]
year: 2026
venue: MICRO 2026
arxiv: '2611.01904'
sources:
  - raw/papers/Superscalar_Loop_Processors_Schnizo_MICRO2026.pdf
  - raw/papers/superscalar-loop-processors-schnizo.md
---

# Superscalar Loop Processors（Schnizo）：循环专用轻量多发射

## 一句话结论
可编程加速器里大量 PE 常用单发射顺序核换密度与能效，结果 IPC 上限为 1、功能单元常闲。完整超标量又能抬面积/功耗。SLP 利用**规则、计算密集循环**的静态结构做轻量多发射，避开动态乱序调度；开源原型 **Schnizo**（增强 Snitch 的 RV32I+FP）在简单线性代数核上相对标量几何均值 **4.4×**，面积效率高 **72%**；多样 ML/HPC 微核在最大问题上可达理想 IPC/FPU 利用率的几何均值 **92%**（MICRO 2026）。

## 动机
- PE 阵列追求密度时倾向 tiny in-order 核，功能单元利用率不足。
- 常规超标量抬 IPC 的同时带来显著面积与能耗，不适合大规模 PE。
- 许多 ML/HPC 核是规则循环，调度信息可在循环结构内复用。

## 方案
1. **SLP 执行模型**：针对规则循环做多发射，用静态结构替代动态 OoO 复杂度。
2. **Schnizo 原型**：开源；在 Snitch 系 tiny RV32I+FP 上增强；先 DCP 再 DEP，循环局部复用调度。
3. **评测**：简单 LA 微核与更多样 ML/HPC 微核；对照标量基线与理想 IPC/FPU 上界。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 简单 LA 核 vs 标量（几何均值加速） | **4.4×** |
| 相对标量面积效率（LA 配置） | **+72%** |
| 多样微核、最大问题规模下相对理想 IPC/FPU（几何均值） | **92%** |
| 会议 | **MICRO 2026**；开源 |

## 与 wiki 的关系
- [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md) — 超标量主线；Schnizo 走「循环专用轻量多发射」支路，面向加速器 PE
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — SLP 刻意避开动态 OoO，用静态循环结构换利用率
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — PE 阵列核微架构在密度 vs IPC 上的折中
- [CVA6S+](/concepts/superscalar-cpu-research-2023-2026.md#cva6s开源工业核) — 同属开源 RISC-V 超标量探索；CVA6S+ 偏通用核，Schnizo 偏循环 PE

## 开放问题
- 对不规则控制流 / 短循环边界的收益会收缩；与完整 OoO 或 VLIW 在更广 kernel 集上的 Pareto 仍待对照。
- 大规模 PE 阵列上的互连与同步开销未在本文主数字中展开。

# Citations
- [arXiv:2611.01904](https://arxiv.org/abs/2611.01904) — Colagrande, Etterli, Benini; ETH Zurich; MICRO 2026
- [raw stub](/raw/papers/superscalar-loop-processors-schnizo.md)
