---
type: Analysis
title: WaferLLM Compiler Research Gaps
description: WaferLLM (OSDI 2025) 作者本人承认但未解决的 3 个 decode 阶段瓶颈（48KB SRAM underutilization、edge cores、K=2 硬编码）→ 编译器视角的 research opportunity：MLIR PLMR-aware dialect + 3 个 pass
tags:
- waferllm
- compiler
- mlir
- gap-analysis
- direction-2
- decode
- mesh-noc
- research-direction
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf
- concepts/waferllm-system.md
- concepts/distributed-gemm-algorithms.md
---

# WaferLLM Compiler Research Gaps

> **TL;DR**：WaferLLM 是 PLMR mesh-NoC 加速器上**首个**完整 LLM 推理系统（OSDI 2025, He et al.）。但论文 **§7.5、§8** 明确承认 3 个 decode 阶段瓶颈**未解**。这 3 个瓶颈是**编译器视角的** —— 需要 MLIR/TVM 层 pass，而非手写 CSL。这是 Direction 2（compiler-aware decode on mesh-NoC）的研究入口。

## 三个被作者承认的未解瓶颈

### Gap 1: 48KB SRAM 限制 → 5× underutilization

> §7.5 原话："limited local SRAM (**48KB**) on WSE-2 cores, which hinders efficient tensor parallelism and necessitates pipeline parallelism, **causing up to 5× underutilization**"

**机制**：48KB/核装不下 decode 阶段 tensor parallel 的完整 working set，被迫用 **pipeline parallelism**（而不是 fine-grained tensor parallel），导致 core 利用率只有 1/5。

**论文给出的"未来方案"**：

> §8 "Increasing a core's local memory by **5-6×** could eliminate the need for pipeline parallelism, enabling full tensor parallelism"

**但作者没做**：有没有**不靠硬件升级**的编译器手段？

**Compiler 视角机会**：
- **Persistent kernel** —— 把 decode 算子 fusion 化，让一个 kernel 在一个核上**常驻**，减少 working set 重载
- **Activation recomputation** —— 编译器自动识别"用完即可丢弃"的中间 activation，主动 recompute 换 SRAM
- **Operator fission** —— 拆小算子，让每个 working set 落在 48KB 内
- **In-place KV cache update** —— 编译器保证 KV 更新原地进行，节省 KV 中间 buffer

### Gap 2: edge cores underutilization（论文一笔带过）

> §7.5 原话："edge cores are **underutilized**"（仅一句话提及）

**为什么 edge core 利用率低**（论文没展开）：
- mesh 边缘核通信邻居少（2-3 个 vs 内部 4 个）
- mesh 边缘核可分配的工作负载少（外圈 mesh 长度 < 内圈）
- 算子 partition 算法默认从 (0,0) 起点放矩形，没考虑 mesh 几何

**Compiler 视角机会**：
- **Topology-aware placement pass** —— 用 ILP/cost model 自动算"哪组核放哪段算子"，让 edge core 不闲置
- **Multi-tile scheduling** —— 把 decode 的小算子（如 RMSNorm、Softmax）显式**多映射**到 edge core，让它们有事可做
- **Geometry-aware NoC 通信预测** —— placement pass 的 cost model 包含 edge 系数

### Gap 3: K=2 K-tree allreduce 硬编码

> §6.2 原话："Considering these factors, we have chosen **K = 2** for our current implementation"

**作者承认**（§6.2）：
> "a larger K is not always better, as it depends on **N and R constraints**. Additionally, larger K increases routing complexity and overhead."

**但作者没做**：cost model 自动搜 K。

**Compiler 视角机会**：
- **K-search pass** —— 给定 N（核数）+ R（路由路径预算）作为输入，cost model 在 (latency, routing) Pareto 前沿上搜最优 K
- **Adaptive K selection per phase** —— prefill 用 K=2，decode 用 K=4（decode 路由预算更紧）
- **Compiler-cost-model-driven autotune** —— 类似 TVM Ansor / AutoScheduler 的 cost model + 搜索

## 进一步：WaferLLM 没提及的 Compiler 视角 Gap

精读论文还发现 3 个**作者完全没提**的 hook：

### Gap 4: Shift-based KV cache 只解决行方向不平衡

> Figure 5 描述 shift 是**行间**老 KV 向上 shift（Y 方向），**X 方向 head 维度的不平衡没解**

**为什么有问题**：
- GQA（Grouped Query Attention）下，**多个 Q head 共享 1 个 KV head** —— X 方向 head 维度的负载天然不均
- 长 context 时 X 方向 head 间的 KV 长度差异更大

**Compiler 视角机会**：
- **二维 KV shift** —— 行 + 列同时做 shift
- **Head-aware shift** —— 编译器根据 head 间 KV size 差异，决定 shift 步长
- **Topo-aware shift ordering** —— shift 方向根据 mesh 长宽比决定

### Gap 5: Routing 资源约束是**硬约束**但**无编译器层 utilization 指标**

> §3.1: "each core can recognize only message headers with a 5-bit address code, so at most **2^5 = 32** distinct routing paths"

**论文假设"软使用 25"**（"less than 25 on Cerebras WSE-2"），但**编译器层没有任何工具**告诉程序员"这个 placement 已用 30/32 paths"。

**Compiler 视角机会**：
- **Routing-aware placement pass** —— placement 输出包含每核已用 routing paths 数 + 余量
- **Routing budget violation diagnostic** —— 当 placement 超出 32 时给 warning
- **Multi-pass iterative placement** —— 像 register allocation 那样做 spillover

### Gap 6: 论文作者承认"未达 7000× 理论上限" —— 这是 honest evaluation 的金矿

> §7.5: "WaferLLM does not achieve the theoretical 7,000× improvement. Profiling identifies three contributing factors: (i) cores cannot fully overlap memory and computation; (ii) edge cores are underutilized; (iii) NoC long-range communication overhead persists, despite MeshGEMV mitigating it."

**编译器视角的 3 个对应优化**：
- (i) overlap → **compiler-directed prefetching** / **double buffering**
- (ii) edge cores → 见 Gap 2
- (iii) NoC long-range → **编译器做通信 schedule 重排**，把长程通信隐藏在短程计算中（类 LoopLynx head-wise pipelining）

### Gap 7: layout-aware mesh GEMV — 编译器视角的第 7 个 research gap

**WaferLLM 论文完全没讨论的问题**：mesh-NoC 上矩阵数据的 **layout mismatch**。

**问题分析**：WSE 上每个 mesh GEMV 算子都涉及**两种物理 layout**：
- **weight streaming layout**：per-row 流过 SRAM
- **KV cache layout**：按 head × seq 在 mesh 上分布

但**算法期望的 layout**：
- GEMV reduction 期望按 column-aligned
- K-tree allreduce 期望 logical-center root
- KV cache shift 期望 head-aware distribution

**这中间没有 alignment** → **explicit transpose / reshape 开销**存在 mesh 数据通路里 → **作者没意识到 / 没量化**。

**借鉴 FEATHER（BIRRD + RIR）的解法**：
- **RIR（Reorder In Reduction）思想**：把 layout 转换塞进 K-tree allreduce 的 reduction 路径
- **Layoutloop 思想**：per-decode-step co-search best (mesh routing, data layout) pair
- **MAERI 思想**：编译器把 model layout 映射进 fabric，让 layout mismatch 在编译期就消除

**Compiler 视角的 3 个新 pass**（加到下面"阶段 B"）：
- Pass 4：**Layout-aware Mesh Routing** —— 在 mesh cyclic shifting 中塞 layout 转换
- Pass 5：**RIR-style Reorder in K-tree Allreduce** —— reduction 路径上重排 partial sums
- Pass 6：**Per-decode-step Layout Co-Search** —— 类 Layoutloop

**关联资产**：见 [Layout-Aware NoC and Flexible Dataflow Accelerators](/concepts/layout-aware-noc-flexible-dataflow.md) — 5 篇核心 paper（MAERI / SIGMA / FEATHER / Venus / SmartMem）+ 5 类技术路线。

## Direction 2 的具体技术路径

### 阶段 A（1-2 月）：搭 PLMR-aware MLIR dialect

```mlir
// 伪代码示意
plmr.mesh_tile {row=0, col=0, sramb_kb=48} : !plmr.tile
plmr.interleave_shift %A, %B {k=2} : (!plmr.tile, !plmr.tile) -> !plmr.tile
plmr.k_tree_allreduce %C {k=2, n_groups=4} : !plmr.tile
plmr.kv_shift %kv {direction="up", stride=1} : !plmr.kv_block
// 新增（Gap 7）：
plmr.layout_transform %data {from="NHWC", to="NCHW"} : !plmr.tile
plmr.rir_reorder %psum {pattern="swap"} : !plmr.partial_sum
```

**目标**：在 MLIR 中表达所有 PLMR-aware 操作

### 阶段 B（2-3 月）：6 个核心 pass（原 3 个 + 新 3 个）

**原 3 个 pass**：
1. **Routing-Aware Placement Pass** —— 输入算子图 + mesh 拓扑 + 路由预算，输出 placement + routing plan
2. **K-Tree Auto-Search Pass** —— 输入 N + R，cost model 搜最优 K（覆盖 Gap 3）
3. **2D KV Cache Shift Pass** —— 输入 GQA/MQA head layout + KV 大小，输出二维 shift plan（覆盖 Gap 4）

**新 3 个 pass（覆盖 Gap 7）**：
4. **Layout-Aware Mesh Routing Pass** —— 在 INTERLEAVE cyclic shifting 中塞 layout 转换（FEATHER 思想）
5. **RIR-style Reorder In K-tree Allreduce Pass** —— reduction 路径上重排 partial sums（FEATHER 思想）
6. **Per-decode-step Layout Co-Search Pass** —— 类 Layoutloop，自动选 best (mesh routing, data layout) pair

### 阶段 C（2-3 月）：仿真评估 + paper

- 评估：cycle-accurate simulator (SCALE-sim / Timeloop 扩展 + mesh topology)
- 目标会议：**MICRO 2026**（11月截）、**HPCA 2027**（7月截）、**MLSys 2026**（已过 deadline）
- 备选：**CGO 2027**（编译器对口）、**ASPLOS 2027**

## 相关页面（已有 wiki 资产）

- [WaferLLM System](/concepts/waferllm-system.md) — WaferLLM 完整机制
- [Cerebras WSE](/entities/cerebras-wse.md) — PLMR 硬件平台
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 阶段差异
- [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md) — T10 rTensor、MeshGEMM 类比
- [Deterministic Execution](/concepts/deterministic-execution.md) — 编译期可控
- [TileLoom Compiler](/concepts/tileloom-compiler.md) — Tenstorrent 上的 MLIR dataflow 规划
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 上的高级 DSL
- [LoopLynx](/papers/looplynx-scalable-dataflow-llm-inference.md) — FPGA 上同问题不同解法
- [SambaNova SN40L](/papers/sambanova-sn40l-dataflow-coe.md) — dataflow 编译器全自动融合
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — GPU 上的同类 KV 解法
- [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — 算子基础（AI、Roofline、Prefill/Decode）
- [Layout-Aware NoC and Flexible Dataflow Accelerators](/concepts/layout-aware-noc-flexible-dataflow.md) — MAERI/SIGMA/FEATHER/Venus/SmartMem 5 篇核心 paper + Gap 7 来源

# Citations

[1] [raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf) — He et al. OSDI 2025, §7.5 & §8
[2] [concepts/waferllm-system.md](concepts/waferllm-system.md) — 现有 wiki 摘要
