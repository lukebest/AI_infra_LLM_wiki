---
type: Concept
title: Layout-Aware NoC and Flexible Dataflow Accelerators
description: NoC 感知 / 转换 / 消除矩阵数据 layout 的 4 类技术路线：L1 raw bytes / L2 multicast 隐式 / L3 reorder network 显式 / L4 runtime fission-fusion + L5 反向（编译期消除）；代表工作 MAERI / SIGMA / FEATHER(BIRRD+RIR) / Venus / SmartMem
tags:
- noc
- layout
- dataflow
- flexible
- reorder
- permutation
- featherm, maeri
- sigma
- venus
- smartmem
- kwon-krishna
timestamp: '2026-07-22T00:00:00Z'
created: 2026-07-22
sources:
- papers/maeri-flexible-dataflow-reconfigurable-interconnects.md
- papers/sigma-sparse-gemm-flexible-interconnects.md
- papers/feather-reconfigurable-accelerator.md
- papers/venus-versatile-reconfigurable-accelerator.md
- papers/smartmem-layout-transformation-elimination.md
- concepts/feather-accelerator.md
- concepts/plasticine-accelerator.md
- concepts/eyeriss-accelerator.md
---

# Layout-Aware NoC and Flexible Dataflow Accelerators（带 Layout 调整的 NoC）

> **核心问题**：DNN layer 之间**所需数据 layout 不同**（row-major vs col-major vs tiled vs blocked），而 **NoC 传输数据时**并不感知这些 layout → 产生**显式 layout 转换开销**（buffer 写入 + bank conflict + intermediate reshape）。
>
> "Layout-aware NoC" 是 NoC **能感知 / 转换 / 适配**矩阵数据 layout 的能力 —— 这是现代 DNN 加速器性能的关键杠杆。

## 为什么 layout mismatch 是问题

DNN layer 之间的 **producer-consumer 边** 经常需要 layout 转换：

```
Conv (输入 NCHW) → 输出 NHWC → LayerNorm → 输出 row-major → MatMul (输入 col-major)
        ↓
        layout1 → layout2 → layout3
        每个箭头都需要"某种形式的转换"
```

**传统的 rigid NoC**（如 systolic、Eyeriss 固定 multicast）**不感知** layout，**每个 layer 用同一个 distribution pattern** → 经常需要显式 transpose / reshape → 开销巨大。

## 5 类技术路线（按"NoC 感知 layout 的能力"分层）

| # | 能力 | NoC 做什么 | 代表工作 |
|---|------|-----------|---------|
| **L1** | **完全不感知** | 只搬 raw flit，按 packet routing | 传统 mesh / Torus |
| **L2** | **隐式感知（multicast / gather）** | 提供 pattern 化通信原语 | **Eyeriss**（RS + multicast NoC）|
| **L3** | **显式 layout 转换（reorder network）** | NoC 内部有 permutation / butterfly 网络，**主动重组数据** | **MAERI, SIGMA, FEATHER（BIRRD）** |
| **L4** | **runtime layout + dataflow 联合可重构** | NoC 每 layer / 每 workload **重新连接** | **Venus, FlexNN, Adapt-NoC** |
| **L5** | **编译期消除 layout 转换**（反向） | NoC 不变，**编译器消除问题** | **SmartMem** |

## L2：Multicast / Gather（隐式感知）

### Eyeriss（MIT, ISCA 2016 / JSSC 2017）

**Row Stationary (RS) dataflow** + **multicast + point-to-point 混合 NoC**：
- multicast 给同一行所有 PE 广播（reuse input row across PEs）
- point-to-point 给单个 PE 送（drain psum）
- **layout 适配能力**：RS dataflow 让 layout 和 NoC multicast pattern **自然对齐**
- **结果**：NoC 不做显式 layout 转换，但**通过 multicast 原语间接支持 RS 的数据 layout**
- **局限**：RS 是单一 dataflow，换成 output-stationary / weight-stationary 就欠优

> Eyeriss **不是 layout-aware NoC**，但**是 layout-friendly NoC**（通过 multicast 原语隐式支持 RS dataflow 的 layout）。

## L3：Reorder Network（显式转换）

### 1️⃣ MAERI（Georgia Tech, ASPLOS 2018）

**核心创新**：**ART (Augmented Reduction Tree) + Distribution Tree + tiny switches**
- 每个 PE 之间可以被 **tiny switches** 重新连接
- 编译器根据 layer 类型，**编译期**配置 switches
- **任意 broadcast / multicast / scatter 模式** → 任意 layout 都能映射

**数字**：vs rigid baseline 利用率 **8-459%** 提升；+6.5% power；+47% area vs systolic。

[paper 摘要](/papers/maeri-flexible-dataflow-reconfigurable-interconnects.md)

### 2️⃣ SIGMA（Georgia Tech, HPCA 2020）

**MAERI 的 sparse + training 延伸**：**Flex-DPE + FAN（Forwarding Adder Network）**
- Flex-DPE = MAC tree + flexible interconnect
- 通过 global NoC 把多个 Flex-DPE 组成 Flex-DPU
- **SIGMA 可以 morph**：1 个大 Flex-DPU 跑 1 个 GEMM，或 N 个小 Flex-DPU 并行
- **FAN**：partial sum 中间节点转发，避免固定层级 reduction
- **专门优化 sparse + training GEMM**

**数字**：vs systolic on irregular sparse **5.7×**；vs SOTA sparse accelerators **3×**；10.8 TFLOPS effective @ 28nm, 65mm², 22W。

[paper 摘要](/papers/sigma-sparse-gemm-flexible-interconnects.md)

### 3️⃣ FEATHER（BIRRD + RIR, Georgia Tech, 2024）

**核心创新 — BIRRD（Butterfly Interconnect for Reduction and Reordering in Dataflows）**：
- 4 种 EGG 开关：**Pass / Swap / Add-Left / Add-Right**
- 在**归约阶段**（partial sum 求和）**同时完成 layout 重排**
- 消除"归约后再 reorder (RAR)" 的 critical path

**关键技术：RIR（Reorder In Reduction）**
- 权重**离线** reorder（weights 可静态 reorder）
- **activation 在归约中 online reorder**（不能离线）
- 把 layout 转换**塞进 GEMM 算子的关键路径** → 节省一次显式 reshape

**Layoutloop 编译器**：每层自动 co-search 最佳 **(dataflow, layout)** 对

**数字**：vs Eyeriss / SIGMA / NVDLA：延迟 **1.27-2.89×**，能效 **1.3-6.43×**；vs 固定 dataflow 仅 +6% 面积。

[paper 摘要](/papers/feather-reconfigurable-accelerator.md) | [concept 页](/concepts/feather-accelerator.md)

**MAERI → SIGMA → FEATHER 谱系**（同一团队，渐进式）：

| | MAERI (2018) | SIGMA (2020) | FEATHER (2024) |
|---|--------------|--------------|----------------|
| **interconnect 形态** | distribution + reduction tree | Flex-DPE + FAN | **BIRRD butterfly** |
| **layout 重排** | 任意 distribution，但**归约后**固定 layout | 任意 sparse + dense layout | **RIR（归约中重排）** |
| **场景** | 通用 DNN | sparse + training | DNN + (dataflow, layout) co-switch |
| **关键 wins** | 利用率 8-459% | sparse 5.7× | RIR + Layoutloop 联合搜索 |

## L4：Runtime Fission / Fusion

### 4️⃣ Venus（GWU HPCAT, DAC 2023）

**NoC fission / fusion**：
- **Fission**：1 个 NoC → 多 sub-NoC，每个 DNN 一个独立子网（QoS 隔离）
- **Fusion**：多 sub-NoC → 1 个大 NoC，给 bandwidth-heavy layer 满带宽
- **Distributed buffer**：per-tile layout 自由选择
- **首篇把 layout 适配扩展到 runtime multi-tenant serving**

[paper 摘要](/papers/venus-versatile-reconfigurable-accelerator.md)

### 5️⃣ Adapt-NoC（Ohio U, DAC 2020）
- **Link merge / split**：把相邻 link 合并成更宽的，反之亦可
- 适应 SSMD（单源多目的地）流量，如 DNN 推理、cache coherence

## L5：反向思路——编译期消除（**对照实验**）

### 6️⃣ SmartMem（NC State, ASPLOS 2024）

**与 MAERI/SIGMA/FEATHER 完全相反**：

| | MAERI/SIGMA/FEATHER 路线 | SmartMem 路线 |
|---|--------------------------|---------------|
| 应对 layout mismatch | 让硬件 (NoC / reorder network) 兜底 | **让编译器把问题消灭在源头** |
| layout 转换开销 | 显式 RAR 仍在 (FEATHER 用 RIR 节省 critical path) | **零开销**（直接消除） |
| 硬件要求 | 柔性 interconnect、buffer 重排 | 标准 2.5D 内存即可 |

**算法**：
1. **分类**所有算子为 4 类（ILD-Fixed / ILD-Variable / Customizable / Both）
2. **消除** ILD-Fixed 的 Transpose / Reshape（直接从图中删除）
3. **Co-search** 剩余算子的 layout
4. **映射**到 2.5D 内存

**数字**：2.8× vs DNNFusion、6.9× vs TVM、7.9× vs MNN；18 networks (CNN, Transformer, LLM, Stable Diffusion)；Snapdragon 8 Gen 2。

[paper 摘要](/papers/smartmem-layout-transformation-elimination.md)

## 横向对比表

| 维度 | MAERI | SIGMA | FEATHER | Venus | SmartMem |
|------|-------|-------|---------|-------|----------|
| **会议** | ASPLOS 2018 | HPCA 2020 | arXiv 2024 | DAC 2023 | ASPLOS 2024 |
| **场景** | 通用 DNN | sparse 训练 | DNN 推理 | 多 DNN serving | mobile GPU |
| **interconnect 形态** | tree + tiny switches | Flex-DPE + FAN | BIRRD butterfly | fission/fusion NoC | 标准 GPU |
| **layout 重排位置** | 编译期 distribution | 编译期 + runtime sparse | **归约中** (RIR) | runtime NoC 形态 | **编译期消除** |
| **代价** | 编译期 search | 同上 | 同上 | runtime NoC 重配 | 编译期 layout search |
| **核心 win** | 利用率 8-459% | sparse 5.7× | co-search 1.27-2.89× | multi-DNN 隔离 | layout 转换 = 0 |
| **代表作 (citation)** | [Kwon'18] | [Qin'20] | [Tong'24] | [Yang'23] | [Niu'24] |

## 对 Direction 2（compiler-aware decode on mesh-NoC）的启示

### 关键 insight：mesh-NoC 也需要 layout-aware

WSE 上的 mesh GEMV 同样存在 **layout mismatch**：

| 维度 | 物理 layout | 算法所需 layout |
|------|-------------|-----------------|
| **weight streaming** | 流过式（per-row） | 算子期望 tiled-block |
| **KV cache shift** | Y 方向行间 shift | 算法期望按 head 维度 |
| **K-tree allreduce** | mesh 二叉树 | 算法期望 root 在 "logical center" |
| **GEMM-T (no transpose)** | mesh 上的转置路由 | 算法期望 row×col 自然对齐 |

### 提议的 3 个 pass（**加到 WaferLLM Compiler Research Gaps 第 7 个**）

#### Pass 1：**Layout-aware Mesh Routing**
- 输入：算子图 + mesh 拓扑 + 各 op 的 preferred layout
- 输出：mesh routing plan，让数据 layout 在 source / 中间节点 / sink **逐步对齐**
- 关键：使用 MeshGEMM 的 INTERLEAVE 算法思想，**把 layout 转换塞进 cyclic shifting**

#### Pass 2：**RIR-style Reorder In Reduction for Mesh GEMV**
- 输入：mesh GEMV 的 reduction tree
- 输出：在 K-tree allreduce 路径上**顺便 reorder partial sums**，避免 RAR
- 关键：把 FEATHER 的 RIR 思想迁移到 mesh NoC

#### Pass 3：**Co-Search Compiler (类 Layoutloop)**
- 输入：LLM decode step + mesh 拓扑 + 物理 layout 约束
- 输出：每 decode step 选 best (mesh routing, data layout) pair
- 关键：跟 WaferLLM 的"每模型 autotune"对齐，但放到 **per-decode-step** 粒度

## 相关页面（已有 wiki 资产）

- [FEATHER Accelerator](/concepts/feather-accelerator.md) — L3 reorder 网络代表
- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — 同期 CGRA 路线（parallel patterns）
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — L2 multicast 隐式适配
- [WaferLLM System](/concepts/waferllm-system.md) — mesh-NoC LLM 推理
- [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — Direction 2 入口（新增第 7 gap）
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — MLIR spatiotemporal
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — 算子基础
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — 分布式 GEMM 视角
- [Adapt-NoC (DAC 2020)](#) — link merge / split（待补）
- [FlexNN (2024)](#) — FlexDrain（待补）

## 5 篇核心 paper 速查

| 名称 | 会议/年份 | 关键概念 | 我的评估 |
|------|----------|---------|---------|
| **MAERI** | ASPLOS 2018 | tiny switches + ART | 柔性 NoC 的开创 |
| **SIGMA** | HPCA 2020 | Flex-DPE + FAN | sparse 适配 |
| **FEATHER** | arXiv 2024 | BIRRD + RIR + Layoutloop | **最对口你的方向** |
| **Venus** | DAC 2023 | fission/fusion | runtime multi-tenant |
| **SmartMem** | ASPLOS 2024 | compile-time elimination | **反向哲学** |

# Citations

[1] [raw/papers/MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf](MAERI_Flexible_Dataflow_Reconfigurable_Interconnects_ASPLOS2018.pdf) — Kwon et al. ASPLOS 2018
[2] [raw/papers/SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf](SIGMA_Sparse_GEMM_Flexible_Interconnects_HPCA2020.pdf) — Qin et al. HPCA 2020
[3] [raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf](FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf) — Tong et al. arXiv 2405.13170
[4] [raw/papers/Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf](Venus_Versatile_Reconfigurable_Accelerator_DAC2023.pdf) — Yang et al. DAC 2023
[5] [raw/papers/SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf](SmartMem_Layout_Transformation_Elimination_ASPLOS2024.pdf) — Niu et al. ASPLOS 2024