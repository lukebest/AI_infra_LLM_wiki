---
type: Summary
title: 'SuperInfer: SLO-Aware Rotary Scheduling on Superchips'
description: UIUC SuperInfer — RotaSched + DuplexKV on GH200 NVLink-C2C; up to 74.7% higher TTFT SLO attainment under KV pressure vs PCIe offload stacks
tags:
- inference
- serving
- kv-cache
- scheduling
- memory
- gpu
- latency
- throughput
- serving-system
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf
---

# SuperInfer: SLO-Aware Rotary Scheduling on Superchips

**Authors:** Jiahuan Yu, Mingtao Hu, Zichao Lin, Minjia Zhang | **Affiliation:** UIUC | **PDF:** [raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf](raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf)

## 一句话总结

SuperInfer 为 GH200 等 **superchip**（NVLink-C2C ~900 GB/s）联合设计 **RotaSched**（按 SLO 进度主动轮转 KV 于 HBM/DRAM）与 **DuplexKV**（全双工 KV 迁移引擎），高负载下 TTFT SLO 达成率最高 **+74.7%**，且 TBT/吞吐与 SOTA 相当。

## 核心贡献

1. **Superchip 瓶颈诊断**：直接移植 PCIe offload 仅利用 **<5%** C2C 带宽 — 根因在软件栈而非硬件
2. **RotaSched**：OS 式 proactive rotary scheduling，用 Virtual Lag Time 按 TTFT/TBT 紧迫度轮转请求
3. **DuplexKV**：合并碎片化 paged KV、全双工无竞态传输、与模型执行 overlap
4. **SLO-aware memory co-design**：突破仅 priority reorder 的 SLO 调度，在 superchip 上缓解 HOL blocking
5. **GH200 全栈评估**：高负载 TTFT SLO **+74.7%**；低负载无退化

## 关键数字

| 设置 | 结果 |
|------|------|
| TTFT SLO attainment (high load) | Up to **+74.7%** vs SOTA |
| NVLink-C2C bandwidth | **~900 GB/s** (vs PCIe **32–64 GB/s**) |
| PCIe offload on GH200 | **<5%** C2C utilization |
| TBT / throughput | Comparable to baselines |

## 与 wiki 交叉引用

- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — KV 压力下 batch/排队与 SLO 冲突
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — paged KV 基线；SuperInfer 解决 scatter 迁移开销
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — GPU–CPU 异构 offload 谱系
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — TTFT vs TBT 双 SLO 维度
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 服务层调度与内存分层

# Citations

[1] [raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf](raw/papers/SuperInfer_SLO_Aware_Rotary_Scheduling_Superchips_2026.pdf) — Yu et al. (2026)
[2] [raw/papers/superinfer-slo-aware-rotary-scheduling.md](raw/papers/superinfer-slo-aware-rotary-scheduling.md) — 结构化摘录
