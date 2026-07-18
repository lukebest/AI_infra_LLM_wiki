---
type: Summary
title: 'MOCAP: Wafer-Scale Chunked Pipelining for Prefill-Only LLM Inference'
description: Tsinghua MOCAP — MBKR + LBCP chunked pipeline on wafer-scale chips for prefill-only workloads; 76.4% lower latency and 3.24× throughput vs GPipe
tags:
- wse
- prefill
- inference
- kv-cache
- pipeline
- parallelism
- throughput
- latency
- llm
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf
---

# MOCAP: Wafer-Scale Chunked Pipelining for Prefill-Only LLM Inference

**Authors:** Zichuan Wang, Huizheng Wang, Yuheng Xiao, Haonan Zuo, et al. | **Affiliations:** Tsinghua University, SJTU, Shanghai AI Lab | **PDF:** [raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf](raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf)

## 一句话总结

MOCAP 针对 **prefill-only**（长上下文、单 token 输出）在 wafer-scale chip 上做 memory-orchestrated chunked pipeline：用 **MBKR** 均衡 stage 间 KV 堆积、**LBCP** 非均匀分块平衡 attention 增长，相对 GPipe 平均 **76.4%** 降延迟、**3.24×** 吞吐。

## 核心贡献

1. **Prefill-only WSC 框架**：首个系统优化 WSC 上 prefill-only LLM inference（非通用 decode 路径）
2. **Memory-Balanced KV Reallocation (MBKR)**：跨 pipeline stage 重分配 KV，缓解因果依赖导致的 memory imbalance
3. **Latency-Balanced Chunk Partitioning (LBCP)**：自适应非均匀 chunk 划分，平衡 attention 成本与 KV 迁移开销
4. **Terapipe 式 token chunk pipeline**：细粒度 chunk 流水线降低 bubble，相对 Terapipe 最大序列长度 **+31%**
5. **WSC 通信优势量化**：同等算力/容量下 WSC 相对 HGX B200 端到端延迟约 **-46.8%**（GR24）

## 关键数字

| 设置 | 结果 |
|------|------|
| vs GPipe | **76.4%** 更低 E2E latency；**3.24×** 平均 throughput |
| vs Terapipe | 最大支持序列长度 **1.31×** |
| WSC vs GPU (GR24) | 平均 total latency **-46.8%** |
| 工作负载 | Prefill-only，上下文可达 **~10⁵** tokens |

## 与 wiki 交叉引用

- [WaferLLM System](/concepts/waferllm-system.md) — WSC 上 LLM 推理系统背景
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — prefill-only 场景下 prefill 主导 wall-clock
- [Cerebras WSE](/entities/cerebras-wse.md) — wafer-scale 通信/容量 substrate
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV 管理对照（MOCAP 侧重 stage 间重分配）
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — prefill/decode 分离与 prefill-only 工作负载

# Citations

[1] [raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf](raw/papers/MOCAP_Wafer_Scale_Chunked_Pipelining_Prefill_2026.pdf) — Wang et al. (2026)
[2] [raw/papers/mocap-wafer-scale-chunked-pipelining.md](raw/papers/mocap-wafer-scale-chunked-pipelining.md) — 结构化摘录
