---
type: Paper
title: "AInfer-PD: Communication-Safe In-Place Prefill–Decode Multiplexing for Distributed MoE"
description: Ant — MoE rollout 同机 P/D 复用；turnstile 排交叉集体 + DeepEP 相位私有态；vs Normal −7.1–22.5%、vs SGLang −24.8–32.9%（H20）
tags:
- moe
- llm
- inference
- serving
- disaggregated-inference
- prefill
- decode
- communication
- architecture
- latency
- throughput
- parallelism
- serving-system
timestamp: '2026-09-04T00:00:00Z'
created: 2026-09-04
updated: 2026-09-04
sources:
- raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf
- raw/papers/ainfer-pd-inplace-prefill-decode-moe.md
---

# AInfer-PD: Communication-Safe In-Place Prefill–Decode Multiplexing for Distributed MoE Rollouts

**Authors:** Guowei Wang, Chaokun Yang, Zhenxuan Pan, Yuhong Guo, Minghua Zhu, Zhechuan Zhang, Shuo Wan, Xiaowei Zhu
**Affiliation:** Ant Group
**arXiv:** [2609.00993](https://arxiv.org/abs/2609.00993)（2026-09-01，cs.DC）
**Venue:** 预印本
**PDF:** [raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf](raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf)

相对 DistServe/Splitwise 的 **PD 解耦**（独立池 + KV 搬运），本文走 **in-place 复用**：同设备共享权重与 KV，但补上大 MoE 缺失的 **通信隔离**——交叉 ADP/ATP 集体排序 + DeepEP normal/low-latency 相位私有态。对照 wiki [Disaggregated Inference](/concepts/disaggregated-inference.md) 表中「阶段层解耦」一行：这是同池并发的安全补丁，不是第二套模型实例。

## 动机

- Agentic RL rollout：多轨迹工具往返 → continuation prefill 与 decode **长期共存**，不是一次性 prompt 摄入。
- 同加速器上长/变长 P 批次干扰延迟敏感 D，拉长固定工作集 makespan。
- 常见实现：P 走 model-wide TP AllReduce，图回放 D 走 DP-attention ReduceScatter/AllGather；交叉 group + 相位偏斜可形成 **跨 rank 进度环**。DeepEP 的 normal-P 与 low-latency-D 共享可变协议态，原设计非并发租户。

## 方案

1. **In-place 调度**：rank 共享 planner 优先准入 D，剩余 batch/KV 容量给 P；共享权重与 KV。
2. **Segment turnstile**：P 按后端通信安全边界切段；每轮各 rank 一致：到边界 → PreDRendezvous → 入队 D → PostDRendezvous → 放行下一 P segment（不等 P GPU 完成）。
3. **Selective device order**：冲突的 P full-TP AllReduce 挂到 D 图启动流上，保证 \(D \prec P\)；非交叉通信保持异步。
4. **DeepEP 相位私有**：P-owned / D-owned 各自 buffer、counter、workspace、event、QP 区间；通知后拆分边界，P 数据搬运需计数 + turnstile 许可。
5. **评测**：匿名内部 RL 轨迹；H20-3E 单节点 8 GPU / 双节点 16 GPU；对照 AInfer Normal（关复用）与 SGLang。

## 效果（仅论文数字）

**单节点 prefill-intensive（Figure 7，H1–H4）：**

| 对照 | Makespan 降幅 |
|------|----------------|
| vs AInfer Normal | **7.1% / 8.7% / 21.5% / 22.5%** |
| vs SGLang | **24.8–32.9%** |

H1–H2 走交叉 ADP/ATP；H3–H4 ATP1，主要量 in-place 调度本身。

**双节点（Table 6）：** vs Normal **18.0–35.3%**；vs SGLang **18.3–31.8%**。相对 Normal，p99 TTFT 可升 **13.2–37.9%**（完成时间优先准入的权衡）。

**同引擎排序阶梯（Table 5，交叉拓扑）：** Fine-grained 相对 Global-Enqueue 再减 **8.6%**（trace-wait）/ **19.8%**（no-wait）；D wait 从 ~114–127 ms 降到 ~17–18 ms。

**DeepEP：** 并发配置每 rank **465.2 MiB**（normal 140.2 + low-latency 325.0）；P 用 **12/132** SM。Live-RL 32 step 聚合 **−17.6%**（17.14→14.12 h；轨迹可发散，非成对证据）。

**实测** H20-3E / 诊断 H200；非新硅架构。

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 补「同池 P/D 复用 + 集体/DeepEP 隔离」一行，对照机柜 PD 解耦
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — 资源正交在同 GPU 上的系统后果
- [LEAP](/papers/leap-imc-noc-llm-inference.md) — 片上 PD 宏角色重配；本文是分布式 MoE serving 运行时
- [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md) — 集体排序/同步税；本文是交叉 communicator 死锁型
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — EP/TP 集体在推理 rollout 的并发变体

## 开放问题

1. 更大世界规模（数百 GPU）上 turnstile 会合开销是否仍可忽略？
2. 非 DeepEP 的其他 EP 运行时能否复用相位私有态模式？
3. 完成时间优先 vs TTFT SLO 的在线自适应分段策略？

# Citations

[1] [raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf](raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf) — Wang et al., arXiv:2609.00993
[2] [raw/papers/ainfer-pd-inplace-prefill-decode-moe.md](raw/papers/ainfer-pd-inplace-prefill-decode-moe.md) — 结构化摘录
