---
type: Paper
title: "A Shape-Adaptive Architecture with Disaggregated Quantization for Efficient LLM Serving"
description: "Duke — DynaCore：脉动阵列计算块三维重塑（32×32→1×1024 + Split-K）+ prefill W8A8 / decode W4A16 分离量化；TTFT vs FIGLUT/Planaria 3.50×/2.97×，TPOT 36.55×/8.02×"
tags:
- accelerator
- dataflow
- quantization
- prefill
- decode
- serving
- inference
- llm
created: 2026-10-08
updated: 2026-10-08
timestamp: '2026-10-08T00:00:00Z'
paper_author: [Cong Guo, Chiyue Wei, Bowen Duan, Haoxuan Shan, Benjamin F. Morris III, Yintao He, Hai Li, Yiran Chen]
year: 2026
arxiv: '2610.07443'
venue: arXiv preprint (cs.AR)
sources:
  - raw/papers/DynaCore_Shape_Adaptive_Disaggregated_Quantization_2026.pdf
  - raw/papers/dynacore-shape-adaptive-disaggregated-quantization.md
---

# DynaCore：形状自适应脉动阵列 + 分离量化

## 一句话结论

脉动阵列一次执行的计算块（论文称 MEU，最小有效单元）同时有 m、n、k 三个维度。decode 的 GEMV（M=1）在 S×S 输出驻留阵列上只用到 1/S 的 PE；DynaCore 把 MEU 在三个维度上都重塑：空间上**非对称**地拉宽阵列（32×32 可平铺到 1×1024，提高权重供给而不动输入路径），时间上用 **Split-K** 把规约维映射到阵列、用阵列已有互连折叠部分和；再配 **prefill 用双侧量化、decode 用纯权重量化**，由运行时逐批选 MEU。

## 动机

- prefill 是大 GEMM（算力受限），decode 是小 GEMV（访存受限）；continuous batching 与 PD 分离让批形状动态变化、阶段分开。
- 现有量化加速器（Olive、FIGNA、FIGLUT 等）固定 MEU，面向 prefill；可重构阵列 Planaria / SARA 只做对称切分，最小到 32×32 / 4×4，batch-1 GEMV 仍大量空闲。

## 方案

- **空间重塑**：S×S 核可实现 S×S、S/2×2S…1×S² 多种形状（32×32 核六种），同 PE 数。
- **Split-K**：阵列沿 K 分 t 组，每组是普通 m×n 输出驻留子阵列，部分和经现有互连折叠，排空时输出已规约结果。约束 m·n·t = S²。
- **分离量化**：prefill W8A8，decode W4A16，KV4；内积式混合精度数据通路沿 K 打包操作数，输出宽度不随精度变化（对比扩展输出 tile 的方案需 4 个累加器、面积超 2×）。
- **运行时**：host 侧调度支持 continuous batching，按批选 MEU，不规则 M 分解成多块填满阵列。
- 实现：16×(32×32) 输出驻留，TSMC 28 nm、500 MHz、8 MB 缓冲、4 TB/s DRAM；Design Compiler 综合 + CACTI 7.0 + 周期级模拟器，ShareGPT / Dolly 服务 trace。

## 效果（仅论文数字）

| 对比 | 数字 |
|------|------|
| vs FIGLUT（量化加速器） | TTFT **3.50×**，TPOT **36.55×** |
| vs Planaria（可重构） | TTFT **2.97×**，TPOT **8.02×** |
| 端到端延迟 | vs 带 DQ 的普通脉动 **23.07×**；vs BitFusion / FIGLUT **23.81× / 14.13×**；vs Planaria / SARA **7.57× / 2.48×** |
| decode 阶段 | vs Planaria / SARA **23.03× / 3.48×** |
| 能效 | vs BitFusion / 脉动 / FIGLUT / Planaria / SARA **4.96× / 13.76× / 7.39× / 5.71× / 2.86×** |
| 面积 / 片上功耗 | **76.44 mm² / 115.74 W**（Planaria 70.98 mm² / 133.37 W；带 DQ 脉动 65.09 mm² / 111.55 W） |
| 精度 | Llama3.1-8B-Instruct 上分离量化相对 FP16 平均掉 **0.07%** |

## 与 wiki 的关系

- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 把"可重构脉动"从对称切分推进到非对称 + 规约维映射
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — 同一硬件按阶段换形状与量化，而不是拆成两类芯片
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — M=1 时空间利用率塌到 1/S 的定量说明
- [SPECTRA](/papers/spectra-speculative-decoding-tiled.md) — 同样在一个 tile 引擎上切 systolic/vector 形态

## 局限与开放问题

- 全部基于 28 nm 综合 + 模拟；基线也统一用其模型重建，不是真实芯片对比。TPOT 36.55× 主要来自 FIGLUT 等固定大阵列在 batch-1 下的空闲，而非绝对带宽优势。
- 4 TB/s 带宽配 28 nm 计算阵列的组合偏理想化；在 HBM 受限的真实 decode 下，形状重塑能否兑现取决于权重带宽是否真成瓶颈。
- 开放问题：PD 分离下 prefill/decode 已在不同机器上，单芯片双形态与"两类专用芯片"相比，面积成本谁更划算？

# Citations

[1] [arXiv:2610.07443](https://arxiv.org/abs/2610.07443) — Guo et al., DynaCore
[2] [raw stub](raw/papers/dynacore-shape-adaptive-disaggregated-quantization.md)
