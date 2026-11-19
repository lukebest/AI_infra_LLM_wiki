---
type: Paper
title: "LASH-PAT: Deadlock-Free Adaptive Shortest-Path Routing for Inter-Chiplet Interconnects"
description: "ETH Zurich — BookSim2 评十个不规则 ICI 拓扑；相对每组最好基线，吞吐 +21.15%、每包能量 −12.77%，负载下延迟相当"
tags:
- chiplet
- noc
- routing
- now
- network-on-wafer
- interconnect
- topology
- mesh
- energy
- simulator
- wafer-on-wafer
created: 2026-11-19
updated: 2026-11-19
timestamp: '2026-11-19T00:00:00Z'
paper_author: [Patrick Iff, Torsten Hoefler]
year: 2026
venue: preprint
arxiv: '2611.22937'
sources:
  - raw/papers/LASH_PAT_Inter_Chiplet_Routing_2026.pdf
  - raw/papers/lash-pat-inter-chiplet-routing.md
---

# LASH-PAT：给不规则芯粒互连补上带路径多样性的分层最短路

## 一句话结论
ETH Zurich 的 Iff 与 Hoefler 把数据中心里九种无死锁路由函数拿到新近提出的 inter-chiplet interconnect（ICI）拓扑上评了一遍，并给出 LASH-PAT：在分层最短路之上增加可按本地拥塞选择的多条最短路。BookSim2 在十个 61/64 路由器拓扑上，相对每个拓扑–流量对上表现最好的基线，饱和吞吐平均 **+21.15%**，每包能量平均 **−12.77%**，负载下延迟平均 **−1.33%**，零负载延迟平均 **+0.59%**。

## 动机
2.5D 芯粒与晶圆级集成（以及二者合在一起的 chiplet-based wafer-scale integration）正在带来一批专用 ICI 拓扑。这些拓扑往往不再是规则 mesh，维序路由（DOR）不再直接适用。转弯限制类函数能提供路径多样性，分层最短路类函数能保证最短路投递，两边的长处很难同时拿到。

## 方案
LASH-PAT 扩展分层最短路（LASH 一族）：为同一对端点保留多条最短路，按本地拥塞自适应选择，并用把路径段细粒度划到虚拟层的办法维持无死锁。虚拟信道不够时可以配置非最短路，定制基路由失败时回退到 SCB。评测里默认 4 层、每层 1 个 VC，另配 3 条附加路径。对照包括转弯类 Prefix、Up*/Down*、Left/Right、L-Turn、SCB，以及分层类 LASH、DFSSSP、A-LASH、LASH-TOR。

仿真用周期精确 BookSim2。64-bit flit、四 flit 报文、每信道 4 VC、每 VC 8-flit 输入缓冲；网络 1 GHz，路由器 4 周期，每个路由器一个端点。能量是 Orion3（45 nm）经 DeepScaleTool 缩放到 7 nm 的路由器能量，加上 0.1 pJ/bit/mm 的信道能量。每组重复 5 次。十个拓扑：Mesh、Torus、Folded Torus、HexaMesh、FoldedHexaTorus、Hypercube、Double Butterfly、ButterDonut、Kite Small、Kite Large（后两者来自 Kite 工作；HexaMesh / FoldedHexaTorus 为 61 个路由器，其余 64）。流量包括对标 MoE 训练 all-to-all 的均匀随机、随机置换，以及截断到 100K 事件的 Netrace blackscholes 与 ATLAHS 生成的 Llama-7B 训练轨迹。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 相对每组最好基线（Table III「Best」行，全部拓扑–流量对平均） | 饱和吞吐 **+21.15%**；零负载延迟 **+0.59%**；负载下延迟 **−1.33%**（注入率 0.1 flits/endpoint/cycle）；每包能量 **−12.77%**；轨迹平均包延迟 **−2.56%** | Table III / §V-F |
| 相对最好转弯类 SCB | 吞吐平均 **+31.92%** | Table III |
| 相对 4 VC 下适用于全部拓扑的最好分层类 LASH-TOR | 吞吐平均 **+105.61%** | Table III |
| 合成流量名次 | 20 个拓扑–流量对里，19 对取得最高吞吐与最低每包能量；负载下延迟在该注入率上为全部 RF 中最低 | §V-F1/F3/F4 |
| 应用轨迹 | 16 个拓扑–轨迹对里 11 对最低延迟；相对第二名最高可到 **25.3%**（ButterDonut + GPU 轨迹）。61 路由器的两个拓扑未跑轨迹 | §V-F5 / Fig. 8 |
| 最短路与适用性 | 十个拓扑上都建立起最短路，没有走到非最短路或回退。A-LASH 在八个拓扑因 VC 不足无法适用，DFSSSP 在两个拓扑无法适用 | §V-F6 |
| 路由表面积（作者估计） | 最坏约 **20 Kbit**；22 nm 约 0.003 mm²，7 nm 约 0.001 mm² | §V-G |

## 与已有页的增量
Wiki 里已有 [自适应路由](/concepts/adaptive-routing-noc.md)、[无死锁路由与 CDG](/concepts/deadlock-free-routing-cdg-dally.md)、[维序路由](/concepts/deterministic-routing-dor.md) 和一批 mesh/晶圆级拓扑讨论，评测对象多是规则 mesh 或数据中心 Clos。本篇把转弯限制与分层最短路这两类不规则网络函数，系统地放到新近 ICI / 晶圆级芯粒拓扑上，并给出一条能同时保留最短路与路径多样性的函数。同日还有同一组的选择函数短文 PAISF（2611.22772），处理保序投递，本轮先记下，未深挖。

## 与 wiki 的关系
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — 按本地拥塞在多条最短路之间选择
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — 用虚拟层划分路径段来维持无死锁
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 评测包括 HexaMesh、FoldedHexaTorus 等面向晶圆级 / ICI 的拓扑
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — 芯粒间 PHY 与端到端建模；本篇补的是这些不规则 ICI 上的路由函数

## 开放问题
- 主结果来自 BookSim2 与缩放后的 Orion3 能量模型，没有在真实 ICI / 晶圆级硅上测量。
- 应用轨迹截断到 100K 事件；LLM 训练轨迹来自 Llama-7B，规模与当代训练全集通信有差距。
- 默认 4 VC、直连网络（concentration = 1）；更高浓度、不同报文长度或真实芯片的表项/面积约束还需要另评。
- 路由表相对部分基线更大，作者认为在 64 芯粒量级、单芯粒面积足够时可以接受，更大系统还要再看。

# Citations
- [arXiv:2611.22937](https://arxiv.org/abs/2611.22937) — Iff, Hoefler（ETH Zurich）
- [raw stub](/raw/papers/lash-pat-inter-chiplet-routing.md)
- [PDF](/raw/papers/LASH_PAT_Inter_Chiplet_Routing_2026.pdf)
