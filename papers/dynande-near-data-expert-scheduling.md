---
type: Paper
title: "DynaNDE: Dynamic Near-Data Expert Scheduling for Batched MoE Inference"
description: IIT — NPU–NDP 分析模型+reuse-aware 调度；vs MoNDE prefill/decode 平均 2.6×/2.2× 吞吐（仿真）
tags:
- moe
- inference
- cxl
- scheduling
- memory
- accelerator
- llm
- throughput
- interconnect
- batching
- expert-parallelism
- serving
- architecture
timestamp: '2026-09-03T00:00:00Z'
created: 2026-09-03
updated: 2026-09-03
sources:
- raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf
- raw/papers/dynande-near-data-expert-scheduling.md
---

# DynaNDE: Dynamic Near-Data Expert Scheduling for Batched MoE Inference

**Authors:** Xiaoyang Lu, Belthangady Akash Vi Narayana Pai, Xian-He Sun
**Affiliation:** Illinois Institute of Technology
**arXiv:** [2609.00407](https://arxiv.org/abs/2609.00407)（2026-09-01，cs.AR）
**Venue:** 预印本（文内 DOI 占位）。
**PDF:** [raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf](raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf)

相对 [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) 把 expert **驻留**在 ReRAM 近存池，本文假定 expert 在扩展内存、用 **NPU↔NDP 协作调度** 决定谁 PMove、谁 AMove。互连是 **PCIe Gen4×16 / CXL**，不是片上 NoC 或 chiplet D2D。

## 动机

Batched MoE 下专家参数搬运常主导延迟（文 Fig.1 DeepSeek 分解）。MoNDE 按固定 PCIe-to-NDP 带宽比把「热」专家丢 NPU，其余 NDP；忽略：NPU/NDP 算力差、PMove vs AMove 体积差、层内专家并发（prefill 可数百请求/专家，decode 骤降）、以及 decode 跨迭代的 expert 复用缓存。

## 方案

**三阶段争用回避执行流。** 共享 PCIe/CXL 上参数与激活不能同时抢：① 输入激活 AMove 到 NDP；② NPU 的 PMove–compute 流水与 NDP 计算重叠；③ 全部 PMove 结束后输出 AMove，并与末个 NPU expert 计算取 max。

**分析模型。** 对每专家算 \(T_{\mathrm{NPU}}\)、\(T_{\mathrm{NDP}}\)、reuse-aware \(T_{\mathrm{PMove}}\)（已在 NPU 缓存则 0）；层延迟 \(T_1+T_2+T_3\)。

**调度。** score \(s(i)=T_{\mathrm{NDP}}(i)-(T_{\mathrm{NPU}}(i)+T_{\mathrm{PMove}}(i))\) 降序；前缀扫描 \(p=0..|E|\) 选最小 \(T_{\mathrm{layer}}\) 的 NPU 子集。复杂度排序后 \(O(|E|\log|E|)\)。主机侧运行时；NDP 指令接口复用 MoNDE，不改 datapath。

**系统配置（Table 2）。** NPU：4×128×128 MAC @1 GHz。NDP：64×4×4 MAC、264 KB buffer、512 GB/s、512 GB。互连 PCIe Gen4×16。默认 NPU expert 缓存 = 专家总数 **10%**（LFU）。基于 NeuPIMs + DRAMSim3 周期精确仿真。模型：Switch-Base-64、FLAME-MoE、DeepSeek-V2-Lite；默认 batch 32；decode 生成 10 token。

## 效果（仅论文数字）

**相对 MoNDE（摘要）：** prefill 平均 **2.6×**，decode 平均 **2.2×** 吞吐。

**Prefill（Fig.8，相对 NPU 归一化）：** vs NPU/NDP/MoNDE/HybriMoE 平均 **1.8× / 2.9× / 2.6× / 1.1×**。Switch-Base（top-1）对 NPU 最高可达 **3.8×**。

**Decode（Fig.9）：** vs 同四基线平均 **30.5× / 1.1× / 2.2× / 1.4×**。相对 HybriMoE：DynaNDE 把产生 PMove 的 NPU 分配压到激活专家的 **3.6%**（HybriMoE **5.3%**），总 NPU 分配 **10.7%** vs **13.7%**——不是靠堆 NPU 占比。

**批大小 / 缓存。** Decode BS 16/32/64 vs MoNDE **2.1×/2.2×/1.8×**，vs HybriMoE **1.2×/1.4×/1.1×**。无 reuse 变体 N-DynaNDE 仍平均优于 MoNDE **2.0×**、HybriMoE **1.3×**；reuse 再给 DynaNDE 相对 N-DynaNDE 约 **1.1×**。

**开销。** NDP 核 28 nm @1 GHz：**2.95 mm²**、**1.81 W**。调度在主机，不改 NDP 硬件路径。

## 与 wiki 的关系

- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 驻留 ReRAM FFN 池；本文是 offload + 异构调度
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) / [FLINT](/papers/flint-hbf-llm-inference.md) — HBF 容量路径；本文是 CXL-NDP 近存算
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 把 CXL 从页迁移扩展到 **MoE expert 近数据执行**
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — NPU vs NDP 角色异构 + 分析模型调度
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 专家执行位置的动态拆分，不是 PD 机柜解耦

## 开放问题

1. 单 NDP；多 NDP 的放置/激活路由/共享带宽协调留作 future work。
2. 仿真器 + 合成配置；无真实 CXL-NDP 硅或商用 PIM 卡对照。
3. Decode 只跑 10 token 观察 reuse；更长生成下缓存命中曲线未给。
4. HybriMoE 是从 CPU–GPU 逻辑改编到 NPU–NDP，原论文场景不完全等价。

# Citations

[1] [raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf](raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf) — Lu et al., arXiv:2609.00407
[2] [raw/papers/dynande-near-data-expert-scheduling.md](raw/papers/dynande-near-data-expert-scheduling.md) — 结构化摘录
