---
type: Summary
title: 'WaferLLM: Large Language Model Inference at Wafer Scale'
description: 首个晶圆级 LLM 推理系统：PLMR 设备模型 + MeshGEMM/MeshGEMV + KV shift；WSE-2 上 E2E 10–20× SGLang/A100 集群、MeshGEMV 606× 单 A100
tags:
- cerebras
- wse
- llm
- inference
- gemm
- gemv
- mesh
- noc
- plmr
timestamp: '2026-07-07T00:00:00Z'
created: 2026-07-07
sources:
- raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf
---

# WaferLLM: Large Language Model Inference at Wafer Scale

**Authors:** Congjie He, Yeqi Huang, Pei Mu (Edinburgh); Ziming Miao, Jilong Xue, Lingxiao Ma, Fan Yang (MSR) | **arXiv:** [2502.04563v3](https://arxiv.org/abs/2502.04563) (May 2025) | **PDF:** [raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf) | **Code:** https://github.com/MeshInfra/WaferLLM

## 一句话总结

**WaferLLM** 用 **PLMR** 设备模型（Parallelism / Latency / Memory / Routing）指导 **prefill 双维 partition + decode replicate + KV shift + MeshGEMM/MeshGEMV**，在 **Cerebras WSE-2** 上实现首个晶圆级全芯片 LLM 推理：相对 GPU 编译器 **Ladder ~625×**、IPU 编译器 **T10 ~160×**，相对 **SGLang/A100 集群 10–20×** E2E TPR。

## 核心贡献

1. **PLMR 模型** — 刻画 mesh NoC 晶圆芯片与 shared-memory GPU 的根本差异（P/L/M/R 四约束）
2. **Wafer-scale LLM parallelism** — prefill 百万 core dist-GEMM(-T)；decode dist-GEMV + 无 transpose 权重布局
3. **MeshGEMM** — cyclic shift + INTERLEAVE → **2-hop** 关键路径（PLMR-L/R/M 合规）
4. **MeshGEMV** — **K-tree allreduce**（K=2）聚合局部 GEMV 部分和
5. **KV cache shift** — 替代 concat，避免 skewed core 利用（**~360–385×** 更多 token vs GPU PagedAttention 可扩展性）

## 关键数字

| 指标 | WaferLLM @ WSE-2 |
|------|------------------|
| vs T10 / Ladder（WSE-2） | **~160×** / **~625×** TPR（短上下文） |
| MeshGEMM vs SUMMA | **2–3×** |
| MeshGEMV vs 单 A100 | **606×** 速度、**16×** 能效 |
| E2E vs SGLang（A100 2×8 NVLink+IB） | **10–20×** TPR、**2.5×** 能效 |
| vs 单 A100 SGLang | **30–40×** |
| 利用率 vs SOTA | 最高 **~200×** |

**硬件：** WSE-2 — 850k core @ 1.1 GHz、48 KB/core SRAM、40 GB 总量、5-bit 路由头（≤25 paths/core）。

## 与 wiki 交叉引用

- [WaferLLM System](/concepts/waferllm-system.md) — PLMR、算子与 parallelism 机制
- [Cerebras WSE](/entities/cerebras-wse.md) — 评测平台与 routing/color 约束
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill GEMM vs decode GEMV 分工
- [SpaDA Programming Language](/concepts/spada-programming-language.md) — WSE 通用 spatial 编译 vs WaferLLM LLM 专用栈
- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — massive mesh memory 架构
- [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md) — PLMR-R 与有限路由路径

# Citations

[1] [raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf) — He et al. (2025)
