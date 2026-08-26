---
type: Paper
title: "Hot Chips 2026: OXMIQ HBF in AI Compute"
description: OXMIQ — HBF 是低 α/低 β 容量点不是更便宜的 HBM；72-GPU 机柜 ~14× 容量 / ~0.6× 带宽；HBM for the rack, HBF for the box
tags:
- oxmiq
- hbf
- hbm
- moe
- inference
- memory
- kv-cache
- serving
- architecture
- llm
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_OXMIQ_HBF_AI_Compute.pdf
- raw/papers/hc2026-oxmiq-hbf.md
---

# HBF in AI Compute: A System Architect's View

**Speakers:** Anurag Agrawal（OXMIQ Labs, System Architecture）；Radhakrishna Giduthuri（PRAXMATI, Software Architecture）  
**Venue:** Hot Chips 2026 Tutorial  
**PDF:** [raw/papers/HC2026_OXMIQ_HBF_AI_Compute.pdf](raw/papers/HC2026_OXMIQ_HBF_AI_Compute.pdf)

和已收录 [DASH](/papers/dash-dual-path-hbf-moe-inference.md)（GPU–HBF 双路径）成对：OXMIQ 给的是系统建筑师的 **(β, α)** 账和 72-GPU 机柜仿真，不是新硅。结论：HBF 只在低 I·b 区（小 batch MoE、稀疏长上下文 KV）赢；dense / 高 B 留 HBM。vLLM 还没有 MoE expert pool 插件。末页招聘不摘。

## HBF 硬件表

OCP HBF Architecture Specification **v0.7.0 (2026)**。口号：**8–16× HBM 容量、相同成本**。HBF 是低 α、低 β 的容量点，**不是**更便宜的 HBM。

| | Grade 1 | Grade 2 | Grade 3 |
|---|---|---|---|
| Max user BW | 0.384 TB/s | 1.536 TB/s | 3.072 TB/s |
| UCIe rate | 8 GT/s | 16 GT/s | 32 GT/s |
| Capacity | 8-high · 256 GiB | 16-high · 512 GiB | 16-high · 512 GiB |
| Access | 64 B–4 KiB reads · 4 KiB writes · 4 KiB page | 同左 | 同左 |
| Write endurance | Left open-ended | 同 | 同 |

部署三档（全文约定：HBM4/4e 对 HBF-G2，HBM5 对 HBF-G3）：

| | 容量 | 带宽 |
|--|------|------|
| HBM-only | **288 GB** | **22.0 TB/s** |
| All-HBF | **4,096 GB** | **12.8 TB/s** |
| **2×HBF + 6×HBM** | **1,240 GB** | **19.7 TB/s peak**（有效 BW 随 batch **19→4 TB/s**） |

同一成本，更多容量、更少带宽。

## Enquiry

- All-HBF 短上下文 **256/256** —— 低 B 时 $/token 赢，但 **85% dead capacity**，HBM 过墙后仍划算。
- 长上下文 **1M/1K** —— 只在 I·b 低时容量赢。
- HBM 作 hot-expert cache：混合查询下 expert 热度变平，缓存只在低 B 或「同类 query 一起 batch」时划算。

## 72-GPU 机柜仿真

Kimi-K2 **1T @ FP4**；主情景 1M in / 1K out；另有 32k/8k、1k/8k；batch 1–512/DP；3 年 capex+opex 比；decode-centric；平台标 **VR300 NVL72**。

| | HBM-only | HBF-only | HBF+HBM |
|---|---|---|---|
| 并行 | TP8 · DP9 | TP1 · DP72 | TP2 · DP36 |
| Mem / DP | 2.3 TB | 4.1 TB | 2.5 TB |
| Mem · rack | 20.7 TB (1×) | 294.9 TB (14×) | 89.3 TB (4.3×) |
| Agg BW | 1,584 TB/s | 922 TB/s (0.6×) | 1,418 → 279 TB/s |
| Per-GPU BW | 22.0 TB/s | 12.8 TB/s | 19.7 → 3.9 TB/s |
| Cost · power | 1× · parity | 1× · parity | 1× · parity |

同机柜同成本：HBF 买 **~14×** 容量、**~0.6×** 带宽。结论句：更便宜的 $/GB ≠ 更便宜的 $/token —— **HBM for the rack, HBF for the box**。

## 软件约束（同一 OCP spec）

满 BW 访问块 **64 KB reads、1 MB writes（64 KB 对齐）**；上电数据保持 **~24 h @ 85 °C**，生命周期 host 管；DMA 通路，**不是**给 GPU cache hierarchy 设计的；HBF+HBM 要两套内存管理；scratchpad SRAM **不能**直接读写 NAND；仔细管理可达 **~10-yr** 或吃满 endurance。

引擎焦点：**vLLM**（也列 SGLang / LMDeploy / Modular MAX / TRT-LLM / OpenVINO / AWS Neuron / JetStream）。

Kimi **K3 2.8T** 权重账：总权重 **1.56 TB**；attention **72.2 GB**；另一块 **30.2 GB**；**MoE 1.45 TB = 93%**；另 **4.7 GB**。1M token KV **30 GB**。HBF 适合 MoE expert 池 + KV offload/prefix-cache；剩下 ~7% 权重和热路径留 HBM。对照 [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md)。

vLLM 提案：HBF 替换 host pinned memory 做 paged KV offload + prefix + MoE experts；**MoE Experts Pool 插件尚无**。配置例：GPU **4×HBM + 4×HBF ⇒ 2.2 TB，~17.4 TB/s peak**。

机会：稀疏 attention（DSA / CSA / Kimi-Linear；引 DeepSeek-V3.2 / V4、Tutti 2605.03375、HiFC）才是 HBF 区。EP×HBF：容量换通信——例 **8 GPU expert shard + 每层 all-to-all** vs **2 node、expert 本地、几乎无 all-to-all**。

## 判据

**$mem = β · max(C, I·b/α)**，figure of merit **(β/α)·b**。HBF 只赢低 I·b。要扩大胜区：读 BW（α↑）、拉大 vs HBM 的 $/GB 差（β↓）、处理写 endurance/写 BW/延迟。软件前提：HBF allocator、placement、async prefetch、endurance telemetry。

> “HBF: A precision instrument, not a hammer — bargain in its zone, trap outside it”

## 与 wiki 的关系

- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — DASH 是 GPU–HBF 双路径硅/仿真方案；本文是机柜级 (β, α) 账，结论互补（HBF 不是万能容量层）
- [DRAM and Memory System](/concepts/dram-memory-system.md) — HBF 与 HBM 并列近 GPU，不是第三层 SSD
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — HBF 栈仍是 TSV 堆 NAND（与 DASH 一致）
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — HBF 换的是 expert 本地化，减少 all-to-all
- [Handy HBM 开场](/papers/hc2026-handy-hbm-tutorial.md) — 同场市场分母

# Citations

[1] [raw/papers/HC2026_OXMIQ_HBF_AI_Compute.pdf](raw/papers/HC2026_OXMIQ_HBF_AI_Compute.pdf) — Agrawal / Giduthuri, Hot Chips 2026 Tutorial
[2] [raw/papers/hc2026-oxmiq-hbf.md](raw/papers/hc2026-oxmiq-hbf.md) — 结构化摘录
