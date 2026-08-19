---
type: Paper
title: Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding
description: ETH Iff et al. — WoW hybrid bonding 下 reticle 放置即拓扑；Aligned/Interleaved/Rotated/Contoured 相对 mesh-like baseline 吞吐最高 +250%、延迟 -36%、每字节能量 -38%
tags:
- wse
- now
- network-on-wafer
- wafer-on-wafer
- hybrid-bonding
- noc
- interconnect
- chiplet
- mesh
- routing
- 3d
- packaging
- training
- llm
- architecture
timestamp: '2026-08-18T00:00:00Z'
created: 2026-08-18
sources:
- raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf
- raw/papers/network-design-wafer-scale-wow-hybrid-bonding.md
---

# Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding

**Authors:** Patrick Iff, Tommaso Bonato, Maciej Besta, Luca Benini, Torsten Hoefler（ETH Zurich）
**arXiv:** [2603.05266](https://arxiv.org/abs/2603.05266)（2026-03-05）
**Venue:** arXiv cs.AR 预印本。abs 页模板写 Design Automation Conference / 2025-07 Long Beach，**未独立核实**，按 2026-03-05 预印本引用。
**PDF:** [raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf](raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf)
**Code:** https://github.com/spcl/nw-design-for-wsi

## 中文摘要

晶圆对晶圆（WoW）hybrid bonding（如 TSMC SoIC-WoW）把两片已曝光 reticle 的晶圆面对面键合：同晶圆相邻 reticle **不能直连**，网络只能由**对侧重叠 reticle** 的垂直 hybrid bond 长成。本文把 reticle 放置当作拓扑设计变量，从近似 2D mesh 的 baseline 出发，提出 Aligned / Interleaved / Rotated（Logic-on-Interconnect）与 Contoured（Logic-on-Logic）四种放置，把每 reticle 邻居数从 4 提到最高 7，从而缩短平均路径。BookSim2 周期精确仿真显示，相对 mesh-like baseline，吞吐最高提升 250%、延迟最高降 36%、每传输字节能量最高降 38%；Llama-7B 训练 trace 上平均延迟降到 baseline 的 60%。

## Motivation

通信带宽跨层级断崖：片上 TB/s → NVLink ≈900 GB/s → NDR InfiniBand ≈100 GB/s。摩尔/Dennard 减速后，WSI 通过放大物理芯片本身缓解搬运。既有 WSI 三条路：

| 路线 | 代表 | 同层相邻 die/reticle |
|------|------|----------------------|
| Chiplet-on-fanout | Tesla Dojo（25×645 mm² D1） | 板级/扇出互连，需 PHY |
| Field stitching | [Cerebras WSE](/entities/cerebras-wse.md) | 曝光重叠缝出连续金属 |
| **WoW hybrid bonding** | TSMC SoIC-WoW（本文） | **同晶圆不能直连**，只连对侧重叠区 |

HB pitch 量产 <10 μm、研究原型 1 μm，电气特性接近上层金属，**不需要 D2D PHY**。因此拓扑被几何重叠硬约束——这是 wiki 已有 field-stitch mesh（WSE）与 chiplet NoC 都没覆盖的设计空间。概念入口见 [Network-on-Wafer](/concepts/network-on-wafer.md)。

## Approach

1. **集成层次**：Logic-on-Interconnect（只有顶片有 GPU-like reticle，底片纯互连，热管理简单）vs Logic-on-Logic（两片都有算力，功耗/热仍是挑战）。
2. **几何**：200/300 mm；矩形网格 vs 最大填充。WoW 无切割道，模型省略 inter-reticle spacing。
3. **网络抽象**：每 compute reticle 收成一个路由器（本地 GPC NoC 折叠）；虫孔 + credit；Dijkstra 最短路 + SCB（任意拓扑 turn-model）无死锁；选择函数随机或局部自适应（看邻居 input buffer 余量）。
4. **放置**：
   - Baseline：互连 reticle 半格错位，近似 2D mesh，radix-4。
   - Aligned / Interleaved：互连 reticle 转 90°，一个互连 reticle 连最多 6 个 compute，互连片更少。
   - Rotated：互连 reticle 缩到 22.98×32.53 mm 并转 45°，radix-7（穷举整数位置/旋转未找到更高 radix）；重叠仍可支撑最高 6 TB/s（10 μm pitch 假设）。
   - Contoured（仅 LoL）：下片 H 形、上片十字，radix-5；为保 2 TB/s 链路，轮廓后面积仍为光罩极限的 98.5%。
5. **评测**：BookSim2（四段流水、32-flit buffer、单 VC）；Orion3.0 + DeepScaleTool 缩到 7 nm；链路 2 TB/s @ 1 GHz、每 2 mm 一级流水；合成流量（uniform / permutation / neighbor / tornado）+ ATLAHS Llama-7B 训练 GOAL trace（消息切 2 KB packet）。

## Results（仅论文数字）

**拓扑表（300 mm、最大利用率、LoI）**：Baseline 64 compute / 直径 18 / 平均路径 7.45 hop / 二分带宽 26.00；Rotated 66 compute / 直径 10 / 平均路径 4.76 / 二分带宽 64.20。

| 指标 | 相对 mesh-like baseline |
|------|-------------------------|
| 饱和吞吐 | 最高 **+250%** |
| 零负载延迟 | 最高 **-36%** |
| 每字节能量 | 最高 **-38%** |
| Llama-7B 训练 trace 平均延迟 | 降到 baseline 的 **60%**，最好 **37%** |

补充：Rotated 在几乎所有架构/流量上优于 baseline；Aligned/Interleaved 在最大利用率下稳定增益，矩形网格 + tornado/neighbor 可能不及 baseline。自适应选择略增吞吐、延迟相近。路由器只占 reticle 很小面积；饱和时网络功耗约 **4 kW**（对照文献 15 kW 晶圆预算）。2 TB/s 双向链路在 10 μm pitch、1 GHz 下约需 **3.2 mm²** 重叠。

## Relation to wiki

- [Network-on-Wafer](/concepts/network-on-wafer.md) — 本页对应的中心概念（WoW 几何约束拓扑）
- [Cerebras WSE](/entities/cerebras-wse.md) — field stitching 均匀 2D mesh 对照；WoW **不能**同层直连
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) / [Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md) — SoIC-WoW 把 hybrid bonding 从 die 堆叠推到整晶圆
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — mesh-like baseline 与 Rotated 高 radix 对照
- [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) / [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — WSE 上集体算法；本文评的是 packet 网络，不是集体原语
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — 另一条 3.5D 晶圆级：NoP-Tree + 专家 chiplet，不是 WoW 重叠拓扑
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Packaging × Wafer-Scale 交点
- [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md) — 同质 repeated-die + 边界 D2D 的可行域/多保真 DSE，不是 WoW 重叠约束

## 开放问题

1. Rotated 的 45° 互连 reticle 与非矩形 Contoured 在真实光刻/对准/良率上是否可制造？论文未给工艺良率数据。
2. LoL 的热/供电（thermal TSV、微流道冷却）何时使双算力晶圆可行？作者预期“数年”。
3. 集体通信（AllReduce / All-to-All）在这些不规则拓扑上如何映射？本文用合成流量 + Llama-7B 消息 trace，没有集体专用算法。
4. 与 [FlooNoC collectives](/concepts/collective-capable-noc.md) / FRED Clos-like WSI 的定量对照仍缺——论文指出 Clos-like 在 WoW 几何下不可行。

# Citations

[1] [raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf](raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf) — Iff et al., arXiv:2603.05266
[2] [raw/papers/network-design-wafer-scale-wow-hybrid-bonding.md](raw/papers/network-design-wafer-scale-wow-hybrid-bonding.md) — 结构化摘录
