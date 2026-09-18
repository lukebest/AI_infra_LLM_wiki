---
type: Raw Source
title: "HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution"
source_url: https://arxiv.org/abs/2609.18675
arxiv: '2609.18675'
ingested: 2026-09-18
sha256: 012e559e4577dd295febc8ed8500ca03bd4d4e95b58ab396a079a768b5a1bdfa
---

# HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution

**Authors:** Shuzhang Zhong, Weikai Xu, Yifan Zhou, Tongbin Zhao, Tenghao Zhao, Yifei Kang, Cunyin Chang, Shu Li, Guangyu Sun, Meng Li
**Affiliation:** Peking University; HKUST; Alibaba Group
**PDF:** [HBFlex_Flexible_Memory_HBF_LLM_2026.pdf](HBFlex_Flexible_Memory_HBF_LLM_2026.pdf)
**arXiv:** [2609.18675](https://arxiv.org/abs/2609.18675)（2026-09-16，cs.AR；Thu 9/17 列表）

## 问题

全 HBF 服务相对混合 HBM/HBF：固定封装预算下保留 HBM 会挤占 HBF 平面/带宽；但 KV 细粒度读、增量写与混合寿命 GC 使单纯搬 KV 到 HBF 无法兑现平面并行。

## 方法要点

- 全 HBF + base-die 缓冲动态 KV。
- 平面感知放置与 attention 读负载均衡；窗口内聚合写回；寿命引导块打包 + 延迟回收。
- 仿真：6×HBF stack（每栈 488 GB/s，合计 2.93 TB/s；3072 planes）；四模型 × 四 Bailian traces + SWE-bench。

## 摘录数字（仅论文给出）

- 吞吐相对 FlashAccel 最高 **1.58×**（FA-CSI）；相对 H3 最高 **3.30×**（高并发）。
- TTFT geomean：vs FA-CLI **1.20×**、FA-CSI **1.33×**；vs H3 **22.65×**。
- TPOT geomean：vs FA-CLI **1.21×**、FA-CSI **1.35×**；vs H3 **1.89×**。
- 朴素 KV-in-HBF GC WAF（DeepSeek-V4-Pro）约 **30×**。
