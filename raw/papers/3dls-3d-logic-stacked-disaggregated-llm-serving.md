---
type: Raw Source
title: 3DLS A 3D Logic-Stacked Architecture for Disaggregated LLM Serving
source_url: https://arxiv.org/abs/2607.01617
arxiv: '2607.01617'
doi: 10.1109/LCA.2026.3709108
ingested: 2026-08-18
sha256: 6ed35645f7c608c8cfb50b3f72babf9e9551c914517f0605555fee5a7ca87f79
---

# 3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving

**Authors:** Jaehun Lee, In-Jun Jung, Joo-Young Kim (KAIST)
**PDF:** [3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf](3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf)
**arXiv:** [2607.01617](https://arxiv.org/abs/2607.01617)
**Venue:** IEEE Computer Architecture Letters, 2026. DOI 10.1109/LCA.2026.3709108

## 问题

PD 解耦 + TP 同时产生两类异构流量：prefill→decode 的 **层间 KV 传输（KVT）** 与 decode 侧 **AllReduce**。2D/2.5D chiplet 上两者共享侧向 D2D，形成 decode 关键路径争用。OPT-175B / TP=16 / 512 GB/s D2D、最高 KV 负载 (batch=16, 16K)：累计 AR 延迟从 **510 ms → 16.37 s（32.1×）**，平均 TBT 从 **61.11 ms → 184.92 ms（3.03×）**（128 输出 token）。

## 方法要点

- Logic-on-logic 两层：上层 prefill pool，下层 decode pool + 侧向 D2D。
- KVT 走垂直 3D 互连（TSV / hybrid bonding / UCIe-3D 类）；decode TP collectives 留在底层侧向 fabric。
- 关键思想：**物理隔离**，不是单纯加带宽。iso-bandwidth：侧向与垂直都按 512 GB/s 总双向（256 GB/s/方向）建模。
- 对照：Naive Planar（共享物理链路）与 PM-Planar（VC + 静态加权带宽预留，仍共享物理链路）。
- 热预算一阶检查：200 W/cm² 先进冷却包络。

## 摘录数字（仅论文给出）

- vs Naive Planar：最高 **1.49×** 吞吐（Code/LLaMA3-8B）、**60.2%** 更低 E2E（Conv/OPT-175B）；六组几何均值 **40.6%** 更低延迟、**1.22×** 吞吐。
- vs PM-Planar：最高 **1.17×** 吞吐、**31.4%** 更低 E2E；几何均值 **18.2%** 更低延迟、**1.11×** 吞吐。
- 最大延迟点 Conv/OPT-175B：44.99 s → 26.08 s → **17.89 s**。
- 最大吞吐点 Code/LLaMA3-8B：24.32 → 32.92 → **36.30 req/s**。
- 峰值吞吐 **261.12 TFLOPS**，内存带宽 **3.35 TB/s**，D2D **512 GB/s**；TP=4/8/16 对应 8B/70B/175B。
