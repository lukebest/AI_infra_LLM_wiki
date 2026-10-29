---
type: Paper
title: "p-DCIM: 28nm Probabilistic SRAM DCIM Ising Machine for Near-Memory RAG Context Selection"
description: "Georgia Tech — 28 nm 流片 SRAM DCIM Ising（0.16 mm² / 0.41 mW / 500 MHz）做 RAG 集合级证据选择；选择能耗约 0.9 µJ（相对 LLM 重排 >6 数量级），整查询能耗 −67%，token F1 可比"
tags:
- cim
- ising
- rag
- near-memory-processing
- sram
- hbm
- hbf
- accelerator
- energy
- inference
- llm
- hardware
created: 2026-10-29
updated: 2026-10-29
timestamp: '2026-10-29T00:00:00Z'
paper_author: [Madhav Vadlamani, Rahul Singh, Yuyao Kong, Haomei Liu, Zheng Zhang, Shimeng Yu]
year: 2026
venue: arXiv cs.AR
arxiv: '2610.37033'
sources:
  - raw/papers/pDCIM_SRAM_Ising_RAG_Context_Selection_2026.pdf
  - raw/papers/pdcim-sram-ising-rag-context-selection.md
---

# p-DCIM：近存 SRAM DCIM Ising 做 RAG 集合级上下文选择

## 一句话结论
把 RAG 的集合级证据选择写成 QUBO / Ising，用同一套 SRAM **数字存内计算（DCIM）** MAC 既构造 embedding 相似系数，又做逐 spin 的 ΔH 退火；退火「温度」由数字幅度平面暴露调度 + SRAM 伪读翻转提供。28 nm 流片宏 **0.16 mm² / 500 MHz / ~0.41 mW**，拟放在 GPU 封装内混合 **HBM+HBF** 的逻辑 base-die：只有入选 passage ID 回到主机。选择能耗约 **0.9 µJ**（相对 LLM 选择 pass **>6 个数量级**），评测整查询能耗 **536→175 J（−67%）**，token-level F1 与 SetR/SetRO 基线可比。

## 动机
- RAG 常把证据选择交给再次跑语言模型重排，权重在 HBM↔GPU 间反复搬运，能耗与延迟高，输出却只是一小撮 passage ID。
- Top-K 独立打分忽略段落间互补/冗余；集合级目标自然是组合优化，适合 Ising / QUBO。
- 若先把候选 embedding 搬到 GPU 再构 QUBO，O(N²) 交互仍穿越封装互连；近存检索（如 HAVEN）之后还缺「近存求解」。

## 方案
1. **双模 DCIM**：同一 MAC 数据通路完成相似度打分（写 Q 矩阵）与退火局部场更新。
2. **数字退火噪声**：固定降压下用伪读扰动 + 可编程幅度平面逐步「冷却」，符号位全程保护。
3. **系统位置**：逻辑 base-die + 混合 HBM/HBF；近存检索出 top-N 后本地构 QUBO、退火，只回传选中 ID。
4. **流片**：28 nm，**32 Kb** SRAM，实测确定性 / 概率模式功耗 **0.406 / 0.413 mW**。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 面积 / 频率 / 功耗 | **0.16 mm²**，**500 MHz**，~**0.41 mW** |
| 单次选择能耗 | ~**0.9 µJ** |
| vs LLM 选择 pass | 宏归一化选择能耗 **>6 数量级**更低 |
| 整查询能耗 | **536 J → 175 J（−67%）** |
| 质量 | 与 SetR/SetRO 在 Exact Match / Gold-Contains / token F1 上可比（文中示例 EM **0.70**、Gold-Contains **0.90**） |

## 与 wiki 的关系
- [HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md) — HBM+HBF 层次里「什么留在近 GPU 存储」；p-DCIM 把 **RAG 选择算子**也压进同一近存平面
- [DuoPD](/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md) / [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 逻辑 die / 近存加速与 GPU 分工；此处加速的是检索后选择而非 decode GEMV
- [CacheSmith](/papers/cachesmith-adaptive-kv-reuse-rag-slo.md) — RAG 服务侧 KV/SLO；p-DCIM 切的是证据选择能耗
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 避免 O(N²) 相似度流量穿出存储子系统
- [Numeric Formats / stochastic](/concepts/numeric-formats-ai-hardware.md) — 伪读扰动作为片上熵源，与随机计算启发相邻

## 开放问题
- 大 N 的 QUBO 需测量参数化仿真外推；片上 32 Kb 对真实语料 top-N 规模的扩展策略未充分展开。
- 与 GPU 侧生成模型的流水重叠、多查询批处理调度未给系统数字。
- 混合 HBM+HBF base-die 集成为提案级，无封装级实测。

# Citations
- [arXiv:2610.37033](https://arxiv.org/abs/2610.37033) — Vadlamani et al., 2026
- [raw stub](/raw/papers/pdcim-sram-ising-rag-context-selection.md)
