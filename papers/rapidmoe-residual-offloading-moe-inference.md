---
type: Paper
title: "RapidMoE: Adaptive Residual Offloading for Large-Scale MoE Inference"
description: "清华 EuroSys'27 — CPU–GPU MoE 卸载从专家粒度改为比特粒度（低比特 W^Q@GPU + 残差 W^R@CPU）；decode 最高 3.5×、prefill 最高 2.1× vs SOTA 卸载系统；DRAM 峰值 240 GB vs KTransformers 385 GB"
tags:
- architecture
- llm
- moe
- inference
- decode
- prefill
- quantization
- memory
- cpu
- gpu
- serving
- throughput
created: 2026-10-05
updated: 2026-10-05
timestamp: '2026-10-05T00:00:00Z'
paper_author: [Wenxun Wang, Likai Ma, Zongle Huang, Chen Tang, Yongpan Liu]
year: 2026
arxiv: '2610.01265'
venue: EuroSys 2027
sources:
  - raw/papers/RapidMoE_Residual_Offloading_MoE_Inference_2026.pdf
  - raw/papers/rapidmoe-residual-offloading-moe-inference.md
---

# RapidMoE：比特级残差卸载

## 一句话结论

工作站（大 DRAM + 少量 GPU）跑 DeepSeek-671B 级 MoE 时，专家级卸载要么卡 PCIe、要么压在 CPU 上。RapidMoE 利用 **Cross-Asymmetry**（路由负载倾斜 ↔ 硬件算力/容量不对称），把专家拆成 **低比特 W^Q（放 GPU）+ 残差 W^R（放 CPU）**：非关键专家只用 W^Q 在 GPU 算，少数关键专家由 CPU 用 W^R 补精度。相对 SOTA 卸载系统 decode 最高 **3.5×**、prefill 最高 **2.1×**。

## 动机

- DeepSeek-V3 需 >700 GB，GPU 显存远不够，必须卸载到 host DRAM。
- GPU-centric（缓存部分专家 + PCIe 拉缺失）受 PCIe 带宽限制；CPU-centric（缺失专家在 CPU 算）受 CPU 算力限制。
- 推理型模型输出更长（文中 R1 在 MATH-500 平均 9363 token），decode 主导端到端延迟。

## 方案

1. **RESplit 表示**：W = W^Q + W^R，紧凑且解耦存储，避免冗余副本。
2. **Split 路由**：top-k 中前 r 个关键专家用 W^Q+W^R；其余 k−r 仅 W^Q。
3. **RESplit 并行**：GPU 承担高 FLOP 的 W^Q 计算；CPU 只精修少数关键专家。
4. **UMIA**：统一局部/空间/时间重要性，运行时调关键集合 r，守住精度–延迟 Pareto。
5. 平台：P1 = A800-80G + 512 GB DDR4；P2 = RTX 4090 + 512 GB DDR4-3200（PCIe）。基线 KTransformers、MoE-APEX、HybriMoE、llama.cpp。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| decode vs SOTA 卸载系统 | 最高 **3.5×**（文中 vs KTransformers 平均：R1 **3.5×** / V3 **2.8×** / Qwen3 **2.1×**） |
| prefill vs SOTA | 最高 **2.1×** |
| P2（4090）平台 | 最高 **2.9×** |
| prefill 吞吐（DeepSeek-V3） | **138.9 tokens/s**；平均约 **2×** 于基线（增益小于 decode） |
| DeepSeek-V3 @P1 峰值 DRAM（HBM 均 ~149 GB） | **240 GB** vs KTransformers **385 GB** / MoE-APEX **471 GB** |

## 与 wiki 的关系

- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — CPU+GPU 异构上的 MoE 卸载新范式
- [ThunderEP](/papers/thunderep-pcie-consumer-gpu-moe.md) — 同为消费卡/PCIe 落点；ThunderEP 攻 EP 通信，RapidMoE 攻权重卸载
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 低比特基 + 残差的精度分层
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — HBM/DRAM 分层放置

## 开放问题

- 高并发（文中定位 <10 并发）下 CPU 精修是否成瓶颈？
- 与 HBF/CXL 等新内存层组合时 W^R 的落点。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.01265) — Wang et al., arXiv:2610.01265（EuroSys 2027）
[2] [raw stub](raw/papers/rapidmoe-residual-offloading-moe-inference.md)
