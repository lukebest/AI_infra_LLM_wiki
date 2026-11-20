---
type: Paper
title: "Obaleth: Compiling Specialized GPU-Initiated Networking"
description: "Koç / fal — 把 GPU-initiated 通信编进 kernel IR；256 卡 all-to-all 相对 NVSHMEM/NCCL GIN 为 1.25×/2.3×；vLLM 上 16×B200 服务 Qwen3-235B，请求延迟相对 DeepEP 最高 1.29×（TTFT p95 更高）"
tags:
- compiler
- gpu
- collective
- nvlink
- rdma
- moe
- expert-parallelism
- serving
- nvidia
- amd
- communication
- programming-model
created: 2026-11-19
updated: 2026-11-20
timestamp: '2026-11-19T00:00:00Z'
paper_author: [Javid Baydamirli, Ismayil Ismayilov, Kaan Oktay, Didem Unat]
year: 2026
venue: preprint
arxiv: '2611.18145'
sources:
  - raw/papers/Obaleth_GPU_Initiated_Networking_2026.pdf
  - raw/papers/obaleth-gpu-initiated-networking.md
---

# Obaleth：把 GPU 发起的通信编进 kernel 的中间表示

## 一句话结论
Koç University 与 fal 的 Obaleth 让 GPU-initiated 通信进入 kernel IR，和计算一起做完成规划、内存序、同步与批提交，再下降到具体传输代码。H100 上 8 B 消息速率最高为 NVSHMEM 的 **3.3×**、NCCL GIN 的 **4.2×**；256 卡 all-to-all（256 B/peer）相对二者为 **1.25×** 与 **2.3×**。接入 vLLM 后，16×B200、EP16 服务 Qwen3-235B-A22B，在 1/2/4 请求每秒下请求延迟相对 DeepEP 2.5.0 为 **1.29× / 1.28× / 1.15×**；TTFT 的 p95 更高（约 1.4–2.0×）。

## 动机
计算已经走进 Triton、CuTe、cuTile 这些按形状特化的编译器，通信仍多在 NVSHMEM、NCCL 这类通用库里，到最后才链进 kernel。库函数要服务任意调用方，排队槽要用原子预留，内存序和完成跟踪也偏保守。作者引用先前测量：一条最小 GPU 路径发出 8 B put 约 0.7 µs，库会再叠上最高 4.6 µs 的 issue 时间。

## 方案
Obaleth 把通信做成与后端无关的 Queue IR，规划完成点以匹配缓冲区寿命，并在 NVIDIA 与 AMD 上优化门铃范围、提交批量和序。对外提供 Tier-1（CUDA/DSL 可调用的库）和 Tier-2（Triton 等 DSL 里与计算共编译的核）。接入 vLLM 只需约 384 行适配器，用已有配置（token 上界、hidden size、top-k、专家放置等）引导编译出 dispatch/combine。

评测平台：H100 为每节点 4 卡、节点内 NVLink、跨节点 200 Gb/s IB；该平台门铃经主机线程转发。B200 为每节点 8 卡、400 Gb/s ConnectX-7，GPU 直接门铃，用于 vLLM。H100 上 NVSHMEM 用 3.4.5。计时多为 200 次预热后至少 1000 次迭代、五次交错运行的中位数。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 点对点往返（H100，两节点各 1 卡，8 B） | Tier-2 **9.98 µs**；NCCL GIN **12.74 µs**；NVSHMEM **13.12 µs** | §6.2 |
| 8 B 消息速率（各库取最佳 issue width） | 16 CTA 为 NVSHMEM 的 **2.8×**；64 CTA 达 **243 M msg/s**，为 NVSHMEM 的 **3.3×**、NCCL GIN 的 **4.2×**。4 KiB 时 4 个 CTA 到线速，NCCL GIN 需要 16 个 | §6.2 / Fig. 5 |
| All-to-all，256 B/peer | 8 卡：相对 NVSHMEM 封装集体 **1.32×**、相对 NCCL GIN **1.52×**。**256 卡**：相对二者 **1.25×** 与 **2.3×**。16 KiB/peer 总线带宽为 NCCL GIN 的 1.6×、NVSHMEM 的 1.2×。从 64 KiB 起受 NIC 限制，1 MiB 起各设备 API 相差在 4% 以内 | §6.2 / Fig. 5e |
| B200、GPU 门铃，256 B | 16 与 32 卡上相对 NCCL GIN **1.11–1.16×**、相对 NVSHMEM **1.24–1.52×**。作者写明，H100 上相对 NCCL GIN 的更大优势，部分来自对方经主机转发门铃 | §6.2 / Appendix Fig. 11 |
| 每 rank 资源 | 设备内存 **4–22 MiB**（8–256 卡），至少比两家库少 **12×**（NCCL 266–426 MiB，NVSHMEM 584 MiB，其中 512 MiB 为对称堆）。All-to-all 每线程寄存器 **60** vs 库的 128 | §6.2 / Fig. 5f–g |
| vLLM，Qwen3-235B-A22B BF16，16×B200 EP16，128 条 GSM8K / 速率 | 1/2/4 请求每秒，请求延迟加速 **1.29× / 1.28× / 1.15×**；TPOT 低 10–24%；TTFT p95 为 376/192、312/218、311/201 ms（更高）。正确条数接近。作者写明这些速率未让引擎饱和；两份 TP8 副本在长报告上的吞吐是 Obaleth 的 **2.4×** | Table 3 / §6.4 |
| 其他服务点 | 同节点四卡 FP8 Qwen3-30B-A3B 请求延迟 **1.21–1.48×** 更快（TTFT 同样更高）；长 GovReport（prefill 为主）**1.33×** | §6.4 |
| 单层 FP8 核 vs DeepEP | 1 token/rank：dispatch **1.7–2.2×**、combine **2.2–3.1×**；Qwen3-235B 从 64 token 起 DeepEP 最快可到 **1.7×**。Ling-1T EP16 三次 decode：NIC 发包少 **5.6×**，send/await GPU 时间少 **4.3×**。存储规划每 GPU 收回 16 GiB，KV 容量比关闭该遍高 45% | §6.4–6.5 / Fig. 7 |
| AMD MI355X（附录，初步） | 经主机代理，8 B 跨节点往返 28.3 vs rocSHMEM 36.6 µs；8 与 16 卡 all-to-all 相对 rocSHMEM / RCCL 为 **1.24–1.70×** 与 **2.2–2.5×** | §6.3 / Appendix C |

## 与已有页的增量
Wiki 已有 [Zero-SM NCCL](/papers/zero-sm-nccl.md)、[NVLinkOneSided](/papers/nvlinkonesided-ep-all-to-all.md)、[NCCL-EP Dispatch Offload](/papers/nccl-ep-moe-dispatch-offload-dbo.md) 等库内或一侧通信路径上的工作。本篇把特化从手写库函数移到编译器：通信进入 kernel IR，按本次调用的形状和缓冲区寿命生成队列与完成规划。vLLM 对照是同一构建里的 DeepEP 2.5.0；小消息、decode 步长上的优势更明显，更大 token 数时 DeepEP 的手写核可以反过来领先。

## 与 wiki 的关系
- [KIWI](/papers/kiwi-reverse-offload-gpu-initiated.md) — 在 MI300X 上把反向卸载做成可编程接口，作为另一条 GPU-initiated 通信路线
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把 all-to-all / dispatch-combine 从通用库特化到编译产物
- [NVLink / NVSwitch Scale-up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 节点内走 NVLink、跨节点走 RDMA 的混合 all-to-all
- [Zero-SM NCCL](/papers/zero-sm-nccl.md) — 同属降低通信占用 SM / 主机往返的路径，本篇走编译器特化
- [NVLinkOneSided](/papers/nvlinkonesided-ep-all-to-all.md) — 同样对标 DeepEP 的 EP all-to-all，实现层次不同

## 开放问题
- H100 集群的门铃经主机转发；B200 上相对 NCCL GIN 的优势收窄到 1.11–1.16×，跨平台数字要分开读。
- vLLM 数字来自未饱和的 1–4 请求每秒；TTFT p95 高于 DeepEP；作者也给出两份 TP8 副本在长报告上吞吐更高的部署对照。
- 从 64 token 起，DeepEP 手写核可以快于编译核（最高 1.7×），作者把差距归到核而不是传输。
- AMD / EFA 后端已有实现，完整评测仍留在附录与后续工作。

# Citations
- [arXiv:2611.18145](https://arxiv.org/abs/2611.18145) — Baydamirli, Ismayilov（共同一作）；Oktay, Unat（Koç University / fal）
- [raw stub](/raw/papers/obaleth-gpu-initiated-networking.md)
- [PDF](/raw/papers/Obaleth_GPU_Initiated_Networking_2026.pdf)
- [arXiv:2611.23848](https://arxiv.org/abs/2611.23848) — KIWI
