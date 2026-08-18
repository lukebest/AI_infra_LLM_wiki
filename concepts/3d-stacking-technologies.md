---
type: Concept
title: 3D Stacking Technologies
description: 3D 集成三路线对垒：TSV-based (via-middle 商业主流)、Monolithic 3D (实验性高密度)、Hybrid Bonding (Cu-Cu 是 2024 商业现实)；对 3D NoC 设计的根本含义对比
tags:
- 3d
- tsv
- monolithic
- hybrid-bonding
- interconnect
- architecture
- packaging
- chiplet
- wse
- noc
timestamp: '2026-08-18T00:00:00Z'
created: '2026-07-31'
updated: '2026-08-18'
sources:
- raw/articles/3d-noc-study-01-tsv-process-tech.md
- raw/articles/3d-noc-study-02-monolithic-vs-tsv.md
- raw/articles/3d-noc-study-03-hybrid-bonding.md
- papers/batude-monolithic-3d-review-2011.md
- papers/hybrid-bonding-3d-integration-recent.md
- papers/network-design-wafer-scale-wow-hybrid-bonding.md
- papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md
- papers/mozart-35d-wafer-scale-moe-training.md
---

# 3D Stacking Technologies（3D 堆叠工艺路线）

3D 集成有**三条根本不同的物理路线**——TSV-based（商业主流）、Monolithic（实验高密度）、Hybrid Bonding (Cu-Cu，当代商业拐点)。每条路线对 3D NoC 设计的含义**根本不同**；本文作为路线对比的入门锚点。

## 定义

```
3D 集成 = 多层 die 通过某种互连机制垂直堆叠形成的集成电路
                          ↑ 必须先选
            TSV         Monolithic      Hybrid Bonding
           (大颗粒)      (微密)         (密度+商业现实)
            ↓              ↓                ↓
          HBM           实验/学术        Apple M-Ultra / MI300
```

## 三路线量化对比

| 维度 | TSV-based (via-middle) | Monolithic 3D | Hybrid Bonding (Cu-Cu) |
|------|------------------------|---------------|------------------------|
| **互连间距** | 5–20 μm | 0.1–1 μm | 0.5–3 μm |
| **IO/mm² 密度** | 10K–100K | 1M+ | 100K–1M+ |
| **KOZ** | 必要 (0.2–5 μm) | 实质 0 | 实质 0 |
| **层间接触高度** | 50 μm (TSV 长) | 100 nm 级 | 100–500 nm |
| **工艺温度预算** | 高 (400+ °C) | 低 (< 400 °C) | 低 (< 400 °C) |
| **堆叠层数 (典型)** | 2–8 (HBM=12-Hi) | 2–4 (实验) | 2–8 |
| **良率模型 λ** | 100–1000 ppm TSV | KGD/KGS 较复杂 | particle/warpage 主导 |
| **采用者 (2024+)** | HBM, V-Cache, HBM4 base | CEA, Imec, MIT, Stanford | TSMC SoIC, Samsung X-Cube, Intel Foveros, Apple M-Ultra |
| **3D NoC 设计核心约束** | 端口、KOZ、热 | 热、密度 | 热、KGD、功耗 |

## 路线含义详解

### 1. TSV-based（商业主流）

**优势**：工艺最成熟；via-middle 是工业标准；HBM 商业出货
**劣势**：KOZ 限制 port；TSV 良率压力；最大端口密度有限（5–7 port）
**对 3D NoC**：feero 2008 baseline 5-port 模型适用

代表产品：HBM3/HBM4/HBM5、AMD 3D V-Cache、部分 TSMC SoIC-L

详见 [TSV Physical Layer](/concepts/tsv-3d-physical-layer.md)。

### 2. Monolithic 3D（实验性高密度）

**优势**：IO 密度 +10–100× vs TSV；无 KOZ；接近晶体管层间密度
**劣势**：低温工艺对上层器件迁移率有损失（20–40%）；工艺非标化；KGD/KGS 复杂
**对 3D NoC**：port 约束打破（7→10 不牺牲面积），但商业不可得

代表研究：CEA-Leti、Imec、IBM Research、MIT、Stanford（多年 IEEE/IEDM）

详见 [Monolithic 3D 综述 papers/batude-monolithic-3d-review-2011.md](/papers/batude-monolithic-3d-review-2011.md)。

### 3. Hybrid Bonding（当代商业拐点）

**优势**：IO 密度高（接近 monolithic）；工艺温度低；pitch 已缩到 1 μm；**商业可得**
**劣势**：对准精度要求高（±200 nm）；particle / wafer warpage 影响良率
**对 3D NoC**：port 数可扩展到 8+ 不牺牲面积；热密度变成新主导约束

代表产品：**Apple M-Ultra, AMD Instinct MI300, Intel Meteor/Lunar Lake, TSMC SoIC-X, Samsung X-Cube, SK hynix HBM4 base die**

详见 [Hybrid Bonding papers/hybrid-bonding-3d-integration-recent.md](/papers/hybrid-bonding-3d-integration-recent.md)。

2026 新用法：TSMC SoIC-**WoW** 把 Cu-Cu 键合从 die 堆叠推到**整晶圆面对面**——同晶圆 reticle 不能直连，拓扑由重叠决定，见 [Network-on-Wafer](/concepts/network-on-wafer.md) 与 [Iff et al.](/papers/network-design-wafer-scale-wow-hybrid-bonding.md)。[Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) 用 hybrid bonding 做 per-chiplet logic-on-SRAM；[3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) 用垂直维隔离 PD 解耦的 KVT 与 decode AllReduce。

## 路线 → 3D NoC 设计的根本含义

| 路线 | port 数 | 路由器主约束 | 拓扑倾向 |
|------|---------|-------------|---------|
| TSV-based | 5–7 | KOZ + pitch | partial connected mesh |
| Monolithic | 7–10 | thermal + 上层器件 | full 3-D Mesh |
| Hybrid Bonding | 8+ (实际) | 热密度 + 功耗 | dense / heterogeneous |

**关键结论**：**2024 之前 3D NoC 论文多在 TSV-based 假设** → 5-port 优化；**2024+ 商业现实 = hybrid bonding** → 8+ port 富余。

## 与 wiki 既有页面的关联

- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — TSV 工艺单元
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel / 3D AI chip 上跑 LLM 工作负载
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Packaging (3D/2.5D/Chiplet) 路线
- [WSE](/entities/cerebras-wse.md) — **反例**：Cerebras 不靠 3D 堆叠，靠整晶圆制造（field stitching，不是 WoW）
- [Network-on-Wafer](/concepts/network-on-wafer.md) — SoIC-WoW 把 hybrid bonding 变成晶圆级网络约束
- [DRAM Memory System](/concepts/dram-memory-system.md) — HBM 即 TSV-based 商业现实
- [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md) — 3D V-Cache 即 TSV-based

## 开放问题

1. **Hybrid Bonding 时代的 3D NoC 拓扑**：full vs partial connected mesh 的现代边界？需仿真验证
2. **3D NoC 与 LLM 商业产品**：HBM4 + SoIC + Apple M-Ultra 的 LLM serving 工作负载多 deal 适用
3. **Monolithic 长期**：学术实验能否走入产品线？observation：3 年内不可能
4. **3D NoC 设计与编译器协同**：3D 集成下 GEMV / GEMM 调度应改进哪部分？

# Citations

[1] [raw/articles/3d-noc-study-02-monolithic-vs-tsv.md](raw/articles/3d-noc-study-02-monolithic-vs-tsv.md) — Monolithic vs TSV 学记
[2] [raw/articles/3d-noc-study-03-hybrid-bonding.md](raw/articles/3d-noc-study-03-hybrid-bonding.md) — Hybrid Bonding 学记
[3] [papers/batude-monolithic-3d-review-2011.md](papers/batude-monolithic-3d-review-2011.md) — Monolithic 综述
[4] [papers/hybrid-bonding-3d-integration-recent.md](papers/hybrid-bonding-3d-integration-recent.md) — Hybrid Bonding 综述
[5] [papers/network-design-wafer-scale-wow-hybrid-bonding.md](papers/network-design-wafer-scale-wow-hybrid-bonding.md) — WoW 放置即拓扑（2026）
