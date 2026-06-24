---
type: Raw Source
title: understanding inference scaling for llms
description: Immutable source material from wiki raw/papers/understanding-inference-scaling-for-llms.md
timestamp: '2026-06-15T00:00:00Z'
resource: https://arxiv.org/abs/2605.19775
source_url: https://arxiv.org/abs/2605.19775
ingested: 2026-06-15
sha256: eae42daf2be52a66b0650c6d99da8fe33ce4f5abbc4c024e97aeb16e71be4941
---

# Understanding Inference Scaling for LLMs: Bottlenecks, Trade-offs, and Performance Principles

**Authors:** Moiz Arif, Avinash Maurya, Sudharshan Vazhkudai, Bogdan Nicolae
**Affiliations:** Micron Technology Inc. + Argonne National Laboratory
**arXiv:** 2605.19775v1 [cs.DC] 19 May 2026

## 核心论点

Reasoning-centric LLM（如 DeepSeek-R1, OpenAI o1）的推理负载从根本上改变了系统瓶颈：从 compute-bound prefill 转向 **capacity-bound decode**。长推理链（OSL ≫ 10k tokens）产生的巨大 KV cache 使得 HBM 容量——而非算力——成为首要约束。

## 实验配置

- **硬件**: 8× NVIDIA H200 (SXM5), 141 GB HBM3e/GPU, 4.8 TB/s peak BW, 900 GB/s NVLink bidirectional
- **推理引擎**: vLLM v1, PagedAttention, block size B=16
- **数据集**: Meta Natural Reasoning (1.15M samples, 77% prompts <150 tokens, 45% outputs >5000 tokens)
- **模型**: DeepSeek-R1-Distill 8B/14B/32B/70B, Llama-3.1-405B, DeepSeek-R1-671B

## Analysis I: Capacity Trap for Small Models (8B-32B)

### Capacity Trap 机制
1. 增加 concurrency → 初始 throughput 提升
2. KV cache 线性增长 → HBM 饱和
3. Scheduler 开始 preempt → 前缀缓存失效 → full recomputation
4. Throughput 崩溃，latency 非线性飙升

### TTFT vs TPOT 权衡
- TTFT (queue-bound): concurrency ↑ → TTFT ↓（更多 admission 槽位）
- TPOT (bandwidth+capacity bound): concurrency ↑ → TPOT ↑（内存争用）
- E2E 呈凸形：sweet spot ≈ 2K sequences for 8B

### DP 不能解决 Capacity Trap
- DP=8 不池化内存：每个 GPU 独立面对 KV 饱和
- "Stranded capacity": GPU 0 thrash 时 GPU 1 可能有空闲
- DP 只在每个 replica 低于饱和点时有效

### 9 个 Key Observations

1. **Capacity Trap**: 增加 concurrency 只在 KV 饱和前有效，之后 preemption + recomputation 导致 throughput 崩溃
2. **TTFT-TPOT Tradeoff**: 最优 batch size 是 TTFT 下降不再补偿 TPOT 恶化的点
3. **DP 限制**: DP 不池化内存，每个 replica 独立面对 capacity wall
4. **DP tail latency**: tail latency 由最先 KV 饱和的 replica 决定
5. **DP→TP Transition**: 32B 是 inflection point——sharding weights releases HBM for KV
6. **Dense vs MoE**: Dense (405B) → high TP; MoE (671B) → hybrid PP+TP
7. **Decode dominance**: reasoning >99% wall-clock 在 decode，arithmetic intensity 极低
8. **Reasoning Cliff**: KV growth pulls saturation earlier, sometimes during prefill
9. **Scheduler = traffic shaping**: HBM capacity bounds throughput, HBM bandwidth bounds per-token latency

## Analysis II: 3D Parallelism for Large Models

### DP→TP Inflection Point (32B)
- 8B/14B: DP optimal（TP 通信开销不值得）
- 32B: TP=8 achieves 6.15× speedup vs DP's 4.9×
  - 32B weights = 64 GB FP16 → DP 每卡 64 GB weights, 仅剩 77 GB KV
  - TP=8: 8 GB weights/卡, 释放 133 GB KV space
  - **TP 的收益来自释放 KV capacity，不是加速 kernel**
- 32B Hybrid optimal: DP=4+TP=2 (484s) — 最小化 TP degree + 最大化 DP concurrency

### Frontier Scale: Dense vs MoE Divergence

**Llama-405B (Dense)**:
- KV: 1.05 MB/token FP16, 126 layers
- TP=8: 986s (唯一可行)
- PP=8: 7537s (灾难性——dense activation 太大，pipeline bubbles 无法填满)
- 需要 high-degree TP 聚合带宽和容量

**DeepSeek-R1-671B (MoE)**:
- 37B active params/token, MLA 压缩 KV cache
- PP=4+TP=2: 1663s (optimal)
- TP=8: 2047s (all-reduce sync 开销主导——compute-to-communication ratio 低)
- MLA 压缩 KV → 支持 higher micro-batch depth → 填满 pipeline bubbles
- **MoE + MLA 天然适配 PP，因为 reduced KV + low active params**

### Model Scaling Impact
- 8B→70B (9× params): throughput 仅降 5-6×（TP 聚合带宽部分抵消）
- 8B: HBM util ≈85% (bandwidth-bound)
- 671B: HBM util ≈50-60% (sync/routing latency bound, 非 bandwidth)
- **MLA Anomaly**: R1 (671B) KV consumption rate 远低于 70B dense model

## Analysis III: Prefill vs Decode Resource Divergence

### Compute-bound Prefill
- 高 SM occupancy, 低 HBM bandwidth util (≈20-30%)
- High arithmetic intensity (GEMM reuse across tokens)
- H200 的 4.8 TB/s 带宽未被充分利用

### Bandwidth-bound Decode  
- 高 HBM bandwidth saturation (≈85% for 8B)
- 低/variable SM occupancy
- Arithmetic intensity 崩溃——每 token 需读全部 weights + KV cache
- Reasoning: >99% wall-clock time 在此阶段

### Reasoning Cliff
- Decode KV 线性增长 with OSL
- 8B: 20M token output → 2 TB memory demand
- 405B: batch=1K with long context → 100% KV utilization during decode
- Batch 5K: saturation 移至 prefill phase → 无法 even initialize requests

### Scheduler Mitigation
- Chunked Prefill: 防止 OOM 但引入 "Start-Up Latency"
- Convoy mode: 新请求仅在旧请求完成释放 KV blocks 后才能 admission
- 系统 stall 在 memory capacity management 而非 productive token generation

## Discussion: 硬件解耦方向

### Prefill ↔ Decode 物理解耦
- **Prefill**: 高 TFLOP accelerators, moderate HBM BW, dense compute optimized
- **Decode**: memory-centric hierarchy — HBM → DDR/LP → CXL → NVMe tiering
- 3D-stacked memory (SRAM-based D-Matrix) 缓解 KV read bandwidth
- High-Bandwidth Flash (HBF): NAND tier 增容量，但 read/write asymmetry + power 挑战

### Tiered Memory Architecture
- Explicit KV placement and migration across HBM, host DRAM, CXL, storage
- Proactive eviction, compression, reuse of pre-generated blocks
- NVLink + optical interconnects 跨 tier 低延迟

### Agentic AI 的乘数效应
- Agent fan-out × branching depth × tool interaction → multiplicative memory demand
- HBM + host DRAM 同时受压
- CPU-GPU tight coupling: CPU 维持 agent environments, tool execution, per-agent state
- 瓶颈从 isolated GPU capacity → system-wide problem

## 参考模型 KV Cache 对比

| Model | Architecture | KV/Token (FP16) | Mechanism |
|-------|-------------|-----------------|-----------|
| Llama-3.1-405B | Dense, GQA (8 KV heads) | ≈1.05 MB | 126 layers |
| DeepSeek-R1-671B | MoE, MLA (37B active) | Low (compressed) | Latent vector compression |
| DeepSeek-32B | Dense, GQA | ≈262 KB | 64 layers |
| DeepSeek-70B | Dense, GQA | ≈328 KB | 80 layers |

## Parallelism Strategy Decision Matrix

| Model Size | Type | Optimal Strategy | Key Constraint |
|-----------|------|-----------------|----------------|
| 8B-14B | Dense | DP=8 | Communication overhead > TP benefit |
| 32B | Dense | DP=4+TP=2 | Weight replication exceeds HBM |
| 405B | Dense | TP=8 | KV footprint demands all memory |
| 671B | MoE | PP=4+TP=2 | Sync latency, not bandwidth |
