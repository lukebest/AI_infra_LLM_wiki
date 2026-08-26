---
type: Raw Source
title: Hot Chips 2026 Samsung HBM Base Die
ingested: 2026-08-26
sha256: 30725ab71c49c7d3f135df27a702a06fe1b8cade5f15eb6ccde0f32f8db1047e
venue: Hot Chips 2026 Tutorial
---

# HBM Base Die: How HBM Will Evolve Using Advanced Logic Processes

**Speaker:** Sangwook Han, Ph.D.（Samsung Electronics Memory Business / DRAM Design Team；Design Lead, Custom HBM4E）  
**PDF:** [HC2026_Samsung_HBM_Base_Die.pdf](HC2026_Samsung_HBM_Base_Die.pdf)  
**Venue:** Hot Chips 2026 Tutorial

数字只取幻灯片正文；代际 BW/容量总图无刻度 → 未知。

## 摘录数字（仅幻灯片正文）

- C-die：**4/8/12/16** stacks → **~30–60 GB**；B-die 对 xPU：**1–2K IO**、**8–16 Gbps/IO** → **~1–5 TB/s**。
- 工艺：HBM2 (2016) C/B-die **2*nm**；HBM2E (2019) **1*nm**；HBM3 (2021) / HBM3E (2023) 仍 **1*nm**；**HBM4 (2026) / HBM4E (2027) B-die 改 4 nm logic**，C-die 仍 1*nm。xPU SoC 收到 **3 nm / <3 nm**。
- Samsung HBM4：**D1c + logic 4 nm**。
- sHBM4 B-die **11 mm × 12.8 mm**；HBM PHY **>8 mm × 4 mm**。代际 PHY/MPGA 见工作层。
- HPB：覆盖 **>50%** PHY 时峰值温度降 **>35%**。sHBM4E I/O **14 Gbps**、功率密度 **0.5 W/mm²**；sHBM5 I/O **>28 Gbps (2×)**、密度 **>2.0 W/mm²**。
- zHBM 假设 GPU **1200 W**、SiP 内 **4** 颗 HBM：相对 HBM4E 标 DRAM BW **230%**、**100 W saving**；I/O 功耗柱 **-70%**（柱高未知）。另有 **8.3%** 标注，所指轴未知。
- interposer 图示 **26 mm × 33 mm**。context window **30×/year**（Epoch.ai 2023–2025）。
