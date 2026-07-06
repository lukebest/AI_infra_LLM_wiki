---
type: Raw Source
title: TileLoom Automatic Dataflow Planning for Tile-Based Languages
source_path: /home/luke/snap/zotero-snap/common/Zotero/storage/TPR5524C/Li 等 - 2026 - TileLoom automatic dataflow planning for tile-based languages on spatial dataflow accelerators.pdf
arxiv: '2512.22168'
ingested: 2026-07-06
sha256: 8319d0fcef3700907e8bb5bfb21ca069591da27c716b7cdb55664909e26967a2
---

# TileLoom: Automatic Dataflow Planning for Tile-Based Languages on Spatial Dataflow Accelerators

**Authors:** Wei Li, Zhenyu Bai, Heru Wang, Pranav Dangi, Zhiqiang Zhang, Cheng Tan, Huiying Lan, Weng-Fai Wong, Tulika Mitra  
**Affiliations:** NUS School of Computing; Arizona State University / Google; Lumai Ltd.  
**PDF:** [TileLoom_Automatic_Dataflow_Planning_2026.pdf](TileLoom_Automatic_Dataflow_Planning_2026.pdf)  
**arXiv:** [2512.22168v2](https://arxiv.org/abs/2512.22168) (May 2026) | **Code:** https://github.com/ecolab-nus/loom-dataflow

## 问题

空间数据流加速器（Tenstorrent、Cerebras、Graphcore、Groq、MTIA 等）靠显式片上数据搬运缓解内存墙，但**性能强依赖 tile 在 core 间的放置与通信**—— naive mapping 拥塞/带宽浪费；用户多依赖 vendor hand-tuned 库，可编程性成 adoption 障碍。

## 与单-tile 编译器的区别

Triton/Helion 等框架优化**单 core 内** tile 代码生成；TileLoom 把 **tile 实例分布到空间分布的 core**，利用 NoC + 分布式 scratchpad 提高 reuse、降通信。

## 框架（Figure 2）

```
Tile DSL (Triton / Helion)
  → Front-end: dataflow-agnostic MLIR (affine + linalg + scf + arith)
  → Dataflow planning: spatiotemporal mapping + reuse + broadcast + df-aware MLIR
  → Performance model (df dialect HW repr) → top-k → optional HW profile
  → Back-end: per-core block codegen → TT-Metalium (Tenstorrent)
```

## 核心机制

1. **df dialect**：多层硬件表示（scale-out：拓扑/NoC/DRAM；scale-in：core compute）
2. **Spatiotemporal mapping**：parallel dim → spatial (mesh index) vs temporal (wave loops)
3. **Reuse analysis**：affine 访问 → intra-core / inter-core reuse；broadcast 枚举
4. **Performance model**：compute + memory capacity + NoC 成本；prune + rank
5. **Two-step selection**：模型 top-k → 真机 profile 选最终 mapping

## 评测（Tenstorrent Wormhole 8×8 / Blackhole 12×10）

| Kernel vs TTNN | Wormhole | Blackhole |
|----------------|----------|-----------|
| FlashAttention | **1.94×** geo mean | **1.98×** |
| Flash Decode | 0.84× | 0.87× |
| GEMM | 0.95× | **1.10×** |
| Mamba Chunk Scan (vs unfused) | **27.23×** | **16.27×** |

FlashAttention 单点 **1.88–2.06×**；Mamba 相对 unfused **10×–55×**。

## 定位

vs Timeloop/AutoSA/Spatial/Plasticine：后者 co-design **PE 级**硬件；TileLoom **固定 intra-core**，以 **core 为原子单元**，只做 **multi-core tile 分布 + NoC 数据流规划**。
