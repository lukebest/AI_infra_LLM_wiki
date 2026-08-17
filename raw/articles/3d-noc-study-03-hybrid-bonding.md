---
type: Raw Source
title: 📰 3D NoC Study Day 3 — Hybrid Bonding & the 2024 Reality Check
source_path: /home/luke/wiki/raw/articles/3d-noc-study-03-hybrid-bonding.md
textbook: 综述整合：IEEE ECTC 2017–2024 历年 Cu-Cu hybrid bonding 报告；IEDM 2022 hybrid bonding system integration；商业白皮书 TSMC SoIC, Samsung X-Cube, Intel Foveros
ingested: 2026-07-31
---

# 📰 3D NoC Study Day 3 — Hybrid Bonding & the 2024 Reality Check

📅 2026-07-31（Day 3 / Layer 1）
🎯 阶段：物理层 + Layer 1 收尾（路线对比 + 商业现实）
📖 教材：商业白皮书与 IEEE ECTC/IEDM 报告；事实诊断型

---

## 今日主题：Hybrid Bonding 时代 — TSV 不再稀缺, 3D NoC 假设被打破

### 🧭 为什么要在 Layer 1 末学 hybrid bonding？

前两天（Day 1 + Day 2）讲的物理约束（TSV KOZ / monolithic 工艺不成熟）都是 2018 之前的"理论"问题。**Hybrid Bonding 是过去七年最重要的"3D 集成技术转折点"** —— 它让 TSV 从"稀缺资源"变成"接近 sufficient"，3D NoC 设计的**根本假设被改写**：

- 早期 (2008–2018)：垂直 port 稀缺 → 5–7 port partial 3-D Mesh
- 现代 (2024+)：垂直 port 充裕 → 8+ port full 3-D Mesh 可行
- **未来**：hybrid bonding 与 monolayer 集成接近 → 物理约束差异变小 → 3D NoC 设计越来越看的是 **热、功耗、算法、与算法层而非物理层**

### 🎯 今天的目标

- 知道 Hybrid Bonding 的核心工艺步骤与关键约束
- 知道 Hybrid Bonding vs μ-bump / TSV 的密度/速度对比
- 知道 HBM / AMD / Apple / Intel 的 hybrid bonding 实际产品已大量部署
- 知道 3D NoC 拓扑研究 在 hybrid bonding 时代 应更新假设
- 知道 Day 4 (3D Mesh 拓扑基线) 应基于 hybrid bonding 假设

---

## 一、Hybrid Bonding: Cu-Cu 直接键合

### 1.1 工艺核心

```
Step 1: CMP 抛光 Cu pad  (Cu oxidation < 1 nm roughness)
Step 2: plasma / wet clean 去氧化层
Step 3: 室温（±200°C）初对准 + 加压预键合
Step 4: anneal @ 200–400°C  Cu-Cu 扩散键合
```

**关键工艺参数**：
- **Cu 粗糙度**：< 1 nm (RMS)
- **对准容差**：±200 nm (production)；±50 nm advanced
- **bonding 温度**：< 400 °C（不允许高温影响下方 BEOL）

### 1.2 与 μ-bump 对比

| 维度 | μ-bump (Sn / Cu pillar + Sn) | Hybrid Bonding (Cu-Cu) |
|------|--------------------------------|-------------------------|
| Pitch (typical) | 10–40 μm | 0.5–3 μm |
| IO/mm² | 2.5K–10K | 100K–1M+ |
| 凸点高度 | 5+ μm | ~100 nm (essentially hidden) |
| 对准容差 | ±2 μm | ±200 nm |
| 电阻 | 高 (Sn alloy) | 与 Cu-wire 等价 |
| 工艺成熟度 | 量产多年 | 量产 (~2018+) |

**关键判据**：μ-bump 已成瓶颈；hybrid bonding 几乎全部接替。

### 1.3 与 TSV 对比

| 维度 | TSV (via-middle) | Hybrid Bonding |
|------|------------------|----------------|
| 工艺次序 | FEOL 后、BEOL 前 | BEOL 完成后 |
| 间距 | 5–20 μm | 0.5–3 μm |
| KOZ | 必要 | **本质无** (CMP 平坦, 工艺更密) |
| 良率 | 良率受 λ·N 重 | 受 particle / wafer warpage 影响 |

hybrid bonding 不需 TSV——是 bonded dies 之间的直接金属键合；但**仍可能与 TSV 组合**（die 内 TSV + die 间 hybrid bonding）。

---

## 二、商业用例 (2024 视角)

### 2.1 TSMC SoIC

```
产品：SoIC-X (≈ pure hybrid bonding), SoIC-L (hybrid + RDL)
客户：Apple M-Ultra, AMD Instinct MI300, NVIDIA Blackwell (部分)
pitch：SoIC-X ~ 3 μm；SoIC-L ~ 6 μm
差异：SoIC-L 含 RDL <-> higher interconnect flexibility
```

### 2.2 Samsung X-Cube

```
pitch：1 μm (亚 μm) — 业内最先进之一
用途：Exynos SoC stack、3D NAND controller
```

### 2.3 AMD Instinct MI300

```
架构：6 die stack (CPU + 6 GPU + HBM stack + interposer)
3D 集成：SoIC 风格 (大部分 chip 用 hybrid bonding)
HBM：HBM2e/HBM3 stack (TSV-based but with hybrid bonding interposer)
```

### 2.4 Intel Foveros

```
Pitch：~ 3 μm 量产；下一代 1 μm
产品：Meteor Lake, Lunar Lake (chiplet-based CPU)
```

### 2.5 SK hynix HBM3 / HBM4 / HBM5

```
HBM3：12-Hi (24 GB), μ-bump TSV based
HBM4：12-Hi (36 GB), hybrid bonding base die
HBM5（预计 2026+）：16-Hi (48 GB)
```

→ 2024 起 hybrid bonding 在 HBM / CPU / GPU 多产品常态化。

---

## 三、3D NoC 假设的根本改写

### 3.1 旧假设 (2008–2018)

1. **TSV pitch 5–20 μm，KOZ 0.5–5 μm** → vertical port 受限 → 5–7 port 路由器
2. **100 K TSVs/die 是上限** → Vertical bisection BW 受限
3. **良率主导 worry** → 设计需冗余 + 容错

### 3.2 新假设 (2024+)

1. **pitch 1–3 μm、无 KOZ** → vertical port 可达 8–10，不严格牺牲
2. **hybrid bonding pitch density ≈ monolithic** → 微结构上 3D 集成接近 2D 平面集成
3. **良率仍关注** → 通过 redundancy + built-in self-test 解决

→ 3D NoC 拓扑 / 路由 / 路由器微架构研究的 **根本假设需要更新**——在 hybrid bonding 假设下：

- "partial vs full connected 3-D Mesh" 不应是核心议题（vertical port 不再稀缺）
- "Bufferless Router in 3D" 不再有明显优势
- "Thermal-Aware DOR" **反而更**重要（功率密度上升）

---

## 四、Layer 1 完结 → 进入 Layer 2

Layer 1 学完：

- ✅ TSV 工艺（via-first/middle/last）
- ✅ KOZ + 寄生 R/C
- ✅ 热密度
- ✅ 良率模型
- ✅ Monolithic vs TSV-based 路线对比
- ✅ Hybrid Bonding 商业现实

→ Layer 2 主题：**3D Mesh / Stacked Mesh / Hybrid Bonded Mesh 拓扑设计**，看 Day 4 笔记。

---

## 五、对 LLM decode / Direction 2 的具体含义

你的研究是 mesh-NoC + decode + 编译器。在这个语境下：

1. **Hybrid bonding 假设的 mesh**（8–10 port / tile full 3-D Mesh）= 比 TSV-based（5–7 port）的 prefill/decode 调度都更简单，因为路由灵活度增加
2. **HBM + hybrid bonding** 是 LLM serving 的事实路径（Apple M-Ultra、AMD MI300、Hopper + NVL72） — 因此研究 3D Mesh 与 hybrid bonding 的 LLM decode 适配是有产业意义的
3. **不要忽略 IEEE 商业现实**：研究应"假设 hybrid bonding 可用"而不仅是学术 monolithic；这其实和你的研究方向 implicit 一致

---

## 六、Wiki 链接

- ← [Concepts 3D Stacking Technologies](/concepts/3d-stacking-technologies.md): 三路线
- ← [Concepts Through-Silicon Via Physical Layer](/concepts/tsv-3d-physical-layer.md): TSV 工艺单元
- → Day 4 (Layer 2): [3D Mesh 拓扑基线 (Feero+Park+Rahimi)]
- → Layer 5: HBM4 / AMD MI300 / Apple M-Ultra hybrid bonding 商业 / LLM serving

---

## 七、个人待解问题

1. **Hybrid Bonding 失败的具体 mode**：wafer warpage / particle 引入缺陷的不同后果
2. **Bonding vs Chartered-aligned RO 关联**：wafer-to-wafer vs chip-to-wafer 的良率差异
3. **Hybrid Bonding 时代的 3D NoC 论文应假设什么 port 数？8？10？**
4. **HBM5 + hybrid bonding 时代的 LLM serving 调度**：会怎样改写 prefill/decode 设计

---

# Citations

[1] [papers/hybrid-bonding-3d-integration-recent.md](../../papers/hybrid-bonding-3d-integration-recent.md) — Layer 1 入口论文页
[2] IEEE ECTC 2017–2024 hybrid bonding 报告
[3] TSMC, Samsung, Intel, SK hynix 商业白皮书
[4] IEDM 2022/2023 hybrid bonding system integration 报告
