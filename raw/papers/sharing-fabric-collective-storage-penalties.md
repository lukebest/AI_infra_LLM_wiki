---
type: Raw Source
title: "Sharing a Fabric with Collective Communication: Two Storage Penalties in Deep Learning Training"
source_url: https://arxiv.org/abs/2609.06506
arxiv: '2609.06506'
ingested: 2026-09-10
sha256: 6b426c9c8282d78f768b6bb71be2b34fbc1e63459742f38bcad163c7b7d18083
---

# Sharing a Fabric with Collective Communication: Two Storage Penalties in Deep Learning Training

**Authors:** Chen Wang, Wenzhao Wu, Hyojin Kim, Jae-Sung Yeom
**Affiliation:** NTU Singapore；Lawrence Livermore National Laboratory (LLNL)
**PDF:** [Sharing_Fabric_Collective_Storage_Penalties_2026.pdf](Sharing_Fabric_Collective_Storage_Penalties_2026.pdf)
**arXiv:** [2609.06506](https://arxiv.org/abs/2609.06506)（2026-09-09，cs.DC/cs.PF）

## 问题

HPC 上 NCCL/RCCL 集体与并行文件系统 I/O 常共享同一 fabric。Slingshot-11 上真实 GNN（MILAN）训练显示两种代价：重尾 DataLoader stall，以及同 traffic class 下 all-reduce 被存储流量拖慢。

## 方法要点

- 测 Lustre（共享 TC）vs VAST（独立 TC）vs 节点本地 NVMe。
- 用 DYAD 做 node-local staging，把存储 I/O 挪出共享 fabric。

## 摘录数字（仅论文给出）

- 稳态 DataLoader 中位等待 **15 ms**；Lustre **28%** / VAST **12%** 的 iteration 冲到秒级。
- 隔离微基准：Lustre 共享 TC 把 all-reduce 拖到最高 **145×**；VAST 独立 TC 最坏 **24×**；本地 XFS **1.0×**。
- 整 epoch：DYAD vs 直读 Lustre **7.4×**，vs VAST **1.06×**；第二 epoch 缓存热后 vs VAST **1.31×**。
- Lustre 整 epoch **11,843.9 s** vs VAST **1,693.9 s**（约 **7×** 差距）。
- 超额时间里 DataLoader stall 约占 **93%**，all-reduce spike 约 **7%**（相对 Lustre）。
