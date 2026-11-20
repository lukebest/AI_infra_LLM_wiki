---
type: Paper
title: "Chimera: A Configurable LLM Decode Accelerator for HBM Multi-Die FPGAs"
description: "UC Irvine — Alveo U280 实测十个设计；同板 Llama-3.2-1B W4 相对 FlexLLM 2.08×；相对四篇先前 FPGA 几何均值 1.6×，tok/J 相对 3090/A100 为 3.0×/1.5×（batch 1）"
tags:
- fpga
- decode
- hbm
- accelerator
- moe
- inference
- energy
- attention
- llm
- serving
created: 2026-11-19
updated: 2026-11-20
timestamp: '2026-11-19T00:00:00Z'
paper_author: [Zhiheng Chen, Yifan Zhang, Yu-An Chou, Ye Qiao, Sitao Huang]
year: 2026
venue: preprint
arxiv: '2611.21677'
sources:
  - raw/papers/Chimera_FPGA_LLM_Decode_2026.pdf
  - raw/papers/chimera-fpga-llm-decode.md
---

# Chimera：在带 HBM 的多裸片 FPGA 上把计算、访存和布局一起做完的 decode 加速器

## 一句话结论
UC Irvine 在 AMD Alveo U280 上实现了可配置的 LLM decode 加速器 Chimera：用 HBM Proxy Ports 把带宽送到每一块 SLR 上的计算道，并用分层专家存储把超出 HBM 的 MoE 权重放到 DDR4 / 主机内存 / NVMe。十个设计覆盖八个模型，最大到 80B 混合 MoE。同板同模型上，Llama-3.2-1B W4 为 **301.1 tok/s**，是 FlexLLM **144.7** 的 **2.08×**。作者按四篇先前 FPGA 发表数字取几何均值，吞吐为 **1.6×**；batch 1 下能量效率（tok/J）相对 RTX 3090 **3.0×**、相对 A100 **1.5×**。

## 动机
单请求自回归 decode 反复读权重和 KV，受内存带宽限制，GPU 算力用不满、功耗却不低。带 HBM 的 FPGA 可以用定制数据通路更省电地吃带宽，但要把带宽用满，计算道和存储接口都要占逻辑与布线；在多裸片 FPGA 上，靠近 HBM 的 SLR 先被接口占满，远处的计算还要跨片连线，往往一块裸片的资源先耗尽。

## 方案
三件事一起设计：计算道、存储访问、楼层规划。HBM Proxy Ports 把 HBM 访问延伸到每块 SLR 上的计算道；分层专家存储按速度把 MoE 权重放在 HBM、板上 DDR4、主机内存和 NVMe 四级。一套配置分析估计每 token 延迟和每 SLR 资源，并在资源预算内给出各配置。实现用 TAPA 与 Vitis/Vivado 2023.1。

十个设计、八个模型，全部 A8 激活，KV 与循环状态在 HBM，上下文最长 4K：稠密 Llama-3.2-1B / Llama-3.1-8B，MoE Qwen1.5-MoE-A2.7B / Qwen3-Coder-30B-A3B，混合 Granite-4.0-H-1B 与混合 MoE Qwen3-Next-80B-A3B，以及三元 BitNet b1.58-2B、Ternary-Bonsai-27B。吞吐是 WikiText-2 上的墙钟 decode 速率，三次中位数（U280 上三次相差不到 1%）。GPU 基线是 vLLM、batch 1、CUDA graphs，权重位宽与板上一致。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 同板同模型 | Llama-3.2-1B W4：**301.1 tok/s** vs FlexLLM **144.7**，**2.08×**（FlexLLM 的 8 个上下文/decode 长度上为 2.04–2.09×）。内核 200 MHz，FlexLLM 为 292 MHz，HBM 带宽相同 | §V / Table III(b) |
| 相对四篇先前 FPGA 的几何均值 | **1.6×**。构成包括 FlexLLM（同板同模型），以及 FlightLLM（U280、LLaMA2-7B sparse，55 tok/s）、EdgeLLM（VCU128、ChatGLM2-6B，51.4 tok/s）、LUT-LLM（V80、Qwen3-1.7B W2A3，约 196 tok/s，且为无 LM head 的单 block RTL 共仿真）。4-bit Llama-3.1-8B 相对后两篇发表速率为 **1.36× / 1.45×** | §V |
| BitNet b1.58-2B | U280 **249.4 tok/s**，相对 PENSA 在 U50 上的 58.1 约为 **4.3×** | §V |
| 能量与吞吐（几何均值，batch 1） | tok/J 相对 RTX 3090 **3.0×**、相对 A100 **1.5×**。U280 带宽约为二者的 49% 与 30%，吞吐几何均值为 **70%** 与 **52%**。U280 板卡 58–76 W，两块 GPU 117–348 W | §V / Table I / Table III(a) |
| 代表点（上下文 512、decode 256；U280 tok/s） | Llama-3.1-8B W4 **74.7**；Qwen3-Coder-30B-A3B FP8 **26.8**（快于 3090 的 24.8，低于 A100 的 158.4）；Qwen3-Next-80B-A3B W4 **29.3**、FP8 **24.5**（FP8 快于 3090 的 16.0 与 A100 的 22.0） | Table III(a) |
| 专家未命中 | 等待时间占 Qwen3-Coder 的 32%、FP8 Qwen3-Next 的 27%、4-bit Qwen3-Next 的 13%。提前拷贝下一层专家后，驻留 HBM 的已选专家从 81% 升到 92%，上下文 ≤512 时吞吐 **+19.9%** | §V |
| 协同设计消融（Llama-3.1-8B W4） | 完整设计 30 道 **74.7 tok/s**，为早期 HLS 原型（22 道）的 **1.7×**。去掉 Proxy Ports 后 65.7 tok/s；15 个伪通道共享时 42.3 tok/s | Table II(b) |
| 量化质量 | 与所实现的量化 Hugging Face 模型相比，WikiText-2 PPL 平均差 0.17%，MMLU 平均差 0.3 分 | Table IV |

## 与已有页的增量
Wiki 里 decode 加速器与解耦推理的讨论，多数落在 GPU / NPU / 预硅 ASIC 上，例如 [Exstill](/papers/exstill-single-chip-next-token.md)、[SiliconForge](/papers/siliconforge-should-you-split-decode.md)。本篇提供一块带 HBM 的多裸片 FPGA 上的可复现板上结果，并覆盖 MoE 与混合注意力，以及专家超出 HBM 时的四级存储。与 GPU 的能量对照限定在 batch 1、上下文最长 4K；1.6× 的 FPGA 几何均值里，有三项对照的模型或板卡与本设计不同，宜与同板 FlexLLM 的 2.08× 一起读。

## 与 wiki 的关系
- [HETEROVLM](/papers/heterovlm-versal-aie-vlm-serving.md) — 同一组在 Versal AIE + PL 上做多请求 VLM 服务与抢占
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) — 针对单请求 decode 带宽墙做定制数据通路
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM Proxy Ports 与 DDR4 / 主机 / NVMe 四级专家存储
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — FPGA 上的可配置计算道与布局约束
- [Exstill](/papers/exstill-single-chip-next-token.md) — 同属单用户 / 低批次 decode 能效问题，实现栈不同

## 开放问题
- 全部端到端数字是 batch 1、上下文最长 4K 的 decode；更大 batch 或更长上下文下，FPGA 相对 GPU 的位置会变化。
- 与 FlightLLM、EdgeLLM、LUT-LLM 的 1.6× 几何均值跨越不同模型、板卡，LUT-LLM 还是共仿真；更干净的对照是同板 FlexLLM 的 2.08×。
- Qwen3-Coder 在 A100 上专家仍能放进显存（158.4 tok/s），U280 为 26.8 tok/s，容量墙在 GPU 侧并不对称。
- 配置分析在专家落到 HBM 之外时，若改用标称峰值带宽，误差会升到 23–35%。

# Citations
- [arXiv:2611.21677](https://arxiv.org/abs/2611.21677) — Chen, Zhang, Chou, Qiao, Huang（UC Irvine）
- [raw stub](/raw/papers/chimera-fpga-llm-decode.md)
- [PDF](/raw/papers/Chimera_FPGA_LLM_Decode_2026.pdf)
- [arXiv:2611.23878](https://arxiv.org/abs/2611.23878) — HETEROVLM
