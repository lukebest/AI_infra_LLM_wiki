---
type: Paper
title: "Release Sooner, Expose Less: Offloading MoE Dispatch in NCCL-EP under Dual-Batch Overlap"
description: "NVIDIA — 在 NCCL-EP + DBO 下提前释放 dispatch send；GB300 NVL72 上 GPI / GPI-MC / GDAKI Free Flow 相对默认 GDAKI 中位 TPOT −15–25%，相对 DeepEP v1 −16–42%；32–512 µs 间隔工作可盖住推迟的网络进度"
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
- rdma
created: 2026-11-11
updated: 2026-11-11
timestamp: '2026-11-11T00:00:00Z'
paper_author: [Hsin-Chun Yin, Khaled Hamidouche, Ian Ziemba, Arjun Kashyap, Pak Markthub, Subhadeep Bhattacharya, Ke Wen, Assaf Ravid, Manjunath Gorentla Venkata, Gil Bloch]
year: 2026
venue: arXiv preprint
arxiv: '2611.12362'
sources:
  - raw/papers/NCCL_EP_Offload_MoE_Dispatch_DBO_2026.pdf
  - raw/papers/nccl-ep-moe-dispatch-offload-dbo.md
---

# 提前释放 Dispatch：NCCL-EP 在双微批重叠里少暴露通信

## 一句话结论
NVIDIA 在 **NCCL-EP** 上评估三条研究配置，目标是缩短 dual-batch overlap（DBO）里 **dispatch send 占住 GPU** 的时间：GPI 由 GPU 提交 GFD 后把传输交给 NIC；GPI-MC 用一条 GFD 描述 token 多目的地扇出；GDAKI Free Flow 把发送推进挪到 host 线程。**GB300 NVL72** 上，多数微基准工作点的 dispatch-send 变短；按配置，发送与接收之间 **32–512 µs** 的独立工作即可盖住推迟的网络进度。解耦 vLLM + DBO 服务（Qwen3-30B-A3B，2P2D）在可靠 DBO 区（concurrency 128–1000）里，三条路径相对 NCCL-EP 默认 GDAKI 的中位 TPOT **−15–25%**，相对 DeepEP v1 **−16–42%**。

## 动机
DBO 把一微批的 MoE 通信叠在另一微批的计算后面，但叠得上的前提是 dispatch send 已经释放 GPU。默认 GDAKI 路径在 GPU 上完成 WQE 构造、发布、门铃、额度等待与排序，这段时间一直暴露；释放之后的网络进度才可以被盖住。优化目标是更早释放 GPU，而不是要求网络更早完成。

## 方案
1. **GPI**：GPU 构造 GPU-Friendly Descriptor（GFD），写入 NIC 可达内存后返回，由 NIC 执行传输。
2. **GPI-MC**：MoE dispatch 里一个 token 常对应多个目的地；把扇出写成一条 GFD，减少 GPU 提交次数。
3. **GDAKI Free Flow**：WQE 仍在 GPU 构造，发送推进与门铃改由 host 线程完成。
4. 对照为 NCCL-EP 默认 GDAKI。平台：GB300-CX8 NVL72、CUDA 13.0、vLLM 0.30.1rc0-based fork（one-stream DBO）。DeepEP 基线是 v1.2.1-based LL 研究叉（作者注明上游已切到统一 V2 接口）。服务形态：16 GPU，两个 4-GPU prefill 节点 + 两个 4-GPU decode 节点。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| dispatch-send 微基准 | 多数工作点上三条路径都短于默认 GDAKI | 摘要 / 参数扫描 |
| 覆盖推迟进度所需间隔 | 按配置 **32–512 µs** 的计算或其他独立工作；覆盖后暴露时间低于默认 GDAKI | 插入 GPU delay 实验 |
| 可靠 DBO 区中位 TPOT | concurrency 128–1000，相对 NCCL-EP 默认 GDAKI **−15–25%**，相对 DeepEP v1 **−16–42%** | Fig 7 |
| 输出长度扫描 | 固定 concurrency 256、输入 128，输出 128–2048，中位 TPOT 优势保持 | Fig 9 |
| 任务一致性 | GSM8K 验证中，949 条参考 prompt 与 DeepEP 输出差异 **0.11–0.84%** | Fig 8 |

作者写明：微基准与端到端服务是分开实验，相关与机制一致，单独不能证明 dispatch-send 时长是 TPOT 变化的孤立原因；服务实验替换的是完整 backend。concurrency 32/64 因跨 rank 的预定 batch 变化，文中不作为传输证据。

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP dispatch/combine 在 DBO 下的提交边界
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — GB300 NVL72 上的 GPU 发起网络
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 2P2D 解耦服务里的 decode 侧 EP 通信
- [flash-comm](/papers/flash-comm-self-synchronizing-collectives.md) — 同属 GPU 域通信，面向 TP all-reduce 的自同步
- [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — ping-pong / 异池 MoE 重叠对照
- [INC-MoE](/papers/inc-moe-innetwork-collectives-moe-inference.md) — 把 EP 集体卸到网络侧的对照

## 开放问题
- DeepEP 对照停留在 V1 LL；与当前 DeepEP V2 的差距未测。
- 生产可能使用更大模型、20+ 节点的 decode 组与更高并发，dispatch 占 TPOT 的份额会变。
- 微基准与 E2E 未做因果分离，解释机制时需要保留作者自己的限定。

# Citations
- [arXiv:2611.12362](https://arxiv.org/abs/2611.12362) — Yin et al.（NVIDIA）
- [raw stub](/raw/papers/nccl-ep-moe-dispatch-offload-dbo.md)
- [PDF](/raw/papers/NCCL_EP_Offload_MoE_Dispatch_DBO_2026.pdf)
