---
type: Paper
title: "The Token-Energy Law of LLM Decode: Active Bytes and Realized Time Account for Joules per Token"
description: "NVIDIA/TTU/TACC — 每输出 token 的 GPU 板级能耗 = 常数 + 权重字节项 + KV 字节项 + 时间项；GH200/GB300 上 270 次留出实测误差全在 3.73% 内；权重与 KV 分开系数比合并系数更准（GB300 最大误差 0.89–2.14% vs 4.38–5.72%）"
tags:
- decode
- energy
- power
- kv-cache
- memory-bandwidth
- batching
- gpu
- nvidia
- hbm
- performance-analysis
- workload-characterization
- inference
created: 2026-10-22
updated: 2026-10-22
timestamp: '2026-10-22T00:00:00Z'
paper_author: [Chenxu Niu, Batuhan Sencer, Wei Zhang, Yong Chen]
year: 2026
arxiv: '2610.28576'
sources:
  - raw/papers/Token_Energy_Law_LLM_Decode_2026.pdf
  - raw/papers/token-energy-law-llm-decode.md
---

# Token-Energy Law：decode 每 token 能耗由「活跃字节 + 实际耗时」决定

## 一句话结论
dense 模型 decode 的每 token 能耗可以写成一个仿射式：e = c + α·(权重字节/有效 batch) + β·(KV 字节×(历史长度+1)) + P_τ·(每 token 实际耗时)。batch 摊薄权重项，长上下文推高 KV 项，吞吐决定时间项；系数按「模型 × 硬件 × 运行时」标定一次后可预测未见过的负载。

## 动机
- 参数量、FLOPs 估能耗不准：量化、GQA、KV 压缩改变实际搬运字节；连续批处理让 batch 成员不断变化。
- 已有方法要么只给经验曲线，要么需要逐算子功耗模型，缺一个可解释、能跨 batch/上下文迁移的紧凑公式。

## 方案
1. **两个字节坐标**：q_w = M_w/(10⁹·B_eff)（一轮迭代内多请求共享的稠密权重）；q_KV = K_KV·(L̄+1)/10⁹（每请求私有 KV 历史读 + 1 条新写入）。权重与 KV 逻辑字节相等的平衡 batch B* = M_w/[K_KV(L+1)]。
2. **时间坐标**：τ = 解码总时长 / 有效输出 token 数；系数 P_τ 单位为瓦。
3. **分层标定**：每个 σ（模型、精度、硬件、运行时、TP 度）一组系数，OLS + HC3 标准误；系数冻结后再采集留出数据。
4. 用 HBM 读计数校验字节坐标（GH200 上 Qwen2.5-7B 拟合 MAPE **0.0498%**）。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 平台 | GH200（144 GB HBM3e，700 W 上限，TP=1/2）、GB300（1,300 W 上限，TP=1）；vLLM，BF16，FlashAttention |
| 模型 | Qwen2.5-7B / 14B-Instruct、Mistral-7B-Instruct-v0.3 |
| 静态留出验证 | 270 次执行、54 个条件，条件均值误差全部 ≤ **3.73%**；本地标定最大误差 0.559–2.22% |
| 同型号换卡零重标定 | GH200 GPU0 系数直接用到 GPU1：中位 **2.62%**、最大 **3.72%** |
| 消融（GB300 最大误差） | 字节+时间 **0.887–2.137%**；权重与 KV 合并成一个字节项 **4.381–5.721%**；只用字节 28.2–35.5%；只用时间 10.97–29.4% |
| 动态成员 | 请求中途离开的 trace 测试中，已标定系数无需重标定仍有效 |

## 与 wiki 的关系
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 受字节驱动的能耗侧证据
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — batch 摊薄权重字节等价于把 GEMV 推向 GEMM
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 私有 KV 项随历史线性增长，KV 压缩直接进 β 项
- [HBM2 Power Characterization](/papers/hbm2-power-characterization-real-chips.md) — 器件级 HBM 功耗，可与本文 J/GB 系数对照
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 能耗随上下文增长的另一种度量

## 开放问题
- 只覆盖 dense、全历史注意力；MoE（专家共享随路由变化）、稀疏/滑窗注意力、量化权重/KV 需要重新定义字节坐标，作者列为后续工作。
- 时间项需要实测或外部时长模型，做前瞻规划时误差会叠加时长模型误差。
- 系数是板级口径，不含 host、网络、机房 PUE；跨 SKU 迁移只做了同型号换卡。

# Citations
- [arXiv:2610.28576](https://arxiv.org/abs/2610.28576) — Niu et al., 2026
- [raw/papers/token-energy-law-llm-decode.md](/raw/papers/token-energy-law-llm-decode.md)
