---
type: Concept
title: Network Interface and System-Level Design
description: Dally & Towles Ch.13–14 — NI 翻译官；End-to-End；服务模型；流控 vs 拥塞控制；Max-Min Fairness；开环/闭环
tags:
- noc
- network-interface
- end-to-end
- congestion
- flow-control
- fairness
- rdma
- system-design
timestamp: '2026-07-21T00:00:00Z'
created: 2026-07-21
sources:
- raw/articles/interconn-study-21d-day-19.md
---

# Network Interface and System-Level Design（NI 与系统设计）

interconn-study **应用篇 Day 19**：Dally & Towles **Ch.13–14**——网络内部（拓扑/路由/流控/微架构）之外的**边缘与系统契约**。协议栈视角见 [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md)。

**Source:** [raw/articles/interconn-study-21d-day-19.md](raw/articles/interconn-study-21d-day-19.md)

## NI：三个职责、两个界面

| 职责 | 内容 |
|------|------|
| **Messaging** | Send/Recv、Remote R/W；内存语义 ↔ 包 |
| **Transport** | CRC、顺序、重传 |
| **Flow / Congestion** | Credit、ECN/pause、注入限速 |

| 界面 | 对端 | 协议 |
|------|------|------|
| Local | CPU/GPU/MEM | PCIe / CXL / 片上 bus |
| Network | Router | Packet / Flit / Credit |

关键硬件：Send/Recv Engine、Doorbell、CQ、DMA。传统主机 NI 厚（驱动 + DMA）；**WSE PE NI 极简**——本地 SRAM + 显式 send/recv，无 OS/TCP/完整 DMA（工程推测）。

## End-to-End Argument（Saltzer 1984）

可靠/安全功能的**完整检查必须在端点**；中间节点不可靠时端点仍要保证正确。

| 解读 | 含义 |
|------|------|
| **强** | 网络只转发；可靠/顺序/加密全在端点（TCP/IP） |
| **弱** | 网络尽力加速，端点仍做完整逻辑（TCP+ECN、PCIe 重传） |

链路 CRC/ECC 可加速，但不能替代端到端可靠。片上极高可靠时可简化链路级纠错，把重传放在 PE（WSE 倾向）。

## 服务模型

| 模型 | 顺序 | 可靠 | 路由器状态 | 典型 |
|------|------|------|------------|------|
| Datagram | ❌ | ❌ | 极小 | UDP/IP |
| Virtual Circuit | ✅ | ✅ | 中–大 | ATM、IB RC |
| Connectionless Reliable | ✅ | ✅ | 极小 | TCP |
| WSE 推测 | 视应用 | ✅ | 极小 | 类 datagram + 端点可靠 |

百万级 PE 难扛虚电路建立 RTT → 倾向无连接 + 端点语义。

## Flow Control vs Congestion Control

| | **Flow Control** | **Congestion Control** |
|--|------------------|------------------------|
| 尺度 | 微秒 / per-hop | 毫秒 / RTT |
| 目标 | 防本跳 buffer 爆 | 防全网过载 + 公平 |
| 信号 | Credit、Pause | ECN、ACK 延迟、速率 |
| 决策 | 路由器 + NI | 端点（可与网络协作） |

Credit **不解**全局拥塞——全网饱和时只会拖慢所有流并加剧 HoL。详见 [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md)。

拥塞位置：Source / Destination / Network-internal。WSE 笔记推测：**链路 credit + 编译时/端点 throttle**；路由器少主动丢包。

## Max-Min Fairness & 开环/闭环

- **Max-Min**：逐步抬升最受限流的份额，直至瓶颈饱和——拥塞控制公平性金标准；结构化 LLM 流量上可能改为 critical-path 优先。  
- **开环**：编译时预约/固定注入（HPC、静态调度推理）。  
- **闭环**：运行时反馈（TCP、DCQCN）。  
- WSE：**开环调度为主 + 局部 credit 闭环**。

## 相关页面

- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — NI 边界
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) / [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md)
- [Æthereal NoC](/concepts/aethereal-noc.md) — GS 预约 vs 端到端 BES
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md) — Day 20
- [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md) — Day 21
- [Cerebras WSE](/entities/cerebras-wse.md) / [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md)

# Citations

[1] [raw/articles/interconn-study-21d-day-19.md](raw/articles/interconn-study-21d-day-19.md) — D&T Ch.13–14（Day 19）
