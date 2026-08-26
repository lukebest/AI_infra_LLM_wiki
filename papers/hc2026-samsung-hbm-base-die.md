---
type: Paper
title: "Hot Chips 2026: Samsung HBM Base Die (cHBM / aHBM / zHBM)"
description: Samsung — HBM4/4E B-die 改 4 nm logic；cHBM 卸 MC/PHY，aHBM 加 PE，zHBM 用 WoW+HCB 取消 2.5D interposer
tags:
- samsung
- hbm
- 3d
- tsv
- hybrid-bonding
- packaging
- chiplet
- memory
- architecture
- through-silicon-via
- wafer-on-wafer
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_Samsung_HBM_Base_Die.pdf
- raw/papers/hc2026-samsung-hbm-base-die.md
---

# HBM Base Die: How HBM Will Evolve Using Advanced Logic Processes

**Speaker:** Sangwook Han, Ph.D.（Samsung Electronics Memory Business / DRAM Design Team；Design Lead, Custom HBM4E）  
**Venue:** Hot Chips 2026 Tutorial  
**PDF:** [raw/papers/HC2026_Samsung_HBM_Base_Die.pdf](raw/papers/HC2026_Samsung_HBM_Base_Die.pdf)

把 HBM 从标准 JEDEC 栈改写成可定制 logic B-die，最终 **zHBM** 取消 2.5D interposer。数字只取幻灯片正文；代际 BW/容量总图无刻度 → **未知**。对照 [SK hynix HyB](/papers/hc2026-skhynix-hbm-advanced-packaging.md) 的封装侧。

## 角色拆分

| | C-die | B-die |
|--|-------|-------|
| 职责 | DRAM cell & core | 对 xPU 通信（PHY–TSV）+ C-die 测试（DA / MBIST / IEEE1500） |
| 栈 / 容量 | **4/8/12/16** stacks → **~30–60 GB** | — |
| 工艺 | D1a/D1b/D1c…（1*nm） | HBM4 起 **4 nm logic** |
| xPU 侧 | — | **1–2K IO**、**8–16 Gbps/IO** → **~1–5 TB/s** |

BW 缩放主瓶颈：TSV 数量与 pitch；B-die PHY I/O 数量与速率。代际 DQ 数 / DQ 速度 / TSV 面积图无可读刻度 → **未知**。

## 工艺年表（幻灯片表格）

| 代 | 年 | C/B-die | xPU SoC |
|----|----|---------|---------|
| HBM2 | 2016 | **2*nm** | 16n/12nm |
| HBM2E | 2019 | **1*nm** | 8n/4nm |
| HBM3 / HBM3E | 2021 / 2023 | 仍 **1*nm** | 4nm |
| **HBM4 / HBM4E** | **2026 / 2027** | C-die 1*nm；**B-die 4 nm logic** | **3 nm → <3 nm** |

HBM4 起必须用先进 logic 压 B-die 功耗；B-die 与 xPU 工艺差在收窄。Samsung 在 HBM4 上同时用 **D1c + logic 4 nm**。目标：降功耗、缩 active area。MPGA 功耗仍涨，pJ/b 在改善（具体 W / pJ/b **未知**）。TSV-to-PHY repeater 的 Power/Delay 柱图有 DRAM/14/8/5/4 nm 轴，柱高 **未知**。

**sHBM vs cHBM**：标准 B-die 只做 data/test path；custom HBM 共用标准 C-die 栈、定制 B-die logic。

## Phase #1 — xPU 面积回收

传统缩放撞墙：节点变慢、monolithic 到 reticle、multi-chiplet interposer 到物理极限（图示 interposer **26 mm × 33 mm**，双 xPU + 多 HBM）。方案：用已是 logic 工艺的 B-die 卸 xPU 功能。

sHBM PHY 是 B-die 最大块；cHBM 用先进 logic 换成 **D2D**。sHBM4 B-die 图注 **11 mm × 12.8 mm**；HBM PHY **>8 mm × 4 mm**。

| 代 | MPGA | PHY / D2D | CH depth |
|----|------|-----------|----------|
| HBM2 | **11.87 × 7.75 mm** | PHY **6 × 1.2 mm** | **3.5 mm** |
| HBM3 | **10.75 × 10.75 mm** | PHY **8 × 3 mm** | **4.5 mm** |
| sHBM4 | **11 × 12.8 mm** | PHY **8 × 4 mm** | **5.5 mm** |
| cHBM4 | — | D2D **8.5 × 1.5 mm** | **2 mm** |
| sHBM5 | **10.7 × 16.3 mm** | PHY **9.5 × 1.7 mm** | **2 mm** |
| cHBM5 | — | D2D/CH **?**（幻灯片原文问号） | — |

好处：更短 channel → 更低 pJ/b；代价：PHY 缩小后功率密度变热斑。

**HPB (Heat Path Block)**：硅 dummy 热通路，来自 cHBM4 经验。覆盖 **>50%** PHY 时峰值温度降 **>35%**。

| | I/O | 功率密度 |
|--|-----|----------|
| sHBM4E | **14 Gbps** | **0.5 W/mm²** |
| sHBM5 | **>28 Gbps (2×)** | **>2.0 W/mm²** |

继续：把 **memory controller** 卸到 cHBM B-die（热开销称 manageable；“正在 port”）。再用 B-die SRAM 做 **cell-level repair**（相对 C-die row/col spare：资源更多、可跨 channel 共享）。

## Phase #2 — aHBM

C-die 栈钉死 footprint，MC 卸完 B-die 仍有未用硅。加 SoC 级 RAS（热/电压/工艺/老化传感器）、on-die ATE/PGEN。动机：context window **30×/year**（Epoch.ai 图，2023–2025）；AGI 分数图里 Memory Storage / Retrieval 是短板（arxiv 2510.18212）。

外沿 shoreline 接 **external memory**（B-die 里放 extension PHY/controller + D2D NoC），称比 PCIe 扩展更高 BW、更低延迟。再把部分 PE 卸到 B-die 减 D2D BW。**aHBM**：B-die 内 PE + MC，尽量不在 interposer 上搬数据。

## Phase #3 — zHBM

xPU 与 C-die **真 3D 垂直叠**，去掉 2.5D interposer；distributed I/O，取消 HBM PHY/D2D；interlayer die ≈ 原 B-die。关键工艺：**WoW + HCB (hybrid copper bonding)** + 统一 SoC–DRAM 设计流。

好处（正文）：去掉 SERDES（data align / DQ I/O）；I/O 功耗柱标 **-70%**（HBM4 / HBM5 / zHBM，柱高未知）。系统假设 **GPU 1200 W、SiP 内 4 颗 HBM**：1×GPU+4×HBM4E vs 1×GPU+4×zHBM，DRAM BW 标 **230%**，**100 W saving**；另有一个 **8.3%** 标注，所指轴 **未知**。

三阶段收束：#1 紧凑 D2D + MC offload 回收 xPU 面积；#2 telemetry / 外存扩展 / PE；#3 zHBM 取消 2D/2.5D 界面。

## 与 wiki 的关系

- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — zHBM 把 HBM 从 2.5D TSV 栈推进到 WoW + HCB
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — 当前 BW 瓶颈仍是 TSV 数量与 pitch
- [Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md) — HCB = hybrid copper bonding
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 这里的 WoW 是 xPU-on-C-die，**不是**晶圆级 NoW 重叠网
- [DRAM and Memory System](/concepts/dram-memory-system.md) — B-die 定制把 HBM 从 JEDEC 栈改成 logic 近存
- [SK hynix packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md) — 同场 HyB vs MR-MUF；SK 引 Samsung HPB+HCB ~30% 温度 ↓

# Citations

[1] [raw/papers/HC2026_Samsung_HBM_Base_Die.pdf](raw/papers/HC2026_Samsung_HBM_Base_Die.pdf) — Sangwook Han, Hot Chips 2026 Tutorial
[2] [raw/papers/hc2026-samsung-hbm-base-die.md](raw/papers/hc2026-samsung-hbm-base-die.md) — 结构化摘录
