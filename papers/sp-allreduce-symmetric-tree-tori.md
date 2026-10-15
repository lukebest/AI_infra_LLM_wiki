---
type: Paper
title: "SP-Allreduce: Symmetric Tree Schedules for Tori and Beyond"
description: "环面 allreduce 新调度：对称化最短路 BFS 树，单跳传输、零带宽冗余、每轮链路负载均衡，轮数 2d⌊n/2⌋ 约为 Bucket 的一半并在同类中最优；SST 模拟方环面最高 1.19×、长条环面 1.65×，HyperX 14.82×（基线每轮只用 4/62 条链路）、spine-leaf 1.72×"
tags:
- allreduce
- collective
- communication
- topology
- mesh
- training
- distributed
- interconnect
- formal-analysis
created: 2026-10-15
updated: 2026-10-15
timestamp: '2026-10-15T00:00:00Z'
paper_author: [Mikhail Cherniavskii, Andrey Kupavskii, Georgy Mironov, Stanislav Moiseev]
year: 2026
arxiv: '2610.16387'
venue: arXiv preprint (cs.DC)
sources:
  - raw/papers/SP_Allreduce_Symmetric_Tree_Tori_2026.pdf
  - raw/papers/sp-allreduce-symmetric-tree-tori.md
---

# SP-Allreduce：环面上的对称最短路树调度

## 一句话结论
环面（TPU v5/v6/Ironwood、Trainium、Graphcore IPU-POD、Tofu-D）上的经典带宽最优 allreduce 是 Bucket，它的轮数随边长线性增长。SP-allreduce 利用环面的对称性，把一棵最短路 BFS 树在群作用下对称化成一族树，每块数据沿自己的树做 reduce-scatter 再反向 allgather。结果同时满足三条：传输总量最小、只走单跳、每轮各链路负载相同，并且轮数约为 Bucket 的一半，在「完全带宽最优」的算法类里可证明最少。

## 动机
- α–β 模型下，大消息看带宽项，中小消息看轮数 × α。Ring 传输量最小但要 2(p−1) 轮；recursive doubling/halving–doubling 轮数 O(log p)，在环面上会产生多跳流量放大；Swing、Trivance 也存在多跳或不均衡。
- 论文定义「完全带宽最优」：无带宽冗余、无多跳引起的流量放大、每轮链路负载完全均衡。Bucket 满足这三条，但需要 2d(n−1) 轮。

## 方案
- **对称化 BFS 树**：在 d 维 n×…×n 环面上取一棵以 0 为根的 BFS 树，用一个在有向物理边上可迁的对称群（含平移等变换）作用其上，生成 2d·nᵈ 个逻辑 chunk 各自的树；同发送者/接收者/路由/轮次的传输打包成一条消息。
- **轮数**：2H = 2d⌊n/2⌋ 轮。n 为奇数时达到下界、最优；n 为偶数时比下界 2H−1 多一轮。
- **k-SP-allreduce**：限定树深 k（k 轮 reduce-scatter + k 轮 allgather），用一定多跳流量换更少轮数，适合小消息。
- 扩展到长方形环面（两棵 BFS 树构造）、HyperX（「风车」基树）、两层 spine-leaf。

## 效果（SST 包级模拟，400 Gb/s 链路，每跳 400 ns）
- 方环面：相对 Swing/Bucket/Trivance 最好者，8×8 / 16×16 / 32×32 / 64×64 最高增益 **8.0% / 19.0% / 17.7% / 18.3%**；64 KiB 时相对 Bucket **1.74×（8×8）/ 2.00×（64×64）**，与轮数减半一致。
- 敏感性：3.2 Tb/s 链路时最高 **+20.6%**（1 MiB）；每跳 1600 ns 时 **+20.2%**（512 KiB）。
- 1024 节点长方形环面 64×16 / 128×8 / 256×4：256 MiB 时达到 **778 / 764 / 731 Gb/s**，即 800 Gb/s 上界的 **97.2% / 95.5% / 91.4%**；最高增益 **1.22× / 1.34× / 1.65×**，越细长优势越大。
- HyperX 32×32：**11.76 Tb/s**（上界 12.4 Tb/s 的 94.9%），Swing **0.794 Tb/s**，比值 **14.82×**；论文说明差距主要因为对比实现每轮只用每节点 62 条链路中的 4 条。
- Spine-leaf（16 spine/32 leaf）：大消息各算法都接近 200 Gb/s 上界（SP 为 199.7 Gb/s）；最大增益出现在 32 KiB，**1.72×**（28.4 vs 16.5 Gb/s）。

## 与 wiki 的关系
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — 环面对称性直接转化为集体通信调度；对 WSE 类 2D mesh 有参考价值
- [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — Rabenseifner 谱系中 Ring / halving–doubling 的环面专用后继
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — 晶圆级 2D mesh 上的归约同样受轮数 × 跳延迟支配
- [TPU v4 OCS Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) — 论文点名的 TPU 3D 环面 + 光重构场景
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 数据并行 allreduce 的拓扑感知调度

## 局限与开放问题
- 只有模拟（SST），无真实 TPU/Trainium 测量；归约本身计零代价，未建模 GPU/加速器端的规约算力与内存带宽。
- 理论保证基于同构多端口模型；有故障链路、OCS 切片后的非完整环面如何保持对称性未讨论。
- HyperX 的 14.82× 主要反映基线未利用全连通；与 HyperX 专用最优算法的对比仍缺。
- 对 WSE/NoW 这类无回绕的 2D mesh（非环面）能否沿用对称化构造，需另行推导（本页判断）。

# Citations
- Cherniavskii, Kupavskii, Mironov, Moiseev, "SP-Allreduce: Symmetric Tree Schedules for Tori and Beyond", arXiv:2610.16387, 2026. [raw](/raw/papers/sp-allreduce-symmetric-tree-tori.md) · [PDF](/raw/papers/SP_Allreduce_Symmetric_Tree_Tori_2026.pdf)
