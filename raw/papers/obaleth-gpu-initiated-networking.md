---
type: Raw Source
title: "Compiling Specialized GPU-Initiated Networking (Obaleth)"
source_url: https://arxiv.org/abs/2611.18145
pdf: Obaleth_GPU_Initiated_Networking_2026.pdf
retrieved: 2026-11-19
ingested: 2026-11-19
org: Koç University / fal
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.18145)

Machine learning systems specialize computation to the workload and hardware, but communication remains in generic libraries whose device code and transport decisions are not visible to high-level compilers. We present Obaleth, a compiler that makes GPU-initiated communication part of a kernel's intermediate representation, co-optimizes it alongside computation, and lowers it to specialized transport code. Obaleth plans completions around buffer lifetimes and optimizes memory ordering, synchronization, and batching across NVIDIA and AMD GPUs. On H100 GPUs, Obaleth sends small messages up to 3.3× faster, and on 256 GPUs runs all-to-all 1.25× and 2.3× faster than NVSHMEM and NCCL GIN, with much smaller memory and register use. In vLLM, it serves Qwen3-235B on 16 B200 GPUs and answers requests up to 1.29× faster than with DeepEP.

# Excerpts / key facts

- Authors: Javid Baydamirli、Ismayil Ismayilov（共同一作）、Kaan Oktay、Didem Unat。单位：Koç University 与 fal。通讯：jbaydamirli21@ku.edu.tr，ismayil@fal.ai。arXiv:2611.18145，cs.DC，上轮已列为优先、本轮摄入。预印本。
- 平台（Appendix Table 6）：H100 为每节点 4 卡、节点内 NVLink、跨节点 200 Gb/s ConnectX InfiniBand；该平台 GPU 不能直接敲门铃，Obaleth 与库在 GPU 上建队列和 WQE，门铃经主机线程转发（CPU-assisted）。B200 为每节点 8 卡、400 Gb/s ConnectX-7，GPU 直接敲门铃（GPU-direct），用于 vLLM 并复核带 GPU 门铃的库对照。H100 上 NVSHMEM 用 3.4.5（作者称 3.8.0 每轮往返慢 2.1 µs）。EP 对照 DeepEP 2.5.0，默认配置，同一 vLLM 构建。计时：内核用 %globaltimer，主机 API 用 CUDA events；若无另行说明，每个点是至少 1000 次迭代、200 次预热后五次交错运行的中位数。
- 点对点（两节点各 1 卡 H100）：Tier-2 8 B 往返 **9.98 µs**，NCCL GIN **12.74 µs**，NVSHMEM **13.12 µs**，大约领先 3 µs。
- 小消息速率（每库取最佳 issue width）：Tier-2 在 16 个 CTA、各一条队列上，8 B 消息速率为 NVSHMEM 的 **2.8×**；64 CTA 达到 **243 M msg/s**，为 NVSHMEM 的 **3.3×**、NCCL GIN 的 **4.2×**。4 KiB 时 4 个 CTA 即可跑到线速，NCCL GIN 需要 16 个。
- All-to-all（每卡与节点内 3 个 NVLink 对等及其余 RDMA 对等交换）。256 B/peer：8 卡上相对 NVSHMEM 封装集体 **1.32×**、相对 NCCL GIN **1.52×**；**256 卡**上相对二者为 **1.25×** 与 **2.3×**。16 KiB/peer 时总线带宽为 NCCL GIN 的 1.6×、NVSHMEM 的 1.2×。从 64 KiB/peer 起受 NIC 限制，从 1 MiB 起各设备 API 彼此相差在 4% 以内。
- B200、GPU 门铃：256 B 时，16 与 32 卡上相对 NCCL GIN **1.11–1.16×**、相对 NVSHMEM **1.24–1.52×**。作者指出，H100 上相对 NCCL GIN 的更大优势，部分来自对方经主机转发门铃。
- 资源：8–256 卡上每 rank 设备内存 **4–22 MiB**，至少比两家库少 **12×**。NCCL 为 266–426 MiB，NVSHMEM 为 584 MiB（其中 512 MiB 为对称堆）。All-to-all RDMA 内核每线程寄存器 **60**，库内核为 128；ping-pong 为 62 vs 210–221。从 DSL 调用时每 rank 仍分配 4 MiB，对照 NVSHMEM4Py / Triton-distributed 的 2.1 / 1.6 GiB。
- 编译器遍（Tier-2）：1 条链上默认比关闭全部可开关遍快 **8.4×**，16 条链上 **23.9×**。8 卡 all-to-all 上可开关遍只再贡献 1.13–1.22×，主要优势来自始终开启的 lowering。
- AMD MI355X + Pollara RoCE（附录，作者称初步）：经主机代理时 8 B 跨节点往返 28.3 µs，对照 rocSHMEM 36.6 µs；8 与 16 卡 all-to-all 相对 rocSHMEM / RCCL 为 **1.24–1.70×** 与 **2.2–2.5×**。EFA 后端已实现，完整 AMD/EFA 评测留待后续。
- vLLM，Qwen3-235B-A22B BF16、16×B200、EP16，每速率 128 条 GSM8K 请求（Table 3，中位数；1/2/4 请求每秒）：请求延迟 5.66/7.31、6.50/8.29、8.10/9.29 s，加速 **1.29× / 1.28× / 1.15×**；TPOT 21.9/28.7、25.9/33.2、33.4/37.3 ms（低 10–24%）；TTFT 中位接近或略好，p95 为 376/192、312/218、311/201 ms（更高，约 1.4–2.0×）。正确条数 123/124、124/120、120/122。作者写明这些速率未让任一引擎饱和；两份 TP8 副本在长报告上的吞吐是 Obaleth 的 **2.4×**。
- 同节点四卡上 FP8 Qwen3-30B-A3B 请求延迟 **1.21–1.48×** 更快，TTFT 同样更高；长 GovReport 提示（prefill 为主）请求延迟 **1.33×** 更快。
- 内核对照：单 token/rank 时，从 vLLM 模式编译的 FP8 dispatch/combine 相对 DeepEP 手写核，dispatch **1.7–2.2×**、combine **2.2–3.1×**；Qwen3-235B 从 64 token 起 DeepEP 最快可到 **1.7×**。Ling-1T EP16 三次 decode 中，Obaleth 的 NIC 发包少 **5.6×**，send/await 核 GPU 时间少 **4.3×**。存储规划每 GPU 收回 16 GiB，KV 容量比关闭该遍高 45%，并在 DeepEP 的 5% 以内；按有效范围发送使字节数减少 58%。
