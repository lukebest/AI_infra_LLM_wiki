---
type: Paper
title: "FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators"
description: UVA/SJTU — Posit + bit-serial 脉动可调分数精度；相对 BitMoD 最高 1.8× 吞吐/1.2× 能，相对 OliVe 1.5×/2.0×（16 nm 综合）
tags:
- llm
- accelerator
- quantization
- inference
- throughput
- dataflow
- transformer
- inference-system
timestamp: '2026-09-08T00:00:00Z'
created: 2026-09-08
updated: 2026-09-08
sources:
- raw/papers/FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf
- raw/papers/flexposit-tunable-fractional-precision-llm.md
---

# FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators

**Authors:** Yimin Gao, Liangtao Dai, Jun Yin, Xinfei Guo, Mircea Stan
**Affiliation:** University of Virginia; Shanghai Jiao Tong University
**arXiv:** [2609.04724](https://arxiv.org/abs/2609.04724)（2026-09-04，cs.AR）
**Venue:** ASP-DAC 2027（预印本）
**PDF:** [raw/papers/FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf](raw/papers/FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf)

把 LLM 量化的「分数位宽」做成可硬件调的时间参数：Posit 锥形精度 + channel-window 敏感度 MPQ + **bit-serial 脉动阵列**（GPCU 控精度窗）。对照 [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md)：仍是脉动数据流，但精度在 4–8 bit 连续可调，追求 group-wise 精度与 channel-wise 规整的折中。

## 动机

- Group-wise 准但 per-PE rescale 面积大（文中 32×32 阵列 per-PE 缩放可抬核心面积 **>30%**）；channel-wise 规整但低比特易崩。
- 现有加速器多停在离散 4/8-bit 模式，未暴露分数精度。

## 方案

1. **Posit(n,es)** 量化与分布感知标定；敏感度排序升级 channel-window（虚拟精度如 4.1 b = 部分窗升到 5 b）。
2. **架构：** per-column SerialPosit decoder + 统一 PE + GPCU；4-way MAC cluster 缓解 bit-serial。
3. **实现：** Verilog RTL，商业 **16 nm** 综合；iso-area 对比 FP16 / BitMoD / OliVe。

## 效果（仅论文数字）

| 对比 | 结果 |
|------|------|
| vs BitMoD（group） | 最高约 **1.8×** 吞吐、**1.2×** 更低能耗 |
| vs OliVe（channel） | 约 **1.5×** 吞吐、**2.0×** 更低能耗 |
| (B=8, L=8192) vs FP16/BitMoD/OliVe | 加速 **3.4× / 1.6× / 1.2×**；能耗降 **3.5× / 1.2× / 1.8×** |
| PE 面积 | FlexPosit ≈ FP16 的 **0.12×**（118.2 µm²）；iso-area 配 32×16 |

sub-5-bit 权重下接近 FP16 PPL。**综合/仿真**，非流片实测。

## 与 wiki 的关系

- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 脉动/位串行精度轴
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 边缘低比特推理加速器对照
- [Mixed Precision Training](/concepts/mixed-precision-training.md) — 训练侧混合精度对照（本文是推理 PTQ+加速器）
- [CHIPSMORE](/papers/chipsmore-cim-chiplets-llm-inference.md) — 另一条低能耗 LLM 推理硬件（CIM）
- [LEAP](/papers/leap-imc-noc-llm-inference.md) — IMC/NoC 推理对照

## 开放问题

1. 激活也走低比特 / KV cache 量化时，GPCU 时间窗如何与 attention 对齐？
2. 更大模型（70B+）的敏感度剖析成本？
3. 与真实 HBM/NoC 带宽耦合后，iso-area 吞吐优势还剩多少？

# Citations

[1] [raw/papers/FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf](raw/papers/FlexPosit_Tunable_Fractional_Precision_LLM_2026.pdf) — Gao et al., arXiv:2609.04724
[2] [raw/papers/flexposit-tunable-fractional-precision-llm.md](raw/papers/flexposit-tunable-fractional-precision-llm.md) — ingest stub
