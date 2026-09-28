---
type: Paper
title: "HBF-Sim: 面向大规模 GPU 内存的可扩展 HBF 仿真器"
description: "Accel-Sim 集成端到端 GPU–HBF 路径；媒体吞吐最高 15.94×；contiguous 放置 page-service 放大 −41.9%；条带化 kernel 最高 3.94×。"
tags:
- architecture
- accelerator
- gpu
- hbm
- hbf
- memory
- memory-bandwidth
- kv-cache
- llm
- inference
- agentic-ai
created: 2026-09-28
updated: 2026-09-28
timestamp: '2026-09-28T00:00:00Z'
paper_author: [Yaqi Li, Jing Wang, Junfeng Wang, Long Yang, Han Yan, Xiaohu Chai, Liang Shi]
year: 2026
arxiv: '2609.29246'
sources:
  - raw/papers/HBFSim_Extensible_HBF_Simulator_GPU_2026.pdf
  - raw/papers/hbfsim-extensible-hbf-simulator.md
---

# HBF-Sim：可扩展 HBF 仿真器

## 一句话结论

HBF-Sim 把 **GPU issue 限流、设备排队与 NAND 页行为** 闭合到同一条 Accel-Sim 请求路径，用来研究共封装 High-Bandwidth Flash（OCP：文中称 **512 GiB**、最多 **16×UCIe**、聚合接口 **3.072 TB/s**）在 LLM 权重/KV 访问下的真实可用带宽；微基准显示媒体吞吐最高 **15.94×**，contiguous 放置相对 interleave 把 page-service amplification 压低 **41.9%**，活跃页条带化 kernel 最高 **3.94×**。

## 动机：HBF 既不是大 HBM，也不是快 SSD

LLM 训练与 agentic 推理把 HBM 容量推到极限：权重相对固定，KV 随上下文/batch 增长。远端 DRAM/闪存受 PCIe 与软件栈限制。HBF 把稠密 NAND 共封装到 GPU 侧，提供近加速器接口带宽与闪存密度，但可用带宽取决于 **64 B cache-line → 4 KiB page** 映射、channel-affine die 并发，以及写聚合/反压如何咬合 GPU 内存流水线。既有 GPU 仿真器把片外当 DRAM；SSD 仿真器走 NVMe/CXL 块语义；近期 HBF 论文多用内部/应用专用模型——公开描述不足以覆盖完整 GPU–HBF 请求与完成语义。

## 方案

### 1. 控制器 ↔ 页级并行栈

Interaction controller（基片之上）负责粒度对齐、地址映射、内存/闪存管理；page-based parallel stack storage 负责合并与检索。GPU 以普通 load/store 驱动 HBF，每请求追踪状态与会计。

### 2. MSHR 页合并与多栈 flash 管理

页键 MSHR 合并同页 outstanding 读；可选聚合窗口/阈值；写路径累积完整 4 KiB 页再 program。默认媒体时序示例：\(t_R=15\,\mu\mathrm{s}\)、\(t_{\mathrm{PROG}}=200\,\mu\mathrm{s}\)、\(t_{\mathrm{BERS}}=2\,\mathrm{ms}\)。placement（interleave / grouped / contiguous）、读优先级与 R/W 通道隔离均可配置。

### 3. 验证与设计空间实验

与外部页服务对照、媒体资源扩展、placement 对放大系数与 kernel 时间的影响，以及 Qwen3-1.7B decode 流量探测（Table 5）。

## 量化结果

- **媒体扩展（Figure 6）**：吞吐 **8.738 → 139.285 GB/s（15.94×）**，媒体占用 **99.6–99.99%**。
- **Placement（§6.1）**：32 entries/page 时 contiguous 相对 interleave，page-service amplification **−41.9%**（8.0625 → 4.6875）；array 读次数不变时 kernel 时间仅 **+0.69%**。
- **条带化（Table 6）**：活跃页条带化相对内置 interleave，kernel speedup 最高 **3.94×**。
- **合并压力**：文中报告回放/合并窗口缩减可达约 **61.1% / 75.8%** 量级（§5）。

## 局限与解读

- 仿真参数对齐行业规格与 MQSim 类对照，**未校准真实 HBF 硅片**；结论是瓶颈形态与策略相对增益。
- 默认无设备端 GC（符合 HBF「memory-interface flash」定位），与 NVMe SSD 语义不同。
- 与 wiki 中 [SPLASH](../papers/splash-sparse-attention-hbf.md)、[HBFlex](../papers/hbflex-flexible-memory-hbf-llm.md)、[Hot–Cold HBM/HBF](../papers/hotcold-hbm-hbf-agentic-llm.md) 形成「应用/系统论文 ↔ 公共仿真底座」互补；数据路径落点见 [End-to-End Memory Data Path](../concepts/end-to-end-memory-data-path.md) 与 [Memory Hierarchy and Cache](../concepts/memory-hierarchy-cache.md)。

# Citations

1. Li, Y., Wang, J., Wang, J., Yang, L., Yan, H., Chai, X., Shi, L. “HBF-Sim: An Extensible HBF Simulator for Large-scale GPU Memory Systems.” arXiv:2609.29246, 2026. [arXiv](https://arxiv.org/abs/2609.29246)
2. [本地原文 PDF](../raw/papers/HBFSim_Extensible_HBF_Simulator_GPU_2026.pdf)；[原始来源记录](../raw/papers/hbfsim-extensible-hbf-simulator.md)
