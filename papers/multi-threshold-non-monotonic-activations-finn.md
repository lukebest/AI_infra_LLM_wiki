---
type: Paper
title: "Multi-Threshold Operators for Non-Monotonic, Fine-Granular Quantized Activations"
description: "Paderborn — 把量化激活（含 SiLU 等非单调函数）与浮点 scale/bias 统一折叠成带方向的多阈值比较，ONNX 代数规则自动转换进 FINN；U55C 上非单调直实现仅多几百 LUT，图级分解最高 1.5×；细粒度阈值直实现最高 58×"
tags:
- accelerator
- fpga
- nonlinear
- activation
- quantization
- compiler
- dataflow
- hardware
created: 2026-10-19
updated: 2026-10-19
timestamp: '2026-10-19T00:00:00Z'
paper_author: [Christoph Berganski, Felix Jentzsch, Marco Platzner]
year: 2026
arxiv: '2610.21825'
sources:
  - raw/papers/Multi_Threshold_NonMonotonic_Activations_FINN_2026.pdf
  - raw/papers/multi-threshold-non-monotonic-activations-finn.md
---

# 多阈值算子：非单调、细粒度量化激活的编译与硬件

## 一句话结论
低比特量化下，激活与「层尾」逐元素链（归一化、激活、量化、浮点 scale）可以精确地折叠成一组阈值比较：输出等级 = 输入越过了几个阈值。本文把这套表示从单调递增函数扩展到 SiLU 这类非单调函数和多维细粒度参数，并做成 ONNX 代数改写，自动接进 FINN 的数据流 FPGA 生成流程。

## 动机
- 权重与 MAC 压到很低比特后，激活/层尾成为硬件瓶颈；浮点 scale 和细粒度量化又是保精度所需。
- FINN 原有多阈值只支持单调递增函数和预定义组合（量化 identity、ReLU），粒度只到最后一维；SIRA 放宽了约束，但依赖昂贵的编译期子图仿真。

## 方案
1. **形式化**：多阈值函数 = 偏置 + 尺度 × Σ 步向权 δᵢ·[x ≥ Θᵢ]；δᵢ∈{−1,+1} 表示升/降台阶。除量化误差外不引入额外近似。
2. **非单调**：对每段单调分支求反函数取阈值；下降分支翻转比较方向并用 Ulp 修正。SiLU 反函数用 Lambert W 的主支/次支，最小点 x≈**−1.28**、y≈**−0.28**。
3. **细粒度**：阈值张量形状是输入形状的子集再加一维 N，地址逻辑按广播取阈值；另给「图级分解」路线：拆成现有 per-channel 阈值 + 逐元素加偏置。
4. **编译器**：代数规则沿层尾函数组合自动折叠（半自动：原语手写、组合自动），代替 SIRA 的子图搜索。
5. **QAT 展望**：前向保持硬台阶，反向用 sigmoid 软化 + STE 使阈值可学。

## 效果（论文数字；Vivado 2024.2，Alveo U55C @100 MHz，只用 LUT，PE=4）
- 非单调 vs 单调：直接硬件实现只多**至多几百 LUT**；图级分解总 LUT 最高 **1.5×**（其中多阈值 1.6×、数据流开销 3.4×）。
- 细粒度：per-tensor/per-channel 两条路线无差别；高比特 3 维细粒度时图级分解最坏 **1.9×**，直接实现约 **58×**（接近参数量 64× 的朴素增长）；β=4 时差距只约 **2.2×**。
- 对比 hls4ml（输入均匀切段查表、无算子融合）：简单函数上 hls4ml 资源更少，但少比特时量化误差更大；多阈值把区间分给函数陡峭处，配合 streamlining 可把整条量化激活数据通路压到几百 LUT。
- QAT：LeNet/MNIST 基线约 99%，允许 2 个百分点损失时可量化到 **4 级（约 2.32 bit）**，学习阈值与手选激活相当。

## 与 wiki 的关系
- [核内非线性运算加速](/concepts/in-core-nonlinear-operator-acceleration.md) — 「比较器阵列」路线：量化后非线性=查阈值
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md)、[FP4 QAT](/concepts/fp4-qat.md) — 低比特格式让激活成为新瓶颈
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — FINN 属层级流水的数据流加速器，层尾单元按层专门化

## 开放问题
- 实验以 LUT 资源为主，没有给端到端模型的时延/吞吐；评测网络为 LeNet 级别，离 LLM 的 SiLU/GELU 规模尚远。
- 细粒度直接实现随参数量线性涨，高比特时需显式存储分区（作者指出 β=4 时综合工具有自动优化迹象）。
- 阈值数随比特数指数增长，>8 bit 激活时与分段多项式/查表的交叉点未量化。

# Citations
- Berganski, Jentzsch, Platzner, "Compiling Multi-Threshold Operators for Quantized Non-Monotonic and Fine-Granular Activations in Custom-Tailored DNN Accelerators", arXiv:2610.21825. [raw](/raw/papers/multi-threshold-non-monotonic-activations-finn.md) · [PDF](/raw/papers/Multi_Threshold_NonMonotonic_Activations_FINN_2026.pdf)
