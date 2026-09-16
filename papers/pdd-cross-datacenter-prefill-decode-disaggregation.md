---
type: Paper
title: "PDD: Cross-Datacenter Prefill-Decode Disaggregation"
description: Infinigence/清华等 — Prefill+RelayDecode+MainDecode 跨 DC；H100×H200 映射 SLA goodput BCR 最高 +37.5%
tags:
- disaggregated-inference
- prefill
- decode
- kv-cache
- serving
- serving-system
- llm
- inference
- latency
- throughput
- rdma
- datacenter
- interconnect
- agentic-ai
- ai-agent
- architecture
timestamp: '2026-09-16T00:00:00Z'
created: 2026-09-16
updated: 2026-09-16
sources:
- raw/papers/PDD_Cross_Datacenter_Prefill_Decode_Disaggregation_2026.pdf
- raw/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md
---

# PDD: Unleashing Economical and Flexible Heterogeneous LLM Inference via Cross-Datacenter Prefill-Decode Disaggregation

**Authors:** Yida Wang, Xiuhong Li, Jianping Ma, Gan Sun, Yunshen Xu, Buhe Han, Jingxu Ng, Yuhao Luo, Ke Hong, Guohao Dai#, Boxun Li#, Yu Wang#（#通讯）
**Affiliation:** Infinigence-AI / Tsinghua / Shanghai Jiao Tong / Peking University
**arXiv:** [2609.13161](https://arxiv.org/abs/2609.13161)（cs.AR/cs.DC；Tue 2026-09-15 列表）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.13161)

相对机柜内 [Disaggregated Inference](/concepts/disaggregated-inference.md) / [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) 的同域 PD，PDD 把解耦拉到 **跨机房 WAN Ethernet**，并用 **RelayDecode** 掩盖 KV 传输，服务对 TTFT 敏感的 **agentic** 负载。

## 动机

地理分散集群用广域 Ethernet 互联，可避免专建同机房异构集群。但跨 DC 搬 KV 抬高 TTFT；**长上下文、高缓存命中、短输出** 的 agentic 工作负载尤其受损。

## 方案

三层 PD：**Prefill**、**RelayDecode (RLD)**、**MainDecode (MD)**。

- Cluster A：Prefill 计算后经 **高速 RDMA** 立刻把 KV 交给同集群 RLD **开始 decode**，同时经 **TCP Ethernet** 向 Cluster B 传 KV。
- Cluster B：MD 收到 KV 与 RLD 已产出 token 后 **handoff** 接续 decode。
- 机制：Decode-side **RadixCache** 减压带宽；**Extend-Decode Handoff**；多阶段 pipeline 编排高并发依赖。
- 部署：算力向 **H100**、内存带宽向 **H200** 的跨 DC 异构映射。

## 效果（仅论文数字）

- 相对 **机房内同构 PD** 基线：跨 DC 映射 H100+H200 在 SLA-compliant goodput 上的 Benefit-Cost Ratio (**BCR**) 最高 **+37.5%**。

**口径提醒：** 系统/部署论文；BCR 为文内定义的效益-成本比，勿与单卡 tok/s 横比。PDF 页眉日期戳与 2609 id 不一致，以 arXiv id / 列表日为准。

## 与 wiki 的关系

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 从同 DC 池扩展到 **跨 DC + RLD 重叠**
- [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md) — 相位分歧在 WAN 上的代价
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — H100/H200 角色分工
- [Heterogeneous Computing for AI Agent Inference](/papers/heterogeneous-computing-ai-agent-inference.md) — agentic TTFT/容量墙动机对齐

## 开放问题

1. WAN 抖动下 RLD→MD handoff 的尾延迟界。
2. RadixCache 与跨 DC 前缀命中率的交互未在摘要展开。
3. 与同 DC RDMA-only PD 的纯延迟对照数字需读正文表。

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.13161) — Wang et al., arXiv:2609.13161
[2] [raw/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md](raw/papers/pdd-cross-datacenter-prefill-decode-disaggregation.md) — 结构化摘录
