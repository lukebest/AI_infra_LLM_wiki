---
type: Raw Source
title: 📰 3D NoC Study Day 2 — Monolithic 3D vs TSV-based
source_path: /home/luke/wiki/raw/articles/3d-noc-study-02-monolithic-vs-tsv.md
textbook: 综述整合：Batude et al. 2011 ICCAD *Low-Temperature 3D Sequential Integration*；多篇 IEEE/IEDM 后续代表 (2012, 2014, 2017)；综述代表 R. Xie et al. & Batude 多年 IEEE Micro
ingested: 2026-07-31
---

# 📰 3D NoC Study Day 2 — Monolithic 3D vs TSV-based

📅 2026-07-31（Day 2 / Layer 1）
🎯 阶段：物理层（路线对比 — Monolithic / TSV / Hybrid）
📖 教材：综述型 — 重点是路线对比、不是工艺入口

---

## 今日主题：Monolithic 不是"更密的 TSV"

### 🧭 为什么要在 Layer 1 路线对比？

昨天（Day 1）讨论的是 **TSV 这一基础单元** —— 但 TSV 不是 3D 集成的唯一路线。**monolithic 3D 是另一条平行路线**，它的物理特性是"接近晶体管密度的层间互连"，根本不在 TSV 框架内。在 hybrid bonding (~1 μm pitch) 商用前，**学术界是 monolithic 唯一可行的高密度路线**。

3D NoC 学界今天讨论的"3D 集成能加几个端口" 直接受路线影响：

- TSV-based 3-D Mesh：~5–7 port（KOZ + pitch 受限）
- Monolithic 3D：~7–10 port（接近晶体管密度）
- Hybrid Bonding 3D：~8+ port（Cu-Cu 已商用）

### 🎯 今天的目标

- 知道 Monolithic 的工艺核心：层间纳米级互连 + 低温沉积 + 无 KOZ
- 知道 Monolithic vs TSV-based 的根本差异（不只是 pitch）
- 知道为什么商业产品只有 TSV-based / Hybrid Bonding 而非纯 Monolithic
- 知道对 3D NoC：monolithic 时代的"port 紧缺"假设不再成立

---

## 一、Monolithic 3D 工艺核心

### 1.1 Sequential Integration

```
晶圆 prep → 层 1 制造 (FEOL+BEOL)  →
晶圆 flip / bond  →
上层 surface prep + 低温处理 → FEOL+BEOL → ...
```

**关键技术点**：
- **低温沉积 (low-temperature process)**：上层不能在 > 400 °C 下处理（否则破坏下层已制铜互连、晶体管等效性）
- **替代工艺**：上层 Si 用低温 poly-Si（LTPS）或 oxide TFT；金属用低温 BEOL（Cu damascene 低温）
- **层间互连**：纳米级微凸点 + 氧化物隔离（SiO₂ / low-k）

### 1.2 与 TSV 路线对比

| 维度 | TSV-Based (via-middle) | Monolithic 3D |
|------|------------------------|---------------|
| 层间互连 | 大 TSV 1–10 μm | 纳米级混合键合 + oxide 隔离 |
| 间距 | 5–20 μm | **< 1 μm** |
| IO/mm² 密度 | ~10K (5 μm pitch) | ~10M+ |
| 工艺温度预算 | 高（> 400 °C 仍可）| < 400 °C |
| KOZ | 需要 | 不需要 |
| 堆叠层数（典型）| 2–8 (HBM) | 2–4 (实验) |
| 量产工艺成熟度 | 已商用 | 实验阶段 |

**核心 trade-off**：Monolithic 把密度拉满，但工艺不在标准节点；TSV 可用主流 28 nm + TSV 加层。

---

## 二、Monolithic Key Insights

### 2.1 三个关键 innovation

1. **密度 +10–100×** vs TSV（pitch + KOZ 全部减小）
2. **KOZ → 0**：层间接近晶体管密度 → 面积利用率几乎与纯 2D 同级
3. **低温工艺可行** → 上层用低温 poly-Si 或新材料（MoS₂、WSe₂ 等 layered 2D）

### 2.2 关键里程碑 / 论文

| 时间 | 来源 | 意义 |
|------|------|------|
| 2009–2011 | Batude, CEA-Leti | 首次 die-to-die 低温 monolithic 集成 demo |
| 2012 | IEDM | 更密集 monolithic 3D SRAM/LUT demo |
| 2017 | IEDM (多) | 上层低温 III-V / MoS₂ devices |
| 2018+ | IBM Research | Monolithic 3D stacked SRAM cache |
| 2020+ | MIT, Stanford, Tel | 上层用 2D materials，下层 Si CMOS |
| 2024 | Batude 综述 | Monolithic 已可在多代工艺继承性实验 |

### 2.3 关键挑战

| 挑战 | 量化 |
|------|------|
| **层间 KGD/KGS 测试** | 下层完成后必须 wafer-level test；上层在 pre-bond 测试更复杂 |
| **上层器件迁移率** | 低温 poly-Si < 低温单晶 Si；电路速度下降 20–40% |
| **层间寄生** | 仍存在，但密度更小 |
| **产品工艺非标准化** | 各公司 / 国家实验室有自家工艺 |

---

## 三、Monolithic 对 3D NoC 的影响

### 3.1 端口约束打破

传统 3-D Mesh 5–7 port 模型是因为 TSV pitch 限制；Monolithic 让端口数可达 **7–10 不牺牲面积**：

```python
# 经制估算
TSV_pitch_typical = 10   # μm
Monolithic_pitch_typical = 0.5  # μm
Ratio = TSV_pitch_typical / Monolithic_pitch_typical  # = 20× 更密
```

→ 这意味着 3D NoC 论文在 **monolithic 假设下** 与 **TSV 假设下** 的 topology/port 数 / partial vs full 连接 结论应**根本不同**。

### 3.2 Bufferless 路由器的争议

TSV-based 3-D Mesh 喜欢 bufferless（少 TSV 利用），
Monolithic 不需要 bufferless → 用 conflict-free routing (Pseudo-Circuit)。

### 3.3 Thermal-aware 更重要

Monolithic 高密度 → 功率密度 +20–50% → **热密度取代 TSV 物理约束成为新 bottleneck**。

---

## 四、商业现实（2026）

| 公司 | 商业产品 | 路线 |
|------|----------|------|
| **TSMC SoIC-X** | Apple M-Ultra、AMD MI300 base | Hybrid Bonding（≈ Monolithic-like 密度）|
| **TSMC SoIC-L** | 部分 7 nm SoIC | Hybrid Bonding 较 via-middle |
| **Samsung X-Cube** | Samsung Exynos 集成 | Hybrid Bonding |
| **AMD 3D V-Cache** | Zen 3+/Zen 4/5 | TSV via-middle |
| **Intel Foveros** | Meteor/Lunar Lake | Hybrid Bonding active interposer |
| **SK hynix HBM4** | HBM4 base die hybrid + DRAM TSV | Hybrid Bonding + TSV |
| **实验 CEA-Leti / Imec** | 学术 demo | Monolithic |

→ 商业上没有**纯 monolithic**——都是 hybrid bonding + TSV 组合。
→ 学术界仍是 monolithic prototype 实验主导。

---

## 五、对研究 LLM decode + Direction 2 的含义

我已经在 wiki 里 fix 了 Direction 2 = mesh-NoC + decode。对 LLM decode 这个场景：

| 3D 路线 | 适配性 |
|----------|--------|
| TSV-based 3-D Mesh | 与 mesh-NoC DEcode 路由器架构兼容；但 port 受限 → 部分连接 mesh |
| Monolithic 3D | 学术性研究；端口约束打破 → 可以做 full 3-D Mesh；但商业不可得 |
| Hybrid Bonding | HBM4 / Apple M-Ultra 形态；商业可用 |

→ 编译器栈研究不必"限定某一路"，但**仿真假设**应指明 —— 比如"假设 hybrid bonding 时代 vertical port 可达 8" —— 这是 Layer 5 阶段的细节，但在 Layer 2 拓扑里你应该先 mark。

---

## 六、Wiki 链接

- ← [Concepts 3D Stacking Technologies](/concepts/3d-stacking-technologies.md): 路线对比概念页
- → [Layer 2: 3D Mesh / Stacked Mesh / Hybrid Bonding 拓扑]: 基于路线后能选择
- → [Layer 5: HBM / AMD MI300 / Apple M-Ultra]: 商用 hybrid bonding 是 LLM serving 现实

---

## 七、个人待解问题

1. **Monolithic 上层电路速度**：低温 poly-Si vs 主流工艺的 性能/能耗比 量化
2. **KGD/KGS 在晶圆级 vs chip 级**：bonding 前还是 bonding 后？这影响哪些 partial defect 是不可救的？
3. **Monolithic 与 CE / DE 的可能架构**：Monolithic 3D 是 3D-Stacked DRAM 的潜在继任者（DRAM die 也是 CMOS-like 可集成）
4. **Monolithic 在 LLM decode 上的可能架构**：比如把 compute + SRAM cache monolithic 集成 vs 用 hybrid bonding HBM？

---

# Citations

[1] Batude et al., *3D Sequential Integration*, IEEE/ACM, 2011 (及后续 IEEE Micro 综述)
[2] [papers/batude-monolithic-3d-review-2011.md](../../papers/batude-monolithic-3d-review-2011.md) — 路线对比入口页
[3] IEDM/ECTC 历年 monolithic 3D 报告
