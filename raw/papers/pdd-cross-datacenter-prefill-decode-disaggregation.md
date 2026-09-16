---
type: Raw Source
title: "PDD: Unleashing Economical and Flexible Heterogeneous LLM Inference via Cross-Datacenter Prefill-Decode Disaggregation"
source_url: https://arxiv.org/abs/2609.13161
arxiv: '2609.13161'
ingested: 2026-09-16
sha256: 0f5d135319f72c0f68c00957ac66b5951519fedf69837fd640ebee48445a798f
---

# PDD: Cross-Datacenter Prefill-Decode Disaggregation

**Authors:** Yida Wang, Xiuhong Li, Jianping Ma, Gan Sun, Yunshen Xu, Buhe Han, Jingxu Ng, Yuhao Luo, Ke Hong, Guohao Dai, Boxun Li, Yu Wang
**Affiliations:** Infinigence-AI; Tsinghua; Shanghai Jiao Tong; Peking University
**PDF:** [PDD_Cross_Datacenter_Prefill_Decode_Disaggregation_2026.pdf](PDD_Cross_Datacenter_Prefill_Decode_Disaggregation_2026.pdf)
**arXiv:** [2609.13161](https://arxiv.org/abs/2609.13161)（cs.AR/cs.DC；Tue 9/15 列表）

## 问题

跨机房 WAN Ethernet 做异构 PD 解耦可省专用同机房异构集群，但 KV 跨集群传输抬高 TTFT；对长上下文、高缓存命中、短输出的 **agentic** 负载尤其伤。

## 方法要点

- 三层：Prefill + RelayDecode (RLD) + MainDecode (MD)。
- Cluster A：Prefill 后经高速 RDMA 立刻把 KV 交给同集群 RLD 开始 decode，同时 TCP Ethernet 向 Cluster B 传 KV；MD 接手后续 decode。
- Decode-side RadixCache；Extend-Decode Handoff；多阶段 pipeline；异构 H100（算力）× H200（带宽）跨 DC 映射。

## 摘录数字（仅论文给出）

- 相对机房内同构 PD 基线：跨 DC 映射 H100+H200 的 Benefit-Cost Ratio (BCR) 在 SLA-compliant goodput 上最高 **+37.5%**。
