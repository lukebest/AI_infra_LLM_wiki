---
type: Paper
title: "CacheFlex: Direct Software-Managed Access to Higher-Level Cache for Scalable Vector Support"
description: "UW/Rutgers MICRO'26 — 运行时把私有 L2 的部分 way 转成软件管理 scratchpad，ISA 扩展 + 乱序核双 LSQ；SVE VL=16 时 GEMM 几何均值 1.44×、访存能耗 −40%，面积仅占 L2 的 2.02%（12 nm 后版图）"
tags:
- cpu
- cache
- isa
- pipeline
- memory
- llm
- architecture
created: 2026-10-13
updated: 2026-10-13
timestamp: '2026-10-13T00:00:00Z'
paper_author: [Jingqun Zhang, Maohua Nie, Jiayi Wang, Weihang Li, Rishi Sappidi, Shwet Chitnis, Ang Li]
year: 2026
arxiv: '2610.12940'
venue: MICRO 2026 (to appear)
sources:
  - raw/papers/CacheFlex_L2_Scratchpad_Scalable_Vector_2026.pdf
  - raw/papers/cacheflex-l2-scratchpad-scalable-vector.md
---

# CacheFlex：让软件直接用私有 L2 当 scratchpad，给宽向量 CPU 补访存

## 一句话结论
CPU 向量宽度从 512 bit 涨到 2048 bit 后，GEMM 吞吐的瓶颈落到 L1D 容量上；L1 绑在流水线里、要求个位数周期延迟，难以加大。CacheFlex 把容量大一个量级的私有 L2 按 way 切出一部分，作为线程私有、非一致的 SPM 交给软件直接读写，绕过地址翻译、tag 比较与一致性探测。

## 动机（论文数字）
- 64 KB L1 下，SIMD 从 512 bit（VL=4）加宽到 2048 bit（VL=16），峰值利用率从 **72%** 掉到 **29%**；L1 加到 512 KB 只能恢复到 **45%**，再往上就轮到 512 KB L2 成瓶颈。
- 商用 Arm/x86/RISC-V 核 L1D 仍停在 32–64 KB；私有 L2 有 256 KB–2 MB，却对软件不可见。

## 方案
| 部件 | 做法 |
|---|---|
| ISA | 特权指令 `spm_config / spm_allocate / spm_deallocate` 按 way 位图切换 cache/SPM 模式；用户态 `spm_ld / spm_st`（向量寄存器↔SPM）与桥接指令 `spm_cp / spm_wb`（常规内存↔SPM，不经寄存器堆） |
| 乱序核集成 | 增设 SPM LQ/SQ；桥接指令同时进常规 LSQ 与 SPM LSQ，各域独立维护 RAW/WAW 顺序，WAR 依靠 ROB 顺序提交；桥接按“缓冲 store”提交 |
| 一致性 | SPM 线程私有、非一致；way 首次转换采用 lazy-copy，被触碰的旧行按普通驱逐语义经 MESI 写回/失效 |
| OS | CSR（`spm_ctl / spm_base / spm_bound / spm_backing_ptr`）+ 上下文切换溢出/回填，tag 阵列复用存 owner 线程 ID 以便切回时复用 |
| 实现 | gem5 建模 Armv8-A SVE 乱序核（Cortex-A710 风格：5-wide 取指、8-wide 发射、128 ROB；64 KB L1D、512 KB L2）；12 nm FinFET 后版图面积开销为 L2 的 **2.02%**（含专用 SPM 读端口） |

## 效果（仅论文数字）
- GEMM（7 种模型形状）：VL=4 时几何均值 **1.12×**、访存子系统能耗 **−26%**；VL=16 时 **1.44×**、**−40%**。收益随向量宽度单调增长。
- 对比理想化“硬件预取 + L2 pinning + 非临时 load”上界：W3/W5 形状仍快 **1.63× / 1.34×**；关掉专用 L2 读带宽后仍快 **1.43× / 1.19×**，说明主要收益来自绕开 L1 流水线、直取大容量 L2。
- 整层 prefill（CacheFlex + FlashAttention）：BERT-Base（T=4096，VL=16）最高 **1.78×**、能耗 **−45%**；LLaMA-3.2-1B **1.64×**、**−38%**。
- 不融合注意力时 CacheFlex 对注意力本身几乎无加速，收益集中在 GEMM 与 FlashAttention 的分块复用上。

## 与 wiki 的关系
- [Memory Hierarchy & Cache](/concepts/memory-hierarchy-cache.md) — cache 与 scratchpad 的混合：按 way 在运行时切换角色
- [Out-of-Order Execution](/concepts/out-of-order-execution.md) — 双 LSQ 协调桥接指令的冒险，复用 ROB 顺序提交处理 WAR
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — CPU 端 GEMM 分块受 L1 容量约束的典型案例
- [CacheFit](/papers/cachefit-cost-aware-llc-replacement.md) — 同为 cache 层“软件/策略介入 + 量化硬件成本”的近期工作

## 局限与开放问题
- 评测限于单核、机制级；多核共享 L3 与多线程争用 L2 way 的行为未覆盖。
- 需要手写/编译器生成 SPM 分块代码；decode（GEMV、访存受限）场景收益未评估。

# Citations
- Zhang et al., "CacheFlex: Direct Software-Managed Access to Higher-Level Cache for Scalable Vector Support", MICRO 2026, arXiv:2610.12940. [raw](/raw/papers/cacheflex-l2-scratchpad-scalable-vector.md) · [PDF](/raw/papers/CacheFlex_L2_Scratchpad_Scalable_Vector_2026.pdf)
