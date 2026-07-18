---
type: Summary
title: 'FlexInfer: Flexible On-Device LLM Offloading'
description: FlexInfer — async prefetch + balanced memory locking + flexible tensor retention for budget-adaptive edge LLM inference; 10.6–12.5× vs prior offload on Llama2-70B
tags:
- inference
- memory
- optimization
- llm
- storage
- latency
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf
---

# FlexInfer: Flexible On-Device LLM Offloading

**Authors:** Hongchao Du, Shangyu Wu, Arina Kharlamova, Nan Guan, Chun Jason Xue | **Affiliations:** CityU HK, MBZUAI | **PDF:** [raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf](raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf)

## 一句话总结

FlexInfer 为资源受限 **on-device** 推理提供 **异步 prefetch + 均衡 memory locking + 灵活 tensor 保留**，按用户内存预算动态选择驻留/卸载，相对现有 offload 在 Llama2-70B 等场景 **10.6–12.5×** 吞吐提升。

## 核心贡献

1. **Budget-adaptive offloading**：无需重调量化/稀疏超参即可切换内存上限
2. **Async prefetch**：I/O 与计算 overlap，缓解 storage-bound decode
3. **Balanced memory locking**：有限 RAM 内均匀锁定热参数，优于 mmap 逐页 fault
4. **Flexible tensor preservation**：按预算智能决定哪些层/张量驻留
5. **llama.cpp 基线诊断**：5–25 GB 可用内存下 70B 4-bit 几乎 **~0.5 tok/s** vs 满内存 **31.14 tok/s**

## 关键数字

| 设置 | 结果 |
|------|------|
| Speedup vs prior offload | **10.6–12.5×** |
| Llama2-70B 4-bit full mem | **31.14 tok/s** |
| 5–25 GB avail mem (baseline) | **0.46–0.51 tok/s** |
| Model size (4-bit 70B) | **~36.2 GB** |

## 与 wiki 交叉引用

- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 单 batch decode 的 weight streaming 特征
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — serving 侧内存管理对照
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — edge CPU/storage 异构 offload
- [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — 内存不足时的吞吐崩塌
- [Prefill Decode Divergence](/concepts/prefill-decode-divergence.md) — decode 逐步读权重

# Citations

[1] [raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf](raw/papers/FlexInfer_On_Device_LLM_Offloading_2025.pdf) — Du et al. (2025)
[2] [raw/papers/flexinfer-on-device-llm-offloading.md](raw/papers/flexinfer-on-device-llm-offloading.md) — 结构化摘录
