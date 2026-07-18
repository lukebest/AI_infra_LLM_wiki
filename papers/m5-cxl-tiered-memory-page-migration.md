---
type: Summary
title: 'M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems'
description: ASPLOS 2025 — CXL 控制器内 HPT/HWT 硬件热页追踪平台，比 CPU 驱动 ANB/DAMON 识别更准（+47% 热度），内存密集型应用 +14% 性能
tags:
- memory
- memory
- cache
- virtualization
- infrastructure
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf
---

# M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems

**ASPLOS 2025** | DOI [10.1145/3676641.3711999](https://doi.org/10.1145/3676641.3711999)  
Sun, Kim, Yu, Zhang, et al.（UIUC, SNU, Intel Labs）

CXL tiered memory 的 **page migration 开发平台**：在 CXL 控制器内做精确 hot-page / hot-word 追踪，暴露给 OS/策略层，纠正 CPU 驱动方案误判 warm/sparse 页的问题。

## 核心贡献

1. **PAC/WAC profiling**：FPGA CXL 设备透明计数每 4KB page / 64B word 访问
2. **CPU-driven 问题量化**：ANB/DAMON 热页访问仅为真值的 **21%/29%**；Redis 等 **86%** 页为 sparse（≤16/64 words 活跃）
3. **M5 = HPT + HWT + M5-manager**：控制器内 top-K 热页/热字追踪 + 用户态策略接口

## 关键数字

| 指标 | 值 |
|------|-----|
| CXL vs DDR 延迟 | **2–3×** |
| 更热页识别 | **+47%** vs CPU 方案 |
| 性能提升 | **+14%** vs 最佳 CPU 迁移；**+20%** vs ANB |

## 与 wiki 交叉

- [DRAM Memory System](/concepts/dram-memory-system.md) — tiered / NUMA 背景
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 页迁移在数据路径中的位置

# Citations

[1] [raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf](raw/papers/M5_CXL_Tiered_Memory_Page_Migration_2025.pdf)
[2] [raw/papers/m5-cxl-tiered-memory-page-migration.md](raw/papers/m5-cxl-tiered-memory-page-migration.md) — 结构化摘录
