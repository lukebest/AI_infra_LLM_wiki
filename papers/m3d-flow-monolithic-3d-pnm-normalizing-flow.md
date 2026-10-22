---
type: Paper
title: "M3D-FLOW: A Monolithic 3-D-Stackable Processing-Near-DRAM Architecture for Generative Normalizing Flow Applications"
description: "肯塔基大学/科罗拉多州立 — Cu-Cu 混合键合逻辑 die + 单片 3D 可堆叠 DRAM；尾数乘法走随机计算（面积 13× 小、功耗 46× 低）、指数与加法留二进制；非线性全部 LUT 化在 PE 内完成；比已有 PNM 至少 6.6× 性能、3× 能效（CASES'26 / TCAD）"
tags:
- near-memory-processing
- pim
- 3d
- monolithic
- hybrid-bonding
- cu-cu
- dram
- stochastic-computing
- nonlinear
- accelerator
- numeric-format
created: 2026-10-22
updated: 2026-10-22
timestamp: '2026-10-22T00:00:00Z'
paper_author: [Bipin Thapa Magar, Ishan Thakkar, Sudeep Pasricha]
year: 2026
arxiv: '2610.27371'
sources:
  - raw/papers/M3D_FLOW_Monolithic_3D_PNM_Normalizing_Flow_2026.pdf
  - raw/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md
---

# M3D-FLOW：单片 3D DRAM 近存 + 随机计算乘法器

## 一句话结论
在单片 3D 可堆叠 DRAM（M3D DRAM）下方用 Cu-Cu 混合键合挂逻辑 die，每个 bank 一个 PE；乘法的尾数部分用随机计算（一根 AND 门做乘法），指数与加法保持二进制，借此在逻辑 die 的热预算内塞下更多 MAC。目标负载是归一化流（NF）生成模型，但「随机-二进制混合 FP 乘法器 + LUT 非线性引擎 + 按 DRAM 层延迟分级放数据」三件事对 LLM 近存设计同样有参考价值。

## 动机
- NF 由大量顺序、可逆的 flow 步组成，GPU/TPU 上每步是独立 kernel，受访存限制。
- 已有 PNM 受计算密度、带宽扩展和热约束限制；M3D DRAM 用混合键合（约 1 µm 节距，比 HBM TSV 细约 5×）提供更高内部带宽，但逻辑 die 的散热限制了能放多少 MAC。

## 方案
1. **分层 DRAM 放置**：M3D DRAM 1024 层按访问延迟分 8 个 tier，关键数据放低延迟层。
2. **混合二进制-随机 FP 乘法器（Multiplier Engine）**：尾数转成随机比特流相乘，指数二进制相加；随机尾数乘法器比二进制面积小 **13×**、功耗低 **46×**；随机加法器反而大 **2.97×**、耗电 **1.46×**，所以加法交给二进制 Vector Adder Engine。
3. **Non-Linear Engine（NLE）**：exp、GeLU、ln、倒数做成单周期 LUT；ReLU 用符号位选择器；max 用归约树；softmax = exp LUT → 归约求和 → 倒数 LUT → 缩放，全部在 NLE 内完成，不回流到乘法/加法引擎。
4. **流水执行**：顺序的 flow 步映射到动态划分的 PE 组，SRAM 双缓冲隐藏 tRCD/tRP。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 性能 / 能效 | 比已有 PNM 加速器至少 **6.6×** 性能、**3×** 能效（对比含 2DRAM-PNM、PNM-DDR、Stratum、NeuPIMs，另含 EPYC CPU、A100、TPUv7） |
| 精度 | BPD 比 bfloat16 高 **2.2%**、比 FP32 高 **4.1%** |
| 比特流长度旋钮 | 256→2,048 bit 执行时间变为 **3.3×**；512/1,024 bit 为 1.2×/1.7×；温度基本不变 |
| PE 功耗分布 | 乘法引擎 61%、加法引擎 30%，其余为 NLE/SRAM 等 |
| 热 | 满载仍在安全 DRAM 温度内（45 °C 环境建模） |

## 与 wiki 的关系
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — LUT 化 exp/倒数拼 softmax 的又一例
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 单片 3D DRAM + Cu-Cu 混合键合
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — bank 下挂 PE 的 DRAM-on-logic 组织
- [Numeric Formats](/concepts/numeric-formats-ai-hardware.md) — 随机比特流本质上是一种以延迟换面积的数值表示
- [TileDRAM](/papers/tiledram-tile-to-dram-layouts-3d-dram-gpgpu.md) — 同样利用 3D DRAM 的物理组织做数据放置

## 开放问题
- 负载是 NF 图像生成，论文举的大 NF 模型 TarFlow 参数量超过 3 亿，仍远小于 LLM；随机尾数乘法在 LLM 低比特权重下的误差累积尚未评估。
- 摘要中的 6.6×/3× 为相对已有 PNM 的下限，各基线的具体倍数需看原文图表逐项核对。
- LUT 非线性的精度/面积在更大位宽（FP16/BF16 全域 exp）下的代价论文只给了整体 BPD。

# Citations
- [arXiv:2610.27371](https://arxiv.org/abs/2610.27371) — Magar, Thakkar, Pasricha, CASES 2026 / IEEE TCAD
- [raw/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md](/raw/papers/m3d-flow-monolithic-3d-pnm-normalizing-flow.md)
