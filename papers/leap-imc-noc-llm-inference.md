---
type: Paper
title: "LEAP: LLM Inference on IMC-NoC with Balanced Dataflow and Fine-Grained Parallelism"
description: NUS — IMC+NMC+INC 片上 mesh；LEAP-D 片上 PD 解耦；vs A100 ≥2.55× 吞吐/≥71.94× 能效，vs H100 LEAP-D 1.52×/24.91×（仿真）
tags:
- noc
- interconnect
- mesh
- accelerator
- memory
- llm
- inference
- kv-cache
- serving
- throughput
- latency
- architecture
- pipeline
- power
- batching
- prefill
- decode
- disaggregated-inference
- dataflow
timestamp: '2026-09-03T00:00:00Z'
created: 2026-09-03
updated: 2026-09-03
sources:
- raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf
- raw/papers/leap-imc-noc-llm-inference.md
---

# LEAP: LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism

**Authors:** Yimin Wang, Yue Jiet Chong, Xuanyao Fong
**Affiliation:** National University of Singapore (NUS)
**arXiv:** [2609.00857](https://arxiv.org/abs/2609.00857)（2026-09-01，cs.AR）
**Venue:** LEAP ICCAD'2025 的期刊扩展版（Comments: 11 pages, 15 figures）。
**PDF:** [raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf](raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf)

同组 [CHIPSMORE](/papers/chipsmore-cim-chiplets-llm-inference.md) 做 **CIM chiplet + UCIe + 层流水**；本文做 **单片 IMC–NMC–INC 统一 fabric + 片上 PD 解耦**。相对 [Collective-Capable NoC](/concepts/collective-capable-noc.md) 的 FlooNoC DCA，这里的 IRCU 是 LLM 专用 in-router 归约/DDMM，不是通用 AXI collective。

## 动机

IMC 吃静态权重（DSMM），但 attention 还有运行时动态矩阵（DDMM）。单 crossbar 通常只有 ~128×128，大矩阵分区后 NoC 上广播输入、收集 partial 成为主瓶颈。Prefill 算力密、decode 带宽密，同质宏上 decode 流水填不满（文中 LEAP-A decode 吞吐可比 prefill 低 **4–6×**）。

## 方案

**三层资源。** IMC PE 存静态权重；路由器内 NMC scratchpad + MAC 扛动态数据；IRCU（INC）做 in-network 归约与部分 DDMM。Macro = PE + router，2D mesh 可 tile 扩展。

**确定性集体数据流。** Broadcast / Reduce / ReduceScatter / E-ReduceScatter / AllReduce / AllGather / MAC（Table II）；编译期定路由，降低运行时仲裁。

**LEAP-A vs LEAP-D。** A：宏同质（scratchpad 32 KB），PD 共享。D：prefill 区保留 IMC；decode 区去掉 IMC、scratchpad 扩到 **64 KB**，把更多并发带宽给 KV/动态；prefill 期间 KV 传到 decode 区，与 AllGather 重叠、文称无额外关键路径开销。

**映射。** 注意力层映射到 \(2\lceil D/C\rceil \times 2\lceil D/C\rceil\) 宏区；KV 循环写入 scratchpad；层间蛇形，方便 autoregressive token 回灌。Batch 聚焦 **2**（边缘场景）；双请求时 decode 与下一请求 prefill 争 IMC，文内给层粒度让步规则。

**实现口径。** 数字部分 Verilog → Synopsys DC 45 nm + Innovus，再缩放到 7 nm；IMC 面积/功耗取自文献 RRAM 128×128；scratchpad CACTI；指令级 NoC 仿真器。**仿真，不是硅。**

## 效果（仅论文数字）

**Table VI（1024 input + 1024 output tokens）**

| | LEAP-A | LEAP-D | A100 | H100 |
|--|--------|--------|------|------|
| 8B tok/s | 202.25 | **446.18** | 78.36 | 274.26 |
| 8B tok/J | 19.21 | **20.84** | 0.2612 | 0.7836 |
| 13B tok/s | 120.62 | **255.17** | 47.86 | 167.51 |
| 13B tok/J | 11.45 | **11.92** | 0.1628 | 0.4786 |

摘要/正文归纳：相对 A100，LEAP-A **≥2.55×** 吞吐、**≥71.94×** 能效；相对 H100，LEAP-D **1.52×** 吞吐、**24.91×** 能效。

**宏功耗/面积（Table V，LEAP-A / LEAP-D prefill）。** IMC 面积 **72.06%**、功耗 **20.15%**；router 面积 **17.51%**、功耗 **56.32%**——数据移动与 on-the-fly 处理主导能耗。Decode 宏（无 IMC）：scratchpad 面积 54.35%、功耗 45.52%。

**行为。** LEAP-D 缩小 prefill/decode 吞吐差；关键路径上 IMC 很少主导，瓶颈在 IRCU 数据移动与 DDMM；64-bit packet + 16-way IRCU 落在文内 roofline 近前沿。Batching 改善 TTFT、抬高 TPOT（IMC 争用），与不 batch 互补。

## 与 wiki 的关系

- [CHIPSMORE](/papers/chipsmore-cim-chiplets-llm-inference.md) — 同组同日窗；chiplet+UCIe+层流水 vs 本文单片 IMC-NoC+片上 PD
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 3D 垂直 KVT / 侧向 AR 物理隔离；本文是平面 mesh 上 PE 角色重配
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — LEAP-D = **片上** PD 解耦，不是机柜 AFD
- [Collective-Capable NoC](/concepts/collective-capable-noc.md) — 对照 in-network 归约设计空间（DCA vs IRCU）
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — mesh + INC 作为 LLM 数据流一等公民
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构在 IMC / NMC / INC 角色，不是 GPU+LPU

## 开放问题

1. 全是仿真 + 45 nm→7 nm 缩放；无硅、无实测 NoC 拥塞 trace。
2. GPU 基线口径（频率/精度/框架）未与 CHIPSMORE 的 H100+vLLM INT8 表对齐，跨文不可直接比 tok/s。
3. Batch=2 边缘导向；云级大 batch 下 scratchpad/IMC 争用未扫。
4. LEAP-D 的 prefill:decode 宏比例如何随模型/SLO 自动配，文内以案例为主。
5. 与同组 CHIPSMORE 的 IPCN/UCIe 路线如何统一成 chiplet 级 LEAP，未讨论。

# Citations

[1] [raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf](raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf) — Wang/Chong/Fong, arXiv:2609.00857
[2] [raw/papers/leap-imc-noc-llm-inference.md](raw/papers/leap-imc-noc-llm-inference.md) — 结构化摘录
