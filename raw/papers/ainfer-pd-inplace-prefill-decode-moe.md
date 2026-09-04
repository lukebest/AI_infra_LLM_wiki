---
type: Raw Source
title: AInfer-PD — Communication-Safe In-Place Prefill–Decode Multiplexing for Distributed MoE Rollouts
source_url: https://arxiv.org/abs/2609.00993
arxiv: '2609.00993'
ingested: 2026-09-04
sha256: ac728b3741c06c74c9c9a9ae99752f777f8fbddf3d0bfeb6e5a8b7e134542b3b
---

# AInfer-PD: Communication-Safe In-Place Prefill–Decode Multiplexing for Distributed MoE Rollouts

**Authors:** Guowei Wang, Chaokun Yang, Zhenxuan Pan, Yuhong Guo, Minghua Zhu, Zhechuan Zhang, Shuo Wan, Xiaowei Zhu
**Affiliations:** Ant Group
**PDF:** [AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf](AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf)
**arXiv:** [2609.00993](https://arxiv.org/abs/2609.00993)（2026-09-01，cs.DC）

## 问题

Agentic RL rollout 中多轨迹异步：continuation prefill 与 decode 长期共存。PD 解耦要额外设备与 KV 搬运；in-place 复用共享权重/KV，但大 MoE 的 ADP/ATP 交叉集体与 DeepEP normal/low-latency 共享可变协议态会使 P/D 并发不安全。

## 方法要点

- Rank-aligned segment turnstile：按通信安全边界切 P，各 rank 一致顺序先入队 D 再放行 P segment。
- Selective stream 路由：冲突的 P full-TP AllReduce 排在 D 图启动之后，消除跨 rank 进度环。
- DeepEP 相位私有态：P 用 normal、D 用 low-latency；拆分通知后边界；独立 buffer/counter/QP 区间。
- 共享模型权重与 KV；H20-3E 单/双节点 + 内部 RL 轨迹回放。

## 摘录数字（仅论文给出）

- 单节点 prefill-intensive（H1–H4）：vs AInfer Normal makespan **−7.1–22.5%**；vs SGLang **−24.8–32.9%**。
- 双节点：vs Normal **−18.0–35.3%**；vs SGLang **−18.3–31.8%**（TTFT 有代价）。
- 同引擎消融：fine-grained 相对 whole-epoch enqueue 再减 **8.6–19.8%**。
- DeepEP 并发：normal NVLink payload 140.2 MiB/rank + low-latency RDMA 325.0 MiB = **465.2 MiB**；P 用 12/132 SM。
- Live-RL 32 step 聚合 wall-clock **−17.6%**（17.14→14.12 h，轨迹可发散）。
- 实测 H20-3E / H200 诊断；非硅新架构。
