---
type: Concept
title: Network-on-Wafer
description: 晶圆级互连（NoW）：field stitching / chiplet-on-fanout / WoW hybrid bonding 三条物理路线决定拓扑是否能同层直连；放置即拓扑
tags:
- now
- network-on-wafer
- wafer-on-wafer
- wse
- noc
- interconnect
- hybrid-bonding
- chiplet
- mesh
- 3d
- packaging
- fabric
- architecture
timestamp: '2026-08-26T00:00:00Z'
created: 2026-08-18
updated: 2026-08-26
sources:
- raw/papers/network-design-wafer-scale-wow-hybrid-bonding.md
- papers/network-design-wafer-scale-wow-hybrid-bonding.md
- papers/mozart-35d-wafer-scale-moe-training.md
- papers/fovea-physical-implication-aware-wafer-scale-dse.md
- papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md
- papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md
---

# Network-on-Wafer（晶圆级网络 / NoW）

把**整片或近整片晶圆**当作一个 scale-up 域时，reticle / die 之间的互连不再是常规 NoC 或板级 D2D，而是被光罩尺寸、键合几何和封装路线卡住的 **Network-on-Wafer**。拓扑往往不是先画图再布线，而是 **物理放置长出拓扑**。

## 三条 WSI 物理路线

| 路线 | 代表 | 同层相邻能否直连 | 垂直维 | 对 NoW 的含义 |
|------|------|------------------|--------|----------------|
| Field stitching | [Cerebras WSE](/entities/cerebras-wse.md) | 能（曝光重叠缝出连续金属） | 无（单片） | 软件看到均匀 2D mesh；缝上有冗余绕故障 |
| Chiplet-on-fanout | Tesla Dojo、若干 WSC 论文 | 能（扇出 / 中介层 + PHY） | 通常无 | 可做 mesh / Clos-like；要付 D2D PHY 面积与功耗 |
| **WoW hybrid bonding** | TSMC SoIC-WoW；[Iff et al. 2026](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) | **不能** | 面对面 HB，pitch <10 μm 量产 / 1 μm 研究 | 只有对侧重叠 reticle 能连；**放置 = 拓扑** |

第三种是 2026 年才被系统当网络问题写的：HB 电气接近上层金属、**不需要 PHY**，但几何重叠是硬约束。详见 [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)、[Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md)。

## WoW 下的设计旋钮

1. **Logic-on-Interconnect vs Logic-on-Logic**：底片纯互连（热简单、算力减半）还是两片都有 compute（密度高、热/电难）。
2. **Radix via overlap**：半格错位 ≈ mesh、radix-4；互连 reticle 旋转/交错提到 radix-6；45° 缩小互连 reticle 提到 radix-7；LoL 用轮廓 reticle 提到 radix-5。
3. **路由**：不规则图上 Dijkstra 最短路 + SCB 破环；选择随机或看邻居 buffer。
4. **利用率**：矩形网格 vs 尽量填满圆晶圆。Iff 文最大收益出现在最大填充 + LoI。

论文数字（只复述）：相对 mesh-like baseline 吞吐最高 **+250%**、延迟 **-36%**、每字节能量 **-38%**；Llama-7B 训练 trace 平均延迟到 baseline 的 **60%**。

## 与 3.5D chiplet 树的对照

[Mozart](/papers/mozart-35d-wafer-scale-moe-training.md) 也是晶圆级，但互连是 **2.5D NoP-Tree**（中心 attention、叶专家、in-network switch），垂直维是 per-chiplet logic-on-SRAM hybrid bonding，不是 WoW 重叠成网。它优化的是 MoE All-to-All 的 token 复制数 C_T，不是平均路径 hop。

[3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) 把隔离做在 **封装垂直维**（KVT vs decode AllReduce），侧向仍是 2.5D D2D，不是整晶圆 NoW。相关工作引用了 WSC-LLM 与 PD-aware NoW 共设计。

[HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) 是 **chiplet-on-fanout 近亲**：被动硅 interposer 上最多 24 个计算 die、2D mesh NoI。它优化 hybrid LLM serving 的组成/放置/D2D 带宽，**不是**场拼接，也不是 WoW 重叠成网。

Samsung [zHBM](/papers/hc2026-samsung-hbm-base-die.md)（Hot Chips 2026）也写 **WoW + HCB**，但是 **xPU 垂直叠到 HBM C-die**、取消 2.5D interposer——封装级 3D，**不是**整晶圆 NoW 重叠网。[Pistil](/papers/hc2026-pistil-20-chiplet-slm.md) 是 20-chiplet 2.5D flower，更不是晶圆级。

## 和 wiki 已有 mesh/WSE 页的关系

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — WSE/Dojo 默认 2D mesh；WoW baseline 只是“像 mesh”，**不能**用 XY 维序。
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上集体硬件；WoW 文评的是 packet 吞吐，集体算法仍空。
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) / [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) — field-stitch mesh 上的 reduce；不能直接搬到重叠约束图。
- [WaferLLM System](/concepts/waferllm-system.md) — 在 Cerebras 均匀 mesh 上做 LLM 算子；NoW 换拓扑后 MeshGEMM/V 的两跳假设要重验。
- [AIC Folded Multi-Ring NoC](/concepts/aic-folded-multi-ring-noc.md) — reticle 尺度折叠环，不是晶圆级重叠网。
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — **封装内** CCD–IOD SerDes PHY（PAM4+FEC）。WoW hybrid bonding 电气接近上层金属、通常不需要这层 PHY；不要把 DICE 的误码/重传数字套到 NoW。

## 晶圆级 DSE：先构造可行域

[Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md)（清华，2026-08）不设计新拓扑，而是论证：**同质 repeated-die 晶圆仍然不是一张万能模板**。die 轮廓同时决定光罩合规、tiling、D2D lane 数和边界 I/O 能否放下；面积可行里平均 29.4% 的分析 top-10% 会被物理约束打掉。分析 vs ASTRA-sim+ns-3 约 4000× 成本且 20.96% 成对反转，所以用 Decision Domain 只精评无法排除的候选。范围是 chiplet-on-wafer 边界 D2D，**不是** WoW 重叠网，也不是 Cerebras field stitch。

## 当前认知

- **NoW 不是“大号 NoC”**：物理路线先决定边集合，再谈路由/流控。
- **2026 年可写进设计空间的轴**：WoW 重叠几何（Iff/ETH）、3.5D 异构树（Mozart）、以及同质 repeated-die 的物理可行域+多保真确认（Fovea）。
- **集体通信、良率、热** 仍是开放层：Iff 指出 FRED 式 Clos-like 在 WoW 几何下不可行；Mozart 自陈仍 memory-bound。

## 开放问题

1. 不规则 WoW 图上的 AllReduce / All-to-All 最优算法是什么？
2. Field-stitch 均匀 mesh 与 WoW 高 radix 不规则图，对 [WaferLLM](/concepts/waferllm-system.md) 类算子谁更友好？
3. Photonic NoW（检索到 ISPASS 2026 DyPNet-MSC，本轮未 ingest）如何与电学 WoW 比较？
4. 3DLS 的垂直隔离能否叠在 WoW 的 LoL 上，做成“层间 KVT + 层内高 radix NoW”？
5. Fovea 的 Decision Domain 能否接到 WoW 重叠几何 / 异构 chiplet 混合物？

# Citations

[1] [raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf](raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf) — Iff et al. 2026
[2] [raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf](raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf) — Luo et al. 2026
[3] [raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf](raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf) — Li et al. 2026
[4] [raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf](raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf) — Lee et al. 2026
