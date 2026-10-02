---
type: Paper
title: "HAPMoE: Heterogeneity-Aware Automatic Parallelism for MoE Training"
description: "异构集群 MoE 自动并行；e2e 训练吞吐最高 3.2×；非均匀 pipeline 再最高 +78%；搜索 <1 分钟"
tags:
- architecture
- llm
- moe
- training
- training-system
- expert-parallelism
- collective
- distributed
- parallelism
- scheduling
- throughput
created: 2026-10-02
updated: 2026-10-02
timestamp: '2026-10-02T00:00:00Z'
paper_author: [Mengyuan Fan, Peizhuang Cong, Zixiao Huang, Si Xu, Tong Qiao, Yanghao Li, Jing Yang, Tong Yang, Quanlu Zhang, Yu Wang]
year: 2026
arxiv: '2609.39350'
sources:
  - raw/papers/HAPMoE_Heterogeneity_Aware_MoE_Parallelism_2026.pdf
  - raw/papers/hapmoe-heterogeneity-aware-moe-parallelism.md
---

# HAPMoE：MoE × 异构集群的自动并行

## 一句话结论

同时面对 **MoE 动态路由/All-to-All** 与 **异构加速器集群**，HAPMoE 用轻量 MoE 代价模型在 **六维** 并行空间搜索，计划可直接落 Megatron-LM；e2e 训练吞吐相对基线最高 **3.2×**，非均匀 pipeline 再最高 **+78%**，搜索 **<1 分钟**。

## 动机

- 自动并行要么做稠密+异构、要么做 MoE+同构，很少同时覆盖 EP/TPE 与设备带宽不对称。
- MoE 的 dispatch/combine 与专家负载不均，使异构上的代价预测与稳定缩放更难。

对照 [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md)、[Mixture-of-Kittens](/papers/mixture-of-kittens-moe-megakernel-nvl72.md)、[Heterogeneous Inference](/concepts/heterogeneous-inference.md)。

## 方案

1. **轻量 profiling + MoE-aware 代价模型**。
2. **六维并行空间搜索**（含非均匀 pipeline 与 EP 相关维），剪枝增强动态规划。
3. **输出**：可部署到 Megatron-LM 的混合并行计划。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| e2e 训练吞吐 vs 基线（异构集群） | 最高 **3.2×** |
| 非均匀 pipeline 附加收益 | 最高 **+78%** |
| 搜索时间 | **<1 分钟** |

## 与 wiki 的关系

- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — MoE All-to-All / 混合并行计划层
- [MoK](/papers/mixture-of-kittens-moe-megakernel-nvl72.md) — NVL72 同构 scale-up megakernel；HAPMoE 主攻 **异构搜索**
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构轴从推理延伸到 **训练并行规划**
- [ThunderEP](/papers/thunderep-pcie-consumer-gpu-moe.md) — 另一端：弱互连上的 EP 通信实现

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.39350) — Fan et al., arXiv:2609.39350
[2] [raw stub](raw/papers/hapmoe-heterogeneity-aware-moe-parallelism.md)
