---
type: Concept
title: Through-Silicon Via (TSV) Physical Layer
description: 3D 集成的基础物理单元：via-first/middle/last 工艺、Keep-Out Zone、寄生 R/C、热密度与良率模型；3D NoC 设计的根本约束由这一层决定
tags:
- 3d
- tsv
- physical-layer
- interconnect
- through-silicon-via
- architecture
- noc
timestamp: '2026-08-26T00:00:00Z'
updated: 2026-08-28
created: '2026-07-31'
sources:
- raw/articles/3d-noc-study-01-tsv-process-tech.md
- papers/katti-tsv-technology-roadmap-2010.md
---

# Through-Silicon Via (TSV) Physical Layer（TSV 物理层）

3D 集成的最基础单元：**穿越硅衬底的垂直金属导线**，与水平互连（BEOL M1–M9）一起构成完整的 3D 互连网络。本概念页定义 3D NoC 设计的物理前提——任何 3D 拓扑 / 路由 / 路由器微架构 / 良率策略都源于这一层的约束。

## 定义

```
硅片 (top die)
   ↓  [TSV：直径 1–10 μm；长度 50–100 μm；填充 Cu 或 W]
   ↓
硅片 (bottom die)
```

TSV 提供 2 维平面 X/Y 之外**唯一的垂直 (Z) 信号通路**，是 3D 集成商业可行的工程基础。

## 工艺分类

| 类型 | 制造阶段 | 工艺特点 | 典型应用 |
|------|---------|----------|----------|
| **Via-first** | FEOL 前 / 同期 | 高温耐受、高纵横比 | 早期 logic-on-logic 3D |
| **Via-middle** | FEOL 后 / BEOL 前 | **当前工业标准**；兼容 BEOL | HBM、AMD 3D V-Cache、TSMC SoIC |
| **Via-last** | BEOL 后 / RDL 后 | 最大尺寸；保护性 | 3D DRAM 后段、legacy die |

via-middle 是 HBM3/HBM4、AMD Instinct MI300 等所有商业 3D 集成的事实工艺。

## 关键约束四要素

### 1. Keep-Out Zone (KOZ)

TSV 不能埋在活性区正下方——Cu 挤压引起 Si 晶格损伤、漏电流与时序失配。

| 工艺节点 | KOZ 半径 |
|----------|----------|
| 130 nm | 3–5 μm |
| 28 nm | ~1.0 μm |
| 7 nm | 0.2–0.6 μm |

→ **节点越先进，KOZ 越小** → 5–7 nm 是 TSV 高密度堆叠的甜蜜区。

### 2. 寄生 R/C

```
R_TSV ≈ ρ·L/(π·r²)         ~5–50 mΩ   （Cu via 50 μm 长）
C_TSV ≈ 2π·ε·L/ln((2·R+K)/r)  ~10–100 fF
delay_TSV ≈ R_TSV × C_TSV + R_driver × C_TSV  ~1–10 ps
```

延迟上单跳 TSV ≈ 5–10× 快于水平 long-wire；**但端口数受 KOZ 与 pitch 限制**，反过来才是真瓶颈。

### 3. 热密度（最讨厌的副作用）

- 3D 堆叠 n 层 → 等效功率密度 n×
- 顶层 die 温度可升至 110–130 °C（vs 单片 70 °C）
- 路由器频次下降 10–20%、NoC 时序失配变严重
- **后果**：几乎每篇 3D NoC 论文都有 thermal-aware 一章

### 4. 良率模型

```
Y_die = exp(-A · N_TSV / A_chip · λ_TSV)
λ_TSV ≈ 100–1000 ppm
```

单 die 100K TSVs → Y ~ 50% 或更糟 → 必须配：冗余 TSV + 自修；分区 KGD 测试。

## 3D NoC 设计的根本意义

| 假设层 | 受 TSV 影响 |
|--------|-----------|
| **拓扑** | Port 数受 KOZ 限制 → Feero 5–7 port model |
| **路由** | Thermal-aware 必须考虑 TSV = 热岛 |
| **路由器微架构** | 7 port crossbar 面积/功耗压力 |
| **buffer 选择** | Bufferless 在 vertical port 受限时可省 VC |
| **良率** | TSV 集群冗余 + 自修 |

## 与 hybrid bonding / monolithic 路线的关系

- **TSV-based 3D**：HBM、AMD 3D V-Cache、早期 3D AI chip；当前 3D 集成主流
- **Monolithic 3D**：接近晶体管密度的层间互连；KOZ ≈ 0；但工艺成熟度低
- **Hybrid Bonding (Cu-Cu)**：1–3 μm pitch，KOZ ≈ 0；**让 TSV 的 port 紧缺约束显著松开**

→ **结论**：TSV 在 2024 已不是 3D NoC 设计的主约束；**热密度** + **算法/编译器层** 才是下一波研究核心。

## 与 wiki 既有页面的关联

- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — TSV / Monolithic / Hybrid 三路线对比
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 视角下 3D 内存+NoC+LLM 协同
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Packaging (3D/2.5D/Chiplet) 路线之一
- [DRAM Memory System](/concepts/dram-memory-system.md) — HBM 即 TSV 商业现实
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 存储+NoC 全景，TSV 是其关键链路
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — HBF 用 TSV 堆 NAND die；GPU 侧是 UCIe，不是 3D logic NoC
- [FLINT](/papers/flint-hbf-llm-inference.md) — 同是 TSV-HBF；封装侧改成 HBM→HBF D2D 级联，基座吃 plane-parallel burst
- [SK hynix packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md) — HBM4 **>20K** TSVs + power TSVs「铺满」，标 75% PDN
- [Samsung HBM Base Die](/papers/hc2026-samsung-hbm-base-die.md) — BW 瓶颈仍是 TSV 数量与 pitch；zHBM 用 HCB 取消 PHY
- [d-Matrix Raptor](/papers/hc2026-dmatrix-raptor-3d-dram.md) — ~700 TSV/mm² 供电穿过 1-Hi DRAM

## 开放问题（向 Layer 2-5 推进）

1. **Hybrid Bonding 时代的 port 数**：5–7 port 假设已被打破，真实 3D NoC 论文应假设多少？
2. **3D-NoC 拓扑 vs thermal-aware 调度**：热密度能否改写 3D Mesh 设计假设？
3. **TSV / Hybrid Bonding / Monolithic 的 layered 组合**：是否仍是一个 3D NoC 设计阶段的核心议题？
4. **良率模型的"modified assumption"**：hybrid bonding 良率如何模型？

## 关键论文

- [Katti TSV Technology Roadmap](papers/katti-tsv-technology-roadmap-2010.md) — Layer 1 主参考
- [Batude Monolithic 3D Review 2011](papers/batude-monolithic-3d-review-2011.md)
- [Hybrid Bonding 3D Integration Recent](papers/hybrid-bonding-3d-integration-recent.md)
- [Feero 3D Mesh NoC Stan 2008](papers/feero-3d-mesh-noc-stan-2008.md) — 3D Mesh 拓扑 baseline

# Citations

[1] [raw/articles/3d-noc-study-01-tsv-process-tech.md](raw/articles/3d-noc-study-01-tsv-process-tech.md) — Layer 1 学习笔记
[2] [papers/katti-tsv-technology-roadmap-2010.md](papers/katti-tsv-technology-roadmap-2010.md) — Layer 1 入口论文页
[3] Dally & Towles 2004 *Principles and Practices of Interconnection Networks* — 2D NoC 设计空间，3D 是扩展
