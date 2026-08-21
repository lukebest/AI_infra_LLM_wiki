---
type: Summary
title: RDMA over Ethernet for Distributed AI Training at Meta Scale
description: SIGCOMM 2024 Meta — 专用 backend RoCE 网络设计/运维：ECMP→流量工程，DCQCN→collective 库接收端准入；千级–32K GPU 集群
tags:
- training
- training-system
- networking
- communication
- congestion-control
- routing
- infrastructure
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/RDMA_Over_Ethernet_Distributed_Training_Meta_2024.pdf
---

# RDMA over Ethernet for Distributed AI Training at Meta Scale

**ACM SIGCOMM 2024** | DOI [10.1145/3651890.3672233](https://doi.org/10.1145/3651890.3672233)  
Gangidi, Miao, Zheng, Bondu, Goes, et al.（Meta）

Meta **大规模 AI 训练 RoCE 网络**的设计、实现与运维经验：独立 backend fabric、路由演进、以及 collective-aware 拥塞控制。

## 核心贡献

1. **Dedicated backend RoCE**：与通用 DC 网络分离，独立演进/扩容；复用 Ethernet Clos 设计与运维工具
2. **Routing**：ECMP 不足 → centralized TE + Enhanced ECMP 适配 collective 流量模式
3. **Transport**：放弃难调 DCQCN → **NCCL 接收端驱动准入** + 网络参数协同调优
4. **Collective 感知**：AllReduce (DDP)、AllGather/ReduceScatter (FSDP)、AlltoAllv (DLRM) 流量特征驱动设计

## 关键数字

| 指标 | 值 |
|------|-----|
| 集群规模 | 数千 GPU/集群；公开提及最高 **32K** |
| 节点内互联 | **4–8** GPU via NVLink |
| 栈 | RoCEv2 + NCCL (RDMA write) |

## 与 wiki 交叉

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — collective 语义与并行策略
- [MPI Reduce / AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — Ring/Tree AllReduce
- [Clos / Fat-Tree Topology](/concepts/clos-fat-tree-topology.md) — Clos backend 拓扑
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — 下一代 MTIA 300：集体离开 NCCL kernel，进包内 ME/NIC chiplet

# Citations

[1] [raw/papers/RDMA_Over_Ethernet_Distributed_Training_Meta_2024.pdf](raw/papers/RDMA_Over_Ethernet_Distributed_Training_Meta_2024.pdf)
[2] [raw/papers/rdma-over-ethernet-meta-training.md](raw/papers/rdma-over-ethernet-meta-training.md) — 结构化摘录
