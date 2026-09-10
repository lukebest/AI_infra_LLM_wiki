---
type: Paper
title: "Sharing a Fabric with Collective Communication: Two Storage Penalties"
description: NTU/LLNL — Slingshot 上存储与 NCCL/RCCL 共享 fabric；Lustre 同 TC all-reduce 最高 145×；DYAD 本地 NVMe 7.4× vs Lustre
tags:
- fabric
- communication
- collective
- training
- storage
- rdma
- scale-out
- networking
- infrastructure
- distributed
timestamp: '2026-09-10T00:00:00Z'
created: 2026-09-10
updated: 2026-09-10
sources:
- raw/papers/Sharing_Fabric_Collective_Storage_Penalties_2026.pdf
- raw/papers/sharing-fabric-collective-storage-penalties.md
---

# Sharing a Fabric with Collective Communication: Two Storage Penalties in Deep Learning Training

**Authors:** Chen Wang, Wenzhao Wu, Hyojin Kim, Jae-Sung Yeom
**Affiliation:** Nanyang Technological University；Lawrence Livermore National Laboratory
**arXiv:** [2609.06506](https://arxiv.org/abs/2609.06506)（2026-09-09，cs.DC / cs.PF）
**Venue:** 预印本；LLNL-CONF-2022824。
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.06506)

相对 [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) 量的是 **域内 barrier 税**，本文量的是 **scale-out fabric 上存储 I/O 与集体争用**。相对 [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md) 改集体 pattern，本文主张把存储流量 **挪出共享路径**（DYAD 节点本地 NVMe）。

## 动机

HPC 训练常让 NCCL/RCCL 集体与并行文件系统共享一张网（文测 **Slingshot-11**）。MILAN（蛋白–配体 GNN，DDP）在 Tuolumne 上暴露两种代价：

1. **主代价**：DataLoader 重尾 stall——稳态中位等待仅 **15 ms**，但一旦共享网抖动，整 batch 卡住。
2. **次代价**：存储与集体落在 **同一 traffic class** 时，all-reduce 被拖慢。

机制不同：stall 对任何穿共享 fabric 的存储路径都成立；all-reduce 争用主要在 **同 TC** 时出现。共同根因：**存储 I/O 穿了那张集体也在用的网**。

## 方案

**测量。** 4 节点 / 16 GPU，对照 Lustre（并行 FS，与 RCCL **共享 TC**）、VAST（全闪 NFS，**独立 TC**）、节点本地 XFS（NVMe，不经 fabric）。隔离微基准：开/关 I/O 看 all-reduce 墙钟。

**缓解。** 用 **DYAD**（flux-framework）做 producer–consumer 本地 staging：把样本拉到节点 NVMe，训练热路径不再打共享 fabric。为 MILAN 的 HDF5 range 访问补了 `dyad_consume_range()` 一类路径（文述）。

## 效果（仅论文数字）

**重尾 DataLoader**

| 存储 | Mean wait | >1 s 占比 | all-reduce mean |
|------|-----------|-----------|-----------------|
| VAST | 324 ms | **11.5%** | 127 ms |
| Lustre | 1,987 ms | **28.2%** | 227 ms |

（文：Lustre 约 **28%**、VAST 约 **12%** iteration 冲到秒级；摘要口径。）

**同 TC 争用（隔离微基准，相对本地 XFS）**

| 路径 | all-reduce stall |
|------|------------------|
| 本地 XFS | **1.0×** |
| VAST（独立 TC） | 最坏 **24×** |
| Lustre（共享 TC） | 最高 **145×** |

**整 epoch**

- Lustre **11,843.9 s** vs VAST **1,693.9 s**（约 **7×**）。
- DYAD vs 直读 Lustre **7.4×**，vs VAST **1.06×**；第二 epoch 本地缓存热后 vs VAST **1.31×**，且 DataLoader stall 可消掉。
- 相对 Lustre 的超额时间：DataLoader stall ≈ **93%**，all-reduce spike ≈ **7%**。

## 与 wiki 概念的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 集体墙钟不仅有算法与 barrier，还有 **存储同 fabric / 同 TC** 的外生抖动。
- [NVLink Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 对照：本文是 **scale-out Slingshot** 共享，不是域内 NVLink。
- [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md) — 共享集群拥塞的另一刀（改 pattern）；本文刀在 I/O 路径。

## 开放问题

1. LLM 大 checkpoint / 打乱数据加载是否同构？本文主负载是 GNN+小样本（~286 KB/sample）。
2. 独立 TC 能否完全替代本地 staging，还是只能压次代价？
3. 与多租户 AI 集群（[REACT](/papers/react-tuning-collective-patterns-shared-clusters.md)）叠在一起时，调度器该先隔离 TC 还是先钉本地缓存？

# Related

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md)
- [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md)
- [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.06506) — Wang et al., arXiv:2609.06506
[2] [raw/papers/sharing-fabric-collective-storage-penalties.md](raw/papers/sharing-fabric-collective-storage-penalties.md) — ingest stub
