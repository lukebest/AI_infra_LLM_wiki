---
type: Paper
title: "MCCL: Measurement-based Collective Communication Library"
description: "EURECOM 等 PACMNET/CoNEXT'26 — 被动测 GPU↔GPU 吞吐 + 暖启动重合成 + 热切换；灰障下相对静态 schedule 训练时间最高 4.99×；热切换 ≈12 ms，开销 <2%"
tags:
- collective
- allreduce
- training
- communication
- distributed
- networking
- llm
- parallelism
created: 2026-10-23
updated: 2026-10-23
timestamp: '2026-10-23T00:00:00Z'
paper_author: [Michele Ferrero, Gabriele Castellano, Paolo Medagliani, Sebastien Martin, Roberto Morabito, Massimo Gallo]
year: 2026
arxiv: '2610.17091'
sources:
  - raw/papers/MCCL_Measurement_Based_Collective_Communication_2026.pdf
  - raw/papers/mccl-measurement-based-collective-communication.md
---

# MCCL：基于测量的集体通信库

## 一句话结论
生产里灰故障会悄悄把链路降速数十分钟到数小时，静态合成的 AllGather/AllToAll schedule 跟着变差。MCCL 把「被动测路径吞吐 → 检测持续退化 → 暖启动重合成 → 热切换」做成闭环，灰障下相对静态 schedule 训练时间最高缩短 **4.99×**，热切换约 **12 ms**。

## 动机
- 厂商 CCL 与 TACCL/TECCL/ForestColl/SyCCL/OptCCL 大多按峰值拓扑开环合成一次；灰故障不告警却把吞吐钉在瓶颈链路上。
- SimAI 小实验：单链路降到 12% 容量时，重优化相对静态最高 **7.1×**。
- 主动探测抢训练带宽；只看交换机计数看不到 PCIe/协议端到端；现有合成器冷启动、对称性假设被灰故障打破。

## 方案
1. **Controller–Executor**：Executor 在 GPU 快路径跑集体并被动采 GPU↔GPU 吞吐；Controller 做 EWMA、割集松弛检测、选择性重合成。
2. **暖启动合成**：AllGather 用 ForestColl-warm（A* 引导复用旧树）；AllToAll 用列生成 + 暖启动（相对冷启动最高 **18.3×** 求解加速）；rounding 间隙 ≤**2.13%**。
3. **热切换**：改编自 MCCS 的 OOB AllGather 对齐版本号与序列号，单 communicator 内切换。
4. 目标集体：AllGather/AllToAll；AllReduce = 静态 ReduceScatter（可吃 SHARP）+ 动态 AllGather。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 测量开销 / 误差 | 饱和点开销 **<2%**；误差 **<1.2%** |
| 热切换 | ≈**12 ms**（合成 13.1 ms + 切换 11.6 ms 量级分解中 OOB 5.74 ms） |
| 原型反应（链路半带宽） | 检测 53.1 ms；总反应 78.2 ms；AllGather algo BW 74.02→44.76→**59.72 GB/s** |
| 离线 SimAI 相对静态 | AllGather 最高 **7.33×**；AllToAll 最高 **7.12×** |
| E2E 训练时间（Llama 405B / DeepSeek 671B） | Fail2 下最高 **2.85×** / **4.99×** vs NCCL 静态 |
| ForestColl-warm 重优化 | Fail1/Fail2 相对冷启动最高 **3.79×** / **4.40×** |

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 从开环合成推进到测量闭环
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上集体能力对照；MCCL 面向跨节点 GPU fabric
- [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — 大规模训练互连语境
- [FastEEP](/papers/fasteep-intra-instance-elastic-ep-moe-serving.md) — 推理侧 EP 成员视图热切换；MCCL 是训练侧 schedule 热切换

## 开放问题
- E2E 大模拟假设「及时故障通知、无 thrashing」；Γ/α 需按集群标定。
- 原型仅 8 GPU / 2 节点；512 GPU 合成仍需数十秒量级（可接受相对小时级灰故障）。
- ReduceScatter 仍走静态路径，未覆盖 in-network 归约的灰故障。

# Citations
- [arXiv:2610.17091](https://arxiv.org/abs/2610.17091) — Ferrero et al., PACMNET/CoNEXT'26
