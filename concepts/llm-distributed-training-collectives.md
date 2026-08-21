---
type: Concept
title: LLM Distributed Training Collectives
description: H&P Ch.6/10 语境下 LLM 训练集体通信：AllReduce/AllGather/All-to-All；Ring vs Tree；DP/TP/PP/EP 配方；通信-计算重叠与 WSE 片上 vs 跨 wafer
tags:
- llm
- training
- allreduce
- collective
- parallelism
- distributed
- noc
- wse
timestamp: '2026-08-21T00:00:00Z'
created: 2026-07-13
updated: 2026-08-21
sources:
- raw/articles/arch-study-30d-day-27.md
- raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf
---

# LLM Distributed Training Collectives（分布式训练与集体通信）

arch-study **并行篇 Day 27**：H&P Ch.6 + Ch.10——当模型装不进单芯片（GPT-3 175B ≫ WSE 44 GB SRAM），**通信成为训练主瓶颈**。经典 MPI 五算法见 [MPI Reduce/AllReduce](/concepts/mpi-reduce-allreduce-algorithms.md)；本页聚焦 **LLM 训练配方与复杂度直觉**。

**Source:** [raw/articles/arch-study-30d-day-27.md](raw/articles/arch-study-30d-day-27.md)

## Collective 原语（训练侧）

| 原语 | 语义 | LLM 用法 |
|------|------|----------|
| **AllReduce** | 每人得全局和 | DP/TP 梯度或 activation 同步 |
| **Reduce** | 仅 root 得和 | 主节点收集 |
| **AllGather** | 每人得拼接全集 | 权重/分片拼回 |
| **Broadcast** | 主节点下发 | 初始化/checkpoint |
| **All-to-All** | 每人与每人交换分片 | MoE token 重排、Attention 重排 |

DP 训练每 step：`forward → backward → AllReduce(grads) → update`。

## Ring AllReduce：为何工程胜出

两阶段，各 **N−1** 步：

1. **Reduce-Scatter**：环上传递并累加，每人最终持有全局和的 **1/N**  
2. **AllGather**：环上传递完整分片，每人持有全集  

| | Ring | Binary Tree | Parameter Server |
|--|------|-------------|------------------|
| 每 worker 传输量 | **≈2D**（与 N 近似无关） | ~D·log₂N | Master **2D**（热点） |
| 步数 | **2(N−1)** | log₂N | O(1) 轮次但串行 |
| 大消息 | **带宽最优** | 根拥塞 | Master 瓶颈 |
| 小消息 | 步数多 → 延迟敏感 | 常更好 | — |

粗算：256 GPU、1 GB、~100 Gb/s → Ring ~**200 ms** 量级；GPT-3 级梯度 ~700 GB 时 AllReduce 可占 step 时间 **30–50%+**。

## 四种并行策略

| | **DP** | **TP** | **PP** | **EP** |
|--|--------|--------|--------|--------|
| 切法 | batch | 张量维（Megatron） | 模型层 | MoE expert |
| 原语 | AllReduce 梯度 | 每层 AllReduce 部分和 | P2P act/grad | **All-to-All** |
| 频率 | 每 step | 每层×2 | 每 micro-batch | 每层 |
| 适用 | 模型 ≤ 单卡 | 单层太大 | 必须切层 | MoE |
| 瓶颈 | 互联带宽 | NVLink/带宽 | **bubble** 10–30% | All-to-All |

推理侧 DP↔TP 切换点见 [Parallelism Transition Point](/concepts/parallelism-transition-point.md)。

## 分布式 Roofline 直觉

```
T_train ≈ T_compute + T_comm(DP/TP/PP/EP)
T_compute ≫ T_comm → 堆算力 / 大批次
T_comm ≫ T_compute → 压互联、压缩梯度、重叠通信
```

弱 scaling 大模型：常出现 **T_comm / T_compute > 1**（笔记例：~3.7×）→ GPU 大量时间等通信。

## Wafer-Scale 如何改写故事

| | GPU 集群 | 单 WSE |
|--|----------|--------|
| AllReduce 介质 | NVLink / IB | 2D mesh NoC |
| 延迟量级 | ms–s（大消息） | **μs** 级 hop 积 |
| 限制 | 模型仍须多卡 | SRAM **装不下**全模 → 多 wafer / Rack-Scale |

片上集体算法谱系见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)；量化见 [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md)。跨 wafer fabric ≈ 新的「长延迟 NoC」——Rack-Scale 核心命题。

## 通信-计算重叠

不必串行等 AllReduce：用 **async AllReduce + 下一层/下一 micro-batch 计算** 掩盖；PP 用 1F1B 等调度减 bubble。重叠率受链路与 kernel 粒度限制。

## 相关页面

- [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — α+nβ 五算法
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — 片上 FRED 等
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — 推理 DP/TP/PP
- [M2N Communication](/concepts/m2n-communication.md) — MoE 非对称通信
- [Cerebras WSE](/entities/cerebras-wse.md) — 片上 vs 片外
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Day 29 前沿
- [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md) — LLM 训练数据中心网络（HPN）
- [Meta RDMA over Ethernet](/papers/rdma-over-ethernet-meta-training.md) — Meta 规模分布式训练 RoCE
- [Comm/Comp Parallelism](/papers/optimizing-comm-comp-parallelism-training.md) — 训练平台通信-计算重叠
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — 晶圆级 chiplet 上用专家共激活布局压 All-to-All 的 C_T
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — **推理** TP AllReduce 与 KVT 争用（对照训练集体）
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — 把 AllReduce/All-to-All 落到 AXI/以太 C2C 的 VC、credit、MAC 组帧
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 片内树 NoC 上的 MoE scatter-gather，不是跨卡集体
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — Meta MTIA 300：集体编译到包内 ME/NMC，机柜内最高 940 GB/s，重叠 GEMM 降幅 <0.5%
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 驻留 MoE 后 EP/TP 权重移动变次级；归约顺序必须匹配 shard 放置（反向 D2D 最高 5.7×）

# Citations

[1] [raw/articles/arch-study-30d-day-27.md](raw/articles/arch-study-30d-day-27.md) — H&P Ch.6/10 + LLM collectives（Day 27）
