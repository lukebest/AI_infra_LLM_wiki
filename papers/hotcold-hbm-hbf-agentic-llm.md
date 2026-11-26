---
type: Paper
title: "Hot–Cold HBM/HBF Tiering for Agentic LLM Serving"
description: "HBM 热集 + HBF 冷池；Qwen3-Coder-30B-A3B：14 ms TBT、resume +≈0.1 ms、会话 24×；相对全闪读 −7.6 kW/8-GPU"
tags:
- architecture
- hbf
- hbm
- kv-cache
- llm
- inference
- serving
- serving-system
- memory
- memory-bandwidth
- packaging
- agentic-ai
- 3d
created: 2026-09-24
updated: 2026-11-26
timestamp: '2026-11-25T00:00:00Z'
paper_author: [Jongjin Baek, Won Ji, Seungjae Yoo, Joo-Young Kim]
year: 2026
arxiv: '2609.25782'
sources:
  - raw/papers/HotCold_HBM_HBF_Agentic_LLM_2026.pdf
  - raw/papers/hotcold-hbm-hbf-agentic-llm.md
---

# Hot–Cold Tiering of HBM and High Bandwidth Flash for Agentic LLM Serving

## 一句话结论

把 agentic KV 的**热集留在 HBM、冷池放进共封装 HBF**，在 Qwen3-Coder-30B-A3B 上做到 **14 ms TBT**、resume 仅加 **≈0.1 ms**、每 GPU 会话 **24×**，并相对全 KV 走闪存砍掉约 **7.6 kW/8-GPU** 读功耗——HBF 是冷层，不是 HBM 替代品。

## 动机

- Agentic 多轮：tool/用户等待期间会话 idle，但 KV 必须保留；暂停池迅速撑爆 HBM。
- 全 KV 进 HBF：每步 decode 付高读能量 + 写寿命压力（对照 [HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md) 全 HBF、[SPLASH](/papers/splash-sparse-attention-hbf.md) 稀疏×HBF）。
- 双峰：Na=48 时热集仅占驻留容量 **3%**，却贡献 **98%** 读流量。

## 方案

1. **共封装层次**：HBM 上叠 HBF；GPU 直访 HBM，HBF 仅经 D2D + base-die 缓冲（预取/驱逐双缓冲）。
2. **放置**：活跃 decode KV → HBM；暂停冷池 → HBF；resume 前预取回 HBM。
3. **写策略**：write-on-evict（块最多写一次），对比 all-KV-to-flash。
4. **评测设定**：B200 **192 GiB** HBM + **3 TiB** SLC HBF（读带宽对齐 HBM）；agentic 轨迹放大并发。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| TBT @ Na=48 / 128 | **14 ms**（72 tok/s）/ **27 ms**（37 tok/s）；均 <50 ms SLO |
| Resume 附加 | 相对 prefill **≈0.1 ms**（HBF≈0.084 ms；NVLink-C2C 1.0 ms；PCIe 7 ms；recompute 14 ms） |
| 并发会话 / GPU | **24×** |
| 读功耗 vs all-flash | 20 pJ/bit 下每卡 ≈**950 W**，8-GPU **7.6 kW**（能量扫描 2.1–12.2 kW/节点） |
| 寿命 @ Na=48 | write-on-evict ≈**20 年**；all-flash ≈11 年 |

**口径：** IEEE CAL 风格 trace 仿真，非硅实测 tok/s。

## 与 wiki 的关系

- [HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md) — 全 HBF 运行时；本文坚持 **热集必须 HBM**
- [SPLASH](/papers/splash-sparse-attention-hbf.md) — 长上下文稀疏×HBF；本文焦点是 **agentic idle 冷池**
- [UNISON](/papers/unison-near-memory-scheduler-llm-agents.md) — 近存调度谁该留快层；本文给 **物理 HBM/HBF 分层**
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 封装内热冷路径

## 2026-11-25 交叉

[Synapse](/papers/synapse-hbm-hbf-nmc-agentic.md) 由同一通讯作者组给出：在 HBM/HBF 分层之上，把注意力与专家计算放到 HBF 近存单元，并与 GPU 跨智能体重叠。评估是 H100 测 GPU 时间加 HBF 仿真。

[Mayfly](/papers/mayfly-lifecycle-aware-hbf-rsi.md) 把停车策略当作 HBF-Park 基线，继续处理递归自我改进里就绪 KV 溢出时的就地读、回落迁回和写放大。评估是 H200 校准的离散事件仿真，HBF 路径为模型。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.25782) — Baek et al., arXiv:2609.25782
[2] [raw stub](raw/papers/hotcold-hbm-hbf-agentic-llm.md)
- [arXiv:2611.29901](https://arxiv.org/abs/2611.29901) — Synapse
- [arXiv:2611.32264](https://arxiv.org/abs/2611.32264) — Mayfly
