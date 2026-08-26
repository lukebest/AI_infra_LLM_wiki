---
type: Raw Source
title: Hot Chips 2026 NVIDIA Rubin GPU
ingested: 2026-08-26
sha256: d3b9ba23a45645feb223fb02aba4f033a7d42f11ac1be4b322360c2910bda5a3
venue: Hot Chips 2026 Conference
---

# NVIDIA Rubin GPU: Driving the Era of Agentic AI

**Speakers:** Manas Mandal, Raj Dash, Rouslan Dimitrov（NVIDIA）  
**PDF:** [HC2026_NVIDIA_Rubin.pdf](HC2026_NVIDIA_Rubin.pdf)  
**Venue:** Hot Chips 2026 Conference

## 摘录数字（仅幻灯片正文）

- 七芯片、五机架。Agentic 输入 **32k & 100k & 400k**。
- AgentX（Unofficial / pending SemiAnalysis）：DeepSeek-v4-PRO **140K+** context；TPS/MW 轴到 **60M**，TPS/User 轴到 **300**；vs GB300 标 **2X / 10X / 30X**。绝对坐标未知。
- **100 MW factory**（不是单 GPU）：NVFP4 inference **2 ZFLOPS**；training **1.4 ZFLOPS**；HBM4 **11 PB** / **800 PB/s**。单卡 HBM/TDP/工艺未知。
- NVLink 6：**72 GPU**；**3.6 TB/s per GPU all-to-all**；相对 Ethernet **3x** 更低延迟、**130 TFLOPS** in-network、**10x** packet rate。**4X** 分母未知。
- 2:4 sparsity：「**2x** faster downstream SoftMax and BMM2」。Counted writes 延迟 µs 未知。
- MGX：**80+** partners；**350+** sites / **30** countries；TCS **45/55 °C**；**800 VDC**。Power smoothing **13%**；「up to **40%** more GPUs per provisioned watt」。
