---
type: Raw Source
title: RDMA over Ethernet for Distributed AI Training at Meta Scale
source_path: /home/luke/wiki/raw/papers/RDMA_Over_Ethernet_Distributed_Training_Meta_2024.pdf
doi: '10.1145/3651890.3672233'
zotero: MK3UYULL
ingested: 2026-07-17
sha256: 49adde1ca0d1d10185ef54345ed872d77feb449e5d20a0b6431505cea63d6e2b
---

# RDMA over Ethernet for Distributed AI Training at Meta Scale

Authors: Adithya Gangidi, Rui Miao, Shengbao Zheng, Sai Jayesh Bondu, Guilherme Goes, et al. (Meta)
Venue: ACM SIGCOMM 2024 | DOI: 10.1145/3651890.3672233

Structured notes / key excerpts:

- **Design choice**: Dedicated **backend RoCE network** for GPU training (separate from general DC); open standards + multi-vendor vs proprietary IB/NVSwitch.
- **Intra vs inter-node**: 4–8 GPUs/node via NVLink; inter-node via RoCEv2 (RDMA verbs in Ethernet/IPv6/UDP, kernel bypass).
- **Routing evolution**: Default ECMP poor for training → centralized traffic engineering + Enhanced ECMP for load balance.
- **Congestion control**: DCQCN hard to tune for collectives → **receiver-driven admission via collective library** (NCCL co-tuning with network config).
- **Collectives table**: AlltoAllv (embedding, full-mesh, high entropy); AllReduce (DDP, tree/ring); AllGather/ReduceScatter (FSDP).
- **Scale**: Prototypes to clusters of **thousands of GPUs**; prior public mention up to **32K GPUs** RoCE cluster.
- **Workloads**: Ranking (DLRM AlltoAll), recommendation, NLP, generative AI, etc.
