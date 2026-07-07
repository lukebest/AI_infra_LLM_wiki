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
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
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

# Citations

[1] [raw/papers/llm-inference-acceleration-comprehensive-hardware-survey-2024.md](raw/papers/llm-inference-acceleration-comprehensive-hardware-survey-2024.md) — 综述引用
[2] [raw/papers/understanding-inference-scaling-for-llms.md](raw/papers/understanding-inference-scaling-for-llms.md) — Inference scaling 视角
