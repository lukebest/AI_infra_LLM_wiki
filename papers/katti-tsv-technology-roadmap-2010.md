---
type: Summary
title: 'Through-Silicon Via: A 3D Technology Road Map (and Earlier Survey Work)'
description: Katti et al. IEEE Comm. Mag. 2010 — TSV 综述原典：工艺分类 (via-first/via-middle/via-last)、keep-out zone、电热耦合、良率模型；常被引作 3D NoC paper 的物理层标准参考
tags:
- 3d
- tsv
- interconnect
- through-silicon-via
- physical-layer
- architecture
timestamp: '2026-07-31T00:00:00Z'
created: 2026-07-31
sources:
- raw/articles/3d-noc-study-01-tsv-process-tech.md
---

# Through-Silicon Via: A 3D Technology Road Map (and Earlier Survey Work)

**Authors:** Kibum Kim (多版本第一作者不同；常见引用为 Katti 2010 与 Kim 多篇 IEEE/IEDM)

**Venue:** IEEE Communications Magazine, **May 2010**（以及 2010 年前后多篇 IEEE 综述）

**经典论文来源：** 综述经常被引，但**主要原典**分散在：Garrou 2008 *Introduction to 3D Microelectronic Packaging*、Lau 2011 *Evolution, Challenges and Outlook of 3D IC/Si Integration*（多次重印于 Springer）、以及 IEEE ECTC/IEDM 历年 paper 集。本页作为 Layer 1 学习入口的**索引页**。

## 一句话总结

TSV 是 3D 集成的"垂直导线"，但**不是免费导线**——keep-out zone、寄生 R/C、热密度、良率四件事把 TSV 与水平 M1-M9 链路彻底区分开来。任何 3D NoC 的设计取舍（前缀/3D 拓扑/路由器端口/bufferless 选择）都必须先吃透这些物理约束。

## 核心贡献（综述层）

### 1. TSV 工艺分类（按与 FEOL/BEOL 顺序）

| 类型 | 阶段 | 工艺特点 | 典型尺寸 |
|------|------|----------|----------|
| **Via-first** | 晶体管制造前或同期 | 高纵横比 (10–20:1)；高温耐受 → 不限制后续工艺；最小尺寸 ~5×10 μm (2010)；现代先进工艺缩小到 ~1–2 μm | 大多数 logic-on-logic 3D 早期方案 |
| **Via-middle** | 晶体管后、互连前 | 与 BEOL 兼容；当前主流 (TSMC、三星 3D-NAND/3D-DRAM HBM)；典型 ~5×50 μm | 商业 HBM、AMD 3D V-Cache、TSMC SoIC |
| **Via-last** | 互连后（甚至 RDL 后） | 可加到既有 die；保护性高但尺寸最大 ~10–20 μm | 3D 堆叠 DRAM 后段，legacy 部分 |

**关键 trade-off**：via-first/温度耐受 → 直径小；via-last/工艺简单 → 直径大、间距宽。一致性是 TSV < 100 ns latency 目标的前提。

### 2. Keep-out Zone（KOZ）

TSV 不能埋在活性区（active area）正下方：Cu 挤压 → Si 晶格损伤 → 漏电/迁移可靠性问题。

| 工艺节点 | KOZ 半径 |
|----------|----------|
| 130 nm | 3–5 μm |
| 28 nm | ~1.0 μm |
| 7 nm | **0.2–0.6 μm** |

KOZ 让每 TSV 占用 1 至 数十 μm² 不可用面积。"100K TSVs/Wafer" 是营销话术；真实可行密度大致 10K–100K TSVs/cm²。

### 3. 寄生 R/C 模型

```
R_TSV ≈ ρ·L/(π·r²)        ~5–50 mΩ
C_TSV ≈ 2πε·L/ln((2R+K)/r) ~10–100 fF
```

**延迟 impact**：水平 M9 wire ~50 ps/mm → 1mm 跳一 router；TSV ~2–10 ps，**单跳比水平快 5×**。但**带宽** 由 TSV pitch 决定 → 单位 die area 的垂直带宽不如想象的高。

### 4. 热耦合（**最讨厌的副作用**）

垂直堆叠密度 → 热传导路径仅数十 μm，**热阻 H ~10× 单片**。
- 顶层 die 温度可升至 110–130 °C（vs 单片 70 °C）
- 一级影响：漏电流指数增长 → 频率墙
- 二级影响：相邻层热梯度 → 时序失配 → 路由器最敏感

3D NoC 论文的 thermal-aware routing / DOR variant 90% 源于这一物理现实。

### 5. 良率模型

Katti 2010 给出标准良率模型：

```
Y_die = exp(-A · N_TSV / A_chip · λ_TSV)
```

- λ_TSV ≈ 100–1000 ppm（按工艺显著变化）
- 一块 die 100K TSVs → 良好率约 exp(-10) ~ 50% 量级 → **yield crash**
- 实际产品（AMD 3D V-Cache、HBM3）通过冗余 TSV + 自检修 (self-repair) 缓解

## 3D NoC 学习中的位置

```
物理层 (Layer 1)  ← 本页
     ↓
拓扑层 (Layer 2): 3D Mesh / Stacked Mesh / Partially Connected
     ↓
路由层 (Layer 3): X-Y-Z DOR / 3D Turn Model / Thermal-Aware
     ↓
NoC 路由器微架构: 3 port 路由器 + 垂直物理通道 + 热感仲裁
```

## 与 wiki 既有页面的关联

- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 论文派，关注 **3D 内存层 + NoC + LLM** 协同，本页是其物理前置
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — "3D / 2.5D / Chiplet" 是该页"三条路"中 packaging 路线的一支
- [DRAM Memory System](/concepts/dram-memory-system.md) — DRAM/HBM/TSV 与内存墙问题的底座
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 存储+NoC 全景图，3D TSV 是其中关键物理链路

## 关键开放问题（Layer 2-3 学习入口）

1. **TSV 高密度 vs 良率**：100K+ TSV/die 的良率极限在哪？冗余 + 自修的成本？
2. **热密度→频率/路由约束**：3D 堆叠下路由器频率上限？
3. **KOZ 与逻辑密度**：KOZ 是否吃掉 5–10% 面积？
4. **垂直链路 vs 水平链路带宽不对称**：如何映射编译？

# Citations

[1] [raw/articles/3d-noc-study-01-tsv-process-tech.md](raw/articles/3d-noc-study-01-tsv-process-tech.md) — Layer 1 学习笔记（Katti+综述整合）
[2] Dally & Towles 2004 *Principles and Practices of Interconnection Networks* — 2-D NoC 设计空间，3D 是其扩展
