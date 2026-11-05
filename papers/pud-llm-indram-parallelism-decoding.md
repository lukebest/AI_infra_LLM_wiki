---
type: Paper
title: "PUD-LLM: Accelerating LLM Decoding with In-DRAM Parallelism"
description: "东大/RIKEN — Processing-using-DRAM decode 共设计；相对 PUD 基线最高 1.41×，相对处理器 2.45×"
tags:
- pim
- near-memory-processing
- dram
- inference
- decode
- llm
- edge
- memory
- pud
created: 2026-11-05
updated: 2026-11-05
timestamp: '2026-11-05T00:00:00Z'
paper_author: [Kevin Xu, Tatsuya Kubo, Daichi Tokuda, Shinya Takamaeda-Yamazaki, Issei Sato]
year: 2026
venue: arXiv
arxiv: '2611.02401'
sources:
  - raw/papers/PUD_LLM_InDRAM_Parallelism_Decoding_2026.pdf
  - raw/papers/pud-llm-indram-parallelism-decoding.md
---

# PUD-LLM：用 In-DRAM 并行加速 LLM Decode

## 一句话结论
边缘设备上自回归 decode 被内存受限 GeMV 主导。Processing-using-DRAM（PUD）可在 DRAM 内跨大量列（文中示例 **65,536**）做位串行并行，但单层权重往往装不满（如 Llama 3 8B QKV 仅 **6,144** 行）。PUD-LLM 用算法把后继投影改写为「当前 residual + 残差更新校正」并打包执行，再用更少 bit-serial 步近似校正；系统侧按 subarray 列（SIMD）或独立 bank（MIMD）提高利用率。端到端 decode 相对 PUD 基线最高 **1.41×**，对应相对处理器执行 **2.45×**。

## 动机
- Decode GeMV 带宽墙：搬权重进出处理器代价高。
- 朴素 PUD 映射下列/bank 并行大量空闲。
- 需要算法与映射共设计，而不是只换计算范式。

## 方案
1. **投影打包**：后继投影 = 当前 residual 状态上的计算 + 残差更新校正；层冗余支撑低精度校正。
2. **SIMD 路径**：共享指令流，打包 QKV 与 Gate/Up lookahead，提高列利用率。
3. **MIMD 路径**：独立 bank/通道上流水重叠当前投影 delta 与后继 lookahead。
4. **评测**：相对 PUD 基线与 CPU/处理器基线的端到端 decode 加速。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 端到端 decode vs PUD 基线 | 最高 **1.41×** |
| 端到端 decode vs 处理器执行 | **2.45×** |
| PUD 列并行示例规模 | **65,536** 列 |
| Llama 3 8B QKV 行数（利用率反例） | **6,144** |

## 与 wiki 的关系
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 在 bank/列物理并行上做位串行运算；PUD-LLM 补利用率共设计
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 GeMV 留在 DRAM 内，缩短 processor–memory 搬运
- [DuoPD](/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md) — HBM 逻辑 die PNM 跑 decode；PUD-LLM 走商品 DRAM 阵列内并行
- [3D-MoE](/papers/3d-moe-complementarity-nmp-moe-decode.md) — 近存 decode；对象从 3D NMP 专家换成 PUD 投影打包

## 开放问题
- 仿真/原型与真实量产 DRAM 命令时序、刷新干扰的差距需硅上验证。
- 与 GQA/MLA 等窄 KV、以及量化权重位串行步数的联合最优点未系统扫完。

# Citations
- [arXiv:2611.02401](https://arxiv.org/abs/2611.02401) — Xu et al., UTokyo / RIKEN AIP, 2026
- [raw stub](/raw/papers/pud-llm-indram-parallelism-decoding.md)
