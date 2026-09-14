---
type: Paper
title: "Composable CXL Memory as K8s Shared Memory for LLM Serving"
description: Seagate — DRA+DAX 组合 CXL；双节点 512 GiB 上 Qwen2.5-7B 跨节点 prefix 复用 TTFT 5.5–36.6×，sharing gap 1–4%
tags:
- cxl
- memory
- kv-cache
- serving
- inference
- fabric
- disaggregated-inference
- latency
- serving-system
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/papers/Composable_CXL_Memory_K8s_LLM_Serving_2026.pdf
- raw/papers/composable-cxl-memory-k8s-llm-serving.md
---

# Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving

**Authors:** Hongjian Fan, Kevin Zhang, David Habinsky, Sean Dykstra  
**Affiliation:** Seagate Technology Research  
**arXiv:** [2609.10790](https://arxiv.org/abs/2609.10790)（2026-09-09，cs.DC）  
**Venue:** 预印本；副标题 *A Feasibility Study on Seagate Composable Memory Appliance*。  
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.10790)

相对 [M5](/papers/m5-cxl-tiered-memory-page-migration.md) / [CosMoS](/papers/cosmos-disaggregated-memory-data-movement.md) 的页迁移与解耦通路，本文把 **可组合 CXL 容量**做成 K8s 可调度共享内存，专门打 **跨节点 KV/prefix 命中**——作者明确写是 **内存解耦** 可行性，不是 P/D 解耦性能评测。

## 动机

Qwen2.5-7B-Instruct 每 token KV **56 KiB**；长提示下容量与跨副本复用成为瓶颈。节点本地 GPU prefix / CPU-DRAM offload **无法**产生跨节点命中，只能重算。

## 方案

1. **Kubernetes DRA driver**：按需组合 CXL 区域，在参与主机上物化为 **DAX**，经统一 **CDI** 名注入 pod。
2. **vLLM / llm-d connector**：共享介质内嵌 slot directory（含 key + CRC），省掉外置元数据服务。
3. 双节点各跑 **完整引擎**（非 prefill/decode 拆池）。

## 效果（仅论文数字）

- 双节点 + **512 GiB** CXL appliance，Qwen2.5-7B-Instruct：跨节点 prefix 复用使 TTFT 降为原来的 **1/5.5–1/36.6**（即 **5.5×–36.6×**），外部命中率 **95.4–99.5%**；本地 GPU/CPU 层在跨节点场景回退全量重算。
- **sharing gap**（跨节点 vs 同节点复用延迟比）**1–4%**。
- 设备特性（文表）：读带宽 **27.1–28.5 GB/s**，延迟 **461–507 ns**；相对本机 DRAM（约 111 ns）更慢，但相对文内 RDMA 对照约 **2.4×** 更低延迟 / **2.2×** 更高带宽。
- 作者强调：单会话 TTFT 指标；**不**报负载下 goodput/尾延迟——feasibility study。

## 与 wiki 概念的关系

- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 从页迁移扩展到「K8s 原生共享 DAX 池 + serving connector」。
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 对照：本文是 **内存** 解耦共享 KV，不是注意力/FFN 池拆分。
- [Aurelia](/papers/aurelia-cxl-fabric-tentacle.md) — fabric 形态对照；本文落在 appliance + DRA 运维面。

## 开放问题

1. 多租户并发写同一 CXL 区域时的一致性/CRC 开销？
2. 与 PD 解耦 serving 叠用时，共享层放在 P 池还是全局？
3. 512 GiB→更大池 / 更多节点时 sharing gap 是否仍 <5%？

# Related

- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md)
- [Disaggregated Inference](/concepts/disaggregated-inference.md)
- [M5](/papers/m5-cxl-tiered-memory-page-migration.md)
- [CosMoS](/papers/cosmos-disaggregated-memory-data-movement.md)
- [Aurelia](/papers/aurelia-cxl-fabric-tentacle.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.10790) — Fan et al., arXiv:2609.10790  
[2] [raw/papers/composable-cxl-memory-k8s-llm-serving.md](raw/papers/composable-cxl-memory-k8s-llm-serving.md) — ingest stub
