---
type: Paper
title: "HBFlex: Full-HBF Memory System for Fine-Grained LLM KV"
description: 北大/阿里 — 全 HBF 服务；吞吐 vs FlashAccel 最高 1.58×、vs H3 最高 3.30×；TTFT vs FA 1.20–1.33×
tags:
- hbf
- hbm
- memory
- kv-cache
- llm
- inference
- serving
- serving-system
- memory-bandwidth
- packaging
- architecture
- agentic-ai
timestamp: '2026-09-18T00:00:00Z'
created: 2026-09-18
updated: 2026-09-18
sources:
- raw/papers/HBFlex_Flexible_Memory_HBF_LLM_2026.pdf
- raw/papers/hbflex-flexible-memory-hbf-llm.md
---

# HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution

**Authors:** Shuzhang Zhong, Weikai Xu, Yifan Zhou, Tongbin Zhao, Tenghao Zhao, Yifei Kang, Cunyin Chang, Shu Li, Guangyu Sun, Meng Li
**Affiliation:** Peking University; HKUST; Alibaba Group
**arXiv:** [2609.18675](https://arxiv.org/abs/2609.18675)（2026-09-16，cs.AR；Thu 9/17 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.18675)

相对 [Trillion MoE HBF 供给](/papers/trillion-param-moe-hbf-memory-provisioning.md) 回答「权重已在 HBF 后状态层要多少」，以及 [FLINT](/papers/flint-hbf-llm-inference.md) / [DASH](/papers/dash-dual-path-hbf-moe-inference.md) 的混合/双路径，HBFlex 做 **全 HBF** 下细粒度 KV 的放置–写回–回收闭环。

## 动机

- 混合 HBM/HBF 在固定封装预算下用 HBM 保动态 KV，会挤掉本可给 HBF 的平面 → 权重读带宽被卡住。
- 全 HBF 多出平面，但 KV 细粒度读导致平面热点、增量 program 与读争用、混合寿命放大 GC（文内 DeepSeek-V4-Pro 朴素 WAF ≈ **30×**）。

## 方案

1. **全 HBF 组织**：封装预算全给 HBF；base die 缓冲动态更新。
2. **读路径**：平面感知放置 + attention/PagedAttention 读时的运行时负载均衡。
3. **写路径**：增量更新聚合，在足够长的计算窗口内写回，降低 write–read 干扰。
4. **回收**：寿命引导块打包 + 延迟回收，减少 valid-page 迁移。
5. 评测：trace-driven；6 stack × 16 die × 32 plane = **3072** planes；每栈 **488 GB/s**、合计 **2.93 TB/s**；四模型 × 四 Alibaba Bailian traces + SWE-bench。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 吞吐 vs FlashAccel FA-CSI | 最高 **1.58×** |
| 吞吐 vs H3（高并发） | 最高 **3.30×** |
| TTFT geomean vs FA-CLI / FA-CSI | **1.20× / 1.33×** |
| TPOT geomean vs FA-CLI / FA-CSI | **1.21× / 1.35×** |
| TTFT / TPOT vs H3 | **22.65× / 1.89×** |
| 朴素全 HBF KV GC WAF（V4-Pro） | ≈ **30×**（动机基线） |

**口径：** 仿真吞吐/延迟，非硅实测 tok/s；基线含 H3、FlashAccel co-located/cascaded。

## 与 wiki 的关系

- [Trillion MoE HBF](/papers/trillion-param-moe-hbf-memory-provisioning.md) — 供给膝点 vs 本文 **全 HBF 运行时管理**
- [FLINT](/papers/flint-hbf-llm-inference.md) / [DASH](/papers/dash-dual-path-hbf-moe-inference.md) / [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md) — HBF 路径族；本文去掉 HBM 槽位
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 平面并行与 KV 读写擦
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 对照：本文是 **单加速器内存层**，不是机柜 PD

## 开放问题

1. 更高并发 / 更长 agent 会话下窗口写回是否仍躲得过读热点。
2. 与 Trillion 文的状态层膝点如何联合闭式供给。
3. 真实 FTL/控制器固件开销未展开。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.18675) — Zhong et al., arXiv:2609.18675
[2] [raw/papers/hbflex-flexible-memory-hbf-llm.md](raw/papers/hbflex-flexible-memory-hbf-llm.md) — 结构化摘录
