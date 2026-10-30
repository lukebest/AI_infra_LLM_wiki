---
type: Paper
title: "DualPace: Decoupled Scheduling and Cooperative GPU–CPU Decoding for LLM Serving"
description: "浙大宁波 — 把 host 做成独立调度的 AMX decode 引擎，与 GPU 引擎解耦协作；相对 NEO 吞吐 +6.9–43.2%、相对 vLLM +11.5–90.6%，同 P99 ITL 下请求率比 NEO +7.3–50.5%"
tags:
- inference
- decode
- serving-system
- kv-cache
- cpu
- gpu
- batching
- latency
- throughput
- llm
created: 2026-10-30
updated: 2026-10-30
timestamp: '2026-10-30T00:00:00Z'
paper_author: [Kingsum Chow, KeQiang Wu, YuXuan Lin]
year: 2026
venue: arXiv cs.DC
arxiv: '2610.33501'
sources:
  - raw/papers/DualPace_Decoupled_GPU_CPU_Decoding_2026.pdf
  - raw/papers/dualpace-decoupled-gpu-cpu-decoding.md
---

# DualPace：解耦调度的 GPU–CPU 协作 decode 服务

## 一句话结论
CPU KV 卸载若仍由 GPU 调度门控，host 侧进度会成脉冲、抬高 P99 ITL。DualPace 把 **GPU 引擎**（prefill + GPU-resident decode）与 **AMX CPU 引擎**（独立批处理 CPU-resident decode）拆成两套调度权威，执行上可本地跑完整 decode 或按离线画像调用 GPU Dense Assist；decode 场景吞吐相对 NEO **+6.9–43.2%**、相对 vLLM **+11.5–90.6%**，同级 P99 ITL 下请求率比 NEO **+7.3–50.5%**。

## 动机
- Batching 抬吞吐，但 KV 随序列增长限制 GPU 常驻并发；CPU offload 扩容量后，既有系统（以 NEO 为代表）仍是 **GPU-gated**：CPU-resident 请求只有在 GPU 暴露合适重叠窗口时才推进。
- 结果：host 内存与 AMX 算力无法成为独立 serving 资源，CPU 侧进度 bursty，负载下 **尾部 ITL** 膨胀。

## 方案
1. **双引擎调度权威**：GPU 引擎负责 prefill 与 GPU-resident decode；AMX CPU 引擎独立组 batch、推进 CPU-resident decode（host PagedAttention + AMX BF16 dense）。
2. **协作而非门控**：CPU 可本地完成一整次 decode；dense 阶段可选 **GPU Dense Assist**；离线 profile 给出硬件相关的 batching / 路由阈值。
3. **评测平台**：Llama-3.1-8B @ RTX 4090 + 12 核 Xeon Silver 4510；Qwen3-14B @ 2×H20 + 24 核 8469C；Qwen3-32B @ 4×H20 + 48 核；Azure-Conv / Azure-Code。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 吞吐 vs NEO | **+6.9–43.2%** |
| 吞吐 vs vLLM | **+11.5–90.6%** |
| 同级 P99 ITL 下请求率 vs NEO | **+7.3–50.5%** |
| TTFT | 保留 NEO 相对 vLLM 的 P99 TTFT 优势 |

## 与 wiki 的关系
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 把 CPU–GPU 轴从权重卸载 / 专家执行推进到 **独立 decode 调度引擎**
- [HiNa-MoE](/papers/hina-moe-cpu-amx-moe-inference.md) — AMX 侧算子引擎；DualPace 补的是 serving 调度解耦
- [HAWK](/papers/hawk-gpu-npu-heterogeneous-kv-transfer.md) — 异构 KV 传输；DualPace 聚焦同机 host 引擎独立性
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — host 侧 PagedAttention 作为 CPU 引擎执行路径
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 调度权威分离与 PD 解耦正交，同属「资源角色拆分」

## 开放问题
- Dense Assist 与多卡 TP/EP 的叠加未展开；Qwen 路径对上游 NEO 做了兼容补丁，跨栈可移植性待验证。
- 超长上下文下 host 带宽与 AMX 饱和后的扩展上界未系统报告。

# Citations
- [arXiv:2610.33501](https://arxiv.org/abs/2610.33501) — Chow, Wu, Lin, 2026
- [raw stub](/raw/papers/dualpace-decoupled-gpu-cpu-decoding.md)
