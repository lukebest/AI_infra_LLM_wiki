---
type: Paper
title: "Tri-Stack-PIM: A Heterogeneous Multi-Die 3D-Integrated PIM Architecture for LLM Inference"
description: "BUPT / 复旦 ICCAD’26 — 顶层 DRAM + 中层 45 nm buffer（PHY/DMA/非线性/UBAR）+ 底层 7 nm SIMD MAC；相对边缘 GPU / AttAcc / H2-LLM 几何均值 4.95× / 2.57× / 1.68×；UBAR 最多收回 in-order 放弃周期的 90%；EDP 相对朴素参数 33–66×"
tags:
- pim
- 3d
- hybrid-bonding
- packaging
- integration
- inference
- accelerator
- memory
- attention
- nonlinear
- microarchitecture
- near-memory-processing
created: 2026-11-12
updated: 2026-11-12
timestamp: '2026-11-12T00:00:00Z'
paper_author: [Shuao Jia, Zichao Ling, Chen Bai, Kang Zhao, Jianwang Zhai]
year: 2026
venue: ICCAD 2026
arxiv: '2611.13644'
sources:
  - raw/papers/Tri_Stack_PIM_3D_LLM_Inference_2026.pdf
  - raw/papers/tri-stack-pim-heterogeneous-3d-llm.md
---

# Tri-Stack-PIM：三层异质 3D PIM，把 PHY 与计算拆到不同 die

## 一句话结论
北邮与复旦在 ICCAD’26 提出 **Tri-Stack-PIM**：顶层 DRAM 只做存储，中层成熟节点 buffer die 承担 host PHY、DMA、近存计算（含 softmax 等非线性）和 UBAR 调度，底层先进节点 base die 专给 SIMD MAC。评测覆盖 MHA / GQA / MQA 与 batch 1–32，几何均值加速相对边缘 GPU 基线 **4.95×**、相对 AttAcc **2.57×**、相对 H2-LLM **1.68×**。UBAR 最多收回 in-order 会放弃的周期的 **90%**；联合架构–数据流探索相对朴素参数选择把 EDP 降 **33–66×**。

## 动机
已有 3D 堆叠 PIM 缓解了片外带宽墙，但仍叠着几件约束：PHY、控制器与 DMA 和算术单元抢先进节点 base die 面积；混合键合的 keep-out 区切割 floorplan，物理设计变难；做在 DRAM 工艺里的计算 tile 逻辑密度低，吞吐封顶；非线性算子若卸载到 host，又把通信瓶颈请回来。Table 1 显示先前设计没有同时关掉这几项。

## 方案
1. **三层混合键合分区**：存储、接口/控制、密集计算分到三张 die。先进节点硅只用来提高计算密度；非线性留在栈内的 buffer die，避免 host 往返。
2. **UBAR 调度器**（Unified Buffer-Aware Ready-based）：在 buffer die 上做硬件乱序微操作调度，用多项优先级函数提高 issue 槽利用率，并在运行时维持跨 die 依赖正确。
3. **联合架构–数据流探索**：搜索 Pareto 配置，避免朴素参数选择。

评测模型为 OPT-6.7B（MHA 32/32）、LLaMA3-8B（GQA 32/8）、PaLM-8B（MQA 16/1）；batch {1,4,8,16,32}；长度对 (128,64)、(512,256)、(1024,64)、(1024,16)。Base die 用 ASAP7，0.5–1.5 GHz，16–256 MACs/tile（73.1–4614.5 µm²/block，0.15–41.2 fJ/MAC）。Buffer die 上的 SRE 用 NanGate 45 nm，0.1–1.0 GHz，**0.47 mm²**，**1.1–9.5 pJ/softmax op**。HB 链路 **0.88 pJ/bit**（沿用 H2-LLM 模型）。周期精确仿真扩展 Ramulator 2。

对照有三个：GPU-Only 是代表性**边缘 GPU** + 4 通道 LPDDR5X **30.7 GB/s**（不是数据中心 GPU）；AttAcc；H2-LLM。正文指出 H2-LLM 把 softmax 放到 host，受 host-device 带宽束缚，且 base die 只有 32 条 SIMD 车道；Tri-Stack-PIM 在 64 车道、MQA 计算受限时会落后 AttAcc，把 base die 扩到 256 车道后超过所有对照。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 几何均值加速（三种 attention × 全部 batch） | 相对 GPU-Only **4.95×**，AttAcc **2.57×**，H2-LLM **1.68×** | 摘要 / 贡献列表 |
| UBAR 回收的调度空档 | 最多收回 in-order 会放弃的周期的 **90%** | 摘要 |
| EDP vs 朴素参数选择 | **33–66×** | 摘要 |
| PHY 晶圆成本 | 7 nm base die 晶圆 **$9,346**，45 nm buffer die **$2,000**；仅 PHY 一项单位晶圆成本降 **4.7×** | §评估 / 成本讨论 |
| 热仿真峰值 | DRAM / buffer / base 约 **63.74 / 63.75 / 62.63 °C** | 热分析图 |

## 与 wiki 的关系
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 用异质三层混合键合把 PHY/控制从先进节点计算 die 上搬走
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — softmax 等非 GEMM 留在 buffer die，避免 host 往返；与昨日 [RVV vs CGRA](/papers/rvv-cgra-nonlinear-functions-soc.md) 同一问题、不同封装层级
- [CAMP](/papers/camp-3d-imc-mapping-placement.md) — 3D-IMC 的权重映射与层间互斥；本文是逻辑/DRAM 混合键合 PIM 的微架构与调度
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把权重与 KV 的带宽路径收进 3D 栈

## 开放问题
- GPU 对照是边缘 GPU + LPDDR5X 30.7 GB/s，不宜直接读成对 H100/H200/GB300 的加速比。
- 模型停在 6.7B–8B，结果来自 ASAP7 / NanGate 45 nm 综合与 Ramulator 2 扩展仿真，不是硅上端到端 LLM 服务。
- 64 车道、MQA 计算受限时会落后 AttAcc；优势依赖于把 base die 扩到 256 车道。
- 成本模型未计入把 PHY IP 迁到 45 nm 的 NRE 与资格认证。

# Citations
- [arXiv:2611.13644](https://arxiv.org/abs/2611.13644) — Jia, Ling, Bai, Zhao, Zhai（BUPT / Fudan）；ICCAD ’26
- [raw stub](/raw/papers/tri-stack-pim-heterogeneous-3d-llm.md)
- [PDF](/raw/papers/Tri_Stack_PIM_3D_LLM_Inference_2026.pdf)
