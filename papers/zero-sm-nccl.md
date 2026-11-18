---
type: Paper
title: "Zero-SM NCCL: SM-Free GPU Communication"
description: "ETH Zurich / NVIDIA — GB200 NVL72 与 B200 NVL8 实测；域内 4 GiB AllGather 714–746 GB/s（摘要称相对 legacy 最高 1.36×）；Qwen GEMM 重叠中位减速 32.9%→3.9%；Megatron-LM 上 GPU-bound FSDP 最高 +3.5%，深流水线 one-sided put 最高 +14.9%"
tags:
- nvidia
- gpu
- collective
- allreduce
- communication
- nvlink
- rdma
- interconnect
- scale-up
- training
- training-system
- fsdp
- moe
- expert-parallelism
- latency
- throughput
- datacenter
created: 2026-11-18
updated: 2026-11-18
timestamp: '2026-11-18T00:00:00Z'
paper_author: [Zhenhao He, Siyuan Shen, Ke Wen, Prajwal Singhania, Shiqing Fan, Youngeun Kwon, Sangkug Lym, Vasudevan Rengasamy, Vishnuswaroop Ramesh, Yicheng Qiang, Craig Belusar, Jeff Hammond, Torsten Hoefler]
year: 2026
venue: arXiv preprint
arxiv: '2611.18075'
sources:
  - raw/papers/Zero_SM_NCCL_2026.pdf
  - raw/papers/zero-sm-nccl.md
---

# Zero-SM NCCL：不占用 SM 的 GPU 通信

## 一句话结论
ETH Zurich 与 NVIDIA 把 NCCL 的 host-initiated 路径做成 **Zero-SM**：域内用 CUDA stream memory operations 做同步、用 copy engine（CE）搬数据，跨域用按流排序的 CPU proxy 驱动 RDMA，全程不启动 SM kernel，并提供 `ncclPutSignal` / `ncclWaitSignal`。在 **GB200 NVL72** 与 **B200 NVL8** 上，域内 4 GiB AllGather 达到 **714–746 GB/s**（symmetric **537–678**、legacy **613–698**；摘要称相对 legacy SM kernel 带宽最高 **1.36×**）；B200 节点上，144 MiB/rank 的 Qwen3-30B-A3B AllGather 把重叠 GEMM 的中位减速从 legacy 的 **32.9%** 降到 CE 的 **3.9%**。Megatron-LM 中，GPU-bound FSDP 相对 legacy ring 最高 **+3.5%**（GB200），一侧 put 在深流水线上最高 **+14.9%**（Qwen3-Next @ GB200）。小消息延迟更高，host-bound 配方会亏。

## 动机
NCCL 等库用 SM 做数据搬运与同步，重叠计算被拖慢，而且互连越快、占用的 SM 越多。图 1 显示，为吃满 NVLink，所需 SM 占比随代际上升。已有 symmetric-memory kernel、NCCLX AllGatherP、VCCL SM-free、MSCCL++ 等部分卸荷方案，仍留下「域内 + 跨域都不占 SM、且能直接接进 NCCL host API」的缺口。

## 方案
1. **范围**：针对 NCCL 的 host-initiated API，不走 GPU-initiated 的 GIN / NVSHMEM 内核路径。依赖 symmetric memory 注册，使 CE 能直接写入对端用户缓冲。
2. **域内**：stream memory wait/write 做同步，CE 异步拷贝；AllGather 在 NVL72 的 72 卡域内可全程走 CE。
3. **跨域**：B200 多节点走分层 AllGather，并使用文中尚未上游发布的 pipelined rail schedule；scale-out 同步由 CPU proxy 按流序发 RDMA。
4. **一侧操作**：`ncclPutSignal` / `ncclWaitSignal` 替换流水线级间 Send/Recv；FSDP 的连续 AllGather 被打成共享同步外壳的单一 plan，摊还提交开销。
5. **平台**：NCCL 2.32.3 + 部分未发布补丁；artifact 在 https://github.com/spcl/zero-sm-artifact。

## 效果（论文数字）
全部为 GB200 NVL72（Grace，NVLink5 900 GB/s/dir，18 节点 / 72 GPU 同一 NVLink 域）与 B200 NVL8（双路 Xeon，节点内 8 GPU，跨节点走 400 Gb/s 轨）上的实测。

**微基准（nccl-tests，10 次试验，扫到 4 GiB）**
- 点对点 NVLink：CE put 在 8 B 时延迟 **16.7 µs**，高于 Send/Recv 的 **9.7 µs**；从 64 KiB 起反超，4 GiB 为 **773 vs 658 GB/s**。跨节点 proxy put 在 8 B 为 **15.9 vs 31.4 µs**，三者都能吃满 50 GB/s 轨。
- 域内 AllGather：4 GiB 时 CE **714–746 GB/s**，symmetric **537–678**，legacy **613–698**。1 KiB 时 CE 延迟地板 **25–29 µs**，SM kernel 为 **12–18 µs**；CE 从 **128–512 MiB** 起才在带宽上超过 symmetric。72 GPU 时 CE 地板 **52 µs**，legacy 环 **118 µs**。
- 跨域（B200 4 / 8 节点，4 GiB）：CE **503 / 436 GB/s**，接近 NIC 界 **517 / 450**；symmetric GIN **482 / 430**，legacy 饱和 **372 GB/s**。

**重叠基准（B200 NVL8，生产前训练轨迹的 GEMM 链，8 rank × 30 次 × 4 轮中位）**
- Qwen3-30B-A3B、MXFP8、144 MiB/rank AllGather：legacy 默认 32 CTA 中位减速 **32.9%**，symmetric 默认 4 CTA **6.2%**、强制 32 CTA **24.0%**，CE **3.9%**（剩余来自内存争用）。
- Llama-3-8B、26 MiB/rank：CE 单颗 GEMM 减速不超过 **0.2%**，legacy 中位 **9.9%**。

**端到端 Megatron-LM（12 个 FSDP + 7 个 PP 配方，15B–405B，32 或 64 GPU，配对 block、每配方 3 组）**
- FSDP 相对 legacy ring：GPU-bound 稠密配方在 GB200 最高 **+3.5%**、B200 最高 **+1.9%**（Qwen3-32B-G2 在噪声内）。相对只占少量 CTA 的 symmetric kernel，只在部分 GPU-bound 配方上明显领先，host-bound 与 Qwen3-235B-G（B200，plan fusion 尚未覆盖更快的 rail schedule）会落后。
- 划算条件：步骤已是 GPU-bound；消息足够大（GB200 上约 240 MiB 的 FSDP gather 打平或落后 symmetric，**820 MiB** 才赢）；路径（单播 / 组播）要匹配并发流量。
- PP 一侧 put 相对 Send/Recv：深流水线在两套系统上都加快，最高 **+14.9%**（Qwen3-Next @ GB200）。浅或高度交织的流水线（Llama-70B 气泡约 2%，以及两级的 Qwen3-32B、Nemotron-15B）无收益或变慢。释放 SM 最多只加快计算 1–2%，主要收益来自去掉 Send/Recv 的会合。

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把 AllGather / 一侧 put 从 SM kernel 挪到 CE 与 host proxy
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 在 NVL72 整域与 NVL8 分层路径上实测
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 通信不再占用 SM，重叠 GEMM 的减速从约 33% 降到约 4%
- [T-CCL](/papers/t-ccl-tma-collective-communication.md) — 同属少占 SM 的集体通信，T-CCL 走 TMA，本文走 CE + 已上游的 NCCL 路径
- [flash-comm](/papers/flash-comm-self-synchronizing-collectives.md) — 关注 decode 小消息自同步；本文明确小消息上 CE 延迟更高
- [SURMA](/papers/surma-scale-up-rma-engine.md) — 同一问题的片上 RMA 引擎方案，对象是细粒度 scale-up 卸载

## 开放问题
- 域内小消息与 CUDA graph capture 的延迟仍高于 SM kernel；作者希望未来有 CE 原子等更好的 CUDA 支持。
- 跨域同步依赖 CPU proxy 线程；CE 数量也可能限制高扇出并发。
- 只改了 FSDP AllGather 与 PP 级间传输，未把 EP AlltoAll 接到端到端配方里。
- 相对 symmetric kernel 并非处处领先；host-bound 配方会把更高的 host 提交成本暴露到关键路径（GB200 上发一次 CE AllGather **26–41 µs**，symmetric **11–17 µs**；B200 为 **77–86 vs 5–7 µs**）。
- 文中 15T token 的美元估算按 CoreWeave 标价外推，作者写明不是完整部署成本模型。

# Citations
- [arXiv:2611.18075](https://arxiv.org/abs/2611.18075) — He, Shen, Wen, Singhania, Fan, Kwon, Lym, Rengasamy, Ramesh, Qiang, Belusar, Hammond, Hoefler；ETH Zurich / NVIDIA
- [artifact](https://github.com/spcl/zero-sm-artifact)
- [raw stub](/raw/papers/zero-sm-nccl.md)
