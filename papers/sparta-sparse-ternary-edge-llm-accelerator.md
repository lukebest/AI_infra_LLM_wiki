---
type: Paper
title: "SPARTA: A Sparse Ternary LLM Accelerator with Adaptive Attention and Unified Datapath for Long-Context Edge Inference"
description: "浙大/Veloxis — 28 nm 13.9 mm² 稀疏三值边缘 LLM 加速器；统一 PE 跑 SpMM/SpMV+bit-serial attention，自适应 page Top-k + token Top-p；KV 流量降 4.1–4.8×，相对 Jetson 吞吐 3.9× / 能效 8.3×"
tags:
- accelerator
- edge
- quantization
- sparse
- numeric-format
- kv-cache
- attention
- chip-design
- inference
created: 2026-10-28
updated: 2026-10-28
timestamp: '2026-10-28T00:00:00Z'
paper_author: [Yanzhen Zhou, Zhengyu Han, Qunyou Liu, Zheyu Yan, Weihong Xu, Cheng Zhuo]
year: 2026
venue: arXiv cs.AR
arxiv: '2610.34824'
sources:
  - raw/papers/SPARTA_Sparse_Ternary_Edge_LLM_Accelerator_2026.pdf
  - raw/papers/sparta-sparse-ternary-edge-llm-accelerator.md
---

# SPARTA：长上下文边缘三值 LLM 的稀疏统一加速器

## 一句话结论
三值权重（{−1,0,+1}，约 **1.58 bit**）把边缘侧权重墙压下去之后，KV/attention 变成主瓶颈。SPARTA 用一套统一 PE 同时吃三值 SpMM/SpMV 与 bit-serial attention，再加 page-level Top-k + token-level Top-p 的自适应稀疏；**28 nm / 1 GHz / 13.9 mm²**，KV 流量相对满注意力 **4.1–4.8×**、相对 SOTA 稀疏 **1.3–1.5×**；相对 Jetson AGX Orin 平均吞吐 **3.9×**、端到端能效 **8.3×**，相对 Ryzen 7 9700X **5.0× / 81.7×**，相对 FIGLUT/TeLLMe/MCBP 吞吐 **1.6–12.0×**、能效 **2.0–4.2×**、面积效率 **1.3–51.4×**。

## 动机
- 边缘设备内存与带宽紧；三值 LLM 把权重存到 8-bit 模型约 1/5，并保住 **88–97%** 全精度「智能」；算术退化为加/减/跳过。
- 上下文拉到数万 token 后，每 token 流量被 KV 主导（论文 Fig.1(b)）。
- 既有加速器常把三值线性层与 attention 拆成两条 datapath（LUT 三值 PE 难兼稀疏 SpMM/SpMV）；稀疏 attention 多为 dense、固定模式或固定 Top-k，难跟输入自适应且长上下文（多数 ≤4K–8K）。

## 方案
1. **相位感知稀疏数据流**：prefill 侧 compute-bound SpMM、decode 侧 memory-bound SpMV，统一挖掘零权重、attention 零比特与动态注意力稀疏。
2. **统一计算阵列**：三值 SpMM/SpMV 与 bit-serial QK/PV 映射到同一条件累加 PE；跳过零权重与零 Q/P 比特；bank-local 累加 + conflict FIFO 处理不规则访问（相对 TENET/TeLLMe，PE 面积效率最高 **2.2×**、能效 **1.5×**）。
3. **两级自适应 attention**：粗粒度 page Top-k（ρk）砍 K 访问 → 细粒度 histogram Top-p（p）再砍 V/PV；默认 **ρk=1/4、p=0.90**，最大序列 **32K**（例：32K 时 k=⌈ρk⌈N/16⌉⌉=512 pages）。
4. 硅侧：8 slice × 16 PE × 32 lane；HBM2 8×128-bit @2 GHz / 8 GB；总面积 **13.9 mm²**，片上平均功耗 **1.40 W**。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 工艺 / 频率 / 面积 | **28 nm**、**1 GHz**、**13.9 mm²**（片上功耗 **1.40 W**） |
| KV 流量 | vs 满注意力 **4.1–4.8×**；vs SOTA 稀疏 **1.3–1.5×**（任务相关精度损失） |
| vs Jetson AGX Orin | 吞吐 **3.9×**，端到端能效 **8.3×**（平均） |
| vs Ryzen 7 9700X | 吞吐 **5.0×**，能效 **81.7×** |
| vs FIGLUT / TeLLMe / MCBP | 吞吐 **1.6–12.0×**，能效 **2.0–4.2×**，面积效率 **1.3–51.4×** |
| 默认稀疏参数 | **ρk=1/4**，**p=0.90**；Top-p 保留候选的 **2.9–10.9%**（随长度上升而下降） |
| 最大上下文 | **32K** |

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 三值权重 + INT4 KV 把瓶颈从权重推到 KV/attention
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 统一 PE 同时覆盖稀疏三值线性与 bit-serial attention 的另一条边缘加速器路径
- [FIGFLEX](/papers/figflex-mixed-precision-fp-int-gemm.md) — 同周低比特 GEMM 协同设计；FIGFLEX 偏 FP-INT 可变比特，SPARTA 偏三值 + 长上下文稀疏 attention 全栈
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — Softmax/指数质量用 histogram + LUT 近似，服务 Top-p 阈值搜索

## 开放问题
- 质量相对 dense 有任务相关损失；ρk 再压到 1/8、1/16 时困惑度陡升，部署端需要按任务锁默认点。
- 对标 GPU/CPU 用 dense + FP16（另报 Jetson INT4 KV）；同稀疏算法软件实现的对照未系统给出。
- 28 nm 综合/面积分解为主；与更新工艺或片上 SRAM-only 无 HBM 边缘形态的外推需另评。

# Citations
- [arXiv:2610.34824](https://arxiv.org/abs/2610.34824) — Zhou et al., 2026
- [raw stub](/raw/papers/sparta-sparse-ternary-edge-llm-accelerator.md)
