---
type: Entity
title: MRC (Multipath Reliable Connection)
description: Multipath Reliable Connection：OpenAI/Microsoft/AMD/NVIDIA/Broadcom 联合设计的多路径
  RDMA 传输协议，包 spraying + 选择性重传，100K+ GPU 训练集群生产部署
tags:
- transport
- protocol
- routing
- load-balancing
- congestion-control
- nvidia
- amd
- retransmission
- scale-up
timestamp: '2026-05-13T00:00:00Z'
created: 2026-05-13
sources:
- raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md
---

# MRC (Multipath Reliable Connection)

## Overview

MRC 是 OpenAI、Microsoft、AMD、NVIDIA、Broadcom 联合设计的多路径 RDMA 传输协议，扩展 RoCEv2 Reliable Connection 层，用于 100K+ GPU AI 训练集群的后端网络。已在生产环境中用于训练 ChatGPT 和 Codex 等前沿模型。

规范以开放许可通过 OCP 发布。

## 核心机制

### 包 spraying 与 EV
- 每个 QP 启动时生成 **EV set**（通常 128-256 个 Entropy Value）
- 32-bit EV 嵌入 UDP source port + IPv6 flow label
- 发送方轮转 EV，将包均匀 spray 到所有平面和路径
- 不同发送方不协调 EV 选择，由 ECN 反馈做全局负载均衡

### 无 PFC 的 lossy 模式
- 主动禁用 PFC（Priority Flow Control），使用 best-effort Ethernet
- 原因：spraying + PFC 导致 head-of-line blocking，跨 collective 干扰

### 快速重传
- **SACK**：精确报告已接收包，触发选择性重传
- **NACK**：packet trimming 触发，payload 被 strip 后优先转发，接收方生成 NACK
- 丢包 → EV 立即退役 → backup EV 替换 → 背景探测定期复活

### ECN 负载均衡
- 中间交换机启用 ECN，最后一跳禁用
- 接收方回传 ECN 信号，发送方暂时避开拥堵路径
- 全双截面带宽下，ECN 充当负载均衡信号而非拥塞控制

### NIC 实现与部署
| NIC | 速率 | 集群 |
|-----|------|------|
| NVIDIA ConnectX-8 | 800 Gb/s | Cluster A (75K GPU), B |
| AMD Pollara | 400 Gb/s | Cluster C |
| Broadcom Thor Ultra | 400 Gb/s | Cluster D |

## 性能数据

| 指标 | 数值 |
|------|------|
| T0-local 延迟 | 5.09 µs |
| Cross-T1 延迟 | 6.54 µs |
| 带宽（T0-local / cross-T1）| ~770 Gb/s (96% peak) |
| NCCL @ 42K GPU | 92 GB/s |
| MRC 1 QP vs RoCE 16 QPs (all-reduce) | MRC 更优，因无 ECMP 碰撞 |

## 容错能力

- **T0-T1 link flap**：几乎无影响，MRC 自动避开，不急修
- **T1 switch reboot**：丢包 ~580K，job throughput 仅短暂下降，reboot 后无影响
- **NIC-T0 port failure**：数秒内重映射 EV，恢复到满速（少一平面）
- **NIC transceiver 全挂**：唯一真正的 SPOF（罕见）

## 与相关协议对比

| | MRC | RoCEv2 | UET |
|---|---|---|---|
| 多路径 | ✅ EV spraying | ❌ ECMP | ✅ spraying |
| 选择性重传 | ✅ SACK/NACK | ❌ Go-Back-N | ✅ |
| Packet trimming | ✅ | ❌ | ✅ |
| PFC | 禁用 | 依赖 | 禁用 |
| 路由 | 静态 SRv6 | 动态 BGP/ECMP | — |
| 实现复杂度 | RoCE 最小扩展 | 基线 | 全新协议栈 |

## 关系

- 扩展 [Roce](#roce) 协议族，借鉴 [Ultra Ethernet Transport](#ultra-ethernet-transport) 设计
- 与 [Multi Plane Clos Topology](/concepts/multi-plane-clos-topology.md) 和 [Srv6 Source Routing](/concepts/srv6-source-routing.md) 协同设计
- [Clustermapper](#clustermapper) 提供网络健康探测和 denylist 管理
- 与 [Nvidia Spectrum](#nvidia-spectrum) 交换机、[Nvidia Connectx 8](#nvidia-connectx-8) NIC 协同部署

# Citations

[1] [raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md](raw/articles/resilient-ai-supercomputer-networking-mrc-srv6.md)
