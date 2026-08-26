---
type: Paper
title: "Hot Chips 2026: NVIDIA Vera CPU"
description: NVIDIA — Vera agent CPU；88 Olympus / 176 threads；NVLink-C2C 1,800 GB/s；SCF 3.4 TB/s；1.5 TB SOCAMM LPDDR5X @ 1.2 TB/s；CXL 3.1；256-Vera rack
tags:
- nvidia
- cpu
- scale-up
- cxl
- memory
- inference
- rack
- interconnect
- architecture
- agentic-ai
- memory-bandwidth
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_NVIDIA_Vera.pdf
- raw/papers/hc2026-nvidia-vera.md
---

# NVIDIA Vera CPU

**Speakers:** Jonathon Evans, Polychronis Xekalakis（NVIDIA）  
**Venue:** Hot Chips 2026 Conference  
**PDF:** [raw/papers/HC2026_NVIDIA_Vera.pdf](raw/papers/HC2026_NVIDIA_Vera.pdf)

Rubin 工厂里的 **agent CPU**。更新 [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) 与 [Vera ETL256](/entities/vera-etl256.md)。同场 GPU 见 [Rubin](/papers/hc2026-nvidia-rubin.md)。CXL 侧对照 [CXL Tiered Memory](/concepts/cxl-tiered-memory.md)。单 socket GHz / TDP：**未知**。

## 工厂角色与微结构

与 Rubin 同一工厂图：七芯片 / 五机架。Vera CPU rack 角色：**tool calls and sandboxes**。NVL72 仍是「Foundation of Every AI Factory」。同一 unofficial AgentX 图：DeepSeek-v4-PRO，**140K+** context，相对 GB300 NVL72 最高 **30X** TPS/MW（*Pending Semi-Analysis Review*）。LPX 旁注（不是 Vera 微结构）：「in full production」；Artificial Analysis **100K** context；「**4X** faster long-context decode」vs 未点名对照。

定位：「max single-threaded CPU at scale」。**88** Olympus cores / **176** threads。对照：Chromium 用 AMD EPYC **9655P**（96/192）；SPECrate 2026 用 EPYC **9755**（pre-production Vera，estimated）。封装对照：「traditional chiplet」vs Vera **monolithic compute die**。

Headless Chromium：「up to **4.5X**」靠去掉 rendering + caching reuse；Speedometer-with-Chromium「**24%** faster」vs traditional CPU，浏览器实例轴到 **200**。

Olympus 标注：L1I **64 KB 4-way**；ITLB **64e FA**；fetch **128 B/cycle**，**16** inst/cycle；decode queue **48**；**10-way** decode；**10** fused inst；**10 uOPs/cycle** rename/commit；L2 **2 MiB 8-way**；STLB **3k**；L1D **96 KB 6-way**；DTLB **112e FA**；L1 I/D **32 B/cycle**。单一 ALU 计数 **未知**。

**Spatial multithreading**（不是 x86 SMT）：isolation / determinism。SPECint 2017 Rate-1「rate-1 of thread with noisy neighbor」Vera 峰约 **13.0**（traditional 轴上精确数 **未知**）。Loaded per-core perf：traditional **67%** vs Vera **100%**。

SPECrate 2026_int_base vs EPYC 9755：Python/cpython **1.8X**；gcc **1.7X**；cppcheck **1.7X**；llvm **1.7X**；gem5 **1.7X**；横幅「**1.8X Agentic** / **1.7X EDA** / **1.5X Data Processing**」。功耗：核数升到 **88** 仍 provisioned；traditional 画成 droop（给定 N 的绝对瓦数 **未知**，Y 轴到 **500 W**）。

## 内存 / SCF / I/O

「industry-first」datacenter **LPDDR5X-9600**；bandwidth/W **5X** vs 16-ch DDR5-8000 和 12-ch DDR5-6400（这两档 = **1X**）；16-ch MRDIMM DDR5-12800 = **0.8X**。封装：**1.5 TB SOCAMM LPDDR5X**，**1.2 TB/s** memory BW。

On-die：**2nd-gen Scalable Coherency Fabric (SCF)**；**164 MB L3**；**3.4 TB/s** bisection。数据处理：p99 streaming latency「up to **6X**」vs 「traditional CPU」/ EPYC Turin。绝对 µs **未知**。

I/O：**4.3 TB/s** aggregate off-die。**NVLink-C2C 1,800 GB/s** coherent CPU–GPU。**x16 PCIe Gen6**，**256 GB/s**，**CXL 3.1**。NVL72 安全页：**72** Rubin GPUs + **36** Vera CPUs + **18** BlueField-4 + STX。收束：Vera 液冷架 **256 Veras / 22,528 Olympus cores**；NVL72 **72 GPUs / 36 CPUs**。

# Citations

[1] [raw/papers/HC2026_NVIDIA_Vera.pdf](raw/papers/HC2026_NVIDIA_Vera.pdf) — Evans / Xekalakis, Hot Chips 2026
[2] [raw/papers/hc2026-nvidia-vera.md](raw/papers/hc2026-nvidia-vera.md) — 结构化摘录
