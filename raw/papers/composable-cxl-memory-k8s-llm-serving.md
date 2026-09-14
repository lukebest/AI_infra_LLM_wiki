---
type: Raw Source
title: "Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving"
source_url: https://arxiv.org/abs/2609.10790
arxiv: '2609.10790'
ingested: 2026-09-14
sha256: f79b6eb4e81541a67ba2a200c8f8e016722fe25d1f034750a487aa8b5a7c63e2
---

# Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving

**Authors:** Hongjian Fan, Kevin Zhang, David Habinsky, Sean Dykstra
**Affiliation:** Seagate Technology Research
**PDF:** [Composable_CXL_Memory_K8s_LLM_Serving_2026.pdf](Composable_CXL_Memory_K8s_LLM_Serving_2026.pdf)
**arXiv:** [2609.10790](https://arxiv.org/abs/2609.10790)（2026-09-09，cs.DC）

## 问题

跨节点 KV/prefix 复用需要共享容量层；普通本机 GPU/CPU 前缀缓存无法跨机命中。

## 方法要点

- Kubernetes DRA driver：按需组合 CXL 区域 → 各主机 DAX → 统一 CDI 名注入 pod。
- vLLM/llm-d shared-memory connector：共享介质内嵌 slot directory，无需外置元数据服务。
- 两副本全引擎；强调 **内存解耦** 而非 P/D 解耦。作者自称 feasibility study。

## 摘录数字（仅论文给出）

- 双节点 + **512 GiB** CXL appliance，Qwen2.5-7B-Instruct：跨节点 prefix 复用 TTFT **5.5×–36.6×**（外部命中率 **95.4–99.5%**）。
- sharing gap（跨节点 vs 同节点复用延迟比）**1–4%**。
- 设备读 **27–28 GB/s**，空闲读延迟约 **461–507 ns**（相对本机 DRAM 约 **2.4×** 更低延迟口径见文；RDMA 对照文称 CXL 约 2.4× 更低延迟 / 2.2× 更高带宽）。
