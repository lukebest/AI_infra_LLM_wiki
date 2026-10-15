---
type: Paper
title: "API-Level Memory Models for Multi-GPU Device Communication (rocSHMEM)"
description: "AMD — 为 GPU 设备端单边通信 API（rocSHMEM/SHMEM，对照 MSCCL++、NCCL/RCCL GIN）定义形式化 API 级内存模型，并引入 com_id 定向排序：网络数据走 cache bypass，fence/wait 不再刷/失效缓存；MI300X 上 RS 最高 2.48×、GEMM+RS 1.77×、DeepEP 1.18×"
tags:
- gpu
- amd
- communication
- collective
- programming-model
- cache
- memory
- expert-parallelism
- moe
- rdma
- formal-analysis
created: 2026-10-15
updated: 2026-10-15
timestamp: '2026-10-15T00:00:00Z'
paper_author: [Johnathan Alsop, Bradford Beckmann, Brandon Potter, Jiakun Yan, Aurelien Bouteiller, Omri Mor, Tony Tye, Sameer Sahasrabuddhe]
year: 2026
arxiv: '2610.16190'
venue: arXiv preprint (cs.DC)
sources:
  - raw/papers/API_Level_Memory_Models_Multi_GPU_Communication_2026.pdf
  - raw/papers/api-level-memory-model-multi-gpu-communication.md
---

# GPU 设备端通信 API 的内存模型与定向排序

## 一句话结论
GPU 内核直接发起 put/get 的通信库（rocSHMEM、MSCCL++、NCCL/RCCL GIN）缺少严格定义的内存语义，用户和实现者只能保守地在 fence/wait 处做系统范围 acquire/release，在 GPU 上这意味着刷写和失效缓存。AMD 给 SHMEM 设备 API 写了一套形式化的 API 级内存模型，再在模型里加入「通信 ID（com_id）」：只对指定 com_id 的数据建立顺序，这些数据统一走 cache bypass 访问，于是同步操作只需等计数器、无需刷缓存。

## 动机
- 设备端单边通信在 MoE all-to-all、计算-通信融合里越来越常用；SHMEM 规范与 GIN 对 fence、quiet、signal、wait_until 和普通访存之间的顺序存在歧义（论文第 IV 节逐条列出）。
- GPU SHMEM 实现为了保证顺序，在 fence/wait_until 使用系统 scope 的 release/acquire，降成缓存 flush/invalidate，既加延迟又破坏与通信无关的数据的缓存复用。

## 方案
- **API 级内存模型**：建立在语言级（scoped）GPU 内存模型之上，定义 ilv、lco、rdo、rco、aso 等关系并汇成 hb_api；用 MP、SB、LB、IRIW、WRC、CoWW、ISA2 等经典 litmus 测试检验。
- **定向排序（targeted ordering）**：每个 SHMEM 操作、访存或内存分配可带 com_id；各排序关系按 com_id 分别定义。若某 com_id 的数据全部用 cache-bypassing 读写，对应 acquire/release 不再需要 flush/invalidate，只保留 waitcnt。作为可选扩展暴露，默认全局 com_id 保持原语义。
- 实现在 rocSHMEM 的 IPC 后端（节点内 xGMI）和 GDA 后端（GPUDirect Async，跨节点 InfiniBand）。

## 效果（8× MI300X 节点；DeepEP 另测双节点）
- Reduce-scatter（IPC）：最高 **2.48×**，小传输收益最大；大传输两者都在约 **220 GB/s/GPU** 饱和（约理论峰值 50%）。
- 融合 GEMM + reduce-scatter（IPC）：最高 **1.77×**，收益同时来自省掉 flush 延迟和保住 GEMM 的缓存复用；M 越大收益越大，N、K 越大越受 GEMM 自身限制。
- DeepEP（DeepSeek 7K 隐层，64–256 token/GPU）：多数 token 数下 **10–20%**，最高 **1.18×**（IPC 与 GDA 均是），token 少时收益最大。

## 与 wiki 的关系
- [Memory Consistency Model](/concepts/memory-consistency-model.md) — 把 CPU 侧一致性模型的方法搬到「GPU + 网络」的 API 层
- [Memory Fence and Barrier](/concepts/memory-fence-barrier.md) — fence 在 GPU 上的硬件成本是缓存 flush/invalidate，定向排序缩小其作用范围
- [GPU-Initiated Communication Dissected](/papers/gpu-initiated-communication-dissected.md) — 同为设备端发起通信，那篇拆解 IBGDA 的延迟与队列争用，本篇处理语义与缓存成本
- [T-CCL](/papers/t-ccl-tma-collective-communication.md) — 另一条减少集体通信 SM/缓存开销的路线（TMA 搬运）
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP all-to-all 与计算-通信融合的同步语义

## 局限与开放问题
- 只在 AMD MI300X 与 rocSHMEM 上实现；NVSHMEM、NCCL GIN 是否接受同类扩展需各自规范跟进。
- cache bypass 适合只用一次的网络数据；若接收端还要反复读，绕开缓存可能吃亏，论文未系统评估这种取舍。
- 大消息下 220 GB/s/GPU 约为峰值一半，瓶颈不在排序语义；收益集中在延迟主导区间。
- 论文提到 API 级模型可为未来数据搬运引擎、智能网卡等专用硬件提供契约，具体硬件设计尚未给出。

# Citations
- Alsop et al. (AMD), "A New Lens on Multi-GPU Communication: API-Level Memory Models for Portable Optimization", arXiv:2610.16190, 2026. [raw](/raw/papers/api-level-memory-model-multi-gpu-communication.md) · [PDF](/raw/papers/API_Level_Memory_Models_Multi_GPU_Communication_2026.pdf)
