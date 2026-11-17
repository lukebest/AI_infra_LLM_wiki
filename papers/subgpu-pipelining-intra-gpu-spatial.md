---
type: Paper
title: "SubGPU Pipelining: Intra-GPU Fine-Grained Spatial Parallelism for LLM Inference"
description: "NVIDIA — 仿真 Pareto 匹配每 GPU 吞吐时 per-user 最高 2.2×、匹配 per-user 时每 GPU 最高 1.9×；硅上单卡 B200 模拟 32 卡 rank，36 层迭代 14.970→13.424 ms（−10.33%），DRAM 71.8%→83.6%"
tags:
- gpu
- nvidia
- inference
- decode
- pipeline
- green-context
- throughput
- latency
- serving
- moe
- expert-parallelism
- llm
- kernel
- memory-bandwidth
- hbm
created: 2026-11-17
updated: 2026-11-17
timestamp: '2026-11-17T00:00:00Z'
paper_author: [Muralidhar Andoorveedu, Marius Juston, Tingkai Liu, Sanjay Patel]
year: 2026
venue: arXiv preprint
arxiv: '2611.14904'
sources:
  - raw/papers/SubGPU_Pipelining_LLM_Inference_2026.pdf
  - raw/papers/subgpu-pipelining-intra-gpu-spatial.md
---

# SubGPU Pipelining：在一张 GPU 里做细粒度空间流水

## 一句话结论
NVIDIA 提出 **SubGPU Pipelining**：把 LLM decode 的算子图切成连续段，绑定到互不相交的 SM 池，再让 microbatch 在 GPU 内做细粒度空间流水。评估对象是 GPT-OSS 120B、32-GPU B200 设定（注意力 TP8/DP4、MoE EP32）。分析仿真给出的 Pareto 前沿上，匹配每 GPU 吞吐时 per-user 吞吐最高 **2.2×**，匹配 per-user 吞吐时每 GPU 吞吐最高 **1.9×**；作者写明该曲线不用于预测实测。硅上用 **一块 B200** 模拟 32 卡中的单 rank，在全局 batch **2,048** 的 Macro 两级配置上，相对同一 TensorRT-LLM 内核、148 SM 全池 Temporal 基线：36 层 decoder 迭代从 **14.970 ms** 降到 **13.424 ms**（**−10.33%**），平均 DRAM 读写吞吐从峰值的 **71.8%** 升到 **83.6%**。

## 动机
Decode 一层内会连续启动数十个短 kernel。在 B200 一类 GPU 上，小 batch decode kernel 只需微秒级，启动开销、空闲计算周期和浪费的 HBM 带宽变得显著。跨 GPU 的 TP / DP / EP / PP 解决不了卡内三类病理：启动延迟占步时比例偏高；访存受限算子在用尽全部 SM 之前就顶满 HBM 带宽；不同瓶颈的 kernel 交替造成带宽突发与低谷。

## 方案
1. **切图与空间级**：把算子图切成 \(K\) 个有序连续段，绑定到 \(D\) 个 stage（各有互不相交的 SM 池）；\(K=D\) 或 \(K=D+1\)（首尾段可共享同一 stage）。再把每 GPU batch 分成 \(m\) 个 microbatch 流动。
2. **搜索**：解析共享资源仿真器在有限网格上找最好配置。作用在外层并行已经分给单 GPU 的工作之上。
3. **Macro 两级**：因层在滑动窗口注意力与全注意力之间交替，探索以两层为宏周期的切分；一级只跑全注意力 FMHA，另一级跑宏周期内全部其余算子。
4. **硅上原型**：CUDA Green Contexts 做 stage 与 SM 分区；计算 kernel 为 TensorRT-LLM **1.3.0rc22.post1**。因实测与仿真 SOL 有差，每级 SM 分配在硬件上重调。通信为虚拟 kernel（下限 3 µs + payload / 900 GB/s）。

## 效果（论文数字）

**仿真 Pareto（§5.2.2；GPT-OSS 120B decode，32×B200，输入与 KV history 均为 32,768）**

| 比较方式 | 相对 Temporal | 条件 |
|---|---|---|
| 匹配每 GPU 吞吐时的 per-user 吞吐 | 最高 **2.2×** | 5,000 tokens/s/GPU 以上为 1.8–2.2× |
| 匹配 per-user 吞吐时的每 GPU 吞吐 | 最高 **1.9×** | 延迟导向端；100–600 tokens/s/user 为 1.1–1.4× |
| 同 batch 2,048 的最好两级 | makespan 降 **6.6%** | 仿真 |

**硅上（§5.3；一块 B200 模拟单 rank；Macro 两级：FMHA 68 SM + 其余 80 SM，两个等分 microbatch；Temporal 用全部 148 SM）**

| 指标 | Temporal | SubGPU | 相对变化 |
|---|---:|---:|---:|
| 36 层 decoder 迭代 | **14.970 ms** | **13.424 ms** | **−10.33%** |
| 平均 DRAM 读写（峰值百分比） | **71.8%** | **83.6%** | 升高 |
| 平均活跃 SM 吞吐 | **85.9%** | **71.7%** | 单 kernel 用更少 SM，重叠缩短端到端 |

测量协议：20 次 warmup 后，三轮、每轮 100 次无插桩 CUDA Graph replay。作者把硬件结果视为可行性证明；仿真对单 kernel 偏乐观（例如允许接近峰值 DRAM 带宽的 99%），是 6.6% 与 10.33% 差的部分原因。

## 与 wiki 的关系
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 把互不相交的 SM 池当成卡内空间级
- [GC-MoE](/papers/gc-moe-green-context-expert-parallel.md) — 同样用 CUDA Green Contexts 做分区，对象是 EP dispatch 与 grouped GEMM 重叠
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 针对 decode 短 kernel 的带宽突发与计算闲置
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 用空间重叠把平均 DRAM 利用率从 71.8% 抬到 83.6%
- [MegaMoE Kernel](/concepts/megamoe-kernel.md) — 单 kernel 融合路线；SubGPU 走多段空间流水

## 开放问题
- 硅上用一块 B200 模拟 32 卡中的单 rank，通信为虚拟 kernel；只详细报告一个调过的 Macro 两级配置。
- 仿真用于搜索机会，作者写明不用于预测实测；外推到端到端部署前需要敏感性分析与实测 kernel 校准。
- batch 太小或大块计算受限 kernel 已经高效用满 GPU 时，重叠机会变小；microbatch 若不能把并发段工作集留在 L2，重复 HBM 流量可能抵消空间重叠。prefetch、动态重配置与 persistent kernel 列为后续工作。

# Citations
- [arXiv:2611.14904](https://arxiv.org/abs/2611.14904) — Andoorveedu, Juston, Liu, Patel；NVIDIA
- [raw stub](/raw/papers/subgpu-pipelining-intra-gpu-spatial.md)
