---
type: Paper
title: "Reorienting the Vector Axis: Restructuring FlashAttention for Long-Vector Processors"
description: "BSC/UPC — 在 16384-bit 向量寄存器的 EPAC RISC-V 芯片上重排 FlashAttention：转置分数块让 query 沿连续轴、exp 多项式系数搬到标量寄存器；硅上整核 cycle 降 1.84–2.08×，FP 利用率 16.2%→29.7%"
tags:
- attention
- nonlinear
- microarchitecture
- kernel
- risc-v
- vector-processor
- fpga
created: 2026-10-26
updated: 2026-10-26
timestamp: '2026-10-26T00:00:00Z'
paper_author: [Emmanuel Irabor, Marc Casas]
year: 2026
arxiv: '2610.29489'
sources:
  - raw/papers/FlashAttention_Long_Vector_RISCV_2026.pdf
  - raw/papers/flashattention-long-vector-riscv.md
---

# 为长向量处理器重排 FlashAttention

## 一句话结论
在 2 KB 向量寄存器的 RISC-V 长向量核上，FlashAttention 的瓶颈在「向量化哪条轴」和「softmax 的 exp 怎么占寄存器」。把分数块转置成 query 沿连续轴、把 exp 多项式系数挪到标量寄存器后，EPAC 硅上整核 cycle 降 **1.84–2.08×**（d=64），FP 利用率从 **16.2%** 升到 **29.7%**；同设计 FPGA 上为 **2.71×**。

## 动机
- 长向量指令的收益与寄存器填充率成正比；EPAC 寄存器 16,384 bit，是商用 RVV 硅和 A64FX 的 32 倍。
- 原样移植 PyTorch CPU FlashAttention-2 前向只到峰值 **16.2%**：逐 query 行遍历，PV 乘只沿 64 元素 head 维向量化；softmax 的行最大值/行和是把整寄存器归约成标量；没有硬件 exp，软件多项式系数与 tile 数据抢向量寄存器导致溢出。
- N=1024、d=64 时 softmax 占 **38%** cycle，PV 乘占 **36%**。

## 方案
1. **重定向向量轴**：转置分数块和运行中的输出，让 query 沿连续轴。算法和数值不变，tile 内 query 数这一个参数决定整个 kernel 每一段的向量长度，可按机器匹配；两处行归约随之消失。
2. **标量系数**：exp 多项式系数放标量寄存器，消除溢出，softmax 的向量访存指令减少 **78.7%**。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 整核 cycle（硅，d=64） | 降 **1.84–2.08×** |
| FP 利用率 | **16.2% → 29.7%** |
| 分项（各自最佳 tile） | 标量系数 1.13×；再加融合遍历 1.29×；改加重定向 1.84×；重定向比融合版快 1.43×（40.23 vs 28.22 Mcyc） |
| FPGA（50 MHz，带宽约为芯片数倍） | 排序一致，**2.71×** |

## 与 wiki 的关系
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 无硬件 exp 时 softmax 软件近似的寄存器压力与行归约代价
- [FlashAttention](/concepts/flashattention.md) — online softmax 分块算法在非 GPU 向量 ISA 上的映射
- [FlashAttention-3](/concepts/flashattention-3.md) — 作者指出 FA3/FA4 依赖 warp 特化、异步拷贝与 tensor core，向量单元没有这些机制
- [CacheFlex](/papers/cacheflex-l2-scratchpad-scalable-vector.md) — 同为宽向量 CPU 上的 LLM 相关访存/算子优化

## 开放问题
- 只测 FP32 前向、单核；BF16/FP16、反向与多核扩展未覆盖。
- 芯片受 SerDes→DDR4 带宽限制（约 6–7 B/cycle），29.7% 的利用率仍远离峰值，硬件 exp 单元能再拿多少需要量化。
- 转置后 query 维成为向量轴，decode（单 query）场景下向量长度又会塌缩，需要改用 batch/head 维填充。

# Citations
- [arXiv:2610.29489](https://arxiv.org/abs/2610.29489) — Irabor & Casas, 2026
- [raw stub](/raw/papers/flashattention-long-vector-riscv.md)
