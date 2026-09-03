---
type: Raw Source
title: LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism (LEAP)
source_url: https://arxiv.org/abs/2609.00857
arxiv: '2609.00857'
ingested: 2026-09-03
sha256: 6ad1fc666568fa40fa261757f457ad376ceb5f6c3847ebb97989b15ab6e279d1
---

# LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism

**Authors:** Yimin Wang, Yue Jiet Chong, Xuanyao Fong
**Affiliations:** National University of Singapore (NUS)
**PDF:** [LEAP_IMC_NoC_LLM_Inference_2026.pdf](LEAP_IMC_NoC_LLM_Inference_2026.pdf)
**arXiv:** [2609.00857](https://arxiv.org/abs/2609.00857)（2026-09-01，cs.AR；LEAP ICCAD'2025 扩展版）

## 问题

IMC 擅长静态权重 DSMM，但 LLM 还有运行时动态中间态（DDMM）；单 IMC 宏容量小，scale-up 后 NoC 上 partial-result 聚合成瓶颈。Prefill（算力密）与 decode（带宽密）资源需求冲突。

## 方法要点

- LEAP：IMC PE（静态权重）+ NMC（路由器 scratchpad 动态数据）+ INC/IRCU（in-router 归约与 DDMM）。
- 2D mesh；macro = PE + router；确定性集体原语（Broadcast / Reduce / ReduceScatter / AllReduce / AllGather）。
- LEAP-A：宏同质，prefill/decode 共享资源；LEAP-D：片上 PD 解耦——prefill 区保留 IMC，decode 区去掉 IMC、扩大 scratchpad（64 KB vs 32 KB）。
- 启发式分区/映射；注意力层映射到方形宏区；层间蛇形布局；batch=2 调度。

## 摘录数字（仅论文给出）

- vs A100：LEAP-A 吞吐 ≥**2.55×**，能效 ≥**71.94×**（tokens/J）。
- vs H100：LEAP-D 吞吐 **1.52×**，能效 **24.91×**。
- Table VI（1024 in / 1024 out）：Llama-3-8B LEAP-A 202.25 tok/s、19.21 tok/J；LEAP-D 446.18 tok/s、20.84 tok/J。13B LEAP-A 120.62 / 11.45；LEAP-D 255.17 / 11.92。
- A100 8B：78.36 tok/s、0.2612 tok/J；H100 8B：274.26 tok/s、0.7836 tok/J。
- LEAP-A 宏：IMC 占面积 72.06%、功耗 20.15%；router 面积 17.51%、功耗 56.32%（45 nm 数字缩放到 7 nm）。
- RRAM 128×128、8-bit cell；packet 64-bit；IRCU 16-way MAC；仿真非硅。
