---
type: Paper
title: "Workload-Static Optical Circuit Switching for Scalable LLM Inference Decode"
description: "Salience Labs/NVIDIA/Heidelberg — 部署期一次配电路的 OCS decode；576 加速器 / 5T MoE / 5M 上下文；all-OCS vs 4:1 EPS 交互性最高 +65%、能效最高 +119%"
tags:
- inference
- decode
- ocs
- optical
- photonic
- scale-up
- fabric
- moe
- serving
- collective
- energy
- llm
- networking
created: 2026-11-06
updated: 2026-11-06
timestamp: '2026-11-06T00:00:00Z'
paper_author: [Maximilian Thürmer, Nicolas Scotto di Perto, Eloise Stein, Natanijel Vasic, Mikaeil Bagherli, Zhenguo Wu, Benjamin Klenk, Holger Fröning, Johannes Feldmann]
year: 2026
venue: arXiv preprint
arxiv: '2611.05104'
sources:
  - raw/papers/Workload_Static_OCS_LLM_Inference_Decode_2026.pdf
  - raw/papers/workload-static-ocs-llm-inference-decode.md
---

# Workload-Static OCS：面向 LLM Decode 的部署期电路

## 一句话结论
给定模型部署与并行度后，decode 的通信结构固定。本文提出 **workload-static OCS**：电路在部署时配置一次，并与模型并行、拓扑感知集体共设计；用 GXNET 图仿真 + 硬件标定的分析/flit 模型评估。576 加速器 scale-up、5T MoE、最长 5M token 上下文下，**all-OCS** 相对 **4:1 过订阅 EPS**，交互性最高 **+65%**、系统能效最高 **+119%**（Megatron 5T 交互性最高 **+52%** / 能效 **+102%**；GPT-OSS-5.3-like 可达 **65%/119%**）。

## 动机
- Decode 反复打细粒度集体，往返时延直接压低每用户 token 率（interactivity）。
- 现有 scale-up 仍以训练向的电子分组交换为主；跨机架扩域抬高路径与跳数。
- 训练侧 OCS（如 Flux）常在 iteration 内重配；decode 更吃「一次配好、整段服务复用」的静态电路。

## 方案
1. **Workload-static 电路**：按部署/并行度配 OCS，服务期内不在 token 环内重配。
2. **共设计**：物理拓扑、路由、集体日程、设备放置与模型并行一起定；用空闲端口换更少通信相位或更高有效带宽。
3. **GXNET**：图工作负载仿真器，耦合分析模型与 flit 级网络模型，接地硬件测量。
4. **对照**：all-OCS vs 过订阅 EPS；扫 Megatron 5T 与 GPT-OSS 族、上下文至 5M。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 规模 | **576** 加速器；**5T** MoE；上下文至 **5M** tokens |
| all-OCS vs 4:1 EPS：交互性 / 能效 | 最高 **+65%** / **+119%** |
| Megatron 5T MoE | 交互性最高 **+52%**，能效最高 **+102%** |
| GPT-OSS-5.3-like | 交互性 / 能效最高 **65% / 119%** |

## 与 wiki 的关系
- [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — pod 级 OCS「拓扑即软件」；本文把旋钮收到 **推理 decode 部署期静态电路**
- [Flux](/papers/flux-ocs-scheduling-llm-training.md) — 训练 iteration 内 OCS MILP 重配；本文强调 decode 侧 **不在生成环内重配**
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 拓扑感知集体日程与并行度共设计
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 大规模 decode 域与 PD/并行部署边界

## 开放问题
- 结果主要来自 GXNET 仿真；与生产 EPS/OCS 实测闭环仍待补。
- 微批等会改变通信形状时，静态电路的重配触发策略未展开。

# Citations
- [arXiv:2611.05104](https://arxiv.org/abs/2611.05104) — Thürmer et al., Salience Labs / NVIDIA / Heidelberg University
- [raw stub](/raw/papers/workload-static-ocs-llm-inference-decode.md)
