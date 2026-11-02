---
type: Paper
title: "FlatCake: A Flat KVCache Storage Architecture for LLM Serving"
description: "复旦/北大/沐曦/中科院计算所 — DRAM+SSD 对等扁平 KV；Claude Code+DeepSeek-V4-Flash@8×B200 命中 94.2–94.6%（Mooncake 降至 64.3%），峰值 mean TTFT 1.6×、吞吐 1.6×，SSD 读放大消除 6.5–6.7×"
tags:
- inference
- kv-cache
- serving-system
- memory
- gpu
- latency
- throughput
- llm
- disaggregated-inference
created: 2026-11-02
updated: 2026-11-02
timestamp: '2026-11-02T00:00:00Z'
paper_author: [Xin Huang, Teng Ma, Zhuoran Li, Yibo Zhao, Zhaoshi Li, Qianchao Zhu, Wei Yang, Chenxi Wang, Tao Xie, Youwei Zhuo]
year: 2026
venue: arXiv cs.DC
arxiv: '2610.38355'
sources:
  - raw/papers/FlatCake_Flat_KVCache_Storage_2026.pdf
  - raw/papers/flatcake-flat-kvcache-storage.md
---

# FlatCake：扁平对等的 KVCache 存储架构

## 一句话结论
生产 LLM 的双峰复用（一次性长距离块 vs 超 DRAM 的多 GB agentic 会话）会击穿「DRAM 作中间缓存」的分层假设。FlatCake 把 host DRAM 与 NVMe SSD 暴露为**统一 64 位地址空间中的对等介质**，写时一次性落到目标介质且会话连续、层主序布局、永不迁移；Claude Code 生产 trace + DeepSeek-V4-Flash @ 8×B200 上负载下命中率维持 **94.2–94.6%**（Mooncake **87.9%→64.3%**），峰值 mean TTFT **1.6×**（7.57 vs 12.24 s）、吞吐 **1.6×**（98.3K vs 61.6K tok/s），并消除 Mooncake SSD 读放大 **6.5×–6.7×**。

## 动机
- 分层系统让块先入 DRAM、经 LRU 驱逐才到 SSD：staging 争用会中止 prefetch，驱逐序布局打散会话块，无法做大顺序读。
- Agentic（如 Claude Code）会话足迹远超 host DRAM，SSD 已在关键读路径上。

## 方案
1. **FC-GVA**：64 位全局虚址；按复用范围在创建时把块直接钉到 DRAM 或 SSD，写后不迁。
2. **FC-MAS**：按介质位拆双队列，避免 SSD 恢复阻塞 DRAM-ready 请求。
3. **FC-CIO**：写时层主序 + 读时 sort-merge 合并，经 GDS 把合并 SSD 读直接流入有界 GPU 窗口。
4. **集成**：SGLang HiCacheStorage；评测含 8×B200 DeepSeek-V4-Flash 与 Llama-3.1-70B（A100 TP4）8K–128K。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 负载下命中率（Claude Code / V4-Flash） | FlatCake **94.2–94.6%**；Mooncake **87.9%→64.3%** |
| 峰值 mean TTFT | **7.57 s** vs Mooncake **12.24 s**（**1.6×**） |
| 峰值 P50 TTFT | **6.26 s**（相对 Mooncake **1.8×**） |
| 峰值吞吐 | **98.3K** vs **61.6K** tok/s（**1.6×**） |
| SSD 读放大 | 消除 Mooncake **6.5×–6.7×**（6.51–6.72×） |
| SSD 带宽 / prefetch | 带宽 **1.9×**；峰值 prefetch 延迟 **5.8×** 更低 |
| Llama-3.1-70B 8K–128K mean TTFT | 最高相对 Mooncake **2.4×**、相对 Mooncake-GDS **1.8×** |

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM–DRAM–SSD 从「迁移分层」改为写时对等放置
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — GDS 顺序读与读放大；对照 [uGDS](/papers/ugds-userspace-gpu-direct-storage.md) 的用户态控制路径
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — HiCache / 前缀缓存存储后端
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 会话级 KV 跨介质放置与 PD 解耦正交
- [KVStream](/papers/kvstream-parallel-storage-kv-cache.md) — 多存储层并行取前缀；FlatCake 侧重写时布局消除放大

## 开放问题
- 主结果绑定 Claude Code + DeepSeek-V4-Flash；跨租户混部与远端 RDMA SSD 的公平性/隔离未展开。
- 与压缩页（ZipFusion）或稀疏逻辑地址（UlaCache）叠加时的布局约束待验证。

# Citations
- [arXiv:2610.38355](https://arxiv.org/abs/2610.38355) — Huang et al., 2026
- [raw stub](/raw/papers/flatcake-flat-kvcache-storage.md)
