---
type: Paper
title: "FIGFLEX: A Mixed-Precision FP-INT GEMM Accelerator Co-Designed with Low-Bit LLM Quantization"
description: "UC Irvine — 权重量化 LLM 的 FP-INT GEMM 加速器：radix-4 移位加 + INT3 车道融合，吞吐随比特数下降而上升；3-bit 混合精度下单位面积吞吐比 AxCore 1.56×、比 FIGLUT 1.42×"
tags:
- accelerator
- quantization
- numeric-format
- llm
- inference
- chip-design
created: 2026-10-26
updated: 2026-10-26
timestamp: '2026-10-26T00:00:00Z'
paper_author: [Faraz Tahmasebi, Haocheng Xu, Andrew Trauger, Yomal Perera, Zhenyu Tang, Nael Chowdhury, Sitao Huang]
year: 2026
arxiv: '2610.30480'
sources:
  - raw/papers/FIGFLEX_Mixed_Precision_FP_INT_GEMM_2026.pdf
  - raw/papers/figflex-mixed-precision-fp-int-gemm.md
---

# FIGFLEX：与低比特 LLM 量化协同设计的混合精度 FP-INT GEMM 加速器

## 一句话结论
2–3 bit 混合精度量化省下了显存，硬件却没把少掉的比特变成少掉的计算。FIGFLEX 让比特并行数据通路的吞吐随权重比特数下降而上升，并配一个直接映射到该通路的量化器：LLaMA-2-7B 在 3/2 bit 平均精度下 WikiText-2 困惑度 **5.85 / 8.77**，3-bit 模型线性 GEMM 的整芯片单位面积吞吐比 AxCore **1.56×**、比 FIGLUT **1.42×**。

## 动机
- 权重量化后主负载是 FP 激活 × INT 权重（FP-INT GEMM）。
- GPU 先把权重反量化回 FP16 再进 tensor core，比特降低只省带宽；FIGNA/AxCore 固定单一精度；FIGLUT 能伸缩精度但走比特串行，并行化代价是查表规模指数增长。

## 方案
1. **radix-4 移位加重写 FP-INT 乘法**：每 2-bit 数字只产生一个部分积，部分积约减半；乘累加融合进一个精度可变的部分积归约树，PE 可跑 INT4/3/2/1，比特越低吞吐越高。
2. **INT3 高位车道融合**：radix-4 下 INT3 的最高位只占半条 2-bit 车道；把两个 INT3 权重配对、融合各自的单比特高位，回收闲置半车道。
3. **补偿感知混合精度量化器**：按 GPTQ 补偿不了的误差给每个通道组分配比特数；逐输入通道列缩放取 2 的幂，让缩放后激活避开 FP16 次正规数区，模型在加速器上与 GPU 上精度一致。
4. 基线 FIGNA/FIGLUT/AxCore 在同一流程重实现：Synopsys DC，NanGate 15 nm，1 GHz。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| LLaMA-2-7B WikiText-2 PPL（3 / 2 bit 平均） | **5.85 / 8.77**，低于 GPTQ、AWQ、SliM-LLM、AMQ、QuIP#（不微调） |
| 3-bit 混合精度线性 GEMM 整芯片吞吐/面积 | 比 AxCore **1.56×**，比 FIGLUT **1.42×** |
| INT4 下能效（TOPS/W） | 仍比 FIGNA 高 **1.18–1.50×** |

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 整数权重 + FP 激活这一格式组合的硬件代价
- [MX-like Tensor Core](/papers/mx-like-tensor-core-npu-codesign.md) — 同周块缩放格式路线；FIGFLEX 走整数权重 + 通道组可变比特路线
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — PE 内部乘法器结构对阵列密度的影响
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 偏带宽时低比特主要省带宽，prefill/大 batch 才吃到算力收益

## 开放问题
- 评测聚焦线性 GEMM 与 LLaMA-2-7B；attention、KV 路径和更大模型上的端到端收益未给。
- 15 nm 综合结果，缺少版图/存储子系统建模，整芯片带宽是否成为新瓶颈要看系统级评估。
- 激活仍是 FP16；与 FP8/FP4 激活或块缩放格式组合时 radix-4 通路怎么改未讨论。

# Citations
- [arXiv:2610.30480](https://arxiv.org/abs/2610.30480) — Tahmasebi et al., 2026
- [raw stub](/raw/papers/figflex-mixed-precision-fp-int-gemm.md)
