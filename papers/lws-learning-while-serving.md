---
type: Paper
title: "LWS: Learning While Serving for Inference-Time Learning Accelerators"
description: "弗吉尼亚大学 — 建模数据中心/边缘 NPU（预算对标 TPU v5e / Jetson AGX Orin）；九模型平均相对串行 1.6×、相对最强共执行基线 1.3× 且保持 Prediction-only 吞吐；TTT-E2E 3B@128K 保留 fully fresh 质量收益的 99.3%；16 nm 综合，含 SRAM 后核心面积 +1.5% / +2.7%"
tags:
- accelerator
- npu
- inference
- prefill
- llm
- attention
- nonlinear
- microarchitecture
- chip-design
- sram
- hbm
- edge
- energy
- throughput
- latency
- architecture
created: 2026-11-18
updated: 2026-11-18
timestamp: '2026-11-18T00:00:00Z'
paper_author: [Yimin Gao, Liangtao Dai, Melika Morsali, Junting Huo, Mircea Stan]
year: 2026
venue: arXiv preprint
arxiv: '2611.18523'
sources:
  - raw/papers/Mutable_Inference_LWS_2026.pdf
  - raw/papers/lws-learning-while-serving.md
---

# LWS：在推理加速器的空闲矩阵能力里做推理期学习

## 一句话结论
弗吉尼亚大学提出 **Learning While Serving（LWS）**，让推理加速器在服务（Prediction，前向）的同时做推理期学习（Learning，反向与权重更新）。硬件管理的**按层权重版本**允许 Learning 发布新权重、正在进行的计算仍读旧版本；**可恢复规约块**让 Learning kernel 跨过碎片化的空闲窗口，并向 Prediction 让路；**专用 softmax 梯度单元**减轻向量争用。在对标 TPU v5e / Jetson AGX Orin 预算的建模数据中心与边缘 NPU 上，LWS 把 Learning 藏进 Prediction 的空闲能力，九个模型都保持 Prediction-only 吞吐（η=**1.00**），平均是串行执行的 **1.6×**、最强先有共执行基线（Equinox）的 **1.3×**。TTT-E2E 3B 在 128K 上，按层策略 `1111|0000`（平均滞后 0.5 个 chunk）保留 fully fresh Learning 的 NLL 收益的 **99.3%**。16 nm RTL 综合给出新增逻辑 **1.47 mm²**；计入片上 SRAM 后，分别占数据中心 / 边缘 NPU 核心面积的 **1.5% / 2.7%**，不必再加一块 MAC 阵列。评测是单条长上下文的 chunked prefill，批量服务与自回归 decode 不在范围。

## 动机
长上下文若走完整注意力，每增加一枚 token 代价上升。推理期学习（ITL）在推理过程中对上下文做训练，把学到的内容写回权重，从而只对最近的固定窗口做注意力，并仍接近全上下文质量。这会在前向之外加上反向与权重更新。现有推理加速器假定权重固定，训练加速器则面向完整训练步。作者看到两处空隙：注意力的非矩阵运算会留下足够的空闲矩阵能力给 Learning；部分层对权重更新滞后不敏感。

## 方案
1. **版本化权重**：按层管理可见性截止时间，Prediction 可以读较旧版本，Learning 按层发布更新。
2. **可恢复执行**：Learning 的规约块可在短空闲窗口里推进、在 Prediction 需要硬件时挂起并保留部分和。
3. **专用 datapath**：为 softmax 梯度提供 dS/dZ 单元，减轻与 Prediction 的向量 / SFU 争用。
4. **对照**：串行（TTT-E2E 参考日程，一个 chunk 的 Prediction、Learning、更新全部完成后再做下一个）；DaCapo（静态划分）；Neu10（租借空闲引擎）；Equinox（指令交织）。三者都留一份上一 chunk 的权重，且没有按层可见性截止。
5. **评测方法**：统一的操作级仿真（含 Ramulator 2，数据中心用 HBM2、边缘用 LPDDR5）；矩阵延迟与抢占开销来自并行 MXINT8 MAC 的 RTL 仿真；面积来自 16 nm、1 GHz 综合与 SRAM 宏，并对配备 LWS 的计算组做了摆放。

## 效果（论文数字）
主工作负载是 TTT-E2E 3B（32 层、最后 8 个 MLP 可更新，1024-token chunk，8192-token 注意力窗口），在 Books3 验证集的 32K / 64K / 128K 上评质量。另外把同一套 Learning 工作负载映射到 BLOOM 3B、Gemma-3 4B、Phi-4 mini、Llama-3.1 8B、Qwen3 8B、Ministral 8B、Mistral-Nemo 12B、Gemma-3 12B；并用 LaCT 与 online LoRA 看方法通用性。

**吞吐与能量（九模型平均，η 相对同一 NPU 上的 Prediction-only）**

| 设计 | 数据中心 η / 边缘 η | 额外 Learning 能量（数据中心 / 边缘） |
|---|---:|---:|
| 串行 | 0.64 / 0.63 | 52.4% / 52.1% |
| DaCapo | 0.69 / 0.70 | 50.9% / 48.2% |
| Neu10 | 0.74 / 0.69 | 49.7% / 49.0% |
| Equinox | 0.75 / 0.77 | 51.6% / 47.6% |
| LWS | **1.00 / 1.00** | **37.6% / 29.3%** |

数据中心上，这相当于相对串行 **1.6×**、相对 Equinox **1.3×**。TTT-E2E 3B 在建模数据中心 NPU 上为 **7,046** prompt token/s，Equinox **5,575**，串行 **4,861**。

**质量（TTT-E2E 3B，Books3 上 16 条序列，保留 fully fresh 相对「无 Learning」的 NLL 收益）**
- 策略 `1111|0000`（输入侧 4 层滞后 1、输出侧 4 层滞后 0，平均 0.5 chunk）：32K / 64K / 128K 保留 **97.60 / 98.72 / 99.34%**（正文取 128K 的 **99.3%**），优于统一滞后 1。
- 冻结输入侧 4 个可更新层只保留 **76.2%**。
- 完全新鲜的 Learning 保留全部质量收益，但 Prediction 吞吐降到 η=**0.84**。
- 建模 NPU 用 MXINT8 矩阵与更高精度的权重更新；TTT-E2E 3B@128K 上相对 BF16 软件参考，额外 NLL 不到 **0.001**。
- LaCT 在原生 lag-0 下，LWS 保持满吞吐并保留 **100%** 收益；Equinox 要靠整模型滞后 1 才到满吞吐，保留 **92.8%**。

**面积（16 nm 综合，相对基线计算逻辑 44.41 mm²）**
- LWS 新增逻辑合计 **1.47 mm²**（**3.3%**），其中数据中心 8 个配备组上的 dS/dZ、stash、Learning Engine slice 等为主要增量，不必再加 MAC 阵列。
- 计入片上 SRAM（数据中心 32 MB，边缘 4 MB）后，新增逻辑占核心面积 **1.5% / 2.7%**。

**扫描**：96 组 TTT-E2E 类配置（模型 1B/3B/8B、可更新层深度、chunk、优化器、数据中心/边缘）里，LWS 在 **94 / 96** 组达到吞吐屋顶线。

## 与 wiki 的关系
- [核内非线性运算加速](/concepts/in-core-nonlinear-operator-acceleration.md) — 专用 softmax 梯度（dS/dZ）单元，专门给 Learning 减轻向量争用
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 在已有 MAC 阵列上做可恢复共享，不再加一块阵列
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 评测落在 chunked prefill；decode 明确不在范围
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 与「推理期空闲算力」同一类问题，对象换成 NPU 上的 Prediction / Learning 共执行
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — Learning 的梯度与权重流量走 Prediction 留下的空闲 DRAM 带宽

## 开放问题
- 结果来自操作级仿真 + 16 nm RTL 综合与摆放，不是硅上整芯片。
- 数据中心 / 边缘配置是「代表 TPU v5e / Jetson AGX Orin 的算力与内存预算」，不是这两款产品的 quant。
- 只评了单条长上下文的 chunked prefill；批量服务与自回归 decode 留待后续。
- 质量保留在 Books3 的 16 条序列上测量；八个额外模型主要看吞吐，Learning 工作负载是从 TTT-E2E 映射过去的。
- 当 Learning 的资源需求超出 Prediction 空闲能力时，吞吐仍受该资源屋顶约束（96 组里有 2 组未到屋顶线）。

# Citations
- [arXiv:2611.18523](https://arxiv.org/abs/2611.18523) — Gao, Dai, Morsali, Huo, Stan；University of Virginia
- [raw stub](/raw/papers/lws-learning-while-serving.md)
