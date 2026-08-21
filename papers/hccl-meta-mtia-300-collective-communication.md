---
type: Paper
title: "HCCL: Collective Communication for Meta MTIA 300"
description: SC 2026 自称 — 包内 NIC chiplet + ME/NMC 卸载集体；机柜内最高 940 GB/s，重叠 GEMM 降幅 <0.5%；推理 PUT 集体 <6 μs
tags:
- chiplet
- interconnect
- scale-up
- scale-out
- communication
- rdma
- accelerator
- training
- inference
- fabric
- protocol
- rack
- hbm
- architecture
- moe
- meta
timestamp: '2026-08-21T00:00:00Z'
created: 2026-08-21
sources:
- raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf
- raw/papers/hccl-meta-mtia-300-collective-communication.md
---

# HCCL: Collective Communication for Meta Training and Inference Accelerators

**Authors:** Wesley Bland, Lars Paul Huse, Chidambaram Muthu 等（Meta Platforms；通讯 wbland / larsph / cmuthu）
**arXiv:** [2608.00358](https://arxiv.org/abs/2608.00358)
**Venue:** abs 写 to be published in *SC '26*。**未独立核实会议程序册，不当成已录用。** 硅细节指向同作者组的 *MTIA-3* ISCA '26 文。
**PDF:** [raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf](raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf)

## 动机

排序/推荐训练被大 embedding、不规则 **AllToAllv**、以及跨数百加速器的通信占比推高。NCCL/RCCL 把集体跑成 device kernel，占 SM。[Meta RDMA](/papers/rdma-over-ethernet-meta-training.md) 是 GPU + 主机 NIC 的 RoCE 运维；MTIA 300 是 Meta **第一颗把 backend 网络做进封装**的芯片——compute chiplet + 两颗 network chiplet + HBM——集体可以完全离开 PE grid。

HCCL（Hoot Collective Communication Library）把「编译出来的集体」交给专用 message engine，而不是再写一层 GPU kernel。

## 方案

**封装与 I/O**

- 两颗 network chiplet，每颗 6 个定制 **800 Gb/s** RDMA NIC。默认 **8 NIC scale-up + 2 NIC scale-out**，合计 **1 TB/s**；另留 2 NIC，可把 I/O 提到 **1.2 TB/s**。
- **Express doorbell**：WQE 写到门铃地址即提交，NIC 内部排队，省掉再去读外部 WQE。不支持 QP 缓存（面积）。
- 读/写请求上的定制 bit 给 compute chiplet 划 cache 分区，避免通信临时缓冲污染应用数据。

**Message Engine（16 个，两组×八）**

- **CPU-M**（RISC-V）：从 HBM 取 subgraph，展开成 WQE，算依赖，打上 ME id，送到 NIC 接口或 NMC。完成走共享 CQ。
- **NIC 接口**：单 FIFO，按 QP 路由到对应 NIC 的 express doorbell；任一 ME 可碰任一 NIC。
- **NMC**：卸载拷贝和加法（S=A+B 等）。每输入 **128 B/cycle**，全 NMC 开时 **96 B/cycle**，合计 **2.8 TB/s**——超过聚合 I/O 一倍以上，够 AllReduce/ReduceScatter 线速。算术在 FP32，再量化回 BF16/FP16/FP32。

**软件：编译通信**

Host 把一次集体编成 work packet → 多个可并行 subgraph → 带依赖的 WQE 序列（RDMA / NMC 计算 / 子图同步）。依赖类型：Fence、Sync、WQE Sync、Receive Sync、Send Sync。CPU-C 按 stream 保序，混排计算与通信。PyTorch 走 c10d 与 torchcomms 后端。

训练侧把 AllReduce ring 等切到多 ME 多环。推理侧三条路径：

1. **One-sided**：PE 经 express doorbell 直发，完成计数由 ME 维护（约 450 ns 静态开销）。
2. **Device-resident / AllToAllvDynamic**：路由 kernel 的 size/offset 写在 device 指针上，HCCL 改 WQE 而不回 host。
3. **Device-triggered**：集体预调度在旁路 stream，等 PE 信号再放行；可预贴 Recv，减 RNR NAK。

## 效果（仅论文数字）

**训练带宽（合成，绕过 H2D/CPU-C 调度；100 warmup + 1000 iter）**

- 机柜内（≤16 rank，纯 scale-up）集体最高 **940 GB/s**（理论 1 TB/s = 800 SU + 200 SO）。
- 超机柜后弯向 scale-out；128-rank AllGather 仍到 **838 GB/s**（跨机柜只有 200 GB/s）——拓扑感知，尽量把交换留在机柜内。
- PARAM 重叠：16-rank 上满载 GEMM 并行跑 100 次集体，GEMM 降幅最多约 **1 TFlop（~0.5%）**，集体带宽曲线与无计算时接近。作者归因为 NIC 抢 HBM。

**控制路径开销**

- 流水满后：H2D **17.1±0.3 μs**，event **3.6±0.1 μs**，CPU-C **2.9±0.1 μs**，CPU-M **1.1±0.1 μs**。Event 计时合计约 **6 μs**。H2D 在真实作业里用并行 copy engine 藏。
- 工作包缓存再入队 **<10 μs**（与 job/input size 无关）。

**推理**

- PE vs ME 发 RDMA Write：PE 直发多约 **450 ns** 静态开销。
- PUT 风格 AllToAllv / AllReduce：**sub-6 μs**（scale-up 域）。作者认为此时已接近网络 RTT。
- Device-triggered AllToAllvDynamic 例：trace 上集体墙钟 123 μs，计算流上暴露只有 **31 μs**（其余在等 PE 信号）。

生产排序作业的 size 分布以中大 AllToAllv / AllReduce / AllGather 为主（40-rank 与 256-rank 各一张图）。文内引用前作：≥16 加速器或 >16 MB 时相对 H100+NCCL 有加速，小消息 H100+NCCL 仍更好。

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把 AllReduce/AllGather/AllToAllv 从算法落到 **专用 ME + 包内 NIC**，而不是 NCCL SM kernel
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 工业对照：NVLink 固定 fat-tree vs MTIA 可重布线的 SU/SO NIC
- [Meta RDMA](/papers/rdma-over-ethernet-meta-training.md) — 2024 RoCE+NCCL 运维；本文是同一公司下一代 **chiplet NIC + 编译集体**
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) — 探索框架；HCCL 是生产芯片上的集体库
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — GPU 上把 MoE 与 NVSHMEM 融进一个 kernel；HCCL 把集体**搬离**计算阵列
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 片上 in-network 算术；HCCL 的 NMC 是近 HBM 的线速归约，不在 NoC 交换机里

## 开放问题

1. SC '26 / 配套 ISCA MTIA-3 文未在本轮核程序册。
2. 小消息相对 NCCL 仍弱；express doorbell + QP 上限对更大 communicator 的压力，文称实践中未碰到回收。
3. 推荐训练为主，LLM/MoE 推理路径是为后续 MTIA 代际铺的（device-triggered / PUT）。
4. 940 GB/s 是合成集体，不是端到端推荐 step 的通信占比拆解。

# Citations

[1] [raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf](raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf) — Bland et al., arXiv:2608.00358
[2] [raw/papers/hccl-meta-mtia-300-collective-communication.md](raw/papers/hccl-meta-mtia-300-collective-communication.md) — 结构化摘录
