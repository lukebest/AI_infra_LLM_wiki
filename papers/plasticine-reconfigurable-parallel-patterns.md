---
type: Summary
title: 'Plasticine: A Reconfigurable Architecture For Parallel Patterns'
description: Stanford CGRA 直接支持 Map/FlatMap/Fold/HashReduce；64 PCU+64 PMU @28nm 112.8mm²、12.3 TFLOPS；相对 Stratix V 最高 76.9× Perf/W、DHDL 数分钟编译
tags:
- accelerator
- cgra
- reconfigurable
- parallel-patterns
- dataflow
- compiler
timestamp: '2026-06-24T00:00:00Z'
created: 2026-06-24
sources:
- raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf
---

# Plasticine: A Reconfigurable Architecture For Parallel Patterns

**Authors:** Raghu Prabhakar, Yaqi Zhang, David Koeplinger, Matt Feldman, Tian Zhao, Stefan Hadjis, Ardavan Pedram, Christos Kozyrakis, Kunle Olukotun (Stanford) | **Venue:** ISCA 2017 | **DOI:** [10.1145/3079856.3080256](https://doi.org/10.1145/3079856.3080256) | **PDF:** [raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf](raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf)

## 一句话总结

以 **PCU（SIMD 可配置流水线）** 与 **PMU（banked scratchpad + 地址 datapath）** 组成的 16×8 空间阵列，为 **Map / FlatMap / Fold / HashReduce** 四类 parallel patterns 提供原生硬件支持；28 nm **112.8 mm²、12.3 TFLOPS、49 W**，相对 Stratix V FPGA 在 CNN 上 **76.9× Perf/W**，DHDL 编译 **数分钟** 完成配置。

## 核心贡献

1. **Pattern-native CGRA**：PCU 归约树/shift 网络 + PMU 多模式 banking/N-buffer + AG gather/scatter coalescing
2. **Parallel patterns 编程模型**：嵌套 Map/Fold/HashReduce 统一 dense（GEMM、CNN）与 sparse（PageRank、BFS、SMDV）
3. **分层静态控制**：sequential / coarse pipeline / streaming 三种协议 + switch 内 outer control
4. **DHDL 编译栈**：virtual unit 划分 + 贪心映射；相对 FPGA 工具链数量级更快
5. **模型驱动架构定标**：6 stage × 16 lane PCU、256 KB PMU；VCS+DRAMSim2 全系统评估

## 关键数字

| 指标 | 值 |
|------|-----|
| PCU / PMU | **64 / 64**（16×8 阵列，1:1） |
| 峰值 FP32 | **12.3 TFLOPS** @ 1 GHz |
| 片上 scratchpad | **16 MB** |
| 面积 / 功耗 | **112.77 mm²** / **≤49 W** |
| vs FPGA Perf/W（CNN） | **76.9×** |
| vs FPGA Perf/W（GEMM） | **24.4×** |
| vs ASIC 面积（同性能，generalized） | geo-mean **~11×** |

## 与 wiki 交叉引用

- [Plasticine Accelerator](/concepts/plasticine-accelerator.md) — PCU/PMU 与 control 机制
- [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md) — 数据流架构谱系
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — 另一 spatial dataflow DSL
- [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — 可重构 vs 固定加速器
- [FEATHER Accelerator](/concepts/feather-accelerator.md) — DNN 域可重构对照
- [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — 固定 CNN dataflow 对照

# Citations

[1] [raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf](raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf) — Prabhakar et al. (2017)
