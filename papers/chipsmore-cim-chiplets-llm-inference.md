---
type: Paper
title: "CHIPSMORE: Compute-in-Interconnect and -Memory Chiplets for Multi-Mode Multi-Request LLM Inference"
description: NUS — RRAM-ACIM+SRAM-DCIM + IPCN in-network DMAC；vs H100 Mistral-7B INT8 最高 2.38× 吞吐、27× 能效（仿真）
tags:
- chiplet
- noc
- interconnect
- mesh
- accelerator
- sram
- memory
- llm
- inference
- kv-cache
- serving
- throughput
- latency
- packaging
- architecture
- pipeline
- power
- batching
timestamp: '2026-09-02T00:00:00Z'
created: 2026-09-02
updated: 2026-09-02
sources:
- raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf
- raw/papers/chipsmore-cim-chiplets-llm-inference.md
---

# CHIPSMORE: Compute-in-Interconnect and -Memory Chiplets for Multi-Mode Multi-Request LLM Inference Acceleration

**Authors:** Yue Jiet Chong, Yimin Wang, Zhen Wu, Zixuan Wang, Wei Zhang, Xuanyao Fong
**Affiliation:** National University of Singapore (NUS)
**arXiv:** [2608.30509](https://arxiv.org/abs/2608.30509)（2026-08-31，cs.AR）
**Venue:** 预印本。文内未另报会议。
**PDF:** [raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf](raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf)

相对 [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) 搜的是 **封装内 hybrid serving 组成/放置**，本文给的是 **一颗 CIM chiplet 加速器怎么同时扛 base/LoRA、长短 KV、多请求**。相对 [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) 的 ReRAM 近存 FFN 池，这里是 **RRAM-ACIM 静态权重 + SRAM-DCIM 动态/LoRA + 片上 compute-in-interconnect**。

## 动机

LLM 推理在适配模式（base / LoRA）、上下文长度、请求并发上波动大。Prefill 偏矩阵–矩阵，decode 反复碰权重和 KV；为长上下文 decode 配的资源在短上下文上白白烧静态功耗。CIM 方向里：RRAM-ACIM 密度高、非易失、适合静态预训练权重，但写耐久/写能差，扛不住运行时中间态；SRAM-DCIM 可快速重写、数字确定，适合 LoRA 和临时存储。既有 CIM 加速器常假定固定上下文、单一内存角色或单 batch；靠权重复制抬多请求吞吐时，RRAM 面积、chiplet 数、泄漏和成本近似随并发线性涨。

## 方案

异构 PE + 可编程 Inter-PE Computational Network（IPCN）+ chiplet 间 UCIe。

**异构 PE。** RRAM-ACIM 做静态权重上的 SMAC；SRAM-DCIM 做 LoRA / 动态；运行时中间张量可卸到 IPCN 上做 DMAC。

**IPCN（片上）。** 2D mesh；路由器兼通信与 in-network 计算（DMAC）。Network Program Mem + Network Main Controller；指令 30-bit。每个 Compute Tile（CT）是自治计算簇。

**Inter-CT。** UCIe：每 CT **2** endpoints，每 endpoint **16** lanes。多数数据留在 tile 内；UCIe 只扛跨 CT 交换。

**分层 KV（Table II 策略）。** Router scratchpad（最近 IPCN/PE）→ SRAM-DCIM（base 模式可作辅助 KV）→ eDRAM（容量第三层，仅当 scratchpad+SRAM-DCIM 不够）。LoRA 模式把 SRAM-DCIM **留给 adapter**，KV 更多落 eDRAM。上下文档：S 2048/2048、L 4096/4096、XL 8192/8192。

**非复制多请求层流水。** 每个 transformer 层静态绑到唯一 weight-bearing CT cluster；多请求按时间偏移注入，同时占不同层，共享同一份 RRAM 预训练权重。不按 batch 复制权重。

**State-aware 重配置 / power gating。** RRAM 权重非易失可不供电保留；LoRA（SRAM-DCIM）与 KV（scratchpad / SRAM-DCIM / eDRAM）是易失态，必须保留。空闲 IPCN 路由器与算力模块可关，内存保留与算力激活解耦；功耗主要跟活跃计算和保留运行时态走，而不是跟模型总容量走。

**系统参数（Table III）。**

| 项 | 值 |
|----|-----|
| Tech / Freq / bit-width | **7 nm** / **1 GHz** / 64 |
| Cluster size | **4** chiplets |
| IPCN | **32×32**；scratchpad **16 MiB** |
| SRAM-DCIM / eDRAM | **16 MiB** / **64 MiB**（eDRAM refresh **10 ms**） |
| UCIe | **2** endpoints/CT，**16** lanes/endpoint |
| Macro（每 Router–PE pair） | RRAM-ACIM 256×256；SRAM-DCIM 256×64；inter-router I/O 4；AXI-Stream 2 对；FIFO 256 B |

评测：Verilog + Synopsys Design Compiler 7 nm；SRAM scratchpad 面积/功耗走 CACTI；周期精确指令级仿真器跑 INT8 权重端到端。**仿真，不是硅。**

## 效果（仅论文数字）

**vs Nvidia H100（Mistral-7B INT8，base-mode long context 4096/4096，Table V；基线 H100+vLLM）**

| | H100 | CHIPSMORE | Speedup | Efficiency× |
|--|------|-----------|---------|-------------|
| BS1 tok/s / W / tok/J | 467.3 / 350 / 1.34 | **1112.5 / 30.7 / 36.24** | **2.38×** | **27×** |
| BS4 tok/s / W / tok/J | 1665.7 / 490 / 3.40 | **3003.9 / 46.4 / 64.73** | **1.80×** | **19.04×** |

同表还列了 Apple M4-Max、Cerebras-2、CENT、H2-LLM、CHIME；本文绝对吞吐低于 Cerebras-2（BS1 4271.5），能效更高。

**短上下文 BS1→4 吞吐增益：** Llama 3.2-1B **3.91×**，Mistral-7B **2.71×**，Qwen3-14B **2.77×**（次线性；层流水填排空、同层独占、IPCN/KV 争用）。

**UCIe：** 即使 BS4，最大利用率仍 **<25%**——互连不是瓶颈；流量随模型/batch 涨，利用率随上下文变长反而降（执行时间涨得更快）。

**行为要点。** 吞吐随模型变大、上下文变长下降（层更深、注意力二次、KV 线性扫）。XL 溢出到 eDRAM 再掉吞吐。LoRA 吞吐大多贴近 base（rank-8 在 Q/V）；平均功耗一般随模型/batch 升，LoRA 高于对应 base（SRAM-DCIM 不再只做辅助 KV）。

## 与 wiki 的关系

- [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md) — HYDRA 是 hybrid serving 的 chiplet DSE；CHIPSMORE 是固定 CIM 宏架构 + 运行时 KV/模式/流水
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — ReRAM 近存做 **MoE FFN 池**；本文 RRAM-ACIM 做 **全模型静态权重 SMAC**，另加 IPCN DMAC
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 3D FeFET/DRAM-PNM 异构 MoE；本文是 2.5D UCIe chiplet + 平面 IPCN mesh
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) / [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — C2C/PHY 侧建模；本文报 UCIe 利用率 <25%，无 PAM4/FEC 细节
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 本文是 **层流水多请求共享权重**，不是机柜 AFD；分层 KV 更接近容量/局部性调度
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构在 **RRAM-ACIM vs SRAM-DCIM** PE 角色，不是 GPU+LPU AFD
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — IPCN = 带 in-network DMAC 的 2D mesh；应用层（LLM 层流水）倒逼片上计算–通信一体

## 开放问题

1. 全是 Design Compiler + 周期仿真，无硅、无实测 UCIe 眼图/误码。
2. H100 基线是 vLLM + Mistral-7B INT8 long；与其他 CIM 列（CENT/H2-LLM/CHIME）工艺/精度未必同口径，只能读相对表。
3. Cluster=4 chiplets、IPCN 32×32 是否覆盖更大模型（>14B）的层绑定深度，文内外推有限。
4. eDRAM refresh 10 ms 对超长 decode 的抖动未单独压力测试。
5. LoRA 只报 rank-8 Q/V；更高 rank / 更多适配层是否挤爆 SRAM-DCIM 未扫。

# Citations

[1] [raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf](raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf) — Chong et al., arXiv:2608.30509
[2] [raw/papers/chipsmore-cim-chiplets-llm-inference.md](raw/papers/chipsmore-cim-chiplets-llm-inference.md) — 结构化摘录
