---
type: Paper
title: "Elastic Precision: Software–Hardware Co-Design of a Mixed-Precision Architecture for Long-Context LLM Inference"
description: "Imperial/Cambridge — Coffee 在 flattened systolic 上按双输入在线分配位宽；Avg4 下 Llama-3-8B PPL 6.58 vs PLENA 6.95、Avg acc 72.23 vs 69.63；长上下文 decode 相对 PLENA 最高 2.55×/2.61×、相对 4×B200 最高 4.96×/12.56×"
tags:
- quantization
- mixed-precision
- systolic
- npu
- inference
- kv-cache
- energy
- accelerator
- llm
- numeric-format
- attention
- dataflow
created: 2026-11-09
updated: 2026-11-09
timestamp: '2026-11-09T00:00:00Z'
paper_author: [Boyang Chen, Xiao Wu, Haoran Wu, Yiren Zhao]
year: 2026
venue: arXiv preprint
arxiv: '2611.00915'
sources:
  - raw/papers/Coffee_Elastic_Precision_Mixed_Precision_LLM_2026.pdf
  - raw/papers/coffee-elastic-precision-mixed-precision-llm.md
---

# Coffee / Elastic Precision：长上下文混合精度推理架构

## 一句话结论
Imperial / Cambridge 提出 **Coffee**：在 PLENA 风格 **flattened systolic** 上，用当前 GEMM **两侧输入**估计输出误差并在线分配两侧位宽（服从离线平均 bit 预算）；同一读路径支持 attention 引导的 KV 读取与 V 跳过。质量上低于 BDQ/PLENA 困惑度、高于零样本均值（如 Llama-3-8B Avg4 WikiText-2 PPL **6.58** vs PLENA **6.95**，Avg acc **72.23** vs **69.63**）；系统模型长上下文 decode 相对重配 PLENA 最高 **2.55×** 吞吐 / **2.61×** 能效，相对 **4×B200** 基线最高 **4.96×** / **12.56×**。ASAP7 **1 GHz** 综合，最大宽度 **INT5**，在线决策逻辑约占核面积 **1.97%**。

## 动机
- 均匀低比特浪费精度：不同 GEMM tile / token 的量化敏感度不同。
- 既有混合精度多只自适应一侧输入；输出误差其实取决于当前 tile 的两侧操作数。
- 双侧在线估计与选宽在常规 GPU/NPU 上开销大，需要软硬协同把决策与搬运重叠。

## 方案
1. **离线预算 + 在线选宽**：校准给敏感计算更高平均 bit；运行时结合两侧输入估计候选宽度下的输出误差，在 tile 预算内向误差降幅更大的子阵列分配更多位。
2. **Flattened systolic 硬件**：沿用 PLENA 式阵列，直接支持所选宽度的访存与计算；误差估计/选宽与传输、计算重叠。
3. **Attention 引导 KV 读**：同一混合精度读路径在 decode 阶段按注意力重要性读 KV，并可跳过 V，降低带宽压力。
4. **实现**：最大支持宽度选 **INT5**；ASAP7 **1 GHz** 综合；在线决策相关逻辑约占核面积 **1.97%**。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Llama-3-8B Avg4 vs PLENA PQ4（Table 1） | WikiText-2 PPL **6.58** vs **6.95**；Avg zero-shot **72.23** vs **69.63** |
| 长上下文检索（Table 2） | 相对 PLENA 在多模型上匹配或更好 |
| vs 重配 PLENA（Table 3，长上下文 decode） | 吞吐最高 **2.55×**；能效最高 **2.61×** |
| vs 4×B200 基线（Table 3） | 吞吐最高 **4.96×**；能效最高 **12.56×** |
| 综合 / 面积 | ASAP7 **1 GHz**；在线决策逻辑 **~1.97%** 核面积；最大宽度 INT5 |

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 运行时双侧混合精度与 INT5 上限
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — flattened systolic / PLENA 式阵列
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — attention 引导 KV 读与带宽预算
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — decode 侧 KV 路径与稀疏读
- [Mixed Precision Training](/concepts/mixed-precision-training.md) — 训练混合精度对照；本文聚焦推理在线位宽

## 开放问题
- 系统吞吐/能效数字来自建模（相对 B200 实测四卡），硅片端到端仍待验证。
- 在线估计对更广模型族与 agentic 长上下文负载的泛化空间可继续压测。

# Citations
- [arXiv:2611.00915](https://arxiv.org/abs/2611.00915) — Chen, Wu, Wu, Zhao；Imperial / Cambridge
- [raw stub](/raw/papers/coffee-elastic-precision-mixed-precision-llm.md)
