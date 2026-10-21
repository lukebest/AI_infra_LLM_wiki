---
type: Concept
title: PagedAttention and vLLM Serving
description: vLLM 服务系统的核心 KV cache 内存管理：借鉴 OS 虚拟内存与分页机制，将 KV cache 切为 fixed-size block 跨请求共享/重映射；解决 KV cache fragmentation 与不可共享
tags:
- llm
- inference
- serving
- kv-cache
- paged-attention
- vllm
- virtual-memory
- memory-management
timestamp: '2026-10-19T00:00:00Z'
created: 2026-07-07
updated: 2026-10-21
sources:
- raw/papers/llm-inference-acceleration-comprehensive-hardware-survey-2024.md
- raw/papers/understanding-inference-scaling-for-llms.md
---

# PagedAttention and vLLM Serving

**PagedAttention**（Kwon et al., SOSP 2023, arXiv 2309.06180）是 LLM 服务系统 **vLLM** 的核心 KV cache 内存管理算法。它**借鉴 OS 虚拟内存与分页机制**，把 KV cache 切为**固定大小 block**（非 contiguous），跨请求可共享 / 重映射。

## 解决什么问题

GPU 上传统 KV cache 分配的痛点：

1. **Memory fragmentation**：连续预分配 chunks 中间出现空洞，浪费 60-80% 内存
2. **跨请求无法共享**：相同 prefix 的请求各自重新计算 attention、KV
3. **动态 batch 中位置变化**：连续 block 假设序列长度稳定，**实际变长时必须重分配**

## 核心机制

| 概念 | 类比 | 作用 |
|------|------|------|
| **KV block** (e.g. 16 token) | Page | 固定大小分配单元 |
| **Block table** | Page table | 逻辑→物理 block 映射 |
| **Copy-on-Write** | COW fork | shared prefix 写时复制 |
| **Beam search / parallel sampling** | shared | 共享 prefix block |

具体：
- 每个请求的 KV cache 拆为 **fixed-size block**（如 16 token 一块）
- **block table** 维护逻辑 block → 物理 block 映射
- 物理 block 在**显存空闲池**动态分配，无需 contiguous
- **shared prefix**（system prompt、few-shot）多个请求可指向**同一组物理 block**，省内存 + 省计算

## 评测

- vs HuggingFace Transformers：吞吐**最高 24×**（[OSDI'23]）
- near-zero KV cache waste（vs 60-80% fragmentation）
- 已被 LMDeploy、SGLang、TensorRT-LLM 等广泛实现 / 借鉴

## 与 WaferLLM KV shift 的关系（**关键对比**）

| 维度 | PagedAttention (vLLM) | WaferLLM KV shift |
|------|----------------------|-------------------|
| **硬件** | GPU shared memory（HBM） | WSE mesh distributed memory |
| **解决** | fragmentation + sharing | **skewed core utilization** |
| **机制** | page table, fixed block | shift 老 KV 到邻行 |
| **粒度** | 16 token / block | per-row shift |
| **优势** | 跨请求共享、零碎片 | **~360-385×** 更多 token capacity vs GPU concat-based PagedAttention |
| **论文** | Kwon et al. SOSP 2023 | He et al. OSDI 2025 |

**共同范式**：都受 OS 虚拟内存 / 分页思想启发 —— vLLM 借鉴 page table；WaferLLM 借鉴"换页时数据搬运"。

## 与 wiki 已有内容关联

- [WaferLLM System](/concepts/waferllm-system.md) — shift-based KV 是 WSE 上的同类解法
- [Cerebras WSE](/entities/cerebras-wse.md) — WSE 内存层次、为何不能直接用 page table
- [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — 编译器视角对比 GPU vs WSE
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 解码加速另一方向
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 容量极限问题
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 跨实例 KV 共享

## 2026-10-13 补充：前缀缓存把瓶颈推到分词

[GraphTok](/papers/graphtok-gpu-tokenization-agentic-serving.md)：agentic 长前缀命中缓存后，CPU 分词占 vLLM 中位 TTFT 从 2% 升到 **67%**（Llama 3.1 8B，130k token）。把整条 BPE 编码流水线做成 GPU 上可重放的 CUDA graph 后，前缀命中下平均 TTFT 降 **2.1–2.4×**，Dynamo 单前端 2 s P99 下可撑 **518 req/s**。另见 [Disaggregated Inference](/concepts/disaggregated-inference.md)。


## 2026-10-16 补充：RAG 上下文缓存质量门控

[CacheSmith](/papers/cachesmith-adaptive-kv-reuse-rag-slo.md) 在 vLLM 上实现自适应选择性重算：请求同时满足 TTFT SLO 与质量门才计入 attainment，最高把 quality-gated SLO attainment 抬高 **27.5%**。与 GraphTok 互补——前者压 prefill 重算预算，后者压前缀命中后的分词。

## 2026-10-19 补充：远端 KV 层的盈亏带宽

[Remote KV Tier for PCP Prefill](/papers/remote-kv-tier-context-parallel-prefill.md)：GLM-5.3 FP8 / 8×B300 PCP8 上，LMCache+Valkey 远端命中 0.88 s、重算 0.31 s。命中划算需供给带宽 > B* = sR ≈ **2.53 GB/s**，另有每命中固定 ≈0.33 s，<17k token 的命中在任何带宽下都输给重算。按 PCP rank 分片 + 每 rank 一实例后 GET **10.76 GB/s**（6.3×），命中密集流 p99 **83.32 → 0.67 s**。与 CacheSmith 一起说明：缓存层要和 GPU prefill 速率比，不只看命中率。

## 2026-10-21 补充：前缀复用跨地域
[KVCompass](/papers/kvcompass-internet-scale-prefix-cache-discovery.md) 把前缀缓存复用从单集群扩到多地域：KV 身份与放置解耦，边缘常数时间查表后按复用、负载、网络距离联合选 worker。

# Citations

[1] [raw/papers/llm-inference-acceleration-comprehensive-hardware-survey-2024.md](raw/papers/llm-inference-acceleration-comprehensive-hardware-survey-2024.md) — 综述引用
[2] [raw/papers/understanding-inference-scaling-for-llms.md](raw/papers/understanding-inference-scaling-for-llms.md) — Inference scaling 视角
[GraphTok] [arXiv:2610.13325](https://arxiv.org/abs/2610.13325)
[CacheSmith] [arXiv:2610.18925](https://arxiv.org/abs/2610.18925)
[RemoteKV] [arXiv:2610.21500](https://arxiv.org/abs/2610.21500)
- [arXiv:2610.24179](https://arxiv.org/abs/2610.24179) — KVCompass
