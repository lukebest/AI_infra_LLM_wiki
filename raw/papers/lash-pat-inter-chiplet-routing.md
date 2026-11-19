---
type: Raw Source
title: "LASH-PAT: Deadlock-Free Adaptive Shortest-Path Routing for Inter-Chiplet Interconnects"
source_url: https://arxiv.org/abs/2611.22937
pdf: LASH_PAT_Inter_Chiplet_Routing_2026.pdf
retrieved: 2026-11-19
ingested: 2026-11-19
org: ETH Zurich
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.22937)

With the slowdown of transistor scaling, chiplet-based systems, and in particular chiplet-based wafer-scale integration, have emerged as a promising approach to sustain growth in computing capability per cost for modern processors and accelerators. In recent years, many specialized inter-chiplet interconnect topologies have been proposed. In these topologies, the simple, well-established, and deadlock-free dimension-order routing scheme is not applicable due to its reliance on regular mesh structures. In this work, we study routing in these recently proposed inter-chiplet interconnect topologies by categorizing and evaluating nine deadlock-free routing functions for irregular topologies known from data center networking in this new context. This reveals a trade-off between turn-based routing, which enables path diversity, and layered routing, which ensures shortest-path delivery. To resolve this trade-off, we propose LASH-PAT, a routing function that extends layered shortest-path routing with adaptive path diversity. LASH-PAT supports multiple shortest paths and dynamically selects among them based on local congestion while preserving deadlock freedom. When compared to the best-performing baseline routing function for each combination of topology, traffic pattern, and evaluated metric, LASH-PAT improves throughput by 21.15% and reduces energy per packet by 12.77%, while providing latency comparable to the lowest-latency baseline routing function.

# Excerpts / key facts

- Authors: Patrick Iff, Torsten Hoefler（ETH Zurich）。arXiv:2611.22937，cs.AR，2026-11-18 公告（提交标注 17 Nov 2026）。预印本。
- 评测栈：周期精确 BookSim2；能量为 Orion3（45 nm）经 DeepScaleTool 缩放到 7 nm 的路由器能量，加上按信道长度与 0.1 pJ/bit/mm 计算的信道能量。每组实验重复 5 次；延迟用算术均值，吞吐用调和均值，相对性能用几何均值，并给非参数 95% bootstrap CI。
- 仿真参数：64-bit flit、四 flit 报文、每物理信道 4 个 VC、每 VC 8-flit 输入缓冲；网络 1 GHz，路由器延迟 4 周期，每个路由器一个端点；信道延迟为每 2 mm 一周期（建模每 2 mm 一级寄存器），收发 chiplet 的 PHY 各 2 周期。负载下延迟在注入率 0.1 flits/endpoint/cycle 处测量。
- 十个 ICI 拓扑（64 个路由器；HexaMesh 与 FoldedHexaTorus 为 61）：Mesh、Torus、Folded Torus、HexaMesh、FoldedHexaTorus、Hypercube、Double Butterfly、ButterDonut、Kite Small、Kite Large。
- 九个基线 RF：转弯类 Prefix、Up*/Down*、Left/Right、L-Turn、SCB；分层类 LASH、DFSSSP、A-LASH、LASH-TOR。LASH-PAT 默认 4 层、每层 1 个 VC，另配 3 条附加路径，代价函数 All，回退 RF 为 SCB；LASH-TOR 默认 1 层、每层 4 个 VC。
- 流量：合成均匀（U，对标 MoE 训练中的 all-to-all）与随机置换（RP）；应用轨迹截断到 100K 事件——CPU 用 Netrace 的 blackscholes，GPU 用 ATLAHS 从 Llama-7B 训练生成 GOAL 轨迹。HexaMesh / FoldedHexaTorus 因 61 路由器未跑轨迹。
- 主结果（Table III，相对每个拓扑–流量对上表现最好的基线，再对全部对取平均）：饱和吞吐 **+21.15%**；零负载延迟 **+0.59%**；负载下延迟 **−1.33%**；每包能量 **−12.77%**；轨迹平均包延迟 **−2.56%**。相对最好的转弯类 SCB，吞吐平均 **+31.92%**；相对在 4 VC 下适用于全部拓扑的最好分层类 LASH-TOR，吞吐平均 **+105.61%**。合成流量上 20 个拓扑–流量对里有 19 对取得最高吞吐与最低每包能量。轨迹上 16 个拓扑–轨迹对里有 11 对最低延迟，相对第二名最高可到 **25.3%**（ButterDonut + GPU 轨迹）。
- 在十个拓扑上，LASH-PAT 都建立了最短路，没有走到非最短路或回退路由。A-LASH 在十个拓扑中有八个因 VC 不足无法适用，DFSSSP 有两个无法适用。最坏路由表约 **20 Kbit**，作者估计 22 nm 约 0.003 mm²、7 nm 约 0.001 mm²。
