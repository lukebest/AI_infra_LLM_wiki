---
type: Concept
title: Interconnection Network Protocol Stack
description: 互连网络四层协议栈（物理/链路/网络/传输）、Network Interface 边界，与 NoC 及 UB 的对应关系
tags:
- interconnect
- noc
- protocol
- physical-layer
- data-link
- transport
- flow-control
- fabric
- chiplet
- serdes
- fec
- scale-up
timestamp: '2026-08-20T00:00:00Z'
created: 2026-06-24
updated: 2026-08-20
sources:
- raw/articles/interconn-study-21d-day-02.md
- papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md
---

# Interconnection Network Protocol Stack（互连网络协议栈）

互连网络在**物理层到传输层**采用与 TCP/IP 类似的四层分解。各层职责边界清晰，便于将 NoC、scale-up fabric、scale-out 网络统一分析。

## 四层结构

```
┌────────────────────────────────────┐
│ 传输层 (Transport)                 │  ← 端到端可靠/有序、拥塞控制
├────────────────────────────────────┤
│ 网络层 (Network)                   │  ← 路由、包格式、拥塞信号
├────────────────────────────────────┤
│ 数据链路层 (Link)                  │  ← 错误检测、重传、链路训练、流控
├────────────────────────────────────┤
│ 物理层 (Physical)                  │  ← 编码、SerDes、信道
└────────────────────────────────────┘
```

| 层 | NoC 典型实现 | 职责 |
|----|-------------|------|
| **Physical** | 片上 wire、收发器 | 比特传输、编码、均衡 |
| **Link** | Credit-based 流控、ACK/NACK | 链路级可靠、VC 分配 |
| **Network** | XY / 自适应 / 确定性 color 路由 | 逐跳转发、死锁避免 |
| **Transport** | 端到端有序、拥塞控制 | 跨多跳的消息语义 |

## Network Interface (NI)

NI 是**计算与网络的边界**——连接 PE/CPU 核心与 Router：

```
   CPU/PE 核心
        ↑
   Network Interface (NI)
        ↑
   Router ←── flit ──→ Router
```

NI 决定：哪些 collective 可硬件卸载、哪些需软件参与、注入/egress 缓冲深度。WSE 与 [UnifiedBus UB](/entities/unifiedbus-ub.md) 均在 NI 处暴露不同抽象（CSL 数据流 vs URMA Jetty）。

## 与本 wiki 其他页面的映射

| 通用层 | UB 实现 | NoC / WSE |
|--------|---------|-----------|
| Physical | [UB 物理层](/concepts/ub-physical-layer.md) | 片上 wire、无 SerDes；chiplet 封装内则为 SerDes+FEC |
| Link | [UB 数据链路层](/concepts/ub-data-link-layer.md) | Credit 流控、VC（见 [NoC Router](/concepts/noc-router-microarchitecture.md)） |
| Network | [UB 网络层](/concepts/ub-network-layer.md) | 24-color 静态路由 |
| Transport | [UB 传输层](/concepts/ub-transport-layer.md) | 端到端 collective 语义 |

## Chiplet 封装内 PHY（相对片上 wire）

片上 NoC 把 Physical 当成 CMOS wire。跨 CCD/IOD 的短距 C2C 不是这条抽象：[DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) 在 gem5 里把这一跳建成 QC-LDPC + PAM4 + AWGN/jitter/crosstalk + LLR 解调 + 按 flit 重传。固定延迟 HeteroGarnet 会把延迟构成画得像 monolithic，IPC 相对 DICE 平均偏 6.8%、最高 27.6%（方向因负载而异）。晶圆级 hybrid bonding / field stitch 通常没有这层 SerDes，见 [Network-on-Wafer](/concepts/network-on-wafer.md)。

## 历史坐标

协议栈各层随互连介质演进：电话网铜线 → HPC 专用链路 → 硅片 NoC → 晶圆级单介质（[Cerebras WSE](/entities/cerebras-wse.md)）。详见 [Switching Principles](/concepts/switching-principles.md) 中的时代划分与里程碑。

## 相关页面

- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 设计空间顶层框架
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — 链路/网络层 Router 实现
- [Switching Principles](/concepts/switching-principles.md) — 交换方式与历史演进
- [UB 数据链路层机制](/concepts/ub-data-link-layer.md) — Credit 流控实例
- [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md) — NI / E2E / 拥塞（Day 19）
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — chiplet PHY 运行时模型（QC-LDPC / PAM4）
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — scale-up C2C 的 AXI/MAC/credit 层，不建模误码

# Citations

[1] [raw/articles/interconn-study-21d-day-02.md](raw/articles/interconn-study-21d-day-02.md) — Dally & Towles Ch.2 学习笔记（21 天互连研究 Day 2）
[2] [papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md](papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — Aligholipour et al., arXiv:2607.24221
