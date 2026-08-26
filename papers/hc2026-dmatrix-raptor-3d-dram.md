---
type: Paper
title: "Hot Chips 2026: d-Matrix Raptor 3D-DRAM"
description: d-Matrix — 1-Hi logic-on-top 3D DRAM 推理机；36 μm F2F；自称 ≈20× BW/mm²、13.5× 更好 mW/GB/s vs HBM4；ISCA 2026 指针
tags:
- d-matrix
- 3d
- hbm
- memory
- memory-bandwidth
- inference
- hybrid-bonding
- tsv
- architecture
- chiplet
- through-silicon-via
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-26
updated: 2026-08-26
sources:
- raw/papers/HC2026_dMatrix_Raptor_3D_DRAM.pdf
- raw/papers/hc2026-dmatrix-raptor-3d-dram.md
---

# Raptor: The First 3D-DRAM Accelerator for Generative Inference

**Speakers:** Sudeep Bhoja（d-Matrix, Co-founder & CTO）；Aayush Ankit（Meta；标注 work done while at d-Matrix）  
**Venue:** Hot Chips 2026 Tutorial  
**PDF:** [raw/papers/HC2026_dMatrix_Raptor_3D_DRAM.pdf](raw/papers/HC2026_dMatrix_Raptor_3D_DRAM.pdf)  
**Paper pointer:** Raptor paper: **ISCA 2026**

用 1-Hi logic-on-top + 36 μm F2F 换 SRAM 级 BW、~1/10 HBM 能量。自称对硅面积归一化打过 HBM4 / Rubin R200。Model Details 表是图，容量分解 **未知**。不写招聘。

## 问题

权重涨 + KV 随 context×batch 涨。例：**64 users × 1M context ≈ 935 GB KV**。

SRAM 对照（Corsair 卡对，Dayo et al.）：BW **300 TB/s**，容量 **4 GB**，延迟 **~1 ns**，I/O **~0.5 pJ/bit**。6T 比 DRAM 1T1C 大约 **10×**；bitcell 冻在 **~0.021 μm²**（N5→N3E→N2）；实用上限 **~4 GB/卡对**；成本 **100× DRAM**。用途例：投机解码 draft model。

HBM：8–16 core dies/栈、8 栈/封装；pin 速与 IO 宽涨得慢，栈数被海滩线卡住。实用上限（点名 Vera Rubin、MI 455）：HBM4 **~20 TB/s**。功耗：**2.4 pJ/bit × 100 TB/s = 1.92 kW**（仅 HBM，不含 fabric）。

## 3D-DRAM 叠法

两种：DRAM-on-top（热要穿过 DRAM）vs **logic-on-top**（供电要穿过 DRAM TSV）。正文结论：**1-Hi、logic-on-top、功率密度 ≤0.5 W/mm²** 可用液冷把 DRAM 压在 **<100 °C**。

能量梯：SRAM on-die **~50 fJ**；on-chip wire **~35 fJ/mm**；**3D vertical IO 0.3–0.4 pJ**；interposer **~500 fJ/mm**；2.5D HBM4 system **2.5 pJ + 3 pJ (on chip)**。3D IO 大约比 HBM 低 **~10×**（无 PHY、毫米级垂直 vs 厘米级 interposer）。3D DRAM **≤4 layers** vs HBM **12–16**，称更好良率。

工作负载：prefill compute-bound；decode 通常 BW-bound；高 GQA+投机时 attention 可转 compute-bound；MoE 在中等 batch+投机下仍 BW-bound。墙钟多数在 decode。见 [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md)。

## 规模与封装

精度 **4-bit weights · 8-bit KV**；scale-up **72 cards**；**1-Hi 32 GB/card** 的 72 卡域声称装下 **Kimi K3 @ 1M context**。再往外靠 disagg / multi-rack。协调 **8K virtual devices** vs 典型 GPU 系统 **~72** devices。

封装：top **TSMC N4** logic（热页写 **N4P**），bottom 3D DRAM，**36 μm F2F**。路线图：hybrid bonding **<2 μm pitch、8-high**。

## 三纠缠挑战

1. **Banking**：**840 banks/chiplet**（72 spare → 768）对 **256 ch**（16 ch × 16 TE-group），每 bank **32 B/col**，flit **128 B** ⇒ 需要 4 banks/ch、只有 3 ⇒ 朴素取会 **33% overfetch ≈ 33 TB/s** 浪费。解法 **stream blocking**：4×96 B = 3×128 B，0% overfetch。
2. **I/O**：**100 TB/s × 0.37 pJ/bit = 296 W**；单周期 256-bit、无 burst、无 DBI 脚。**Stream flipping**（pinless DBI）省 **20%** I/O，tag 和 ECC 共置，开销 **0.8%**。
3. **热**：**Tj 105 °C**，retention **32 ms@85 °C → 4 ms**（**8×** refresh）。**~700 TSV/mm²**，无 DBI pin。

可靠性：deep banking **1366 rows** vs 商品 **~32K**，4 ms refresh 只吃 **1.37%** BW，仍标 **∼100 TB/s**。ECC：124 col 里最后 8 列为 **[132,128] Reed–Solomon + DBI**。72 spare 用 **M=2** bank chaining 保 channel 对称。

## 硅面积归一

Raptor 83% / Rubin 85% 有效 BW；Rubin R200 = 8× HBM4 24 Gb SoC。

| Metric | Raptor 3D-DRAM | HBM4 24 Gb | HBM4 32 Gb | Rubin R200 |
|---|---|---|---|---|
| Capacity (MB/mm²) | 11.4 | 21.9 | 26.3 | 21.9 |
| Bandwidth (GB/s/mm²) | 32.6 | 1.67 | 1.51 | 1.39 |
| Power (mW/GB/s) | 2.96 | 40.0 | 40.0 | 40.0 |

自称 **≈20×** BW/mm²、**13.5×** 更好的 mW/GB/s。

服务口号：**~1000 TPS/User**，3T 级模型、**1M context**。片内/片间 fabric：package full-mesh（虚拟对角 D2D），push-style、单边、无 ACK。拓扑图无 GB/s 数字。

## 与 wiki 的关系

- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 是 DRAM-on-logic 仿真；Raptor 是 **1-Hi logic-on-top** 商品叙事
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 今天 36 μm F2F；路线图 HB <2 μm / 8-high
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — ~700 TSV/mm² 供电穿过 DRAM
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 相对 HBM4 ~20 TB/s 海滩线；3D IO ~10× 低于 HBM
- [Handy HBM 开场](/papers/hc2026-handy-hbm-tutorial.md) — 同场市场分母
- [NVIDIA Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 幻灯片点名的 HBM4 实用上限对照

# Citations

[1] [raw/papers/HC2026_dMatrix_Raptor_3D_DRAM.pdf](raw/papers/HC2026_dMatrix_Raptor_3D_DRAM.pdf) — Bhoja / Ankit, Hot Chips 2026 Tutorial
[2] [raw/papers/hc2026-dmatrix-raptor-3d-dram.md](raw/papers/hc2026-dmatrix-raptor-3d-dram.md) — 结构化摘录
