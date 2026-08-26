---
type: Paper
title: "Hot Chips 2026: SK hynix HBM Advanced Packaging"
description: SK hynix — HBM4 12Hi 量产/16Hi Qual；HyB 才能 ≥20Hi、pitch <18 μm；i-HBM 热阻 >30% ↓；对照 Samsung HPB/zHBM
tags:
- sk-hynix
- hbm
- 3d
- tsv
- hybrid-bonding
- packaging
- memory
- architecture
- through-silicon-via
- microbump
- cu-cu
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_SK_hynix_HBM_Advanced_Packaging.pdf
- raw/papers/hc2026-skhynix-hbm-advanced-packaging.md
---

# Advanced Packaging for High Bandwidth Memory (HBM)

**Speaker:** Jaesik Lee（SK hynix America，VP of Package Engineering）  
**Venue:** Hot Chips 2026 Tutorial  
**PDF:** [raw/papers/HC2026_SK_hynix_HBM_Advanced_Packaging.pdf](raw/papers/HC2026_SK_hynix_HBM_Advanced_Packaging.pdf)

公开数字把 16Hi 量产挑战、**HyB 才能 ≥20Hi**、以及 CoWoS-S/R/L 对 HBM 应力写清楚。相对倍率（0.5× gap、0.40× 热阻）保留原文，不换算成绝对 μm。对照 [Samsung B-die / zHBM](/papers/hc2026-samsung-hbm-base-die.md)。

## 结构（引 ISSCC 2024）

HBM = base die + 最多 **16** 片 core die，TSV 3D 叠；**4 slices/rank、4 ranks/16Hi**；每 slice **4 channels / 16 banks**。GPU+HBM 在 Si interposer 上 2.5D，**1024 IOs / 16 channels**。（后文 HBM4 表是 2048 IO——代际不同，勿混。）

空间/容量/BW/能效对照（ISMP 2024）：GDDR6 ×12 = **24 GB / 768 GB/s** vs HBM3E ×4 = **144 GB / 4 TB/s**，面积 **-50%**。

| | DDR4 | GDDR6 | HBM3 | HBM3E |
|--|------|-------|------|-------|
| 单器件 BW | **5.4 GB/s** | **56 GB/s**（×12.8 vs DDR4） | **717 GB/s**（×18.3 vs GDDR6） | **1024 GB/s** |
| 能效归一 | **1.0** | **0.82** | **0.33** | **0.29**（标 70%） |

## 代际表（正文）

| | HBM2E | HBM3 | HBM3E | HBM4 |
|---|---|---|---|---|
| Density (Gb) | 16 | 16 | 24 | 24 |
| Capacity | 16 GB | 24 GB | 36 GB | 36 GB |
| Total I/O | 1024 | 1024 | 1024 | 2048 |
| IO Speed (Gbps) | 3.6 | 5.6 | 8 | 8 |
| Max BW (GB/s) | 460 | 717 | 1024 | 2048 |
| PKG size | 10×11 | 11×11 | 11×11 | 12.4×11 |

HBM4 立方另一页（与上表不完全同字）：**>2 TB/s** BW，**40+% lower power efficiency**（原文用词），热阻比 HBM3E 好 **14+%**，容量最高 **48 GB**（**12Hi 量产，16Hi under Qual**），Z 高 **775 μm**，平面 **12.8×11 mm²**，**16148** base micro-bumps，**>20K** TSVs。

HBM4+ 带宽：data IO 从 ~1K（HBM3E）扩到 **>1K（HBM4）**；速度/IO 路径写 HBM2E **0.5 TB/s**、HBM3 **0.7 TB/s**、HBM3E **1.18 TB/s** → HBM4 **2.0 TB/s (Logic)**。功耗：logic foundry B-die + “power TSVs spread everywhere”，标 **75% PDN improvement**（ISSCC 2024）。

## 键合两路线

| | TC+NCF | MR+MUF |
|--|--------|--------|
| 工艺 | 热压 + 非导电膜 | mass reflow + molded underfill |
| 优点 | 对薄片翘曲不敏感 | 产能高、热阻低 |
| 缺点 | 逐片键合产能低、热阻高 | 对翘曲敏感、gap-fill 窄 |

HBM3E **16Hi @ 48 GB/cube** 靠 advanced MR-MUF。12Hi→16Hi：总封装高 **720 → 775 μm**；chip thickness **1.0× → 0.9×**（die warpage）；gap-height **1.0× → 0.5×**（gap-fill）；bump pitch **1.0× → 0.9×**。栈世代标注：8Hi HBM2E~，12Hi HBM3~，16Hi HBM4~，>16Hi 往后。

容量/热路线：8Hi/12Hi mass production，16Hi development，**≥20Hi research**。热阻技术轴：TC-NCF → MR-MUF → Adv. MR-MUF → **HyB**；相对热阻收到约 **0.40×**（HBM4E / HyB 一档）。中间档有 0.55–0.65×、0.45–0.55× 区间。

## Hybrid bonding（HyB）

流程：室温 pick & place 做 **SiO₂–SiO₂**，再 **>200 °C** anneal 做 **Cu–Cu**。相对 MR-MUF：同样限高下 core die 可厚最多 **24%**（20Hi vs 20Hi）；bump pitch **below <18 μm**（MR-MUF 轴标 30/20/10/5，HyB 落在更窄侧）。卖点：≥20Hi 容量、更窄 pitch、更高热导。

**“Hybrid bonding is a promising more memory capacity (≥ 20Hi), more performance (narrow pitch) and more thermal efficiency.”**

## 竞品热方案（SK 引用公开源）

| | 方案 | 数字 |
|--|------|------|
| SK **i-HBM** | 热 D2D PHY 区埋高导热电绝缘冷却件 | 热阻 **>30%** ↓ |
| Samsung **HPB + hybrid copper bonding** | 硅 dummy 热通路 + HCB | ~**30%** 温度 ↓、热阻抗 **16%** ↑（原文 “improvement in thermal impedance”） |
| Micron | 电路 + 增强 base die | 能效 **>20%** ↑ |

系统集成：过去 memory 最后装；AI 先进封装里 HBM **第一步** 装，可靠性更难。封装菜单：CoWoS-S / CoWoS-R（RDL interposer）/ CoWoS-L（ITPS Si+EMC、EMIB）及 PKG-to-PKG → D2D-on-interposer → Die-on-Die。应力图无数字。

## 与 wiki 的关系

- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — HyB 是 HBM4E 之后 ≥20Hi 的键合拐点；HBM4 本体仍是 MR-MUF / TSV
- [Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md) — 室温 SiO₂ + >200 °C Cu–Cu；pitch <18 μm vs MR-MUF
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — HBM4 **>20K** TSVs + power TSVs 铺满，标 75% PDN
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 代际 BW/容量表
- [Samsung HBM Base Die](/papers/hc2026-samsung-hbm-base-die.md) — 同场 B-die logic / HPB / zHBM

# Citations

[1] [raw/papers/HC2026_SK_hynix_HBM_Advanced_Packaging.pdf](raw/papers/HC2026_SK_hynix_HBM_Advanced_Packaging.pdf) — Jaesik Lee, Hot Chips 2026 Tutorial
[2] [raw/papers/hc2026-skhynix-hbm-advanced-packaging.md](raw/papers/hc2026-skhynix-hbm-advanced-packaging.md) — 结构化摘录
