---
type: Paper
title: "When the KV Cache Is Slower Than the GPU: Remote KV Tiers for Context-Parallel Prefill"
description: "Multiverse Computing — GLM-5.3 FP8 / 8×B300 PCP8 上 LMCache+Valkey 远端 KV：盈亏带宽 B*=sR≈2.53 GB/s、每次命中固定 0.33 s → <17k token 命中永远打不过重算；按 rank 分片 + 每 rank 一实例 GET 6.3×（10.76 GB/s），命中重流 p99 83.32→0.67 s"
tags:
- inference
- prefill
- kv-cache
- serving-system
- disaggregated-inference
- context-parallelism
- memory-bandwidth
- storage
- latency
- nvidia
created: 2026-10-19
updated: 2026-10-19
timestamp: '2026-10-19T00:00:00Z'
paper_author: [Muhammad Ibrahim]
year: 2026
arxiv: '2610.21500'
sources:
  - raw/papers/Remote_KV_Tier_Context_Parallel_Prefill_2026.pdf
  - raw/papers/remote-kv-tier-context-parallel-prefill.md
---

# 远端 KV 层何时慢过 GPU：上下文并行 prefill 的实测与修复

## 一句话结论
在 B300 这类 prefill 很快的 GPU 上，重算就是一个很强的基线。远端 KV 命中要划算，供给带宽得超过「每 token KV 字节数 × prefill 速率」，还要摊掉每次命中的固定开销；在上下文并行（PCP）锁步执行下，任何单 rank 卡顿都会拖住全部 rank。

## 动机（生产现象）
- 部署：GLM-5.3（FP8 MoE + MLA），8×B300 节点，PD 分离，每个 prefill 节点一个 vLLM 引擎跑 PCP8，远端层为 LMCache + Valkey。
- 打开远端层后 TTFT 中位数不变，16k token 的 p99 从 **3.96 s** 涨到 **17.3 s**。
- 隔离回放：一次远端命中 **0.88 s**，重算同一 prompt 只要 **0.31 s**；同步加载把命中密集的流变成不稳定队列，p99 **83.32 s**，GPU 只忙 **7%**。

## 双项成本模型
| 量 | 含义 | 本文取值 |
|---|---|---|
| s | 每 token KV 字节 | 48.4 KB/token |
| R | 冷 miss prefill 速率 | 52.2k token/s |
| B* = sR | 盈亏带宽（与 prompt 长度无关） | ≈ **2.53 GB/s** |
| T0 | 每次命中引擎固定开销 | ≈ **0.33 s** |
| R·T0 | 低于此长度命中永远亏 | ≈ **17k token** |

单个 Valkey 实例服务 8 个 PCP rank 最多 **1.71 GB/s**，低于 B*，所以每次命中都比重算慢。同步加载下引擎等价单服务台队列：λ=1.21 req/s、中位 prompt 0.79 GB、单实例 0.78–0.89 GB/s → ρ≈**1.13**，队列无稳态；8 实例 ρ≈**0.09**。

## 方案（均已提交 LMCache 上游）
1. MLA KV 存储按 PCP rank 分片；证明现有「各 rank 取最小」的查找返回最长已缓存前缀，且加载协议不会让集体通信失步。
2. 远端层按 rank 拆分，每 rank 一个服务实例、无协调：GET 带宽 **6.3×**，到 **10.76 GB/s**。
3. 分片存储上做异步加载。
4. 修三个会导致无界卡顿的客户端 bug。

## 效果（论文数字）
- 命中密集流（98.5% prompt token 来自远端层）：p99 **83.32 → 0.67 s**（**124×**）；8 实例中位 0.41 s。
- prefill 吞吐：分片存储 **+14%**，加上上游 kernel 修复 **+34%**。
- 五节点 PD 分离部署通过该负载 SLA。

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 前缀缓存层级的又一实测反例：命中率高不等于更快
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — PD 分离下 prefill 侧的 KV 外置层
- [CacheSmith](/papers/cachesmith-adaptive-kv-reuse-rag-slo.md) — 同样在「复用 vs 重算」之间做取舍，侧重 RAG 质量门
- [Adaptive DHiSparse](/papers/adaptive-dhisparse-speculative-hierarchical-kv.md) — 同为 B300 + GLM-5.3，关注 decode 侧 host 层级 KV
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 远端层带宽需与 GPU 计算速率对齐

## 开放问题
- 每条件只跑一次；<10% 的差异不成立。
- 只看 prefill、单引擎独占 Valkey；多引擎争用与 KV 交接 decode 未覆盖。
- GPU 越快 B* 越高（B*=sR 的直接推论）：下一代 GPU 上远端 KV 层的盈亏带宽会继续上移；论文未评测 RDMA/GPUDirect 类数据通路，这是 wiki 侧的待验证方向。

# Citations
- Ibrahim, "When the KV Cache Is Slower Than the GPU: Scaling Remote KV Tiers for Context-Parallel Prefill", arXiv:2610.21500. [raw](/raw/papers/remote-kv-tier-context-parallel-prefill.md) · [PDF](/raw/papers/Remote_KV_Tier_Context_Parallel_Prefill_2026.pdf)
