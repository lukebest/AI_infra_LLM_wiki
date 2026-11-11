---
type: Raw Source
title: "Release Sooner, Expose Less: Offloading MoE Dispatch in NCCL-EP under Dual-Batch Overlap"
source_url: https://arxiv.org/abs/2611.12362
pdf: NCCL_EP_Offload_MoE_Dispatch_DBO_2026.pdf
retrieved: 2026-11-11
ingested: 2026-11-11
org: NVIDIA
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.12362)

Dual-batch overlap (DBO) hides mixture-of-experts (MoE) communication behind another microbatch’s computation, but only after dispatch send releases the GPU. The time dispatch send holds the GPU therefore stays exposed, while network progress after release can be hidden. We evaluate three research configurations built on NCCL-EP that target this exposed communication time: GPI, in which the GPU constructs GPU-Friendly Descriptors (GFDs) and submits them to NIC-accessible memory for transport; GPI-MC, which describes MoE token fan-out in one GFD; and GDAKI Free Flow, which moves send progression to a host thread. On a GB300 NVL72 system, all three approaches reduce dispatch-send time relative to default GDAKI over most operating points in the evaluated parameter sweep. An experiment that inserts a GPU delay between dispatch send and receive shows that offload increases the in-flight interval. Depending on the configuration, 32–512 µs of computation or other independent work between send and receive hides the deferred progress, leaving less exposed time than default GDAKI. In disaggregated vLLM serving with DBO, these approaches lower median TPOT by 15–25% relative to NCCL-EP default GDAKI and by 16–42% relative to DeepEP v1.

# Excerpts / key facts

- Authors: Hsin-Chun Yin, Khaled Hamidouche, Ian Ziemba, Arjun Kashyap, Pak Markthub, Subhadeep Bhattacharya, Ke Wen, Assaf Ravid, Manjunath Gorentla Venkata, Gil Bloch (NVIDIA). arXiv:2611.12362, 2026-11-09/10, cs.DC. © 2026 NVIDIA.
- 平台（Table I）：GB300-CX8 NVL72，aarch64，CUDA 13.0；vLLM 0.30.1rc0-based fork，one-stream DBO；DeepEP 基线为 v1.2.1-based LL research fork（作者说明上游已用统一 V2 替换 V1 API）。模型：Qwen3-30B-A3B BF16。服务：16 GPU 分配，2P2D（两个 4-GPU prefill 节点 + 两个 4-GPU decode 节点）。
- 机制：DBO 里 dispatch send 释放 GPU 之前的时间一直暴露；释放之后的网络进度可以被另一微批计算盖住。提前释放即使网络完成不变或更慢，只要有足够覆盖工作，暴露通信仍可下降。
- 三条配置：GPI（GPU 构造 GFD 交给 NIC 可达内存后返回）；GPI-MC（一次 GFD 描述 token 多目的地扇出）；GDAKI Free Flow（WQE 仍在 GPU 构造，发送推进改到 host 线程）。对照为 NCCL-EP 默认 GDAKI（GPU 侧完成 WQE、门铃与推进）。
- 微基准：多数工作点上三条路径都缩短 dispatch-send；在 send 与 receive 之间插入 GPU delay 显示 offload 拉长 in-flight interval；按配置，**32–512 µs** 的间隔工作即可盖住推迟的进度，暴露时间低于默认 GDAKI。
- E2E（Fig 7）：可靠 DBO 区为 client concurrency **128–1000**。该区内三条优化路径相对 NCCL-EP 默认 GDAKI 中位 TPOT **−15–25%**，相对 DeepEP v1 **−16–42%**。每个点是三次 run 中位的均值。concurrency 1 是稳定的非 DBO 对照；32/64 因跨 rank 的预定 decode batch 变化，作者不把它当作传输证据。Fig 9：固定 concurrency 256、输入 128，输出长度 128–2048 时，中位 TPOT 优势保持。
- 准确性：GSM8K 验证中，正确配置与 DeepEP 相比，949 条参考 prompt 输出差异 **0.11–0.84%**。
- 限定：dispatch-send 微基准与 E2E serving 是分开实验，相关与机制一致，单独不能证明 dispatch-send 时长是 TPOT 变化的孤立原因。服务实验替换的是完整 backend。
