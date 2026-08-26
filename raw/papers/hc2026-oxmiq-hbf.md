---
type: Raw Source
title: Hot Chips 2026 OXMIQ HBF in AI Compute
ingested: 2026-08-26
sha256: 784dbff9e73c3344d823137398360186fd3087a839f297ec29c5466a14cd3f7e
venue: Hot Chips 2026 Tutorial
---

# HBF in AI Compute: A System Architect's View

**Speakers:** Anurag Agrawal（OXMIQ Labs, System Architecture）；Radhakrishna Giduthuri（PRAXMATI, Software Architecture）  
**PDF:** [HC2026_OXMIQ_HBF_AI_Compute.pdf](HC2026_OXMIQ_HBF_AI_Compute.pdf)  
**Venue:** Hot Chips 2026 Tutorial

OCP HBF Architecture Specification **v0.7.0 (2026)**。末页招聘不摘。

## 摘录数字（仅幻灯片正文）

- Grade 1/2/3：Max user BW **0.384 / 1.536 / 3.072 TB/s**；UCIe **8 / 16 / 32 GT/s**；Capacity **8-high · 256 GiB** / **16-high · 512 GiB** / **16-high · 512 GiB**。
- 口号：**8–16× HBM 容量、相同成本**。
- 部署：HBM-only **288 GB · 22.0 TB/s**；All-HBF **4,096 GB · 12.8 TB/s**；**2×HBF + 6×HBM** **1,240 GB · 19.7 TB/s peak**（有效 BW 随 batch **19→4 TB/s**）。
- 72-GPU 机柜（Kimi-K2 **1T @ FP4**；平台 **VR300 NVL72**）：HBM-only Mem·rack **20.7 TB**、Agg BW **1,584 TB/s**；HBF-only **294.9 TB (14×)**、**922 TB/s (0.6×)**；HBF+HBM **89.3 TB (4.3×)**、**1,418 → 279 TB/s**。
- 软件：满 BW 访问块 **64 KB reads、1 MB writes（64 KB 对齐）**；上电保持 **~24 h @ 85 °C**；可达 **~10-yr** 或吃满 endurance。
- Kimi K3 **2.8T**：总权重 **1.56 TB**；attention **72.2 GB**；另一块 **30.2 GB**；**MoE 1.45 TB = 93%**；另 **4.7 GB**。1M token KV **30 GB**。
- vLLM 配置例：GPU **4×HBM + 4×HBF ⇒ 2.2 TB，~17.4 TB/s peak**。MoE Experts Pool 插件尚无。
- 判据：**$mem = β · max(C, I·b/α)**。
