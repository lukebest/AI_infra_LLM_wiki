---
type: Paper
title: "REACT: Tuning Collective Patterns to Alleviate Congestion in Shared AI Clusters"
description: UIUC/Meta/IBM — NCCL shim 按拥塞改写集体 pattern；共享集群算法带宽 +13–38%，ns-3 最高约 +75%
tags:
- llm
- training
- collective
- communication
- congestion-control
- fabric
- scale-out
- gpu
- nvidia
- training-system
timestamp: '2026-09-08T00:00:00Z'
created: 2026-09-08
updated: 2026-09-08
sources:
- raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf
- raw/papers/react-tuning-collective-patterns-shared-clusters.md
---

# REACT: Tuning Collective Patterns to Alleviate Congestion in Shared AI Clusters

**Authors:** Eashan Gupta, Yongzhou Chen, Apoorve Mohan, Pavlos Maniotis, Abdullah Kayi, Radhika Mittal
**Affiliation:** UIUC; Meta; IBM Research
**arXiv:** [2609.04417](https://arxiv.org/abs/2609.04417)（2026-09-03，cs.NI/cs.DC）
**Venue:** 预印本
**PDF:** [raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf](raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf)

共享集群里外部作业会造成持久/间歇拥塞，而用户往往不能改交换机或全局调度。REACT 在 **CCL 层**检测流级拥塞，**改写集体通信的边集**（保留语义：谁聚合、ring 邻居等），单边可部署。对照 [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)：这是 **pattern/拓扑自适应**，不是压缩载荷，也不是新硬件 fabric。

## 动机

- 集体一轮 = 多条并发流；一流变慢 → 整轮变慢。
- 全局协同（作业调度、交换机自适应）在多租户云里常不可用。
- 需要只依赖流统计、可在 NCCL 上 shim 的运行时。

## 方案

1. **检测：** epoch 批末收集 FCT/吞吐；相对基线降幅与波动阈值判定稳态/间歇拥塞。
2. **变换：** TEN 展开集体；对 tree/ring/recursive-doubling 做位置等价 swap，避开拥塞节点/边。
3. **反馈：** RTuner 试变换；要求至少约 5% 改进否则回退；探索轮次有上限。
4. **实现：** PyTorch + NCCL shim；自定义 pattern 用 P2P API 拼图。

## 效果（仅论文数字）

**平台：** 学术共享集群 — 4×A100/节点 NVLink + **200 Gbps Cray Slingshot**；自适应路由与 GPU Direct RDMA 开。

| 设定 | 结果 |
|------|------|
| 实测拥塞下算法带宽 | **+13%–38%** |
| ns-3 多场景 | 最高约 **+75%** |
| 文内小例（拥塞 656µs → 调后 576µs） | 约 **14%** |

覆盖 dual-tree AllReduce、Ring AllReduce、recursive doubling AllGather。

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — Ring/Tree 配方的运行时改写
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 对照：本文攻「边拥塞」，Sync Tax 攻「barrier 等待」
- [CIERA](/papers/ciera-cross-iteration-exponent-reuse-allgather.md) — 对照：载荷压缩 vs pattern 改写
- [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md) — 数据中心网络侧对照
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — 专用加速器集体卸载对照

## 开放问题

1. 多作业同时跑 REACT 是否互相振荡（文中多作业重叠有改善但仍依赖探测）？
2. 与 ECMP/自适应路由同时开时，收益如何归因？
3. 超大规模（千卡）TEN 搜索与探测开销是否仍可摊薄？

# Citations

[1] [raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf](raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf) — Gupta et al., arXiv:2609.04417
[2] [raw/papers/react-tuning-collective-patterns-shared-clusters.md](raw/papers/react-tuning-collective-patterns-shared-clusters.md) — ingest stub
