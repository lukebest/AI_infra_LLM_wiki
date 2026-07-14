---
type: Concept
title: Æthereal NoC
description: Philips Æthereal — contention-free TDM 电路交换实现 Guaranteed Services；GS+BES；slot table；分布式/集中编程与路由器代价谱系
tags:
- noc
- aethereal
- guaranteed-service
- tdm
- qos
- circuit-switching
- wormhole
- philips
timestamp: '2026-07-14T00:00:00Z'
created: 2026-07-14
sources:
- raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf
- raw/papers/aethereal-network-on-chip.md
---

# Æthereal NoC（Æthereal 片上网络）

Goossens et al., *IEEE Design & Test*, 2005：[papers/aethereal-network-on-chip.md](/papers/aethereal-network-on-chip.md)。纲领：**Guaranteed Services（GS）** 对稳健 SoC 必要；片上可用 **contention-free routing** 做到硬吞吐/延迟界，并用 **BES** 回收闲置容量。

## 为何片上能做硬保证

| 问题 | 片外 | 片上（Æthereal 立场） |
|------|------|------------------------|
| 丢包 | 常见 → 只有统计保证 | 可靠 SoC + 流控 → 可无丢包 |
| 争用 | 延迟抖动 / 拥塞 | 用 **时分预约** 消除同时争用 |
| 大缓冲仲裁 | rate/deadline 可行 | 路由器缓冲太贵 → 不可接受 |

多媒体多流「同等重要」→ 纯优先级会退化成 BES；TDM 可给**不同带宽预约、同一优先级**。

## Contention-free routing

**流水线 TDM 电路交换**：连接打开期间预约线、缓冲与时隙。

```
Slot table T[S slots × N outputs]:
  T(s, o) = i  →  时隙 s：输入 i → 输出 o
  每 slot 每端口最多 1 block；下一 slot 转发
```

性质：

- **无争用 by construction**（每输出每 slot ≤1 输入）  
- 每跳延迟 = 1 slot；带宽 ∝ 块大小 / S  
- GS 块可**无 header**（路径在表里）  
- 单 block 输入队列即够；**路由器间 GS 无需链路流控**  
- store-and-forward 块推进 → **无死锁**（相对虫孔资源环）

同步：集中时钟，或邻居间 token/SDF 式分布式 slot 同步。

对照：[Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) 的电路/SAF/虫孔谱系；[Switching Principles](/concepts/switching-principles.md) 的 TDM。

## GS + BES

| | GS | BES |
|--|----|-----|
| 机制 | slot 预约 TDM | 虫孔 + 输入排队 + 源路由 |
| 优先级 | 高（占预约时隙） | 低（吃空闲/未用预约） |
| 缓冲 | 1 block | 多 flit + credit 流控 |
| 死锁 | 构造避免 | 靠路由策略 |

组合路由器：GS∥BES 共享开关/链路；BES 仅在无 GS 块时前进。

## 编程模型

| | Distributed | Centralized |
|--|-------------|-------------|
| 配置 | SetUp / TearDown / Ack（BES 系统包） | 根进程 / MMIO 写 NI（可无路由器 slot 表） |
| 优点 | 可扩展、一致 | 面积小、贴近当时 SoC |
| 代价 | 每路由器 slot 表 + RCU | 可扩展性差；GS 可能带 header |

拓扑仅强假设：**路径可逆**（TearDown 回退）。设计时冲突无关分配 → 运行时顺序无关仍确定性。

## 实现谱系（0.13 µm，文中表）

| 点 | Area | 备注 |
|----|------|------|
| GS-BE + 分布式 | 0.24 mm² @ 500 MHz | 可扩展端 |
| GS-BE + 集中 | 0.13–0.175 mm² | 中间 |
| **GS-only + 集中** | **0.033 mm² @ 1 GHz** | 便宜端；4 GB/s/port |

队列若用寄存器可占面积 ~80% → **最小 GS 队列 + 专用 FIFO** 是关键选择。

## 与现代确定性 NoC 对照

| | Æthereal GS | [Cerebras Color](/concepts/cerebras-color-mechanism.md) |
|--|-------------|----------------------------------------------------------|
| 确定性手段 | 全局/邻居同步 **时隙表** | 静态 **color 路由配置** |
| 粒度 | TDM slot × 连接 | wavelet/color 通道 |
| BES | 显式虫孔旁路 | 少见「软」旁路；偏全确定性 |
| 目标年代 | 多媒体 SoC QoS | 晶圆级 AI 数据流 |

同属「预配置 → 运行时无仲裁争用」家族；机制不同。亦见 [Deterministic Execution](/concepts/deterministic-execution.md)。

## 相关页面

- [papers/aethereal-network-on-chip.md](/papers/aethereal-network-on-chip.md) — 论文摘要
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) — 电路/虫孔/HoL
- [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md) — BES 侧 VC/Credit
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — 虫孔路由器
- [NoC Router Pipeline and Allocators](/concepts/noc-router-pipeline-allocators.md) — 现代 SA（对比「无仲裁 GS」）
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 流控层定位
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 现代加速器 NoC 另一极（collective 硬件）

# Citations

[1] [raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf](raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf)
[2] [raw/papers/aethereal-network-on-chip.md](raw/papers/aethereal-network-on-chip.md)
