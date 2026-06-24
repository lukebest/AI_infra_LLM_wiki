---
type: Concept
title: Switching Principles
description: 交换原理基础：电路交换/分组交换，三对基本概念，交换系统结构
tags:
- fabric
- routing
- deterministic
- tdm
- topology
timestamp: '2026-05-08T00:00:00Z'
created: 2026-05-08
sources:
- raw/articles/浅谈交换原理（1）——概述.md
---

# Switching Principles（交换原理）

交换是通信网的核心机制：在源和目的终端之间建立通信信道、传送信息。当多终端需要互连时，全互连需要 N(N-1)/2 线对 + 每终端多路选择开关 → 引入交换节点降低复杂度。

通信网三要素：**终端设备、交换设备、传输设备**。

## 三对基本概念

### 1. 面向连接 vs 无连接
- **面向连接**：先建连接 → 传信息 → 释放连接。又分物理连接（独占通路）和逻辑连接（虚电路）
- **无连接**：边选路边传递，每个分组独立路由

### 2. 同步时分复用 vs 统计时分复用
- **同步 TDM**（位置化信道）：按时间轴位置区分信道，无信息时也占位，子信道速率恒定
- **统计 TDM**（标志化信道）：用标志码标识信道，与时间位置无关，统计复用提高利用率

### 3. 固定带宽 vs 动态带宽
- 固定分配：每信道带宽恒定
- 动态分配：按需分配（类似潮汐车道）

## 交换方式

### 电路交换（Circuit Switching）

最早、最普遍的交换方式（电话网，100+ 年历史）。

三阶段：连接建立 → 信息传送 → 连接拆除

| 特性 | |
|------|--|
| 连接方式 | 面向连接（物理连接） |
| 复用 | 同步 TDM（固定带宽） |
| 差错控制 | 无 |
| 信息处理 | 透明传输（不作处理） |
| 流量控制 | 呼叫损失制（拒绝超额请求） |

### 分组交换（Packet Switching）

存储-转发机制，以分组为单位交换。源自报文交换，但分组更小所以更快。

| 特性 | |
|------|--|
| 连接方式 | 面向连接（逻辑）或无连接 |
| 复用 | 统计 TDM（动态带宽） |
| 差错控制 | 有 |
| 信息处理 | 处理首部、路由 |
| 流量控制 | 呼叫延迟制（排队等待） |

两种模式：

| | 虚电路 (VC) | 数据报 (DG) |
|--|-------------|-------------|
| 连接 | 面向连接（逻辑） | 无连接 |
| 分组头 | 简单（逻辑信道号） | 复杂（完整选路信息） |
| 选路 | 基于虚连接表（建立时一次性） | 每分组独立选路 |
| 顺序 | 保序 | 可能失序 |
| 故障敏感性 | 敏感（连接中断需重建） | 不敏感（自动重路由） |
| 适用 | 连续数据流 | 询问/响应型 |

## 交换系统基本结构

```
┌─────────────────────────────────────┐
│           控制系统                   │
│  控制结构、多处理机架构              │
├─────────┬──────────┬────────────────┤
│ 接口技术 │ 交换网络  │ 信令技术       │
│ 用户/中继│ 互联拓扑  │ 用户/局间信令  │
│ 模拟/数字│ 选路策略  │               │
│         │ 阻塞特性  │               │
│         │ 多播/故障 │               │
└─────────┴──────────┴────────────────┘
```

## 与 AI 基础设施的关联

- **[Deterministic Execution](/concepts/deterministic-execution.md)**：电路交换的确定性通路思想与 LPU 确定性执行一脉相承
- **Scale-up fabric**：NVLink/C2C 网络本质上是高速电路交换/虚电路（固定路径、低 jitter）
- **Scale-out fabric**：Ethernet/IP 网络是数据报模式（无连接、逐跳路由）
- **TDM 概念**：同步 TDM 对应固定时隙调度，统计 TDM 对应 packet switching → 理解 [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) 中 C2C 确定性互联 vs Spectrum-X Ethernet 的设计选择
- **虚电路 vs 数据报**：AFD 中 token routing 的 dispatch/combine 操作需要在确定性路径（虚电路式）和灵活路由（数据报式）之间权衡

## 相关页面
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行（与电路交换思想对应）
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX C2C 网络（确定性互联）
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — AFD token routing

# Citations

[1] [raw/articles/浅谈交换原理（1）——概述.md](raw/articles/浅谈交换原理（1）——概述.md)
