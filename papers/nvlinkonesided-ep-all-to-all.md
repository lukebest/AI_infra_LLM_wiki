---
type: Paper
title: "One-Sided Expert-Parallel All-to-All for Mixture-of-Experts Inference over NVLink"
description: "NVIDIA — NVLink 域一侧 EP all-to-all（Fence/Sentinel）；8×B300 上相对 DeepEP V2.5，dispatch/combine 1.75–3.00×（≤128 token）与 1.17–1.63×（≥256 token）；MoE 层相对 DeepEP+DeepGEMM 最高 2.4×；已接入 FlashInfer3 / vLLM / SGLang / TRT-LLM"
tags:
- moe
- expert-parallelism
- communication
- collective
- nvlink
- interconnect
- decode
- inference
- serving
- serving-system
- latency
- nvidia
- gpu
- quantization
created: 2026-11-13
updated: 2026-11-13
timestamp: '2026-11-13T00:00:00Z'
paper_author: [Bo Li, Chulian Zhang, Or Biri, Anthony Chang, Anton Korzh, Noam Duvdevani, XingFei Xi, Daniel Stokes, Zhenhuan Chen, Ludwig Schneider, Artem Y. Polyakov, Julien Demouth, Chandler Zhou]
year: 2026
venue: arXiv preprint
arxiv: '2611.13188'
sources:
  - raw/papers/NVLinkOneSided_EP_AllToAll_2026.pdf
  - raw/papers/nvlinkonesided-ep-all-to-all.md
---

# NVLink 域一侧专家并行 All-to-All

## 一句话结论
NVIDIA 的 **NVLinkOneSided** 在单一 NVLink 域内做专家并行的 dispatch/combine：源 rank 按本地路由把 token 直接写入对端的 rank-major 缓冲区，grouped GEMM 原地读取，并用 **Fence**（大批次）与 **Sentinel**（小批次）两套同步。八张 B300 上，相对 DeepEP V2.5，往返在不超过 128 token/rank 时快 **1.75–3.00×**，从 256 token 起快 **1.17–1.63×**（摘要写成 **1.2–3.0×**）。整层相对 DeepEP+DeepGEMM 最高 **2.4×**；在最多 128 token/rank 时也低于融合 MegaMoE（延迟最多低约 30%）。实现已进入 FlashInfer3，并接入 vLLM、SGLang 与 TensorRT-LLM。

## 动机
推理每步每卡 token 远少于训练。小批次下，dispatch/combine 的固定同步与中间拷贝占主导：理论上数个 token 的传输不到 1 µs，实测往返仍是数十微秒（§1 / §5）。常见路径（NCCL、DeepEP）先写入中间缓冲再由接收端整理成计算布局，既增加延迟也占用带宽。NVLink 对称内存允许内核直接对对端做 load/store。

## 方案
1. **一侧推送 + rank-major 布局**：源 rank 只凭本地路由把每个 token（及其 k 个专家 id 与路由权重）写入目标 rank 的槽位；同一目标 rank 的多个本地专家只传一次。计算侧按槽索引原地读，省掉 per-expert 拷贝。
2. **两种同步**：Sentinel 从数据到达本身检测完成，适合 decode 小批次；Fence 按 peer 发布/等待标志，适合大批次。交叉点约在 **256 token/rank**（Fig 5）。
3. **与计算解耦**：通信接口不绑激活量化格式，也不绑 MoE 计算后端；本评测搭配 Prims-TS grouped GEMM（MXFP4 权重、MXFP8 激活），并用 CUDA graph 与 PDL 衔接相邻 kernel。
4. **平台**（§5.1 / Table 3）：§5.2–5.3 为八张 NVLink 相连的 B300；§5.4 为一台 GB200 NVL72。模型为 DeepSeek-V4.1-Flash（384 专家、top-k=6）与 Kimi-K3（896 专家、top-k=16，latent MoE）。对照：DeepEP V2.5、融合 DeepGEMM MegaMoE、未融合 DeepEP+DeepGEMM（DE+DG）。默认完美路由，另用 Zipf 看偏斜（Table 5）。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| dispatch+combine vs DeepEP | 每个批次都更快；≤128 token/rank **1.75–3.00×**，从 256 起 **1.17–1.63×**；摘要 **1.2–3.0×** | §5.2 / Fig 5 / 摘要 |
| 1 token 往返（DeepSeek，8×B300） | Sentinel **17.4 µs**，Fence **27.6 µs**，DeepEP **47.9 µs** | §5.2 |
| 4096 token 带宽 | Fence 达到单向 NVLink 900 GB/s 的 **68–71%** | §5.2 |
| 低精度载荷（4096 token，Fence） | NVFP4 dispatch 相对 BF16 **3.0×**（字节比 3.5×）；MXFP8 **1.8×**（1.9×） | Fig 7 |
| MoE 层 vs DE+DG | 每个批次都更快，最高 **2.4×**；Kimi-K3 T=1：Sentinel **42.1 µs** vs DE+DG **99.7 µs**（2.37×） | Table 4 / §5.3 |
| MoE 层 vs MegaMoE | 最多 128 token/rank 时更快，延迟最多低约 **30%**（Kimi T=1：MegaMoE **60.4 µs**）；从 256 token 起 MegaMoE 更低，4096 token 时最多低 **35%**（DeepSeek 766.1 vs Fence 1185.2 µs） | Table 4 / §5.3 |
| Zipf α=1.25、T=1024，最忙 rank 通信 | DeepSeek dispatch/combine **160 / 135 µs**，对照 DE+DG **267 / 400 µs** | §5.3 / Table 5 |
| NVL72 扩展（DeepSeek T=1） | Sentinel 往返在 8–64 GPU 上维持 **16.6–17.8 µs**；Fence 从 43.0 升到 47.6 µs | Fig 8 / §5.4 |
| NVL72 层延迟（DeepSeek T=128） | 64 GPU 上 **102.6 µs**，8 GPU 上 **181.7 µs**（正文写 103 vs 182） | Table 6 |

作者把主要限制写在 §6：专家并行组需要落在同一个 NVLink 域，协议依赖对端内存的直接访问以及 32 位字整词到达。工作区按 rank 分区，占用随 EP 规模增长。

## 与 wiki 的关系
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 单一 NVLink 域内的直接 load/store 与 B300 / GB200 NVL72 评测
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP dispatch/combine 的一侧协议与 DeepEP V2.5 对照
- [NCCL-EP Dispatch Offload](/papers/nccl-ep-moe-dispatch-offload-dbo.md) — 同属 NVIDIA、面向 EP 通信；该文在 NCCL-EP+DBO 上提前释放 dispatch send，对照含 DeepEP v1
- [flash-comm](/papers/flash-comm-self-synchronizing-collectives.md) — 同属 GPU 域低延迟同步，对象是 TP all-reduce / all-gather
- [Relief](/papers/relief-per-step-ep-load-balancing.md) — 逐步专家负载拆分，与通信协议互补
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — decode 侧 EP 通信仍是解耦服务的常见组成

## 开放问题
- 跨 NVLink 域的 RDMA 路径尚未实现；一侧设计如何接到多域层次 all-to-all，仍待后续工作。
- 融合 MegaMoE 在大批次靠 kernel 内重叠取胜；作者计划把一侧推送与到达检测做进融合算子，以覆盖大批次重叠。
- 评测以完美路由为主，Zipf 只覆盖通信与层延迟，未报告端到端服务 SLO。

# Citations
- [arXiv:2611.13188](https://arxiv.org/abs/2611.13188) — Li et al.（NVIDIA）
- [raw stub](/raw/papers/nvlinkonesided-ep-all-to-all.md)
- [PDF](/raw/papers/NVLinkOneSided_EP_AllToAll_2026.pdf)
