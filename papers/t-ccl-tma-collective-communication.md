---
type: Paper
title: "T-CCL: Resource Efficient and Performant Collective Communication using Tensor Memory Accelerator"
description: "Chalmers — 节点内集体通信的搬运与规约都交给 Hopper TMA 异步流水；vs NCCL 最高 2.4×（受限 SM 预算 3.42×），占用 SM 同等或更少；vLLM 吞吐最高 1.31×"
tags:
- collective
- allreduce
- communication
- gpu
- nvidia
- kernel
- inference
- parallelism
created: 2026-10-08
updated: 2026-10-08
timestamp: '2026-10-08T00:00:00Z'
paper_author: [Keyvan Dadashzadeh, Yuehong Zhou, Minyu Cui, Miquel Pericàs]
year: 2026
arxiv: '2610.07098'
venue: SC'26 Workshops
sources:
  - raw/papers/T_CCL_TMA_Collective_Communication_2026.pdf
  - raw/papers/t-ccl-tma-collective-communication.md
---

# T-CCL：用 TMA 做节点内集体通信

## 一句话结论

NCCL 一类库靠大量 GPU 线程换带宽或延迟，通信时占掉 SM，挤压同时运行的 GEMM。T-CCL 把节点内 AllReduce / AllGather / ReduceScatter 的**数据搬运和规约都卸给 Hopper 的 TMA（张量内存加速器）**，每个集体操作变成一串流水化的异步 TMA 操作。结果是带宽不降、SM 占用更少，通信–计算重叠时 GEMM 能拿到更多 SM。

## 动机

- 通信与计算并发时，集体通信的 SM 足迹直接限制重叠收益。
- NCCL 2.27 起有对称内存 kernel（降低 SM 占用），但要求通信缓冲按对称方式分配；NCCL 开启 TMA 后也只用于数据搬运，规约仍由线程做，且逐个等待 TMA 完成。

## 方案

- TMA 同时承担 load/store 与规约，按 chunk 组成 fill / steady / drain 三段流水，以 chunk 级完成信号（TMA load 完成经 barrier 跟踪）串起依赖的规约；另做 fan-out 等优化。
- 以就地（in-place）操作为主；staging buffer = 深度 D × chunk C，需装进 SMEM（H100 每 CTA 最多 228 KB）。
- 离线按消息大小测 CTA 配置并排序，运行时取在 CTA 预算内的最优配置。
- 平台：2×H100 NVL（NV12 互连，TP=2）与 4×GH200 120 GB（两两 NV6，TP=4）；基线 NCCL 2.28 与对称内存 NCCL。

## 效果（仅论文数字）

| 场景 | 数字 |
|------|------|
| 不限 CTA，vs NCCL | 最高 **2.4×**（GH200 ReduceScatter 1.11–2.40×） |
| 受限预算（H100 8 CTA / GH200 9 CTA），vs NCCL | 最高 **3.42×**（H100 ReduceScatter 0.95–3.42×） |
| vs 对称内存 NCCL | 大体持平或略优（如 H100 AllGather 不限预算 1.06–1.23×） |
| 平均活跃 SM（GH200，128 MB AllGather） | T-CCL **6.60** vs NCCL **23.76** vs 对称 NCCL **9.24** |
| GEMM–集体重叠（FlashOverlap），vs 串行 | TP=2：NCCL **1.12×** → T-CCL **1.25×**（最高 1.51×）；TP=4：**1.04× → 1.14×**（最高 1.34×） |
| vLLM 后端，Qwen2.5-72B TP=4（GH200） | 端到端吞吐 vs vLLM 自动后端最高 **1.31×**，所有批大小都更好 |

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 通信–计算重叠的硬件资源账：SM 是被通信"偷走"的那份算力
- [Purlin](/papers/purlin-collectives-orchestration-datapath.md) — 同样把集体通信数据通路从 SM 线程里剥离，Purlin 偏编排/数据路径解耦，T-CCL 用现成 DMA 类硬件
- [Weave](/papers/weave-dynamic-sm-moe-overlap.md) — 在 megakernel 内动态分配通信 SM；T-CCL 直接把通信需要的 SM 压到最少
- [NVLink/NVSwitch Scale-up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 仅节点内 NVLink 点对点拓扑

## 局限与开放问题

- 只到 2–4 GPU、对称拓扑；未覆盖 8-GPU NVSwitch、跨节点。
- vLLM 实验关闭了 CUDA Graph（T-CCL 尚不支持），NCCL 同样吃到 host 启动开销，绝对数值偏离生产配置。
- 开放问题：Blackwell 的 TMA / 拷贝引擎与 NVLS（交换机内规约）同时可用时，"用哪块固定功能硬件做规约"会成为新的调度维度。

# Citations

[1] [arXiv:2610.07098](https://arxiv.org/abs/2610.07098) — Dadashzadeh et al., T-CCL
[2] [raw stub](raw/papers/t-ccl-tma-collective-communication.md)
