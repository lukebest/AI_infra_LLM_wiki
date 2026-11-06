---
type: Paper
title: "UMLoad: Fast On-Demand Model Loading on Unified Memory Architecture"
description: "上交 IPADS — UMA 按需重建去掉冗余 H2D；加载时间相对 vanilla −36.6%–71.9%、相对流水 −19.9%–62.7%；路由 TTFT −51.3%–59.3%"
tags:
- inference
- serving
- edge
- memory
- uma
- latency
- kv-cache
- virtualization
- llm
created: 2026-11-06
updated: 2026-11-06
timestamp: '2026-11-06T00:00:00Z'
paper_author: [Zimeng Wang, Jinrong Yang, Rong Chen]
year: 2026
venue: arXiv preprint
arxiv: '2611.04253'
sources:
  - raw/papers/UMLoad_Unified_Memory_Model_Loading_2026.pdf
  - raw/papers/umload-unified-memory-model-loading.md
---

# UMLoad：统一内存上的按需模型装载

## 一句话结论
上交 IPADS 的 UMLoad 把框架逻辑分配与物理页 backing 解耦：用**按需重建**去掉 UMA 上多余的权重 H2D 拷贝，并用 **GPU 辅助页清零**加速运行时分配。落地 Intel / AMD / NVIDIA UMA，覆盖 llama.cpp、PyTorch、vLLM 与六种模型：平均装载时间相对 vanilla **−36.6%–71.9%**、相对流水装载 **−19.9%–62.7%**；LLM 路由均值 TTFT **−51.3%–59.3%**；模型支撑工具完成时延 **−10.2%–31.6%**。

## 动机
- 边缘设备普遍采用 UMA（CPU/GPU 共享物理内存），权重本已在 GPU 可见地址空间。
- 框架仍沿用离散 GPU 的「读文件 → H2D 拷权重 → 运行时分配」路径：重复拷贝抬延迟并翻倍峰值内存；运行时分配又触发同步页清零（安全要求）。

## 方案
1. **On-demand reconstruction**：保留缓冲区独立性与装载器可移植性，同时消除冗余权重拷贝。
2. **GPU-assisted page zeroing**：加速 KV/工作区等运行时分配，保留跨进程隔离语义。
3. **跨平台**：Intel / AMD / NVIDIA UMA；接入 llama.cpp、PyTorch、vLLM。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 平均装载时间 vs vanilla | **−36.6%–71.9%** |
| 平均装载时间 vs pipelined | **−19.9%–62.7%** |
| LLM-routing 均值 TTFT | **−51.3%–59.3%** |
| 模型支撑工具完成时延 | **−10.2%–31.6%** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 装载进入 TTFT 关键路径的服务栈
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重进 GPU 可见内存的冷启动段
- [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md) — 页 backing / 清零与地址空间语义
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 边缘 UMA 上的多模型按需装载
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 统一主存池上的权重驻留

## 开放问题
- 离散 GPU 路径上收益有限；与分层卸载/前缀缓存的组合仍待测。
- 超大权重与并发多模型抢页时的策略未完全展开。

# Citations
- [arXiv:2611.04253](https://arxiv.org/abs/2611.04253) — Wang, Yang, Chen, SJTU IPADS
- [raw stub](/raw/papers/umload-unified-memory-model-loading.md)
