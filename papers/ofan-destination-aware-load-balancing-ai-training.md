---
type: Paper
title: "Ofan: Optimal Load Balancing for AI Training"
description: "UC Berkeley/Technion/NVIDIA — 胖树上目的地无关的包喷洒会出现 Θ(√m) 排队；交换机目的地感知负载均衡 Ofan 做到 O(1)，P4/Tofino 可实现；Llama-3 405B FSDP2 CCT 膨胀降 16–39×"
tags:
- routing
- switch
- congestion-control
- scale-out
- collective
- training
- topology
- nvidia
created: 2026-10-12
updated: 2026-10-12
timestamp: '2026-10-12T00:00:00Z'
paper_author: [Sarah McClure, Evyatar Cohen, Jakob Krebs, Alexander Shpiner, Mark Silberstein, Scott Shenker, Sylvia Ratnasamy, Isaac Keslassy]
year: 2026
arxiv: '2610.07230'
venue: arXiv preprint (cs.NI/cs.DC)
sources:
  - raw/papers/Ofan_Destination_Aware_Load_Balancing_AI_Training_2026.pdf
  - raw/papers/ofan-destination-aware-load-balancing-ai-training.md
---

# Ofan：AI 训练的目的地感知交换机负载均衡

## 一句话结论
胖树上包一旦选定上行路径，下行到目的地的路径就唯一确定。只看本地拥塞、不看目的地的喷洒（随机/自适应路由、REPS/MRC 等端侧方案、DRILL/Spectrum-X AR 等交换机方案）在上行两级均衡，到下行两级会塌缩。作者证明这类方案对大小 m 的消息排队为 **Θ(√m)**，最终触发拥塞控制降速；Ofan 让交换机按目的地做均衡，排队为 **O(1)**。

## 动机
- AI 集体通信所有源同时满速发送，负载逼近 100%；论文图 1 显示现有喷洒在满载时利用率低于 95%，队列随负载陡增。
- 拥塞控制一旦介入，集体完成时间（CCT）被拉长，训练迭代跟着变慢。

## 方案
- **Ofan**：交换机端目的地感知负载均衡（destination-aware LB），上行选路时考虑包最终下行要走的端口，使下行各级也保持均衡。
- **pOfan**：适配当前交换机 pipe（流水线分片）结构的变体；P4 实现在 Intel Tofino 上，资源占用不大。
- 本文扩展自 Cascadia（arXiv:2507.21372）的第二部分。

## 效果（仅论文数字）
| 指标 | 数字 |
|---|---|
| 排队理论界 | 目的地无关方案 Θ(√m) vs Ofan O(1) |
| Llama-3 405B FSDP2 端到端 | CCT 膨胀相对现有算法降 **16–39×** |
| 硬件 | P4/Tofino 实现，资源开销适中 |

## 与 wiki 的关系
- [Clos / Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 抓住"上行可选、下行唯一"这一结构性质
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 从网络负载均衡角度缩短 CCT
- [RailWave](/papers/railwave-ep-rail-incast-scheduling.md) — 同样处理满速集体流量下的 incast/轨道失衡，RailWave 在端侧排波次，Ofan 在交换机侧

## 局限与开放问题
- 评测以仿真+P4 资源为主，尚无大规模真机部署数据。
- 多租户、链路故障、非胖树（dragonfly、rail-only）下的表现待验证；与 UEC 端侧喷洒如何共存需要协议层设计。

# Citations
- McClure et al., "Ofan: Optimal Load Balancing for AI Training", arXiv:2610.07230, 2026. [raw](/raw/papers/ofan-destination-aware-load-balancing-ai-training.md)
