---
type: Paper
title: "MX-Like Tensor Core for LLM Inference with NPU Integration"
description: "KU Leuven 等 — 系统扫 MX/NVFP4 类块缩放格式（8 bit 缩放族 × 非对称 W/A 精度，126 种配置）并在 SNAX NPU 上 28 nm 综合；缩放格式只在 FP4 下要紧，推荐 UE5M3：比 NVFP4-like 降 25.3% 困惑度劣化，仅 +0.06% 面积、+0.49% 功耗"
tags:
- quantization
- numeric-format
- npu
- edge
- accelerator
- design-space-exploration
- inference
- llm
- chip-design
created: 2026-10-21
updated: 2026-10-21
timestamp: '2026-10-21T00:00:00Z'
paper_author: [Zijun Zhao, Ruichu Ao, Stef Cuyckens, Marian Verhelst, Chao Fang]
year: 2026
arxiv: '2610.26083'
sources:
  - raw/papers/MX_Like_Tensor_Core_NPU_CoDesign_2026.pdf
  - raw/papers/mx-like-tensor-core-npu-codesign.md
---

# MX-like 张量核：块缩放格式的软硬协同设计空间

## 一句话结论
块缩放格式里「共享缩放因子用什么格式」只在 FP4 激进量化时才影响精度；6 bit 以上直接用 UE8M0（纯指数缩放）最省硅。FP4 场景推荐 UE5M3 缩放，比 NVFP4 的 UE4M3 精度明显更好、硬件代价几乎为零。

## 动机
- OCP MX 与 NVFP4 已是 LLM 推理主流格式，但缩放格式 × 权重格式 × 激活格式构成的空间没人系统扫过。
- 已有工作要么只算精度、硬件代价粗估，要么只为单一格式做硅；边缘 NPU 的精度-硅联合 Pareto 前沿空白。

## 方案
1. 定义完整的 8 bit 缩放格式族（UE8M0、UE5M3、UE4M4、UE4M3 等；NVFP4 的 UE4M3 浪费符号位，这一族把每一位分给指数或尾数），叠加 A6W6/A4W4/A6W4/A8W4 等非对称精度。
2. 按格式特化的 MAC 数据通路模板（对齐乘积和、缩放乘法器、移位、累加、归一化），保证跨格式硬件代价可比。
3. 自动协同设计流程接入开源 SNAX NPU（Snitch RISC-V 核 + DMA + 多 bank scratchpad + 张量核），每个点都生成、验证、综合。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 实验条件 | TSMC 28 nm、400 MHz、0.8 V；4×16 PE 阵列；Qwen2.5-3B、Qwen3-1.7B、Llama-3.2-1B、Gemma-3-1B；WikiText-2 与 C4 |
| 面积构成 | 累加器占 MAC 面积 **39–66%**；分数缩放的乘法器最高 **36%** |
| 高精度区（A6W6 以上） | UE8M0 为 Pareto 最优；分数缩放不提精度却多 **+22%** 系统功耗、**+17%** 面积 |
| FP4 区 | UE4M4 缩放把平均 ΔPPL 从 **45.0%**（UE8M0）降到 **17.9%**；同样开销在 FP4 下只有 **+4.6%** 面积、**+20.8%** 功耗 |
| 推荐点 UE5M3 | 相对 NVFP4-like（无 per-tensor scaling）困惑度劣化降 **25.3%**，面积 **+0.06%**、功耗 **+0.49%** |
| 系统级 | 126 种配置中 60 种在面积和功耗上都更省 |

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 补上 MX/NVFP4 缩放格式的硅代价
- [FP4 QAT](/concepts/fp4-qat.md) — 训练侧 FP4；本文给推理侧 FP4 缩放格式选择
- [DSA Processor Design Trade-offs](/concepts/dsa-processor-design-tradeoffs.md) — 累加器主导面积这一结论对张量核设计通用
- [DynaCore](/papers/dynacore-shape-adaptive-disaggregated-quantization.md) — 另一条量化 + 硬件协同路线

## 开放问题
- 只测 1–3B 小模型与困惑度；大模型、下游任务与长上下文下的结论未验证。
- 不含 per-tensor scaling 的 NVFP4-like 基线与真实 NVFP4 有差距，对比数据需按此口径理解。
- 28 nm 边缘 NPU 结论能否平移到数据中心张量核（面积占比不同）未讨论。

# Citations
- [arXiv:2610.26083](https://arxiv.org/abs/2610.26083) — Zhao et al., 2026
