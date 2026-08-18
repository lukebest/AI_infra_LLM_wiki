---
type: Raw Source
title: Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding
source_url: https://arxiv.org/abs/2603.05266
arxiv: '2603.05266'
ingested: 2026-08-18
sha256: bd110b3feca716eaaf688485c4643a0e36a304363aeded2cc681922fb592e72b
---

# Network Design for Wafer-Scale Systems with Wafer-on-Wafer Hybrid Bonding

**Authors:** Patrick Iff, Tommaso Bonato, Maciej Besta, Luca Benini, Torsten Hoefler (ETH Zurich)
**PDF:** [Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf](Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf)
**arXiv:** [2603.05266v1](https://arxiv.org/abs/2603.05266) (2026-03-05)
**Code:** https://github.com/spcl/nw-design-for-wsi

## 问题

Transformer LLM 训练被数据搬运约束：带宽从片上 TB/s 级跌到 NVLink ~900 GB/s、NDR IB ~100 GB/s。晶圆级集成（WSI）把芯片面积本身做大。第三条 WSI 路线——**晶圆对晶圆（WoW）hybrid bonding**（TSMC SoIC-WoW）——与 Cerebras field stitching、Tesla Dojo chiplet-on-fanout 不同：同晶圆相邻 reticle **不能直接连线**，只能通过两片晶圆上**重叠 reticle** 的 hybrid bond 垂直互连。拓扑完全由 reticle 放置决定。

## 方法要点

- 两种垂直集成：Logic-on-Interconnect（LoI，底片纯互连）与 Logic-on-Logic（LoL，两片都有算力）。
- 200/300 mm 晶圆；矩形网格 vs 最大利用率填充。
- 虫孔 + credit；Dijkstra 最短路 + SCB 破环保证无死锁；随机 / 局部自适应选择。
- LoI 放置：Baseline（半格错位近似 2D mesh，radix-4）→ Aligned / Interleaved（互连 reticle 转 90°，radix-6）→ Rotated（互连 reticle 缩到 22.98×32.53 mm 并转 45°，radix-7）。
- LoL 放置：Contoured（H 形 + 十字形，radix-5）。
- 评测：BookSim2 + Orion3.0→DeepScaleTool 缩到 7 nm；合成流量 + ATLAHS Llama-7B 训练 trace。链路 2 TB/s @ 1 GHz（对齐 Dojo）。

## 摘录数字（仅论文给出）

- 相对 mesh-like baseline：吞吐最高 **+250%**，延迟最高 **-36%**，每字节能量最高 **-38%**。
- Llama-7B 训练 trace：平均延迟降到 baseline 的 **60%**，最好 **37%**。
- HB pitch：量产 **<10 μm**，研究原型 **1 μm**。2 TB/s 双向链路在 10 μm pitch、1 GHz 下仅需约 **3.2 mm²** 重叠。
- 饱和吞吐下网络功耗约 **4 kW**，对照文献 15 kW 晶圆功耗预算。
