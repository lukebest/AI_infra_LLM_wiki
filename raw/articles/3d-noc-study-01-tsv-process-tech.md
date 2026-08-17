---
type: Raw Source
title: 📰 3D NoC Study Day 1 — TSV 工艺与物理层
source_path: /home/luke/wiki/raw/articles/3d-noc-study-01-tsv-process-tech.md
textbook: 综述整合：Katti et al. IEEE Comm. Mag. 2010（TSV 工艺综述）+ Garrou 2008 *Introduction to 3D Microelectronic Packaging* + Lau 2011 *Evolution, Challenges and Outlook of 3D IC/Si Integration*
ingested: 2026-07-31
---

# 📰 3D NoC Study Day 1 — TSV 工艺与物理层

📅 2026-07-31（Day 1 / Layer 1）
🎯 阶段：物理层（TSV / via / 寄生 / 热 / 良率）
📖 教材：综述型；主源 Katti 2010 IEEE Comm. Mag. 二道 / Garrou 2008 / Lau 2011

---

## 今日主题：3D 集成的"垂直导线"不是免费导线

### 🧭 为什么开篇学 TSV？

3D NoC 的所有设计取舍（路由器端口数 / 是否 bufferless / 垂直拓扑密度 / 良率模型）都源于 **TSV 这一基础单元的物理现实**。如果不理解：

1. KOZ 的面积代价
2. 寄生 R/C 对延迟/带宽的影响
3. 热密度对频率的限制
4. 良率与冗余设计

那么读 **任何一篇 3D NoC 论文** 你都会"在拓扑层读懂 / 在物理层卡住"。所以这一层是必须的，不重复 Voexl / 3D-Stacked AI Chip 论文（它们关注协同 + 工作负载，不重工艺）。

### 🎯 今天的目标

- 知道 **via-first / via-middle / via-last** 三种工艺类型的取舍
- 知道 **KOZ** 的量化代价
- 知道 **寄生 R/C** 量级 → 延迟、带宽估算
- 知道 **热密度** 是 3D 集成的根本约束之一
- 知道 **良率模型** 是为什么商用 3D 必带冗余 + 自修

---

## 一、TSV 工艺分类

### 1.1 Via-first

- **制造阶段**：晶体管制造**前**或同期（FEOL 之前 / 同期）
- **温度耐受**：必须承受后续高温处理（> 1000 °C）
- **尺寸**：较大（2010 早期 ~5×10 μm 到 5×50 μm）
- **优点**：高纵横比；最早期 3D 集成方案
- **缺点**：需高温工艺 → 与 BEOL 互连工艺冲突
- **应用**：logic-on-logic 3D 堆叠（早期 MIT/Stanford 实验）

### 1.2 Via-middle

- **制造阶段**：晶体管制造**后**、互连（BEOL）**前**
- **温度耐受**：中等
- **尺寸**：典型 5×50 μm；最小 1–3 μm 现代工艺
- **优点**：兼容 FEOL + BEOL，是**工业标准**（TSMC、三星、HBM）
- **缺点**：需 BEOL 后处理集成；可能影响前端晶体管
- **应用**：HBM（HBM3 / HBM4 / HBM5）、AMD 3D V-Cache、TSMC SoIC、SK hynix 大多数产品

### 1.3 Via-last

- **制造阶段**：互连**后**（甚至 RDL 之后）
- **温度耐受**：低（BEOL 已完成）
- **尺寸**：最大（10–20 μm）；间距宽
- **优点**：可加到既有 die；保护性高
- **缺点**：TSV 间距大 → 端口密度受限
- **应用**：3D DRAM 集成后段、legacy die 升级

### 1.4 工艺取舍 → 3D NoC 含义

**via-middle 是当下主流**，因此所有 3D NoC 物理层分析均基于 **BEOL 兼容 + 5–10 μm 深 TSV + 5×50 μm 长×宽** 的特征规格。

| 类型 | KOZ 半径 | 端口数 / tile | 良率目标 |
|------|---------|------------|---------|
| Via-first | 0.5–5 μm | 中（5–8） | 良（KOZ 较小）|
| Via-middle | 0.3–3 μm | 高（可达 10+）| 高（主流工艺）|
| Via-last | 1–5 μm | 低（3–5）| 一般 |

---

## 二、Keep-Out Zone（KOZ）

### 2.1 物理原因

TSV 铜挤压 → Si 晶格损伤 →

1. 漏电流（induced by TSV stress → bandgap 变化）
2. 迁移可靠性（electromigration）
3. 时序失配（mobility 变化）

→ 不能埋在活性区正下方 → 必须保持 **KOZ**（半径约 0.2–5 μm，与节点强相关）

### 2.2 工艺节点 vs KOZ

| 工艺节点 | KOZ 半径 | TSV 间距最小 |
|----------|---------|--------------|
| 130 nm | 3–5 μm | ~20 μm |
| 28 nm | ~1.0 μm | ~5 μm |
| 7 nm | **0.2–0.6 μm** | ~2 μm |

→ **节点越先进，KOZ 越小** → 高密度 3D 集成是 modern SoC（5–7 nm）的甜蜜区。

### 2.3 面积代价

单 TSV KOZ 占比：
- 130 nm：约 5% 面积（KOZ/TSV-pitch²）
- 7 nm：约 0.5%

但**多层堆叠** KOZ 累加 → 一颗 8 层 HBM 总 KOZ 体积约 8–15% 总 die 体积。

**实际影响**：3D NoC 路由器的 vertical port 数必须包含 KOZ 区域；多层堆叠时顶层与底层的 "可通过 TSV 数" 差异大。

---

## 三、寄生 R/C 模型

### 3.1 关键公式

```
R_TSV ≈ ρ·L / (π·r²)        ~5–50 mΩ  （L=50 μm, r=2.5 μm Cu）
C_TSV ≈ 2π·ε·L / ln((2·R+K)/r)  ~10–100 fF  （L=50 μm, 间距 10 μm）
```

### 3.2 延迟量级

```
delay_TSV ≈ R_TSV × C_TSV + R_driver × C_TSV
         ≈ 1–10 ps               （TSV 本征延迟）
```

**对照**：
- 水平 M9 wire ~50 ps/mm → 1 mm 跳一 router 节点 ~50 ps
- TSV 垂直跳 ~5 ps（同 die**等长度等价**延迟约 5–10× 快）

→ "垂直更快" 在物理层成立。

### 3.3 带宽

```
BW_TSV ≤ data_rate × pitch_density × wires_per_link
```

- pitch 5 μm × 5-wire × 1 Gbps/wire = 1 Gbps/μm = 不需要
- 实际上商品 TSV 单 Gbps 链路；HBM3 TSV 单 Gbps 级 TSV 通道**约 1024 通道/TSV-stack 每 die** → 总带宽 TB/s 量级

### 3.4 重要的反直觉

TSV 物理延迟比水平 wire 快，**但端口密度受 KOZ 与 pitch 限制**。这导致：

- 垂直链路 100% 单向能力被端口数约束 → 真正瓶颈是 **port count**，不是 **per-port speed**
- 这就是为什么 2008–2018 年 3D NoC 论文普遍 "5-port vertical 部分连接 mesh" 的原因

---

## 四、热密度（最讨厌的副作用）

### 4.1 量级

单片功率密度 ~1 W/cm² 量级。
3D 堆叠（4–8 层）：
- 单层仍 1 W/cm²
- 但**热导出仍在单层基底** → 等效堆叠芯片温度 = 1 W/cm² × n 层 / K_th
- K_th 3D 集成 ~10× 单层硅（堆叠高阻） → n=4 时等效 0.4 W/cm² 不变（密度不是温度决定因素，**实际温度**因**热流密度**上升）

```
T_top - T_ambient = Σ(P_i × R_th_i)
```

3D 集成上层温度 110–130 °C（vs 单片 70 °C），路由器命中 ≥ 5 GHz 时频率下降~10–20%。

### 4.2 路由器影响

- **最热**：router + local SRAM（消耗 local 40% 功耗）
- **次**：附近 tile 的 port 连接 TSV 区域

→ 3D NoC 路由器经常是**最热也最慢**的组件，从而路由往往转向 → thermal-aware DOR。

### 4.3 解药（学术方向）

| 思路 | 代表 |
|------|------|
| Thermal-Aware Routing (TA-DOR) | 多篇 2009–2014 |
| Dynamic Thermal Management (DTM) | 综述型 |
| 热感 + voltage scaling | DVFS + thermal model |
| layout-aware mapping | Voxel + FEATHER |

---

## 五、良率模型

### 5.1 标准模型

```
Y_die = exp(-A · N_TSV / A_chip · λ_TSV)
```

其中：
- A = 芯片面积（cm²）
- N_TSV = TSV 总数
- A_chip · λ_TSV = 每片 TSV 缺陷率；λ_TSV ~ 100–1000 ppm

**一块 1 cm² die × 100K TSVs × 100 ppm**：
```
Y = exp(-100) ≈ 0
```

→ **不可接受**。这就是为什么商用 3D 必带：

### 5.2 良率增强

1. **TSV 冗余 + 自修**：每个逻辑 TSV 群附加 1–4 冗余 TSV；自修电路连接
2. **分区测试**：die 内分多个 TSV 簇，独立测试
3. **die-matching**：堆叠前 KGD（Known Good Die）筛选

### 5.3 工业级表现

- **AMD 3D V-Cache**：12 TSV 簇 × 13 TSV/簇 = ~150 TSV； 良率实际可逆
- **HBM3 12-Hi**：每 die ~5000 TSV；通过冗余 / 测试策略实际良率 > 60%

---

## 六、为什么这层 Layer 1 是 3D NoC 的关键

1. **假设所有 3D NoC 论文应追溯到 TSV 物理约束**：纸面上的 5-port / 7-port 路由器必说 TSV
2. **假设 hybrid bonding 之后（2018+）物理约束松动**：再读 newer 论文时 KOZ 不再主导 → 但是**热密度**仍主导
3. **假设良率模型关注**：任何 3D IC 实际产品 paper 必谈良率；纯算法型 paper 可免，但这不是现实的盲区

---

## 七、Wiki 资产复用 + Layer 1 后进入的下一个层

- ← [Concepts 3D Stacking Technologies](/concepts/3d-stacking-technologies.md)：与既有 3D-Stacked AI Chip / Post-Moore 互补
- ← [Concepts Through-Silicon Via Physical Layer](/concepts/tsv-3d-physical-layer.md)：本笔记提炼的入门概念
- → Layer 2（拓扑）：[3D Mesh / Stacked Mesh / NoC-over-NoC-under] — 学完 TSV 物理约束后才能真正读懂"为什么 7-port 路由器是 trade-off"
- → Layer 3（路由）：X-Y-Z DOR + thermal-aware routing
- → Layer 5（系统）：HBM3 / HBM4 / 3D-DRAM 实产品 / AMD MI300 / Apple M-Ultra — hybrid bonding 商用案例

---

## 八、个人待解问题（学完后自检）

1. **monolithic 3D vs TSV**：2026 工艺下，KOZ 是 still 主导 vs monolithic dense 主导？
2. **HBM3 / HBM4 / HBM5 的趋势**：TSV 数 / die 是平稳 / 上升 / 怎样向 hybrid bonding 过渡？
3. **热：能否 3D NoC layer 中允许"hot layer 专做 compute" + "cold layer 专做 SRAM/DRAM"？** Voxel 论文事实上做了
4. **良率：冗余 TSV cluster 的最佳分组粒度**？在 1 Gbps/per TSV 链接下？

---

# Citations

[1] Katti et al., *IEEE Comm. Mag.* 2010 — TSV 综述（IEEE Xplore）
[2] Garrou et al., *Introduction to 3D Microelectronic Packaging*, Wiley 2008 — 教科书入门
[3] Lau, J.H., *Evolution, Challenges and Outlook of 3D IC/Si Integration*, Springer 2011
[4] [papers/katti-tsv-technology-roadmap-2010.md](../../papers/katti-tsv-technology-roadmap-2010.md) — 本笔记提炼的标准入口论文页
