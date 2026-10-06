---
type: Paper
title: "AFORE: Attention–FFN Disaggregation with Overlapped Reconfiguration of Experts"
description: "HKUST 等 — AFD 下专家负载不均被放大（偏斜路由吞吐 −20.1% vs 单体 −11.9%）；利用提前可见的下一微批路由做专家副本重配 + NVLink 迁移重叠流水；GLM-4.5-Air 吞吐 +10.1–17.6%、P95 ITL −7.1–9.5% vs 最强基线，迁移 0 暴露"
tags:
- moe
- expert-parallelism
- disaggregated-inference
- serving-system
- inference
- decode
- scheduling
- latency
- throughput
- gpu
- nvidia
created: 2026-10-06
updated: 2026-10-06
timestamp: '2026-10-06T00:00:00Z'
paper_author: [Wenshuang Li, Youhe Jiang, You Peng, Jiawei Jiang, Binhang Yuan]
year: 2026
arxiv: '2610.03203'
sources:
  - raw/papers/AFORE_AFD_Expert_Reconfiguration_2026.pdf
  - raw/papers/afore-afd-expert-reconfiguration.md
---

# AFORE：AFD 流水窗口里"预知 + 重叠"的专家重配置

## 一句话结论

Attention–FFN 解耦（AFD）把 FFN 变成独立流水级后，**热专家直接卡住整条流水**。AFORE 发现 AFD 天然提供两样东西：① 下一微批的 expert-token 分布在进入 FFN 前就已知（不用猜历史）；② 前面在飞微批的计算构成迁移窗口。于是用"按目标微批真实需求挑副本 + NVLink GPU-GPU 拷贝重叠"做微批级重配：相对最强基线吞吐 **+10.1–17.6%**、P95 ITL **−7.1–9.5%**；相对静态放置吞吐平均 **+29.8%**、P95 ITL 平均 **−18.2%**；迁移延迟被 **完全隐藏**。

## 动机

- top-8 路由下一个 AFD 窗口内热专家 max/mean **5.2×**；静态放置时 8 个 EP worker 最忙者达平均 **2.5×**；ShareGPT 最不均层 **3.3×**。
- 合成偏斜路由：单体 attention-FFN 执行吞吐 **−11.9%**，AFD 下 **−20.1%**——AFD 放大了不均。
- 动机实验（16×A100，PD+AFD：4 prefill / 4 attention / 8 FFN，EP=8）：静态不均比 **1.70×**；历史重配 → **1.42×**（吞吐 +4.5%）；加 demand prefetch → **1.10×**（再 +7.1%）；再加迁移重叠 → 暴露等待 **0.461 / 0.437 → 0.000 ms**、再 +16.4%；合计 vs Static 吞吐 **+30.3%**、P95 ITL **−17.8%**。

## 方案

1. **微批感知调度问题**：主副本 + 冗余副本布局；迁移感知代价模型只在"FFN 瓶颈收益 > 关键路径暴露迁移"时触发；贪心负载再分配。
2. **Demand prefetch**：attention worker 把目标微批路由导出的紧凑向量直接发给调度器。
3. **重叠迁移**：一旦目标需求可得即发起 NVLink p2p 专家权重拷贝，与前序微批 FFN 计算重叠；在微批边界原子切换路由，不打断在飞执行（attention↔FFN 回传走 StepMesh）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 平台 | 2 节点 × 8 A100；NVLink/NVSwitch **300 GB/s**/GPU 单向；每节点 8 个 RDMA bond，各 **50 GB/s** |
| 模型 / 负载 | GLM-4.5-Air **110B**，PD+AFD；ShareGPT / FineWeb / CodeForces / GSM8K 回放 |
| vs 最强基线（EPLB / HarMoEny / Lina / Libra 中最强） | 吞吐 **+10.1–17.6%**，P95 ITL **−7.1–9.5%** |
| vs Static | 吞吐 **+26.0–34.1%**（平均 **29.8%**），P95 ITL **−16.7–19.6%**（平均 **18.2%**） |
| 去掉 prefetch | 吞吐 **−12.4–17.9%**，P95 ITL **+6.3–10.5%** |
| 去掉重叠 | 吞吐 **−15.2–21.3%**，P95 ITL **+12.2–16.0%** |
| 迁移成本 vs 窗口 | 原始迁移 **0.453–0.495 ms** vs 前瞻窗口 **2.008–2.119 ms**；**324/324** 样本 0 暴露；剩余余量中位 **1.459–1.668 ms**，最小 **0.447 ms** |
| 调度器 | 中位 **8.23 µs**（EP=2）→ **245.81 µs**（EP=128）；1,400 目标中 **99.5%** 达最优，EP≥8 全最优 |

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — AFD 的副作用（FFN 级被热专家拖慢）与对应解法
- [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — AFD/M2N 原型；AFORE 在其上补"动态专家重配"
- [M2N Communication](/concepts/m2n-communication.md) — attention↔FFN 的 M:N 通信路径
- [MegaFlux](/papers/megaflux-skew-resilient-moe-megakernels.md) — 同是热专家复制，MegaFlux 在 megakernel 内、AFORE 在 AFD 流水级间
- [RailWave](/papers/railwave-ep-rail-incast-scheduling.md) — 上层改需求（AFORE）与下层改执行（RailWave）互补

## 局限与开放问题

- 只在 A100、16 GPU、单一 110B 模型上评测；Hopper/Blackwell + 更大 EP 与 NVL72 级 scale-up 域下迁移窗口是否仍充裕？
- 副本显存开销与 KV 预算的权衡未充分量化。
- AFD 的微批前瞻窗口约 2 ms；若 attention 侧更快（短上下文）窗口收窄，隐藏是否失效？

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2610.03203) — Li et al., arXiv:2610.03203
[2] [raw stub](raw/papers/afore-afd-expert-reconfiguration.md)
