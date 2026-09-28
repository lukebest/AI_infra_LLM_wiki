---
type: Raw Source
title: "HBF-Sim: An Extensible HBF Simulator for Large-scale GPU Memory Systems"
description: "华东师大/上海创智 — Accel-Sim 集成的端到端 GPU–HBF 仿真器；媒体吞吐最高 15.94×；contiguous 放置 page-service 放大 −41.9%。"
timestamp: '2026-09-28T00:00:00Z'
source_url: https://arxiv.org/abs/2609.29246
arxiv: '2609.29246'
ingested: 2026-09-28
sha256: b41dc57ae1c7481c3a1513f9cef7be84904e30cc93779ce2240252097c9846bb
---

# HBF-Sim: Extensible HBF Simulator

**Authors:** Yaqi Li, Jing Wang, Junfeng Wang, Long Yang, Han Yan, Xiaohu Chai, Liang Shi  
**Affiliation:** East China Normal University; Shanghai Innovation Institute  
**PDF:** [HBFSim_Extensible_HBF_Simulator_GPU_2026.pdf](HBFSim_Extensible_HBF_Simulator_GPU_2026.pdf)  
**arXiv:** [2609.29246](https://arxiv.org/abs/2609.29246)（2026-09-24，cs.AR）

## 问题

OCP HBF（SK hynix + SanDisk）把 NAND 共封装到 GPU 侧（文中称 512 GiB 密度、最多 16×UCIe、聚合接口 **3.072 TB/s**），但既不是大容量 HBM，也不是 NVMe SSD：可用带宽取决于 64B cache-line→4 KiB page 映射、channel-affine 并行与媒体管理。既有 GPU/SSD/应用内 HBF 模型无法闭合 GPU issue↔排队↔NAND 全路径。

## 方法要点

- Accel-Sim/GPGPU-Sim 扩展：分离 **GPU–HBF interaction controller** 与 **page-based parallel stack storage**。
- **MSHR** 页键合并 cache-line；页级多栈 flash 管理器；可配置 placement/聚合/隔离策略。
- 面向 LLM 权重顺序读、KV 复用读、追加写与 RAG gather 等访问模式。

## 摘录数字（仅论文给出）

- 媒体扩展：吞吐 **8.738 → 139.285 GB/s（15.94×）**，媒体占用 **99.6–99.99%**（Figure 6）。
- Contiguous 相对 interleave：page-service amplification **−41.9%**（32 entries/page）。
- 活跃页条带化相对内置 interleave：kernel speedup 最高 **3.94×**（Table 6）。
- 合并/回放窗口：文中给出最高约 **61.1% / 75.8%** 量级的窗口缩减（§5）。

**Working page:** [HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md)
