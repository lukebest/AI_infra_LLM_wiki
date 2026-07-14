---
type: Concept
title: Flow Control Fundamentals
description: Dally & Towles Ch.9 — Message/Packet/Flit/Phit；电路/报文/虫孔/VCT 延迟公式；HoL blocking；与死锁的关系
tags:
- noc
- flow-control
- wormhole
- flit
- hol
- switching
- vct
timestamp: '2026-07-13T00:00:00Z'
created: 2026-07-13
sources:
- raw/articles/interconn-study-21d-day-15.md
---

# Flow Control Fundamentals（流控基础）

interconn-study **流控篇 Day 15**：Dally & Towles **Ch.9**——路由回答「走哪条路」，流控回答「带宽与缓冲怎么分」。电信侧演进见 [Switching Principles](/concepts/switching-principles.md)；本页聚焦 **NoC 粒度与延迟公式**。

**Source:** [raw/articles/interconn-study-21d-day-15.md](raw/articles/interconn-study-21d-day-15.md)

## Message / Packet / Flit / Phit

| 层 | 单位 | 含义 | 典型大小 |
|----|------|------|----------|
| L4 | **Message** | 应用语义（整块张量） | B–KB |
| L3 | **Packet** | 路由/流控单元；可拆 Message | B–KB |
| L2 | **Flit** | 缓冲与链路原子；同包同路径 | 64–256 bit |
| L1 | **Phit** | 一拍物理位宽 | 16–64 bit |

Packet ≈ head + body×N + tail。WSE 侧：用户 Memory Stream 块 ≈ Message；fabric 上色通道传输的原子更接近 Flit/Packet（公开细节不足，作工程猜测）。

## 四种交换与延迟

| 方式 | 缓冲 | 空载延迟直觉 | 缓冲代价 |
|------|------|--------------|----------|
| **电路** | 预占通路 | setup + 数据；setup ∝ H | 低，但占链路 |
| **报文 (SAF)** | 每跳整包 | **∝ H × T_packet** | 大 |
| **虫孔 (WH)** | 每跳数 flit | setup + 流水；H 项 ≈ flit 级 | **小** |
| **VCT** | 足够装整包 | 空载≈WH；拥塞可整包停 | 中–大 |

空载粗公式（H 跳，路由器延迟 T_r，链路 T_w）：

| 方式 | 延迟 |
|------|------|
| SAF | ≈ H × (T_packet + T_r + T_w) |
| Wormhole | ≈ T_packet + H × (T_flit_setup + T_r + T_w)（头建路径后体流水） |
| VCT | 空载 ≈ WH；堵时接近 SAF |

笔记量级：WSE 规模 ~30 跳时，**虫孔可比 SAF 快一个数量级**——NoC 几乎必选 WH/VCT。

## HoL Blocking

虫孔下 head 卡住 → body 占满沿途缓冲/链路 → **无关目的地的报文也被堵**。抗性：SAF/VCT 较好（整包可让路），纯 WH 最差。解药：**虚通道** → [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md)。

## 与死锁

虫孔把资源依赖拉到「缓冲槽」粒度 → CDG/无死锁路由成为刚需。见 [Deadlock-Free Routing CDG](/concepts/deadlock-free-routing-cdg-dally.md)、[Duato Escape VC](/concepts/duato-escape-vc-deadlock-free-routing.md)。

## 选型直觉（AI / WSE）

| 场景 | 倾向 |
|------|------|
| PE–PE 短消息、延迟敏感 | Wormhole |
| 大突发、可接受缓冲 | VCT 或 WH+更大缓冲 |
| 固定带宽虚电路 | 电路 / TDM |

## 相关页面

- [Switching Principles](/concepts/switching-principles.md) — 电路→虫孔演进（电信视角）
- [Æthereal NoC](/concepts/aethereal-noc.md) — TDM 电路交换硬 GS vs 虫孔 BES
- [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md) — Day 16：VC + Credit
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — 实现层
- [NoC Router Pipeline and Allocators](/concepts/noc-router-pipeline-allocators.md) — Day 17
- [Cerebras WSE](/entities/cerebras-wse.md) — 虫孔 + color
- [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md)

# Citations

[1] [raw/articles/interconn-study-21d-day-15.md](raw/articles/interconn-study-21d-day-15.md) — D&T Ch.9 Flow Control（Day 15）
