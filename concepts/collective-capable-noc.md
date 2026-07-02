---
type: Concept
title: Collective-Capable NoC
description: FlooNoC 扩展：AXI 多地址 mask、XY fork 组播、并行/宽归约；DCA 范式（互连借 FPU 做 in-network 算术归约，router +16.9%、tile <1%）
tags:
- noc
- interconnect
- collective
- multicast
- reduction
- barrier
- accelerator
- mesh
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf
---

# Collective-Capable NoC（片上 collective 互连）

大规模 tile-based ML 加速器（Snitch cluster + 2-D [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)）在 die 内已近似「分布式系统」——**barrier / broadcast / reduction** 若仅靠软件 DMA + 原子计数器，会饱和互连与 SPM。Colagrande et al. (MLSys 2026) 在开源 **FlooNoC** 上扩展 **collective-capable NoC**：保持 AXI4 合规，以 **16.9% router 面积** 换组播、窄/宽归约与 **Direct Compute Access (DCA)** 高吞吐算术归约。

## 基线：FlooNoC + Tile SoC

| 组件 | 配置 |
|------|------|
| 拓扑 | 2-D mesh，compute + memory tile |
| Compute | Snitch cluster：8× RV32I + SIMD FPU + 128 KiB L1 SPM；第 9 core 带 DMA |
| Memory | 每 memory tile 1 MB L2 SPM |
| NoC | **Wide** 512b（burst 数据）+ **Narrow** 64b（latency-critical）；三物理链路 req/rsp/wide |
| 单播模型 | `T_transfer = α + nβ`（α 往返延迟，β cycles/beat） |

## 多地址编码（Multi-address）

扩展 AXI **AWUSER**：`(dst_addr, mask)`——mask 位为 1 的地址位视为 **don't care**，n 位 mask 可表示 **2ⁿ** 目的地址组合；开销随地址空间 **对数增长**，与目的数无关。NI 将 address mask 译为 **X/Y coordinate mask** 供 XY 路由 fork。

**Collective 子网约束**：可 collective 区域为 `(X,Y,W,H)` 子 mesh，W/H 为 2 的幂，(X,Y) 对齐；各 tile 地址空间等宽、对齐、Y-major 连续映射 → mask→XY 翻译退化为 **bit-select**。

## Router 扩展

```
AW/opcode → NI(mask→XY) → xy_route_fork → stream_fork (multicast)
                         → output_arbiter → parallel reduction (CollectB/LsbAnd/SelectAW)
                         → wide reduction controller → DCA offload (2-input FPU)
```

| 扩展 | 机制 | 面积（相对 baseline router） |
|------|------|------------------------------|
| **Multicast** | `xy_route_fork` + `stream_fork` 按 X/Y mask 多端口 fork | +5.8%（含 AXI 必需的 response reduction） |
| **Parallel reduction** | 每输出端口 `reduction_arbiter`；`sync` 模块 + LZC 仲裁；CollectB / LsbAnd / SelectAW | +2.7%（窄网 barrier） |
| **Wide reduction** |  centralized 2-input 归约 + hdr buffer 隐藏 FPU 流水；可 offload 到 cluster | +16.9% 合计 |
| **NI** | mask 寄存、地址 resolve、collective response 生成 | +3.5% |

**LsbAnd**：对 flit LSB 做 AND-reduction → 硬件 **barrier**（替代 cluster 0 上 amoadd 计数器 + interrupt multicast）。

## Direct Compute Access (DCA)

**DCA**（Direct Compute Access）是 Colagrande et al. 提出的片上互连范式：**NoC router 可直接调用 compute tile 内的算术单元（Snitch FPU），无需 core 发指令**。论文 claim 这是首个在可编程 ML 加速器上实现 **高吞吐 on-chip 算术 reduction** 的开源路径。

### 与 DMA 的对称关系

| 机制 | 绕过对象 | 直连资源 | core 状态 |
|------|----------|----------|-----------|
| **DMA** | core 指令路径 | **memory**（SPM/L2） | 可 idle / 做其他事 |
| **DCA** | core 指令路径 | **FPU**（cluster 算术） | 可 idle / 低功耗 |

设计动机：wide network 浮点 reduction 若在 router 内建 **5-input FP 归约树**，面积与时序不可接受；而 tile P&R 后 **FPU 面积远大于 router**——借现有算力比复制算力便宜（full tile 扩展 **< 1%** vs router **+16.9%**）。

### 三层归约中的位置

Collective-capable NoC 的归约分三层，DCA 只服务 **宽网算术**：

| 层级 | 网络 | 操作 | 实现 |
|------|------|------|------|
| Parallel reduction | Narrow 64b | CollectB / SelectAW / **LsbAnd** | Router 内轻量逻辑（AXI 耦合 + barrier） |
| Wide reduction 控制 | Wide 512b | sync、2-input merge、hdr buffer | Router centralized controller |
| **算术执行** | Wide 512b | FP elementwise add 等 | **DCA → cluster FPU** |

软件 wide reduction 典型路径：各 cluster **DMA** partial sum 到 root → **core 发 FPU 指令** 做 elementwise add → **barrier** → 重复（seq/tree）。瓶颈是 SPM↔NoC 往返 + 8 core 必须醒着。DCA 把「算」前移到 **flit 到达 tile 时 router offload 到 FPU**。

### 数据路径

```
Wide flit → Router wide reduction controller
              ├─ sync：等最多 2 路 operand（router 仅 2-input merge）
              ├─ offload ──→ Snitch DCA 口
              │                 ├─ 512b op1 → 8×64b → FPU 0..7
              │                 ├─ 512b op2 → 8×64b → FPU 0..7
              │                 └─ 512b result ← 拼回
              ├─ hdr buffer：深度 > FPU pipeline → burst 时 1 reduction/cycle
              └─ 结果 flit → 普通 unicast 继续路由
```

**Router 不做 heavy ALU**：多路归约靠 mesh **多跳逐级 2-input merge**（类似 tree reduce，算术在 tile FPU 完成）。

**接口**：2×512b operand in + 1×512b result out + opcode；与 FlooNoC wide link 位宽对齐（1 beat = 一次 SIMD 归约）。

**FPU 共享**：tag 贯穿 FPU pipeline，区分 DCA vs core 请求；结果按 tag 路由回 DCA 口或 core 寄存器。

**Backpressure**：operand 路径 valid-ready；FPU 可对单路反压等另一路到齐；router–FPU 间 **cut** 寄存器缓冲。

### 吞吐与面积

| 指标 | 值 |
|------|-----|
| FP64 reduction/cycle | **8 路**（8 FPU） |
| FP8 reduction/cycle | **64 路**（SIMD） |
| Router 全 collective 面积 | **+16.9%** |
| Full compute tile 面积 | **< 1%** 增量 |

### 性能与能效（vs 优化软件基线）

4×4 mesh、1–32 KiB：**2.8× geomean** reduction speedup。软件模型（seq/tree + DMA + hw barrier）：

```
T_seq  = tm + 2(c−2)·max(tm,tc) + k·tc + (2(c−2)+k)·δ
T_tree = {tm + δ + (k−1)[max(tm,tc)+δ] + tc} · log₂c
```

DCA 同时削减 **core 参与 tc** 与 **多次 DMA round-trip**。FCL GEMM 能效 **1.13×**：少 DMA hop + DCA 时 **core 可 low-power**（软件基线需 8 core 全醒发 FPU 指令）。

**结构性限制**：router 每跳仅 **2-input**；2D reduction 时首列 router 可能收 east+north+local 三路 → 32 KiB 传输 **1 beat/2 cycles**（约 1.9× 慢于 1D）。**FPU 争用**：DCA 与 core 共用 FPU；FCL kernel 中 reduction 严格在 compute 之后，无 overlap 争用。

### 为何不用 router 内 ALU

```
Wide FP reduction 需要高吞吐 ALU
  ├─ Router 内 5-input FP tree → 面积/时序不可接受
  └─ DCA 借 tile FPU → router 轻量 + tile <1%，8×DP/cycle
```

Parallel reduction（CollectB/LsbAnd）处理窄网 bitwise/AXI 语义；**宽网浮点归约必须借 DCA** 才有意义。论文将此作为 **generalizable** 前提之一：tile 需暴露可借用算术单元（WSE-3、Blackhole、MTIA、SN40L 等 2-D tile 加速器均满足结构，机制各异）。

## 性能摘要（4×4 mesh，1–32 KiB）

| 原语 | vs 优化软件基线 | 备注 |
|------|----------------|------|
| Hardware barrier | 斜率 1.3 vs 3.3 cycles/cluster | LsbAnd + fence |
| Multicast | **5.3×** geomean | `T_hw = α + (n+c−1)β`；2D 几乎不随行数增长 |
| Reduction (DCA) | **2.8×** geomean | 2-input/router 限制首列 2 beats/2 cycles |
| SUMMA GEMM | 最高 **3.8×**（256×256 mesh） | hw multicast 使 kernel 保持 compute-bound 至更大 mesh |
| FusedConcatLinear GEMM | 最高 **2.4×** reduction | MHA fused concat+linear |
| 能效 | SUMMA 最高 **1.17×**；FCL **1.13×** | 少 DMA hop + DCA 时 core 可 idle |

**GEMM 加速条件**（论文归纳）：① `T_comm` 在 critical path；② 通信模式可映射为 multicast/reduction。

## 与 WSE / 其他加速器

| 维度 | FlooNoC collective（本文） | [Cerebras WSE](/entities/cerebras-wse.md) |
|------|---------------------------|------------------------------------------|
| 组播 | XY mask fork，AXI 语义 | [Color 路由](/concepts/cerebras-color-mechanism.md) multicast（免费复制） |
| 归约 | Router 轻量 + **[DCA 借 FPU](/concepts/collective-capable-noc.md#direct-compute-access-dca)** | 数据流 + DSD；见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) |
| Barrier | LsbAnd in-network | Fabric hardware barrier |
| 编程 | Bare-metal C++ / DMA opcode | CSL / [SpaDA](/concepts/spada-programming-language.md) |
| 开源 | FlooNoC v0.8.0 + picobello | 闭源 |

工业同类（专有、机制未公开）：MTIA、SambaNova SN40L、Tenstorrent Blackhole——均具 2-D tile、片上算术、可编程 DMA/LSU。

## 相关页面

- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — **GIN 单周期 (row,col) tag 组播** NoC；CNN 固定映射下的 custom multicast（非 hop-by-hop mesh）
- [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — wormhole/仲裁/流控基线
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — XY 路由前提
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — 另一 mesh collective 设计空间
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — 大规模 barrier 硬件必要性
- [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md) — WSE multicast 对照

# Citations

[1] [raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf](raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf) — Colagrande et al., MLSys 2026 (arXiv:2603.26438)
