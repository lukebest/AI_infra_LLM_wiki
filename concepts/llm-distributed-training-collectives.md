---
type: Concept
title: LLM Distributed Training Collectives
description: H&P Ch.6/10 语境下 LLM 训练集体通信：AllReduce/AllGather/All-to-All；Ring vs Tree；DP/TP/PP/EP 配方；通信-计算重叠与 WSE 片上 vs 跨 wafer
tags:
- llm
- training
- allreduce
- collective
- parallelism
- distributed
- noc
- wse
timestamp: '2026-09-10T00:00:00Z'
created: 2026-07-13
updated: 2026-09-14
sources:
- raw/articles/arch-study-30d-day-27.md
- raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf
- raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf
- raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf
- raw/papers/Einsummable_Multi_GPU_Parallelism_2026.pdf
- raw/papers/CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf
- raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf
- raw/papers/Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf
- raw/articles/bojieli-ai-infra-book.md
---

# LLM Distributed Training Collectives（分布式训练与集体通信）

arch-study **并行篇 Day 27**：H&P Ch.6 + Ch.10——当模型装不进单芯片（GPT-3 175B ≫ WSE 44 GB SRAM），**通信成为训练主瓶颈**。经典 MPI 五算法见 [MPI Reduce/AllReduce](/concepts/mpi-reduce-allreduce-algorithms.md)；本页聚焦 **LLM 训练配方与复杂度直觉**。

**Source:** [raw/articles/arch-study-30d-day-27.md](raw/articles/arch-study-30d-day-27.md)

## Collective 原语（训练侧）

| 原语 | 语义 | LLM 用法 |
|------|------|----------|
| **AllReduce** | 每人得全局和 | DP/TP 梯度或 activation 同步 |
| **Reduce** | 仅 root 得和 | 主节点收集 |
| **AllGather** | 每人得拼接全集 | 权重/分片拼回 |
| **Broadcast** | 主节点下发 | 初始化/checkpoint |
| **All-to-All** | 每人与每人交换分片 | MoE token 重排、Attention 重排 |

DP 训练每 step：`forward → backward → AllReduce(grads) → update`。

## Ring AllReduce：为何工程胜出

两阶段，各 **N−1** 步：

1. **Reduce-Scatter**：环上传递并累加，每人最终持有全局和的 **1/N**  
2. **AllGather**：环上传递完整分片，每人持有全集  

| | Ring | Binary Tree | Parameter Server |
|--|------|-------------|------------------|
| 每 worker 传输量 | **≈2D**（与 N 近似无关） | ~D·log₂N | Master **2D**（热点） |
| 步数 | **2(N−1)** | log₂N | O(1) 轮次但串行 |
| 大消息 | **带宽最优** | 根拥塞 | Master 瓶颈 |
| 小消息 | 步数多 → 延迟敏感 | 常更好 | — |

粗算：256 GPU、1 GB、~100 Gb/s → Ring ~**200 ms** 量级；GPT-3 级梯度 ~700 GB 时 AllReduce 可占 step 时间 **30–50%+**。

## 四种并行策略

| | **DP** | **TP** | **PP** | **EP** |
|--|--------|--------|--------|--------|
| 切法 | batch | 张量维（Megatron） | 模型层 | MoE expert |
| 原语 | AllReduce 梯度 | 每层 AllReduce 部分和 | P2P act/grad | **All-to-All** |
| 频率 | 每 step | 每层×2 | 每 micro-batch | 每层 |
| 适用 | 模型 ≤ 单卡 | 单层太大 | 必须切层 | MoE |
| 瓶颈 | 互联带宽 | NVLink/带宽 | **bubble** 10–30% | All-to-All |

推理侧 DP↔TP 切换点见 [Parallelism Transition Point](/concepts/parallelism-transition-point.md)。

## 分布式 Roofline 直觉

```
T_train ≈ T_compute + T_comm(DP/TP/PP/EP)
T_compute ≫ T_comm → 堆算力 / 大批次
T_comm ≫ T_compute → 压互联、压缩梯度、重叠通信
```

弱 scaling 大模型：常出现 **T_comm / T_compute > 1**（笔记例：~3.7×）→ GPU 大量时间等通信。

经典 Hockney 只写 `T = pα + qS/B`。 [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) 把集体墙钟拆成 **wait + transfer**：先到 barrier 的 rank 空等最慢 rank，这段 **τ 与互连带宽无关**。增广式 `T = pα + qS/B + τ`。8-GPU NVLink 域上 τ 可占通信时间 >50%；中位 rank 可把 >80% 的 TP 通信花在等。GEMM 跨 rank 差驱动 78% 的 GPU 计算差异。因此把 T_comm 全算成「带宽不够」会高估 scale-up 该配的 B。


## Wafer-Scale 如何改写故事

| | GPU 集群 | 单 WSE |
|--|----------|--------|
| AllReduce 介质 | NVLink / IB | 2D mesh NoC |
| 延迟量级 | ms–s（大消息） | **μs** 级 hop 积 |
| 限制 | 模型仍须多卡 | SRAM **装不下**全模 → 多 wafer / Rack-Scale |

片上集体算法谱系见 [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)；量化见 [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md)。跨 wafer fabric ≈ 新的「长延迟 NoC」——Rack-Scale 核心命题。

## 通信-计算重叠

不必串行等 AllReduce：用 **async AllReduce + 下一层/下一 micro-batch 计算** 掩盖；PP 用 1F1B 等调度减 bubble。重叠率受链路与 kernel 粒度限制。

## Sequence Parallelism / Ulysses All-to-All（2026-09 增量）

长上下文训练把序列切开后，attention 常需 **All-to-All** 把头维重排（DeepSpeed-Ulysses）。[BASP](/papers/basp-batch-aware-sequence-parallelism.md) 在 \(N=KB\) 时把全局 N-way A2A 拆成 B 组并行 K-way，每 GPU 仍 \(BS/N\) tokens；8×A100 上相对 Ulysses 端到端 **1.17–1.32×**，大 B 时 A2A 墙钟可降约 **85×**（端到端收益会被 ZeRO 集体吃掉一部分）。[Einsummable](/papers/einsummable-multi-gpu-parallelism.md) 从另一端自动搜 join-agg 分解，可在 128K 单序列上自动落到类似 Ulysses 的头/token 切分，且通信用合成 exchange 而非罐头 NCCL。


## 存储与集体共享 Fabric（2026-09）

[Sharing a Fabric](/papers/sharing-fabric-collective-storage-penalties.md)（NTU/LLNL）在 Slingshot-11 上拆出两种代价：重尾 DataLoader stall（主），以及存储与 NCCL/RCCL **同 traffic class** 时 all-reduce 被拖到最高 **145×**（次）。DYAD 节点本地 NVMe staging 整 epoch vs Lustre **7.4×**。提醒：集体墙钟的外生项不只是集群拥塞 pattern（[REACT](/papers/react-tuning-collective-patterns-shared-clusters.md)），还有 **I/O 是否还在那张网上**。

[Entwine](/papers/entwine-tiled-computation-fine-grained-gpu-comm.md)（中科院）把重叠从「整核后再集体」推进到 **tile 产出顺序 + 细粒度 SM 通信核 + 资源预算**：A800 NVLink 上 GEMM–ReduceScatter vs cuBLAS+NCCL geomean **1.232×**（最高 1.433×），相对 FlashOverlap/Async-TP/FLUX 等再高 **3.1–9.8%**。

## 书 Ch.6–7、10：分层、环/树、就绪偏差（2026-09）

[Ch.6](/analyses/ai-infra-book/ch06-supernode.md) / [Ch.7](/analyses/ai-infra-book/ch07-datacenter-network.md) / [Ch.10](/analyses/ai-infra-book/ch10-training-system.md) 把集体从「记得 Ring」推进到可算的路径：

- 环 \(T=2(n-1)\alpha+2(n-1)M/(nB)\)；未分段树 \(2\log_2 n(\alpha+M/B)\)。H100 八卡、\(\alpha=0.822\) μs、450 GB/s/dir，交点约 **680 KiB**。decode 10 KiB 偏启动/树；prefill 80 MiB 偏环。
- **分层梯度**：16 rank、192 MiB。连续环跨机 720 MiB/1 NIC；分层 384 MiB/8 NIC。发送总量可相同，出口不同。
- NCCL `busbw=2(n-1)M/(nT)` ≠ 每 NIC 线速。重叠必须测并发，不能独占时间相减。
- 关键路径从**数据就绪**起：三人 0 ms、一人 2 ms + 0.4 ms 交换 = 2.4 ms；对齐就绪到 0.4 ms（与 Synchronization Tax 的 \(\tau\) 同构）。MegaScale：带宽稳、rank 越来越晚到。
- 1024 卡、TP8×DP128：超节点 8→64 且出口随卡增长，步时间 0.939→0.690 s（**+36% tok/s**）；再大收益 <2%。同条件仍选 TP8。
- 训练状态 16 B/param；ZeRO 减复制不自动减峰值激活。checkpoint \(\epsilon\approx C/I+\lambda(I/2+R)\)。

## 相关页面

- [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md) — α+nβ 五算法
- [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — 片上 FRED 等
- [Parallelism Transition Point](/concepts/parallelism-transition-point.md) — 推理 DP/TP/PP
- [M2N Communication](/concepts/m2n-communication.md) — MoE 非对称通信
- [Cerebras WSE](/entities/cerebras-wse.md) — 片上 vs 片外
- [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md) — Day 29 前沿
- [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md) — LLM 训练数据中心网络（HPN）
- [Meta RDMA over Ethernet](/papers/rdma-over-ethernet-meta-training.md) — Meta 规模分布式训练 RoCE
- [Comm/Comp Parallelism](/papers/optimizing-comm-comp-parallelism-training.md) — 训练平台通信-计算重叠
- [Mozart 3.5D](/papers/mozart-35d-wafer-scale-moe-training.md) — 晶圆级 chiplet 上用专家共激活布局压 All-to-All 的 C_T
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — **推理** TP AllReduce 与 KVT 争用（对照训练集体）
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — 把 AllReduce/All-to-All 落到 AXI/以太 C2C 的 VC、credit、MAC 组帧
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 片内树 NoC 上的 MoE scatter-gather，不是跨卡集体
- [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md) — Meta MTIA 300：集体编译到包内 ME/NMC，机柜内最高 940 GB/s，重叠 GEMM 降幅 <0.5%
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 驻留 MoE 后 EP/TP 权重移动变次级；归约顺序必须匹配 shard 放置（反向 D2D 最高 5.7×）
- [Maia 200 SDLA](/papers/maia-200-sdla.md) — 8 芯 Ethernet Allgather 到延迟界 78% / 带宽界 94% SoL；direct vs ring
- [晶圆级光互连热 stall](/papers/wafer-scale-optical-interconnect-moe-thermal.md) — MoE EP All-to-All 被 MRR 热光 stall ~47–49 ms 放大到 2.7–3.8×
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 集体墙钟含与 B 无关的 barrier 税 τ；B* 随域规模下降
- [CIERA](/papers/ciera-cross-iteration-exponent-reuse-allgather.md) — MoE AllGather 指数复用无损压缩
- [REACT](/papers/react-tuning-collective-patterns-shared-clusters.md) — 共享集群拥塞下改写集体 pattern
- [Sharing a Fabric](/papers/sharing-fabric-collective-storage-penalties.md) — 存储与集体同 fabric / 同 TC 的两重罚
- [Entwine](/papers/entwine-tiled-computation-fine-grained-gpu-comm.md) — NVLink 域内 GEMM–RS tile 顺序×SM 通信预算；vs NCCL 1.232× geomean
- [AI Infra Book Ch.6](/analyses/ai-infra-book/ch06-supernode.md) / [Ch.7](/analyses/ai-infra-book/ch07-datacenter-network.md) — 分层集体与超节点缩放

# Citations

[1] [raw/articles/arch-study-30d-day-27.md](raw/articles/arch-study-30d-day-27.md) — H&P Ch.6/10 + LLM collectives（Day 27）
[2] [raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf](raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf) — Devraj et al., arXiv:2608.22503；τ 与 B 无关
[3] [raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf](raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf) — BASP；Ulysses 子组 A2A
[4] [raw/papers/Einsummable_Multi_GPU_Parallelism_2026.pdf](raw/papers/Einsummable_Multi_GPU_Parallelism_2026.pdf) — Einsummable；自动 intra-op 并行
[5] [raw/papers/CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf](raw/papers/CIERA_Cross_Iteration_Exponent_Reuse_Allgather_2026.pdf) — CIERA；无损指数复用 Allgather
[6] [raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf](raw/papers/REACT_Tuning_Collective_Patterns_Shared_AI_Clusters_2026.pdf) — REACT；拥塞感知集体 pattern
[7] [raw/papers/Sharing_Fabric_Collective_Storage_Penalties_2026.pdf](raw/papers/Sharing_Fabric_Collective_Storage_Penalties_2026.pdf) — Wang et al., arXiv:2609.06506；存储×集体 fabric 争用
[8] [raw/papers/Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf](raw/papers/Entwine_Tiled_Computation_Fine_Grained_GPU_Comm_2026.pdf) — Ma et al., arXiv:2609.11562；tile 级 GEMM–RS 重叠
[9] [Ch.6–7 manuscripts](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/06-超节点.md) — 李博杰《AI Infra》
[10] [AI-Infra-Book.pdf](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
