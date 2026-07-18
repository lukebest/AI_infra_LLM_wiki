---
type: Summary
title: 'Alibaba HPN: A Data Center Network for Large Language Model Training'
description: SIGCOMM 2024 阿里云 — LLM 训练专用 2-tier dual-plane DCN，15K GPU/Pod；+14.9% 训练吞吐，non-stacked dual-ToR 防单点
tags:
- training
- training-system
- llm
- networking
- topology
- infrastructure
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Alibaba_HPN_Datacenter_Network_LLM_Training_2024.pdf
---

# Alibaba HPN: A Data Center Network for Large Language Model Training

**ACM SIGCOMM 2024** | DOI [10.1145/3651890.3672265](https://doi.org/10.1145/3651890.3672265)  
Qian, Xi, Cao, Gao, et al.（阿里云 Cloud）

面向 **LLM 分布式训练** 的数据中心网络 **HPN**：针对低熵周期性 **400Gbps** burst 与同步训练对 ToR 单点故障的敏感性，重新设计拓扑与 ToR。

## 核心贡献

1. **2-tier dual-plane**：单 Pod **15K GPU**（传统 3-tier Clos 规模），避免 aggregation 层 hash polarization
2. **Non-stacked dual-ToR**：双独立 ToR 消除堆叠同步，提升大规模可靠性
3. **Rail-optimized + 51.2T 芯片**：tier-1 **1K GPU**；**96.3%** 作业最优网络性能

## 关键数字

| 指标 | 值 |
|------|-----|
| Pod 规模 | **15K** GPU |
| NIC burst | **400 Gbps** |
| vs 传统 DCN 吞吐 | **+14.9%** |
| ToR 故障代价 | **20×** vs 通用云 |
| 生产部署 | **8+** 个月 |

## 与 wiki 交叉

- [Clos / Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — 传统 3-tier Clos 对照
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — AllReduce/AllGather 流量模式

# Citations

[1] [raw/papers/Alibaba_HPN_Datacenter_Network_LLM_Training_2024.pdf](raw/papers/Alibaba_HPN_Datacenter_Network_LLM_Training_2024.pdf)
[2] [raw/papers/alibaba-hpn-datacenter-network-llm.md](raw/papers/alibaba-hpn-datacenter-network-llm.md) — 结构化摘录
