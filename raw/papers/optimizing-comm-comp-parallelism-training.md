---
type: Raw Source
title: Optimizing the Parallelism of Communication and Computation in Distributed Training Platform
source_path: /home/luke/wiki/raw/papers/Optimizing_Comm_Comp_Parallelism_Distributed_Training_2024.pdf
doi: '10.1007/978-981-97-0834-5_20'
zotero: 599QACPR
ingested: 2026-07-17
sha256: 57b00999d2248e8968841af62dc6c5849ebbe73fdf13ed8aec92b589ac4aae2a
---

# Optimizing the Parallelism of Communication and Computation in Distributed Training Platform

Authors: Xiang Hou, Yuan Yuan, Sheng Ma, Rui Xu, Bo Wang, et al. (National University of Defense Technology)
Venue: ICA3PP 2023 (LNCS 14487, 2024) | DOI: 10.1007/978-981-97-0834-5_20

Structured notes / key excerpts:

- **Platform**: Hierarchical Torus-Ring topology — NAP (Neural Accelerator Package) × NAM (module with compute + HBM + NIC); intra-package NVLink/PCIe, inter-package Ethernet/InfiniBand.
- **Problem**: Computation and communication run on different hardware; exposure time limits training speed.
- **Data parallelism**: Overlap weight-gradient AllReduce (Ring) with activation computation → reduce **communication exposure**.
- **Model parallelism**: Overlap activation AllGather with weight-gradient computation → reduce **computation exposure**.
- **Collectives**: All-gather (activations FP / input grads BP), All-reduce (weight grads WU in DP), All-to-all.
- **Results** (5 iterations): ResNet50 **+23.77–25.64%**; Transformer **+11.66–12.83%** vs prior scheduling.
- **Reference topology**: Google 16×16 2D Torus for 256 TPUs.
