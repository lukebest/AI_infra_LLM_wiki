---
type: Paper
title: "WaferTrans: IOMMU-free Distributed VA Translation for Wafer-scale GPUs"
description: 清华 — 片上 PTE Presence Directory 去掉 CPU-IOMMU；vs Trans-FW 平均 2.5×（Sequential/Adjacent 3.1×）
tags:
- wse
- now
- network-on-wafer
- gpu
- memory
- interconnect
- mesh
- architecture
- scale-up
- fabric
- virtualization
timestamp: '2026-09-10T00:00:00Z'
created: 2026-09-10
updated: 2026-09-10
sources:
- raw/papers/WaferTrans_IOMMU_free_Wafer_Scale_GPU_2026.pdf
- raw/papers/wafertrans-iommu-free-wafer-scale-gpu.md
---

# WaferTrans: Enabling IOMMU-free Distributed Virtual Address Translation for Wafer-scale GPUs

**Authors:** Xinru Tang, Jingxiang Hou, Guanghong Wu, Yang Hu, Shouyi Yin
**Affiliation:** Tsinghua University
**arXiv:** [2609.06125](https://arxiv.org/abs/2609.06125)（2026-09-05，cs.AR）
**Venue:** 预印本（IEEE 格式稿）。
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.06125)

相对 [Network Design WoW](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) 谈的是 **边怎么长出来**，本文谈的是晶圆级 GPU 阵列上 **远程虚址怎么在片上翻译完**。相对 [WaferLLM](/papers/waferllm-wafer-scale-llm-inference.md) 的算子层，本文卡在 Unified Memory 的地址翻译路径。

## 动机

晶圆级 GPU（WSG）把多 die 放进同一片上域，片上带宽够高时 **Unified Memory（UM）** 的远程访问可以接近本地。但现有 UM 仍把远程 VA→PA 丢给 **CPU-IOMMU**：请求要走 Wafer2CPU（文内仿真 **180-cycle**、PCIe 协议），再争用有限的 CPU 侧 PTW/IO TLB。die 数到几十时，翻译本身变成瓶颈。

SOTA **Trans-FW** 在 IOMMU 旁加集中 Forwarding Table，把请求转到持有 PTE 的 GPU，但 **off-wafer 往返消不掉**，集中 FT 在上千 SM 下也会堵。文内对照：B200 级 **8 TB/s** 内存 vs **0.9 TB/s** 互连（比 ≈0.225）；理想化 4×4 mesh wafer 标 **7.5 TB/s** wafer BW——算力/互连账已经乐观，翻译开销仍会吃掉 UM 收益。

## 方案

**PTE Presence Consistency（PTE-PC）。** 只跟踪 PTE 的 insert/remove，不复制整页表一致性语义。

**PTE Presence Directory（PPD）。** 每 GPU 一份：用 fingerprint 查「哪块 GPU 持有该 PTE」。再配 Domain Presence Broadcaster（DPB）维护域成员。

**分布式 PTE-PC mapping + cooperative query。** 本地 TLB/GMMU miss 后，在晶圆内查 PPD → 转发到持有者 → 回填；维护流量尽量局部，查找仍保持覆盖完整。目标：GPU 阵列在 **片内** 解析远程翻译，去掉对 CPU-IOMMU 的依赖。

**实现。** RTL：PPD **1,024** slots、11-bit fingerprint；仿真对照 Trans-FW（集中 FT）。负载含 Sequential / Adjacent / Scatter-Gather / Random 等访问模式。

## 效果（仅论文数字）

- vs Trans-FW：平均 **2.5×**；Sequential 与 Adjacent 类平均 **3.1×**。
- Trans-FW 远程访问延迟分解：Wafer2CPU 与 CPU 侧翻译约占总延迟 **49%** / **13%**（WaferTrans 切掉这条路径）。
- 面积：PPD+控制 **0.00167 mm²**（约本地 L2 TLB 的 **4.71%**），整系统约 **0.40%** 开销。
- FT/PPD 容量：文示 WaferTrans 在 **1,024** slots 附近饱和；Trans-FW 需更大集中表（文示到 **4,096**）才饱和。

## 与 wiki 概念的关系

- [Network-on-Wafer](/concepts/network-on-wafer.md) — 补「晶圆域内软件可见的 UM 翻译」一层；拓扑仍可是 mesh，但地址解析不再绕 CPU。
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 把 scale-up 域的 **控制面/翻译面** 从数据面带宽分开记账。
- [GPU SIMT](/concepts/gpu-simt-architecture.md) — TLB/GMMU/PTW 参数进入 WSG 语境。

## 开放问题

1. PTE-PC 在频繁换页 / 多进程 OS 语义下的一致性边界？
2. 与 Cerebras field-stitch / WoW 重叠网的对照：本文假设可路由的 GPU mesh，几何约束换图后 PPD 查询直径怎么变？
3. 翻译开销切掉后，UM 是否真能吃满 7.5 TB/s 量级 wafer BW，还是又回到应用侧 locality？

# Related

- [Network-on-Wafer](/concepts/network-on-wafer.md)
- [WaferLLM](/papers/waferllm-wafer-scale-llm-inference.md)
- [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md)
- [Network Design WoW Hybrid Bonding](/papers/network-design-wafer-scale-wow-hybrid-bonding.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.06125) — Tang et al., arXiv:2609.06125
[2] [raw/papers/wafertrans-iommu-free-wafer-scale-gpu.md](raw/papers/wafertrans-iommu-free-wafer-scale-gpu.md) — ingest stub
