---
type: Paper
title: "When Does Heterogeneity Pay Off? Understanding GPU–WSE System Complementarity"
description: "Stevens/Argonne — WSE-3+A100 上 DP/PP/PD 互补边界；DP 两阈值三区制、标准 PP 难超单平台、架构感知 PP 可赢 WSE-only（7B/13B/35B）；模型中位误差 DP 6.8%/PD 8.2%"
tags:
- inference
- gpu
- wse
- cerebras
- llm
- disaggregated-inference
- prefill
- decode
- latency
- throughput
- parallelism
created: 2026-11-02
updated: 2026-11-02
timestamp: '2026-11-02T00:00:00Z'
paper_author: [Ziyu Hu, Zhijing Ye, Jiamin Wang, Zhiqing Zhong, Zhendong Mi, Shaoyi Huang, Weijian Zheng, Rajkumar Kettimuthu, Xiaodong Yu]
year: 2026
venue: arXiv
arxiv: '2610.39222'
sources:
  - raw/papers/GPU_WSE_Heterogeneity_Complementarity_2026.pdf
  - raw/papers/gpu-wse-heterogeneity-complementarity.md
---

# GPU–WSE 异构何时划算：互补性刻画

## 一句话结论
GPU 与 WSE 在算力/内存/通信组织上差异大，互补与开销并存。本文用分层基准 + 解析模型，在 Cerebras **WSE-3** 与 **A100**（SimAI）上扫 DP / PP / PD：DP 呈**两阈值三区制**，批量足够时 hybrid 逼近聚合上界；**标准统一微批 PP 均未超过单平台**；允许跨平台不同微批的架构感知 PP 可让 **7B/13B/35B** 超过 WSE-only，但仍低于理论界；PD 上 GPU 更擅 prefill，WSE decode 维持**微秒级**步进而 GPU 随上下文升至**数十–数百毫秒**；模型中位预测误差 DP **6.8%** / PD **8.2%**。

## 动机
- 异构加速器入统一系统成新范式；AWS–Cerebras 亦有 Trainium+WSE 集成意向，但何时把架构差变成端到端增益仍不清。
- 需要可复现的分层刻画（应用 / 系统 / 硬件）与能指示瓶颈边界的解析模型。

## 方案
1. **分层基准**：DP、BSP 风格异构 PP、任务级 PD 解耦；测量 ALCF 上 WSE-3 与 DGX A100，系统仿真走 SimAI。
2. **DP 区制**：Threshold 1 / 2 划分小负载（异构难赚）、扩展不对称、以及逼近聚合上界的饱和区。
3. **PP**：先扫统一微批异构放置；再做架构感知、允许 GPU/WSE 不同微批并配对多 GPU 管线到单 WSE 管线。
4. **PD + 模型**：按请求形状刻画 prefill/decode 偏好；解析模型拟合 hybrid 吞吐并报告误差分位。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| DP | 两阈值三区制；大批量下 hybrid 逼近聚合上界 |
| 标准 PP | 所测异构配置**均未超过**单平台 |
| 架构感知 PP | **7B / 13B / 35B** 吞吐可高于 WSE-only；仍低于理论上界 |
| PD decode 延迟形态 | WSE 单步约**数十 µs**、跨长度较稳；GPU 随上下文从数十升至**数百 ms** |
| 模型中位误差 | DP **6.8%**（P90 13.4%）；PD **8.2%**（P90 16.4%） |

## 与 wiki 的关系
- [Cerebras WSE](/entities/cerebras-wse.md) — WSE-3 侧 SRAM/数据流与 A100 层次内存对照
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 把互补从「阶段分硬件」推进到 **何时划算** 的区制与阈值
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — PD 解耦作为异构任务切分实例
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — GPU prefill vs WSE decode 的阶段资源分歧定量化
- [WaferLLM System](/concepts/waferllm-system.md) — WSE 上 LLM 执行路径的既有系统视角

## 开放问题
- 实验为两套同构系统组合仿真/测量，跨域通信栈与真实共机架部署仍有抽象。
- 动态负载下 work stealing 与最优 GPU/WSE 配比的在线控制未做成闭环系统。

# Citations
- [arXiv:2610.39222](https://arxiv.org/abs/2610.39222) — Hu et al., Stevens / Argonne, 2026
- [raw stub](/raw/papers/gpu-wse-heterogeneity-complementarity.md)
