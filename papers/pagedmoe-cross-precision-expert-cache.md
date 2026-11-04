---
type: Paper
title: "PagedMoE: Cross-Precision Expert Caching for Token-Level Dynamic Precision in SSD-Resident MoE Inference"
description: "清华 — SSD 常驻 MoE 跨精度专家缓存；树码本+bitplane 使精度=共享状态 refinement；Avg 2.5-bit 质量近 GPTQ-INT4/MXFP4；24 GiB 缓存 8.89 tok/s，相对独立精度对象 1.33×、均匀 4-bit 1.56×"
tags:
- moe
- quantization
- bitplane
- storage
- ssd
- inference
- llm
- expert-parallelism
- memory
created: 2026-11-04
updated: 2026-11-04
timestamp: '2026-11-04T00:00:00Z'
paper_author: [Yutong Lin, Yingdi Shan, Shaoyuan Chen, Yuanyong Chen, Yongwei Wu, Mingxing Zhang]
year: 2026
venue: arXiv
arxiv: '2611.03173'
sources:
  - raw/papers/PagedMoE_Cross_Precision_Expert_Cache_2026.pdf
  - raw/papers/pagedmoe-cross-precision-expert-cache.md
---

# PagedMoE：SSD 常驻 MoE 的跨精度专家缓存

## 一句话结论
路由专家池可落 SSD、DRAM 做热缓存，但实用缓存容量下关键路径仍有大量 I/O。按 token 动态精度本可减带宽，若把同专家各 bit-width 当独立对象则无法跨精度复用。PagedMoE 用**前缀兼容的树码本 + bitplane**，把精度定义为同一专家状态的 **refinement depth**：低精度是高精度的合法前缀，命中后只补缺 plane。平均路由专家 **2.5 bit** 时质量接近 GPTQ-INT4（Qwen3.5-397B-A17B）与多数 GLM5.2 任务上的 MXFP4；**24 GiB** 专家缓存下 Qwen3.5 达 **8.89 tok/s**，相对独立精度对象 **1.33×**、均匀 4-bit **1.56×**。

## 动机
- 本地大 MoE：专家常驻 SSD、DRAM 缓存近期专家；重叠计算后 I/O 仍常进关键路径。
- 按重要性/量化敏感度动态分配 bit 可降数据量，但多精度副本互不共享字节会重复拉重叠数据。

## 方案
1. **树码本 + bitplane**：每专家只存一份；低精度表示是高精度的合法前缀。
2. **I/O 前选前缀长度**：结合当前路由权重与离线专家误差剖面，决定需要的 refinement。
3. **直接执行缓存前缀**：1–8 bit 前缀可直接 CPU GEMV，无需物化全精度专家。
4. **评测**：Qwen3.5-397B-A17B、GLM5.2；对照独立精度对象与均匀 4-bit。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 平均路由专家精度 | **2.5 bit** |
| 质量 | 接近 GPTQ-INT4（Qwen3.5-397B-A17B）；多数 GLM5.2 任务接近 MXFP4 |
| 24 GiB 专家缓存吞吐（Qwen3.5） | **8.89 tok/s** |
| vs 同动态请求、独立精度对象 | **1.33×** |
| vs 均匀 4-bit 执行 | **1.56×** |

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — SSD↔DRAM 专家权重路径与跨精度复用
- [SSD / NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — 专家页/plane 级 I/O
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 本地 SSD-resident MoE 与 CPU 侧前缀执行
- [PDScope](/papers/pdscope-phase-aware-moe-cpu-gpu.md) — 同属专家加载优化；PDScope 相位预取，PagedMoE 跨精度缓存复用
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — bitplane / 低比特前缀执行

## 开放问题
- 树码本与误差剖面依赖离线校准；跨模型族迁移成本未系统报告。
- GPU 侧直接执行前缀与更大并发 batch 下的 I/O 调度仍可扩展。

# Citations
- [arXiv:2611.03173](https://arxiv.org/abs/2611.03173) — Lin et al., Tsinghua, 2026
- [raw stub](/raw/papers/pagedmoe-cross-precision-expert-cache.md)
