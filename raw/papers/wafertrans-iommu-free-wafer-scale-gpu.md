---
type: Raw Source
title: "WaferTrans: Enabling IOMMU-free Distributed Virtual Address Translation for Wafer-scale GPUs"
source_url: https://arxiv.org/abs/2609.06125
arxiv: '2609.06125'
ingested: 2026-09-10
sha256: cf4c86d2ea0a2ccb05b3370defb8a338736df0bf4c756e2d7961426a4f7ff5d7
---

# WaferTrans: Enabling IOMMU-free Distributed Virtual Address Translation for Wafer-scale GPUs

**Authors:** Xinru Tang, Jingxiang Hou, Guanghong Wu, Yang Hu, Shouyi Yin
**Affiliation:** Tsinghua University
**PDF:** [WaferTrans_IOMMU_free_Wafer_Scale_GPU_2026.pdf](WaferTrans_IOMMU_free_Wafer_Scale_GPU_2026.pdf)
**arXiv:** [2609.06125](https://arxiv.org/abs/2609.06125)（2026-09-05，cs.AR）

## 问题

晶圆级 GPU（WSG）片上带宽足以支撑近无损 Unified Memory，但远程虚址翻译仍走 **CPU-IOMMU**：请求要出晶圆、争用 CPU 侧资源。Trans-FW 在 IOMMU 加转发表，仍消不掉 off-wafer 路径，集中 FT 在上千 SM 下也会堵。

## 方法要点

- **PTE Presence Consistency (PTE-PC)**：轻量一致性，只跟踪 PTE insert/remove。
- 每 GPU 一个 **PTE Presence Directory (PPD)**，定位持有目标 PTE 的 GPU。
- 分布式 PTE-PC mapping + cooperative query：在片上完成远程翻译，去掉对 CPU-IOMMU 的依赖。
- RTL 实现：PPD 1,024 slots / 11-bit fingerprint。

## 摘录数字（仅论文给出）

- vs SOTA Trans-FW：平均 **2.5×**；Sequential / Adjacent 类负载平均 **3.1×**。
- Trans-FW 远程访问延迟中 Wafer2CPU 与 CPU 侧分别约占 **49%** / **13%**。
- 面积开销约 **0.40%**（PPD+控制逻辑 0.00167 mm²，约本地 L2 TLB 的 4.71%）。
- 文内对照：B200 级 8 TB/s 内存 vs 0.9 TB/s 互连 → interconnect/memory ≈ **0.225**；理想化 4×4 mesh wafer 标 **7.5 TB/s** wafer BW。
