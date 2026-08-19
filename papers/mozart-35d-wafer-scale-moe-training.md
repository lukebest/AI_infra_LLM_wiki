---
type: Paper
title: "Mozart: Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures"
description: UNC/UMN — 3.5D 晶圆级 NoP-Tree + 专家共激活布局与流式调度；Qwen3-30B / OLMoE / DeepSeek-MoE post-training 相对 baseline 1.92× / 2.37× / 2.17×
tags:
- wse
- chiplet
- moe
- training
- hybrid-bonding
- 3d
- noc
- interconnect
- parallelism
- communication
- llm
- architecture
- now
- network-on-wafer
timestamp: '2026-08-18T00:00:00Z'
created: 2026-08-18
sources:
- raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf
- raw/papers/mozart-35d-wafer-scale-moe-training.md
---

# Mozart: Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures

**Authors:** Shuqing Luo, Han Ye, Pingzhi Li, Jiayin Qin, Jie Peng, Yang (Katie) Zhao, Yu (Kevin) Cao, Tianlong Chen（UNC Chapel Hill / University of Minnesota）
**arXiv:** [2603.07006](https://arxiv.org/abs/2603.07006)
**Venue:** arXiv 预印本（正文含 NeurIPS checklist）。**正式会议接收未独立核实**。
**PDF:** [raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf](raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf)
**Code:** https://github.com/UNITES-Lab/Mozart

## 中文摘要

MoE-LLM 把计算模块化，但稀疏路由造成内存局部性差、All-to-All 重、资源利用率低。Mozart 是面向 **3.5D 晶圆级 chiplet** 的算法–硬件协同：先剖析指令微调数据上的专家激活/共激活先验，把常一起激活的专家聚到同一或相邻 chiplet 以降低 All-to-All 的 token 复制数；再用流式 token/expert 调度把 DRAM 权重加载与片上计算重叠。硬件上，每个 compute chiplet 用 hybrid bonding 做 logic-on-SRAM 垂直堆叠，chiplet 间用 2.5D **NoP-Tree**（中心 attention、叶专家、带 in-network 聚合的 switch）。在 Qwen3-30B-A3B、OLMoE-1B-7B、DeepSeek-MoE-16B 的 post-training 仿真中，相对无优化 baseline 分别达到 1.92×、2.37×、2.17× 加速。

## Motivation

Routed experts 在现代 MoE 中常占 **>90%** 参数。标准专家并行流水是 Dispatch → All-to-All → Expert → All-to-All → Combine。既有 chiplet 加速器（Maestro、Cambricon-LLM、ScalePoM）多是亚晶圆、偏推理；FRED 做晶圆级训练但假设稠密均匀划分。MoE 的动态不均负载会让静态 tiling 产生过量跨 chiplet 通信。Mozart 把 MoE 的逻辑模块性对齐到 3.5D 的物理模块性。

## Approach

1. **先验剖析**（Alpaca + 预训练模型 prefilling）：专家负载向量 V；共激活图 C / 归一化 P。
2. **专家聚类 + 分配**：按共激活做 farthest-point 风格聚类，再整数规划把 cluster 分到共享同一 DRAM I/O 的 chiplet 组，平衡组间负载。同 chiplet 上共激活专家只需一份 token 副本，降低 C_T（标准 top-k 时 C_T = k）。
3. **流式调度**：按 V 优先加载高激活 expert cluster；token micro-batch 与 expert 顺序计算重叠（加载高激活 vs attention 计算；加载低激活 vs 高激活计算）。
4. **3.5D 硬件**：
   - 3D：logic die + SRAM die，hybrid bonding，激活放近计算。
   - 2.5D NoP-Tree：中心 attention（更靠 DRAM）、4 个 switch 组 × 4 专家 chiplet = 16 MoE chiplet；switch 做 in-network MoE 聚合。
   - 两级存储：权在晶圆周边分布式 DRAM（每 4 专家共享 I/O）；激活在本地 SRAM。
   - 训练映射：每步 32 sample、4× micro-batch=8；一次只流一个 transformer block 的权重。
5. **实现**：Verilog + Design Compiler 28 nm + PrimePower；cycle-accurate 仿真对齐网表；1 GHz；FP16。

## Results（仅论文数字）

模型：Qwen3-30B-A3B（128 routed, top-8）、OLMoE-1B-7B（64, top-8）、deepseek-moe-16b-base（64+2 shared, top-6）。

| 配置 | 优化组合 | 相对 baseline |
|------|----------|---------------|
| Baseline | 无 | 1× |
| Mozart-A | 仅通信–计算重叠 | Qwen3 **1.33×**，OLMoE **1.58×**，DeepSeek **1.49×**（正文 Q2） |
| Mozart-B | A + 高效 All-to-All | （中间点，见表 4 归一化延迟） |
| Mozart-C | B + 专家布局 | Qwen3 **1.92×**，OLMoE **2.37×**，DeepSeek **2.17×** |

C_T：Qwen3 8 → 6.58 → **5.77**；OLMoE 8 → 6.84 → **5.63**；DeepSeek 6 → 5.56 → **4.32**。seq=512 时 Mozart-C **2.34×**，seq=128 **1.47×**（相对同设定 baseline）。HBM2（256 GB/s）比 SSD（15.8 GB/s）更能吃到重叠收益。

硬件表：Qwen3 14175 mm² / 3.34 kW；OLMoE 10200 mm² / 3.55 kW；DeepSeek 11230 mm² / 3.19 kW。DRAM 8192 MB、SRAM/tile 2.265 MB；2.5D 与 3D 链路各 0.125 GB/s、pitch 50 μm。作者自陈系统仍 **memory-bound**（专家权重串行加载）。

## Relation to wiki

- [Network-on-Wafer](/concepts/network-on-wafer.md) — 晶圆级互连的另一拓扑：NoP-Tree vs WoW 重叠 mesh
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 专家并行 All-to-All；Mozart 用共激活布局压 C_T
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — logic-on-SRAM hybrid bonding + 2.5D NoP
- [Cerebras WSE](/entities/cerebras-wse.md) — 单片 field-stitch mesh vs 异构 chiplet 树
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) / [MegaMoE Kernel](/concepts/megamoe-kernel.md) — GPU 上 MoE 通信重叠；Mozart 是 chiplet/DRAM 层次
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — Mozart 在训练侧把 attention 与 expert 分到不同 chiplet
- [WoW Network Design](/papers/network-design-wafer-scale-wow-hybrid-bonding.md) — 同是晶圆级，几何约束完全不同
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 推理侧 FeFET/DRAM PNM + 树 NoC；Mozart 是训练侧 NoP-Tree

## 开放问题

1. Attention 独占一个 chiplet，可能成为次级瓶颈；作者建议再加 DP/TP。
2. Switch 在高通信下会堵；未探索给 switch 更多面积/带宽。
3. 正文写 post-training / instruction tuning，不是从零预训练。
4. 2.5D/3D 链路表列 0.125 GB/s @ 50 μm pitch，与 WoW 文 2 TB/s 量级差很大——跨论文对比需非常小心，可能是 per-link 微架构参数而非系统级 D2D。

# Citations

[1] [raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf](raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf) — Luo et al., arXiv:2603.07006
[2] [raw/papers/mozart-35d-wafer-scale-moe-training.md](raw/papers/mozart-35d-wafer-scale-moe-training.md) — 结构化摘录
