---
type: Paper
title: "KIWI: A Fast, Programmable GPU-to-CPU Invocation Layer for GPU-Initiated Communication"
description: "AMD — MI300X + RoCE 实测；反向卸载队列 RTT 中位 1.92 µs；EP 通信延迟相对最好已有后端最高 2.3×，vLLM 上 GLM-5.3 的 TPOT 最高降低 29%"
tags:
- gpu
- amd
- communication
- moe
- expert-parallelism
- serving
- interconnect
- rdma
- collective
- programming-model
- latency
- disaggregated-inference
created: 2026-11-20
updated: 2026-11-20
timestamp: '2026-11-20T00:00:00Z'
paper_author: [Jiakun Yan, Shiksha Patel, David Sidler, Gengyu Rao, Brandon Potter, Bradford Beckmann]
year: 2026
venue: preprint
arxiv: '2611.23848'
sources:
  - raw/papers/KIWI_Reverse_Offload_GPU_Initiated_2026.pdf
  - raw/papers/kiwi-reverse-offload-gpu-initiated.md
---

# KIWI：把 GPU 发起的通信做成可编程的反向卸载

## 一句话结论
AMD 的 KIWI 把 GPUDirect Async（GDA，由 GPU 线程直接驱动网卡控制路径）里常被当作退路的反向卸载做成一等编程接口：GPU 内核用一次 wave 宽度的存储把请求交给主机回调，代理线程再去发 RDMA。在 MI300X + 400 Gb/s RoCE 集群上，队列本身的 GPU–CPU–GPU 往返中位为 **1.92 µs**，与 raw store 下限相同；KIWI-EP 的 dispatch+combine 延迟相对 AMD GPU 上最好的已有后端最高低 **2.3×**，接入 vLLM 服务 GLM-5.3 时，decode 侧 TPOT 最高降低 **29%**（八节点）。

## 动机
融合核、持久核和 MoE 通信需要比主机发起的 NCCL 式 collective 更灵活的设备发起通信。业界后来偏向 GDA，把主机代理视为更慢的退路。作者认为：网卡控制路径是一串标量依赖步骤（选协议、入队描述符、响门铃），GPU 线程做这些步骤要走分支、全局访存和 system-scope fence；GPU 并行度又远高于网卡端点数，GDA 为减争用会分配大量 QP，线程之间仍要同步。反向卸载把控制路径放到擅长串行控制的 CPU，并把 GPU 并发与传输并发解开。

## 方案
KIWI 的核心是注册任意主机函数为回调，并从 GPU 内核异步调用。队列是单生产者–单消费者（SPSC）：一次 wave 宽度的 PCIe 存储发布请求，不用原子操作或 fence，空队列轮询在主机上通常命中 L1。KIWI-P2P 用不到 1,000 行 C++ 把 KIWI 接到主机侧的 Lightweight Communication Interface（LCI），提供 SHMEM 式原语。KIWI-EP 进一步把 MoE 协议里的组播 put、计数 all-to-all 和 barrier 做成工作负载自定义回调，GPU 核主要负责打包、提交和拆包。代码在 https://github.com/AMDResearch/kiwi。

评测全部在每节点八张 MI300X、八张 400 Gb/s ConnectX-7、两路 56 核 Xeon Platinum 8480+ 的 RoCE 集群上进行；每张 GPU 与一张 NIC 共享 PCIe 交换机，GPUDirect RDMA 不经过 CPU 根复合体。每个数据点至少三次运行的中位数。NVSHMEM 与 rocSHMEM 的反向卸载队列在 AMD 上不可用或为库内部实现，作者按上游源码重实现其发布协议；其余队列跑未改动的上游设备代码。RCCL GIN 的代理队列是 NCCL GIN 的移植，并打开更快的 GDRCopy 路径。EP 工作负载使用 DeepSeek-V3 的 MoE 尺寸（hidden 7168、256 experts、top-8），BF16 的 dispatch 与 combine，报告最慢 rank 上一对 dispatch+combine 的延迟。vLLM 实验服务 GLM-5.3（FP8、prefill–decode 解耦），N 个 prefill 节点加 N 个 decode 节点、每节点八路数据并行与专家并行，请求为 8K 输入 / 1K 输出；prefill 始终用 vLLM 在 AMD 上推荐的 MORI-EP，decode 在 MORI-EP 与 KIWI-EP 之间切换。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| GPU→CPU 队列（单卡 MI300X） | KIWI 往返中位 / p99 为 **1.92 / 1.98 µs**，与 raw store 下限 1.92 / 1.96 µs 相同；最快的已有队列为 2.68–2.80 µs。1,024 个 wave 时 push 仍为 **0.12 µs**；256 个 wave 时自有队列吞吐 **392.0 Mops/s**，为最好已有队列的 **3.3×**。空队列轮询 **0.87 ns** | Table III / §VI-B |
| 可编程回调开销 | 中位往返与单 wave push 不变；1,024 wave 时 push 为 0.16 µs；256 wave 时吞吐降到裸队列的 62%。FlyDSL / Triton 内核往返与 HIP C++ 相差在 2% 以内，单端点吞吐为其 78–96% | §VI-B |
| 点对点（相对 MORI / rocSHMEM 的 GDA） | 小 put **5.64 µs**，延迟为二者的 **1/1.8** 与 **1/3.4**；八个 workgroup 时 KIWI-P2P 在 8 KiB 接近打满链路，另外两者要到 64 KiB。八个代理线程从 8 KiB 起把 400 Gb/s 网卡推近载荷上限 | Fig. 5–6 / §VI-C |
| 与 flag+LCI 对照（8 字节单 put） | KIWI-P2P 延迟 5.23 µs、吞吐 2.88 Mops/s；flag+LCI 为 5.25 µs / 2.97 Mops/s（吞吐少约 3%） | Table I |
| EP 微基准（2–8 节点） | 相对最好已有后端（ROCm DeepEP / MORI-EP / UCCL-EP），延迟最高低 **2.3×**。两节点上优势保持到每 GPU 16 token，四节点到 32 token，八节点在全部 token 数上都最低。大 token 数时 RDMA 带宽成为瓶颈：KIWI-EP 按目的 GPU 各发一次，MORI 按目的节点发一次再在节点内转发 | Fig. 7 / §VI-D |
| 相对自研 GDA 变体的消融（八节点） | 每 GPU 1 / 8 / 64 token 时分别快 **1.77× / 1.29× / 1.08×**。1 token 时仅换成反向卸载的 Proxy-MPSC 已低 27%，每 wave 的 SPSC 再低 14%；64 token 时若只用轮转分配，两个 proxy 变体比 GDA 高 28% 与 29%，自定义回调与偏斜轮转再把差距拉回来 | Fig. 9 / §VI-D |
| vLLM TPOT（GLM-5.3，FP8，PD 解耦） | 在所测规模与并发上相对 MORI 均更低，八节点上最高 **−29%**。GSM8K 与针检索精度测试中 KIWI-EP 不影响精度 | Fig. 8 / §VI-D |

## 与已有页的增量
[Obaleth](/papers/obaleth-gpu-initiated-networking.md) 把 GPU-initiated 通信编进 kernel IR，主要数字在 NVIDIA H100 / B200 上，并与 NVSHMEM、NCCL GIN、DeepEP 对照。[GPU-Initiated Communication: Dissected](/papers/gpu-initiated-communication-dissected.md) 则拆过 IBGDA 与 CPU proxy 的开销。本篇把反向卸载做成可编程接口，并在 AMD MI300X + RoCE 上给出相对 GDA 的延迟、带宽和 vLLM TPOT。两端的平台与基线都不同，倍数不宜直接横比。

## 与 wiki 的关系
- [Obaleth](/papers/obaleth-gpu-initiated-networking.md) — 同属 GPU-initiated 通信与 MoE EP 后端，实现层次与评测平台不同
- [GPU-Initiated Communication: Dissected](/papers/gpu-initiated-communication-dissected.md) — 先前对 GDA 与 proxy 路径的解剖
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — dispatch / combine 与设备发起通信
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — vLLM 实验采用 PD 解耦，prefill 固定为 MORI-EP

## 开放问题
- 全部主数字来自 AMD MI300X + RoCE；NVSHMEM / rocSHMEM 队列为按上游协议的重实现。
- 大 batch 时 KIWI-EP 尚未做按节点的层次化 token 转发，RDMA 带宽会先成为瓶颈。
- vLLM 里由于 PD 解耦与连续批处理，decode 瞬时并发低于配置并发，TPOT 收益不能按 kernel 倍数直接换算。
- KIWI-EP 部署为每 GPU 四个可抢占的普通操作系统线程做代理；作者在实验中未观察到抢占伤害，也指出操作系统若提供专用调度会更可预测。

# Citations
- [arXiv:2611.23848](https://arxiv.org/abs/2611.23848) — Yan, Patel, Sidler, Rao, Potter, Beckmann（Advanced Micro Devices, Inc.）
- [raw stub](/raw/papers/kiwi-reverse-offload-gpu-initiated.md)
- [PDF](/raw/papers/KIWI_Reverse_Offload_GPU_Initiated_2026.pdf)
