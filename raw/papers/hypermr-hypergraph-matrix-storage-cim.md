---
type: Raw Source
title: 'HyperMR: Efficient Hypergraph-enhanced Matrix Storage on Compute-in-Memory Architecture'
source_path: /home/luke/wiki/raw/papers/HyperMR_Hypergraph_Matrix_Storage_CIM_2025.pdf
doi: '10.1145/3709695'
zotero: 6ECE27F6
ingested: 2026-07-17
sha256: 61da5635e2703e30294ae903a6cbf228d5d3e5320140f42af3361f1850d7d082
---

# HyperMR: Efficient Hypergraph-enhanced Matrix Storage on Compute-in-Memory Architecture

Authors: Yifan Wu, Ke Chen, Gang Chen, Dawei Jiang, Huan Li, Lidan Shou (Zhejiang University)
Venue: Proc. ACM Manag. Data (SIGMOD) 2025 | DOI: 10.1145/3709695

Structured notes / key excerpts:

- **Problem**: CIM 上 MVM 为 O(1) 但矩阵 tile 布局决定通信成本（input vector 分发）和累加成本；现有 reorder 方案只优化零 tile、假设特定矩阵结构/访问模式。
- **HyperMR**: 超图建模矩阵结构与访问模式；两阶段超图划分求解两个 CIM 专用 NP-hard 优化目标。
- **CIM hierarchy**: tile → PE → crossbar；矩阵切为固定大小 sub-matrix 存 tile；reorder 可释放 empty tile。
- **Limitations addressed**: L1 优化目标不足（通信成本为主瓶颈）；L2 依赖对称/对角块等结构；L3 缺乏灵活访问模式。
- **Results**: 优于 SOTA，**100%** 矩阵有效优化 vs 最佳 baseline **75%**；合成查询 **+29.65%**；科学图像滤波最高 **+34.9%**。
- **CIM context**: 非易失 crossbar（ReRAM/PCM/Flash）；可达 **106×** TOPS/W vs TPU（引用）。
