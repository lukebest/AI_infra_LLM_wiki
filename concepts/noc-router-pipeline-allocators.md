---
type: Concept
title: NoC Router Pipeline and Allocators
description: Dally & Towles Ch.11–12 — RC/VA/SA/ST/LT 五级流水；Crossbar；RR / Matrix / iSLIP / Wavefront 仲裁
tags:
- noc
- router
- pipeline
- crossbar
- arbitration
- islip
- virtual-channel
timestamp: '2026-07-13T00:00:00Z'
created: 2026-07-13
sources:
- raw/articles/interconn-study-21d-day-17.md
---

# NoC Router Pipeline and Allocators（路由器流水线与分配器）

interconn-study **微架构篇 Day 17**：Dally & Towles **Ch.11–12**——flit 进路由器后的五级路径与交叉开关仲裁。设计师视角补集见 [NoC Router 微架构](/concepts/noc-router-microarchitecture.md)；延迟优化见 [Day 18](/concepts/noc-router-pipeline-optimizations.md)。

**Source:** [raw/articles/interconn-study-21d-day-17.md](raw/articles/interconn-study-21d-day-17.md)

## 五级流水线

```
Input → RC → VA → SA → ST → LT → next hop
        路由  VC   开关  过开关  过链路
```

| 级 | 名称 | 做什么 | 备注 |
|----|------|--------|------|
| **RC** | Route Compute | 算输出端口 | 仅 head |
| **VA** | VC Allocation | 选输出 VC | 仅 head；常关键 |
| **SA** | Switch Allocation | 争用 Crossbar | **关键路径** |
| **ST** | Switch Traversal | 穿过 Crossbar | |
| **LT** | Link Traversal | 链路上发送 | 可与 ST 重叠 |

**Body/Tail** 通常只走 **SA → ST → LT**（省 RC/VA）。@1 GHz 标准五级 → 头延迟约 **5 ns/跳**（未做 look-ahead/投机优化前）。

## Crossbar

N 端口全连接：约 **N² crosspoint**。Mesh 路由器常见 **5×5**（N/E/S/W + Local）→ 25 点；面积/线延迟随 N² 恶化 → 推动 [High-Radix / CMesh](/concepts/noc-router-pipeline-optimizations.md) 权衡。

## Switch Allocator

| 仲裁器 | 思想 | 公平 / 吞吐 | 复杂度 |
|--------|------|-------------|--------|
| **Round-Robin** | 指针轮转 | 简单公平 | 低；难达最大匹配 |
| **Matrix Arbiter** | 优先级矩阵 | 强公平 | 中 |
| **iSLIP** | 多轮 request–grant–accept；指针延迟更新 | **高吞吐 + 公平** | 多轮，可流水 |
| **Wavefront** | 对角波前匹配 | 高吞吐 | 硬件波前逻辑 |

iSLIP（McKeown 1999）是输入排队交换机经典；笔记中 WSE SA **强候选**（非官方确认）。

## Head vs Body 时序

| Flit | 级数 | 直觉 |
|------|------|------|
| Head | 5（可优化到 3–4） | 建路径贵 |
| Body | 3 | 跟车流水 |

大规模 Mesh 上累加跳延迟 → 必须做 Day 18 优化（speculative SA、look-ahead、bypass）。

## 相关页面

- [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md) — Day 16：VA 前置
- [NoC Router Pipeline Optimizations](/concepts/noc-router-pipeline-optimizations.md) — Day 18
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — EB/credit/VA-SA 电路
- [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md) — Day 15
- [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md) — 高基数动机
- [Cerebras WSE](/entities/cerebras-wse.md)

# Citations

[1] [raw/articles/interconn-study-21d-day-17.md](raw/articles/interconn-study-21d-day-17.md) — D&T Ch.11–12（Day 17）
