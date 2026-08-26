---
type: Raw Source
title: Hot Chips 2026 Cerebras CS-4 Nexus
ingested: 2026-08-26
sha256: 6a3ce2998f1f6322bed7c629cd04ee2bdbe39d31b0a637be95fdceb584db6a9e
venue: Hot Chips 2026 Conference
---

# Rack-Scale Architecture for Wafer Scale Engine

**Speaker:** Jean-Philippe Fricker（Cerebras）  
**PDF:** [HC2026_Cerebras_CS4.pdf](HC2026_Cerebras_CS4.pdf)  
**Venue:** Hot Chips 2026 Conference

## 摘录数字（仅幻灯片正文）

- 3× WSE-3 Turbo。vs CS-3：compute **125→750 PFLOPS**；SRAM **44→132 GB**；mem BW **21.6→129.6 PB/s**；fabric **26.7→160.5 PB/s**；I/O **1.2→7.2 Tbit/s**；I/O latency **5→2 µs**。
- 单片 **43,200 TB/s** mem BW vs Rubin **22 TB/s**；wafer fabric **53.5 PB/s**。NVL72 引作 **260 TB/s** / **5,000 cables**。
- Direct Wafer Links + RoCE。Per-wafer I/O **2.4 Tb/s**；user net **3 µs**；wafer-to-wafer **2 µs**。
- 54.5 VDC；DC/DC **~0.5 mm** vs GPU **~50 mm**。CS-4 EA now，GA later Q3 2026。CS-6 FLOPS/BW 未知。
