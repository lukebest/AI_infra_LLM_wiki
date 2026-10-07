---
type: Paper
title: "Beyond LLM Serving: Characterizing Vision-Language-Action Workloads for Embodied AI System Design"
description: "KAIST（ASPLOS'27）— batch-1 闭环 VLA 推理刻画：动作张量维度决定访存/计算受限；Orin 降频省能 24–32%、Thor 仅 1–4%；推理与动作执行重叠带来精度–速度–能耗三向权衡（−56 pp / 3.9× / 5.1×），无 Pareto 最优配置"
tags:
- inference
- latency
- benchmark
- hardware
- gpu
- memory-bandwidth
- power
- agentic-ai
- architecture
created: 2026-10-07
updated: 2026-10-07
timestamp: '2026-10-07T00:00:00Z'
paper_author: [Seonghun Jung, Sieun Moon, Jiyoung Jeong, Jimin Lee, Jaehyuk Huh]
year: 2026
arxiv: '2610.05062'
venue: "ASPLOS '27"
sources:
  - raw/papers/VLA_Workload_Characterization_Embodied_AI_2026.pdf
  - raw/papers/vla-workload-characterization-embodied-ai.md
---

# VLA 负载刻画：具身 AI 不是 LLM serving 的翻版

## 一句话结论

机器人用的视觉-语言-动作（VLA）模型每个控制周期都有硬截止，单机器人只能 **batch-1** 在端侧/近端推理，落在 LLM serving 的设计点之外。KAIST 用 4 个模型 × 3 个平台 + 43,200 个闭环 episode 刻画：**动作张量维度** 决定一个阶段是访存还是计算受限；平台的算力/带宽配比会挪动瓶颈；GPU 调频的能耗甜点因平台而异；推理与动作执行重叠带来 **精度–速度–能耗** 三向权衡，没有一个配置在所有 SLO 下 Pareto 最优。

## 动机

- LLM serving 工具箱（continuous batching、paged KV、PD 分离）假设并发自回归请求；VLA batch-1 无并发，动作块模型非自回归，主导阶段随架构而非自回归阶段变化，现成优化只能 **选择性** 适用。
- 自回归 OpenVLA（RTX 4090，eager）：6 次 cached decode **140.90 ms**，是 LLM prefill（43.50 ms）的 3.2×，占 E2E **209.56 ms** 的 67%；decode 100% 访存受限，KV 每个动作只增长 D−1 位就丢弃，难以复用。OpenVLA-OFT 一次出整个 K 步动作块，LIBERO 上动作吞吐约为自回归版的 26×（引自原论文）。

## 方案（方法学）

- 模型：GR00T N1.6、π0.5（迭代去噪动作头）、OpenVLA-OFT（并行解码）、Cosmos-Policy（视频生成 DiT）。
- 平台：RTX 4090、Jetson Thor、Jetson AGX Orin（功耗跨一个数量级以上）。
- 手段：阶段延迟分解、NCU roofline 归因、GPU 频率/内存带宽 DVFS 扫描、MuJoCo + LIBERO 闭环部署（43,200 episode）。

## 效果（仅论文数字）

| 发现 | 数字 |
|------|------|
| torch.compile 收益差异 | 动作头主导 vs 骨干主导的模型之间相差 **>5×** |
| RTX 4090 屋脊点 | 165.2 TFLOP/s FP16 ÷ 1.008 TB/s = **163.9 FLOP/B**；去噪动作头 GEMM 在其下，长序列骨干与视频 DiT GEMM 在其上 |
| 访存/计算受限占比（GPU 时间） | GR00T N1.6 **62%**、π0.5 **58%** 访存受限；OpenVLA-OFT **84%**、Cosmos-Policy **77%** 计算受限 |
| GPU 降频能耗甜点 | Orin 省能 **24–32%**；Thor 仅 **1–4%**；两种 SoC 上限内存带宽都不省能 |
| 分阶段调频 | 孤立看可同时降延迟和能耗，端到端里切频开销会抵消 |
| 推理–执行重叠 | 精度最多掉 **56 pp**、速度最高 **3.9×**、能耗变化最高 **5.1×**；无 Pareto 最优配置 |

## 与 wiki 的关系

- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — batch-1 动作头的小 GEMM 落在屋脊点下，本质是 GEMV 式访存受限
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — VLA 把"阶段 → 资源"映射换成"动作张量形状 → 资源"
- [DRAM and Memory System](/concepts/dram-memory-system.md) — Roofline ridge point 直接给出加速器带宽/算力配比依据
- [EdgeAgent](/papers/edgeagent-uma-multi-agent-edge-inference.md) — 同为端侧 SoC（UMA）上的 agent/具身推理刻画，前者看多智能体文本，本文看机器人闭环

## 局限与开放问题

- 只覆盖 NVIDIA 平台（4090/Thor/Orin），没有 NPU 或专用机器人 SoC；仿真闭环（MuJoCo/LIBERO）非真机。
- 硬件启示：VLA 专用 SoC 应按动作头（访存）与骨干/DiT（计算）分别配资源；运行时需要 SLO 感知的工作点选择，而不是静态配置。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.05062) — Jung et al., arXiv:2610.05062（ASPLOS '27）
[2] [raw stub](raw/papers/vla-workload-characterization-embodied-ai.md)
