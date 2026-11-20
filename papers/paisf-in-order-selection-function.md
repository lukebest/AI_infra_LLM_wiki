---
type: Paper
title: "PAISF: A Partially Adaptive In-Order Selection Function for On-Chip, Inter-Chiplet, and Wafer-Scale Networks"
description: "ETH Zurich — BookSim2 评 NoC / ICI / WSI 不规则拓扑上的保序选择函数；相对已有保序方法，饱和吞吐平均 +15.2%，每包能量 −12.1%，负载下延迟 −11.3%"
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
created: 2026-11-20
updated: 2026-11-20
timestamp: '2026-11-20T00:00:00Z'
paper_author: [Patrick Iff, Luca Oertig, Andrin Weber, Luca Benini, Torsten Hoefler]
year: 2026
venue: preprint
arxiv: '2611.22772'
sources:
  - raw/papers/PAISF_In_Order_Selection_Function_2026.pdf
  - raw/papers/paisf-in-order-selection-function.md
---

# PAISF：用不规则网络上的选择函数保证保序投递

## 一句话结论
ETH Zurich 的 Iff、Oertig、Weber、Benini 与 Hoefler 提出 ISF / PAISF：用报文熵值的哈希决定下一跳，同一消息共用熵值则走同一条路并保持顺序，随机熵值则利用路径多样性。BookSim2 在 NoC、芯粒互连（ICI）与晶圆级（WSI）拓扑上，相对确定性路由函数 LASH-TOR、确定性选择函数 DET 以及 Multi 中间层，饱和吞吐平均 **+15.2%**，每包能量平均 **−12.1%**，注入率 0.1 时延迟平均 **−11.3%**，零负载延迟平均 **+3.3%**。

## 动机
芯粒与晶圆级集成带来一批不规则拓扑，路由算法拆成保证无死锁的路由函数（RF）和选择下一跳的选择函数（SF）。许多应用要求保序投递；若网络不处理，端点需要重排序缓冲，缓冲满时还可能丢包重传。已有做法包括走单一路径的确定性 RF、始终选同一下一跳的确定性 SF，以及在目的路由器输入缓冲里重排序的 Multi 中间层。

## 方案
ISF 在每个路由器上用该路由器自己的哈希，把报文熵值映射到 RF 给出的合法下一跳；PAISF 在此基础上按本地拥塞做有限自适应。发送端决定消息要保序还是可乱序：保序消息共用熵值，乱序消息使用随机熵值。作者把思路类比 Ultra Ethernet 的熵值选路。对照包括 LASH-TOR（用满全部 VC 层并均衡路径）、DET，以及搭配随机 / 自适应 SF 的 Multi；这些再与 XY、SCB、Up*/Down*、L-Turn、Left/Right、Prefix 六种 RF 组合。LASH 与 DFSSSP 在所评拓扑上分别需要最多 6 和 8 个 VC，超出默认 4 个 VC，因而未纳入对照。

仿真用周期精确 BookSim2，每组跑 3 次；延迟用算术均值，吞吐用调和均值，相对性能用几何均值，并给非参数 95% bootstrap CI。吞吐的平均相对半宽为 **15.80%**，延迟为 **2.82%**。能量为 Orion3（45 nm）经 DeepScaleTool 缩放到 7 nm 的路由器能量，加上 0.1 pJ/bit/mm 的链路能量。默认：每条消息 16 个报文、每个报文 4 个 flit，**50%** 消息要求保序；网络 1 GHz；NoC / ICI 用 64-bit flit，WSI 用 16-kbit flit（对标 Tesla Dojo 的 2 TB/s）；路由器 3 周期；每物理信道 4 个 VC；VC 缓冲在 NoC / ICI / WSI 上分别为 8 / 16 / 32 flit。链路延迟每 2 mm 一周期，ICI 另加 4 周期 PHY。合成流量包括均匀随机（对标 MoE 训练 all-to-all）、随机置换与非对称；轨迹截断到 100K 事件，CPU 用 Netrace blackscholes，GPU 用 ATLAHS 生成的 Llama-7B 训练轨迹。拓扑按域分为 NoC（Mesh、Torus、Folded Torus、Hypercube、Flattened Butterfly，64 端点）、被动基板 ICI-P、有源中介层 ICI-A，以及间接网络的 WSI（计算晶圆加互连晶圆，约 188–318 个路由器、约 64 个端点）。代码发布在 https://github.com/spcl/PAISF。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 全部拓扑与工作负载平均（相对三种已有保序方法中每组最好） | 饱和吞吐 **+15.2%**；每包能量 **−12.1%**；负载下延迟 **−11.3%**；零负载延迟 **+3.3%** | Abstract / §VI |
| NoC | 吞吐平均 **+18.9%**；零负载延迟 **+3.6%**；注入率 0.1 时延迟 **−8.9%**；每包能量 **−17.0%**；PAISF 相对 ISF 吞吐 **+2.7%** | §V-E |
| ICI-P | 吞吐 **+15.1%**；能量 **−11.9%**；零负载延迟 **+2.9%**；注入率 0.1 时延迟 **−11.9%**；PAISF 相对 ISF **+4.6%** | §V-F1 |
| ICI-A | 吞吐 **+18.9%**；能量 **−12.1%**；零负载延迟 **+4.2%**；注入率 0.1 时延迟 **−25.6%** | §V-F2 |
| WSI（间接网络，平均跳数约高三倍） | 吞吐 **+7.8%**；能量 **−7.3%**；零负载延迟 **+2.3%**；注入率 0.1 时延迟 **+1.2%**；ISF 与 PAISF 接近 | §V-G |
| CPU 轨迹 | 平均包延迟相对最好基线 **−12.2%**；Multi 在多数轨迹上出现消息级死锁 | §V-H1 |
| GPU 轨迹（Llama-7B） | (PA)ISF 相对 LASH-TOR 平均延迟 **−3.8%** | §V-H2 |
| 熵值位数 | 从 0 位增到 2 位吞吐明显上升；超过 3 位几乎不再增加 | §V-I6 |

## 与已有页的增量
同一组前一天ingest 的 [LASH-PAT](/papers/lash-pat-inter-chiplet-routing.md) 处理不规则 ICI 上的**路由函数**（分层最短路加路径多样性）。本篇补的是同一类拓扑上的**选择函数**，专门处理保序与拥塞避免，并覆盖间接 WSI 拓扑。评测栈同为 BookSim2 + 缩放到 7 nm 的 Orion3，参数略有差别（本篇默认 3 次重复、路由器 3 周期、50% 保序消息）。

## 与 wiki 的关系
- [LASH-PAT](/papers/lash-pat-inter-chiplet-routing.md) — 同一组的路由函数短文；本篇的对照里也包括 LASH-TOR
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md) — PAISF 按本地拥塞做有限自适应
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md) — 无死锁仍由底层 RF 负责，SF 在 RF 给出的合法下一跳中选择
- [Network-on-Wafer](/concepts/network-on-wafer.md) — WSI 评测为计算晶圆加互连晶圆的间接网络

## 开放问题
- 主结果来自 BookSim2 与缩放后的 Orion3，没有在真实 ICI / 晶圆级硅上测量；吞吐 CI 平均相对半宽 15.80%，读平均增益时宜一并看待。
- WSI 间接网络上收益最小，负载下延迟还略增 1.2%；作者把原因归到平均跳数约高三倍，第一跳自适应难以缓解下游拥塞。
- 故障场景下 LASH-TOR 在多数情况吞吐最高，(PA)ISF 次之，路径多样性缺失会明显限制后者。
- 轨迹截断到 100K 事件；GPU 轨迹来自 Llama-7B。默认 50% 保序、4 个 VC、约 64 端点。

# Citations
- [arXiv:2611.22772](https://arxiv.org/abs/2611.22772) — Iff, Oertig, Weber, Benini, Hoefler（ETH Zurich）
- [raw stub](/raw/papers/paisf-in-order-selection-function.md)
- [PDF](/raw/papers/PAISF_In_Order_Selection_Function_2026.pdf)
