---
type: Raw Source
title: 📰 3D NoC Study Day 4 — Feero 3D Mesh NoC 基线 + 后续派生
source_path: /home/luke/wiki/raw/articles/3d-noc-study-04-3d-mesh-baseline.md
textbook: Feero et al. IEEE Microelectronics Journal 2008；Park HPCA 2008 (NoC-over-NoC-under); Rahimi et al. (partially-connected 3-D Mesh). 此为综述学记
ingested: 2026-07-31
---

# 📰 3D NoC Study Day 4 — Feero 3D Mesh NoC + 后续派生

📅 2026-07-31（Day 4）
🎯 阶段：Layer 1 收束（边缘 — 要开始 Layer 2 拓扑，但 Feero 必须以基线形式先建立）
📖 教材：综述整合 + Feero 原文 + Park + Rahimi 派生

---

## 今日主题：3-D Mesh 拓扑基线 + 历史假设与新假设

### 🧭 为什么学 Feero 2008？

Layer 1（物理层）最后一天的边界：**抽象地把物理转成拓扑**。3D NoC 拓扑研究的起点必是 Feero 2008 "Networks-on-Chip in a Three-Dimensional Environment"，原因：

1. **架构师必读** — 任何现代 3D NoC paper 几乎都 cite 它作 baseline
2. **基本 trade-off 已建立**：垂直 port 数 trade-off；直径 vs 路由器面积；bandwidth per dimension
3. **历史局限 = 现代机会**：今天 hybrid bonding 已 commercial，Feero 的 5-port 假设在 2024 并不成立 → 这是研究空间

### 🎯 今天的目标

- 熟记 **3-D Mesh 拓扑 关键量化指标**：port/diameter/bisection
- 熟记 **X-Y-Z DOR 路由**，能写伪代码
- 知道 Feero 假设的 TSV 物理约束（5-port）与 hybrid bonding 不匹配 → 这是研究 gap
- 知道 Park NoC-over-NoC-under 与 Rahimi partial 3D Mesh 的扩展思路
- 知道 Day 5 (3-D Stacked Mesh / 拓扑对比) 从这里引出

---

## 一、Feero 2008 抽象模型

### 1.1 拓扑

```
3-D Mesh: n³ 个 tile，每个 tile 在 (x, y, z) 坐标
每 tile 沿 x, y 双向各有一邻居
z 方向同样：每 tile 有上下 + 上下 + 邻居 = 6 个外置 port + 1 local CPU port
```

### 1.2 量化对比 2D vs 3D

| 指标 | 2-D Mesh n × n | 3-D Mesh n × n × n |
|------|----------------|---------------------|
| 节点数 | n² | n³ |
| 直径（零负载 hop） | 2(n−1) ≈ 2√N | 3(n−1) ≈ 3 N^(1/3) |
| 路由器 port | 5 (N, E, S, W, Local) | **7** (5 + Up, Down) |
| bisection BW 边界 | √N | N^(2/3) |
| 单 port area | 0.5× | **1.4×** (more port) |

→ **直觉结论**：3-D Mesh 半径短，但每个 router 更贵。净效应：

- 较好工作负载 (uniform random / hotspot / multicast)
- 较差工作负载 (nearby traffic) — 2-D 已经够

### 1.3 关键 Feero 结论原文摘录（rephrased）

1. **3D 缩短直径**：约 1/3 (n=4 cube: 2D 直径 6 → 3D 直径 3)
2. **路由器功耗+35%，面积+40%**：5 vs 7 port 都是真实代价
3. **总功耗降低 ~10%** 因为直径缩短
4. **TSV pitch 与 KOZ 是 5-port 假设的根源**

---

## 二、X-Y-Z DOR（确定性 + 无环）

### 2.1 路由算法

```python
def xyz_dor_route(src, dst, mesh):
    """Deterministic routing in a 3-D Mesh using dimensional order (X→Y→Z)."""
    path = [src]
    x, y, z = src
    # Phase 1: cancel ΔX
    while x != dst.x:
        x += 1 if dst.x > x else -1
        path.append((x, y, z))
    # Phase 2: cancel ΔY
    while y != dst.y:
        y += 1 if dst.y > y else -1
        path.append((x, y, z))
    # Phase 3: cancel ΔZ
    while z != dst.z:
        z += 1 if dst.z > z else -1
        path.append((x, y, z))
    return path
```

**无环证明 (CDG)**：3 维 DOR 仍是无环的 deterministic 路由。 拓扑隐式给出：维度序约束 ↔ 通道依赖形成 DAG。

### 2.2 路由器的 4-cycle 处理

每个 router 内部 5 stage pipeline 不变（见 H&P App.F 第 4 节）：
- RC → VA → SA → ST → LT
- 关键是 **port count 从 5 → 7** 让 crossbar / allocators 更复杂

---

## 三、后续论文的派生

### 3.1 Park HPCA 2008: NoC-over-NoC-under

Park 把 3-D Mesh 扩展：

```
┌──────────────────┐   ← 上层：logic
│ 2-D Mesh NoC     │   
├──────────────────┤   
│ vertical link    │   ← 通过 via-middle TSV
├──────────────────┤   
│ 下层：DRAM bank  │   
│ 2-D Mesh NoC     │   
└──────────────────┘   
```

**目的**：3-D Mesh 假设全局同质，但事实上 memory 层 ≠ compute 层；分层 NoC 单独优化 — Pack 不强制两层用相同 router / link speed

**关键贡献**：在不增加 port 假设下推 Heterogeneous 3-D Mesh

### 3.2 Rahimi (Partially-Connected 3D Mesh)

为缓解 KOZ+TSV 比不足：
- 仅在 **每 n 行** 设立 vertical port（n > 1）
- 牺牲 ~5–10% diameter 节省 30–40% port 数 / KOZ

→ "减少端口" 在 TSV 时代是学术主流对策。

### 3.3 Modern Era (2020+): Hybrid Bonding 重写假设

**关键事实**：Feero+PArd+Rahimi 共同基础是 "5-port 极限"—— hybrid bonding 1 μm pitch 之后不严格成立。但是**仍大论文沿用**：

- 因为论文需 reproducibly (与 baseline 对比) → 用 TSV-based 假设对比
- 因为复用 2-D NoC components（router 微架构）→ 7 port 兼容 router 关键设计

---

## 四、对 Direction 2 研究的 position

你的 mesh-NoC + decode research 是在 2-D Mesh 假设下做 → 3D NoC 是个有趣侧途：

- **不直接相关**：你的研究在 2-D Mesh 上做 decode GEMV 调度
- **但 hybrid bonding 3D 把 2-D Mesh 变 3-D Mesh 不需要编译器重写**：这意味着未来你的方案可以向上扩展 → 给研究一个"应用场景"
- **但 short-term 来说**：hybrid bonding 3D Mesh 仍然 KOZ-小但 thermal-budget 紧 → 对你现有的 mesh-NoC 模型仅需调整 thermal-aware 部分

→ 我建议在你的研究中**先固定 2-D Mesh 假设**，3D Mesh 作为未来扩展标定。

---

## 五、Wiki 链接

- ← [Concepts Through-Silicon Via Physical Layer](/concepts/tsv-3d-physical-layer.md)
- ← [Concepts 3D Stacking Technologies](/concepts/3d-stacking-technologies.md)
- ← [Concepts Mesh and Torus Topology](/concepts/mesh-torus-topology.md)：2-D Mesh base
- → [Concepts Deterministic Routing DOR](/concepts/deterministic-routing-dor.md)：X-Y DOR base
- → [Layer 2: 3D 拓扑分类]: Day 5 学 Stacked Mesh + NoC-over-NoC-under + Hybrid Bonding Mesh

---

## 六、个人待解问题

1. **Feero baseline 5-port 与 hybrid bonding 8+ port 的性能差异量化**：需要实际 仿真
2. **Hybrid Bonding 时代的 3-D Mesh topology**：是否能用 simple full 3-D Mesh？还是 仍需 partially connected？
3. **Bufferless Router 在 3-D Mesh 中**：TSV 假设下成立，hybrid bonding 假设下是否仍成立？
4. **Thermal-Aware DOR**：3D 层间冷却是关键，路由算法能否回避热门层？

---

# Citations

[1] Feero et al., *Networks-on-Chip in a Three-Dimensional Environment*, 2008 (and 多年后续)
[2] Park HPCA 2008 *NoC-over-NoC-under*
[3] Rahimi et al. (on Partial 3D Mesh)
[4] [papers/feero-3d-mesh-noc-stan-2008.md](../../papers/feero-3d-mesh-noc-stan-2008.md) — 入口论文页
