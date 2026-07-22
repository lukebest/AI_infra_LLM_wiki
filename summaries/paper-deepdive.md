---
type: Summary
title: Paper Deep-Dive Map
description: 论文精读专项 Day 1–8 地图：NoC 经典链 → VC/Clos → TPU v4 OCS vs NVLink 两条 scale-up 哲学
tags:
- paper
- methodology
- noc
- scale-up
- summary
- wse
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- raw/articles/paper-deepdive-overview.md
- raw/articles/paper-deepdive-day-01.md
- raw/articles/paper-deepdive-day-08.md
---

# Paper Deep-Dive Map（论文精读地图）

专项概述：[raw/articles/paper-deepdive-overview.md](raw/articles/paper-deepdive-overview.md)。方法底座：[Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md)（5 步 + 四武器 + 红旗）。

## Day 1–8 一览

| Day | 论文 | 概念 / 论文页 | Raw |
|-----|------|---------------|-----|
| 1 | Luczynski HPDC'24 Wafer-Scale Reduce | [WSE Reduce](/concepts/wse-reduce-algorithms.md), [paper](/papers/near-optimal-wafer-scale-reduce.md) | [day-01](raw/articles/paper-deepdive-day-01.md) |
| 2 | Dally & Towles DAC'01 Route Packets | [NoC Research Cases](/concepts/noc-research-methodology-case-studies.md), [paper](/papers/route-packets-not-wires.md) | [day-02](raw/articles/paper-deepdive-day-02.md) |
| 3 | Hoskote 5GHz Mesh / Polaris | 同上 + [paper](/papers/hoskote-5ghz-mesh-polaris.md) | [day-03](raw/articles/paper-deepdive-day-03.md) |
| 4 | Balfour MICRO'06 CMP tradeoffs | [CMP NoC Pareto](/concepts/cmp-noc-pareto-design-tradeoffs.md) | [day-04](raw/articles/paper-deepdive-day-04.md) |
| 5 | Dally TPDS'92 Virtual Channels | [VC Flow Control](/concepts/virtual-channel-flow-control.md), [paper](/papers/dally-virtual-channel-flow-control.md) | [day-05](raw/articles/paper-deepdive-day-05.md) |
| 6 | Kim SC'06 High-Radix Clos adaptive | [High-Radix Clos Adaptive](/concepts/high-radix-clos-adaptive-routing.md) | [day-06](raw/articles/paper-deepdive-day-06.md) |
| 7 | Jouppi ISCA'23 TPU v4 OCS | [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) | [day-07](raw/articles/paper-deepdive-day-07.md) |
| 8 | NVIDIA Hopper/Blackwell NVLink | [NVLink/NVSwitch](/concepts/nvlink-nvswitch-scale-up-fabric.md) | [day-08](raw/articles/paper-deepdive-day-08.md) |

## 叙事链

```
Day1 WSE Reduce ──依赖──► Day2 NoC 范式
                              │
                    Day3 工业 5GHz Mesh
                              │
                    Day4 CMP Pareto（Mesh+WH+VC）
                              │
              ┌───────────────┴───────────────┐
           Day5 VC 原典                    Day6 Clos 挑战 Mesh
              │                               │
              └───────────────┬───────────────┘
                              ▼
              Day7 TPU OCS（拓扑可重构）
                              │
                              ▼
              Day8 NVLink（固定拓扑+胖链路）
```

## 三条 scale-up 对照

| 路线 | 代表 | 旋钮 |
|------|------|------|
| 晶圆 Mesh | [WSE](/entities/cerebras-wse.md) | 规模 × 确定性片上带宽 |
| 可重构光 | [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md) | 拓扑随 workload |
| 胖链路 Clos | [NVLink](/concepts/nvlink-nvswitch-scale-up-fabric.md) | 每 hop 带宽 × 高基数 switch |

## 相关页面

- [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md)
- [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md)
- [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md)

# Citations

[1] [raw/articles/paper-deepdive-overview.md](raw/articles/paper-deepdive-overview.md)
[2] [raw/articles/paper-deepdive-day-01.md](raw/articles/paper-deepdive-day-01.md) … [day-08](raw/articles/paper-deepdive-day-08.md)
