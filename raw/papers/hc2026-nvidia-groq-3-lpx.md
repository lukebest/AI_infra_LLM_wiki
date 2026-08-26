---
type: Raw Source
title: Hot Chips 2026 NVIDIA Groq 3 LPX / LP30
ingested: 2026-08-26
sha256: 46cdba46e07a160ff1de264a8d35b059dade9b70524bbb2c06b3b340e1a2ff81
venue: Hot Chips 2026
---

# Think Fast: LPU Accelerator for Heterogeneous Compute

**Speakers:** Igor Arsovski, Santosh Raghavan（NVIDIA）  
**PDF:** [HC2026_NVIDIA_Groq_3_LPX.pdf](HC2026_NVIDIA_Groq_3_LPX.pdf)  
**Venue:** Hot Chips 2026 Day 2

TPS/MW 曲线绝对值 **未知**。

## 摘录数字（仅幻灯片正文）

- Gemma 4 31B：**10,996 TPS/user**，16K ISL / max **264K** context。SPEED-bench **4,767** median output tok/s。AA 100K context：**4×** 更快长上下文 decode。
- LPX：**256 LPU**；**128 GB** SRAM；**315 PFLOPs FP8**；**40 PB/s** 聚合 SRAM；C2C **350 ns** SRAM→SRAM。
- 可达 SRAM 延迟：0.35 µs @ 8 GB … 2.95 µs @ 1152 GB。扩展到 **1000+** LPU。
- PEP：>60% 更少 droop，>70% 更少 overshoot。确定性热目标每块 **105 °C**（非确定例 **128 °C**）。
- 与 72 Rubin 三种拆分：draft / ATTN-FFN / prefill-decode。GPT-OSS-2T 相对 NVL72-only：**~3× / ~3× / ~5×** 交互。
