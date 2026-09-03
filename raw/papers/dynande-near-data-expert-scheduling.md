---
type: Raw Source
title: DynaNDE Dynamic Near-Data Expert Scheduling for Batched MoE Inference
source_url: https://arxiv.org/abs/2609.00407
arxiv: '2609.00407'
ingested: 2026-09-03
sha256: fb076ac3c125641b9fd0ae32f2e69ec16d9aabac793539c8f6a6c1c857237179
---

# DynaNDE: Dynamic Near-Data Expert Scheduling for Batched MoE Inference

**Authors:** Xiaoyang Lu, Belthangady Akash Vi Narayana Pai, Xian-He Sun
**Affiliations:** Illinois Institute of Technology
**PDF:** [DynaNDE_Near_Data_Expert_Scheduling_2026.pdf](DynaNDE_Near_Data_Expert_Scheduling_2026.pdf)
**arXiv:** [2609.00407](https://arxiv.org/abs/2609.00407)（2026-09-01，cs.AR）

## 问题

MoE 专家参数常 offload；NPU 上 PMove 主导延迟。MoNDE 等 NPU–NDP 协作用固定 PCIe/NDP 带宽比启发式，未建模异构算力、专家级并发与 decode 时间复用。

## 方法要点

- 分析模型：三阶段争用回避流（AMove in → 重叠 PMove/NPU 与 NDP 计算 → AMove out）；reuse 时 PMove=0。
- 运行时：reuse-aware score 排序 + 前缀扫描选 NPU 专家子集，O(|E| log |E|)。
- 主机侧调度；NDP 经 CXL；不改 NDP datapath（复用 MoNDE 指令接口）。

## 摘录数字（仅论文给出）

- vs MoNDE：prefill 平均 **2.6×**，decode 平均 **2.2×** 吞吐。
- Prefill vs NPU/NDP/MoNDE/HybriMoE：平均 **1.8× / 2.9× / 2.6× / 1.1×**。
- Decode vs 同四基线：平均 **30.5× / 1.1× / 2.2× / 1.4×**。
- Decode 批大小 16/32/64 vs MoNDE：**2.1× / 2.2× / 1.8×**；vs HybriMoE：**1.2× / 1.4× / 1.1×**。
- NDP 核 28 nm @1 GHz：面积 **2.95 mm²**，功耗 **1.81 W**。
- 配置：NPU 4×128×128 MAC；NDP 64×4×4 MAC、512 GB/s、512 GB；PCIe Gen4×16；默认缓存 10% experts（LFU）。
