---
type: Raw Source
title: CHIPSMORE Compute-in-Interconnect and -Memory Chiplets for Multi-Mode Multi-Request LLM Inference
source_url: https://arxiv.org/abs/2608.30509
arxiv: '2608.30509'
ingested: 2026-09-02
sha256: d8723964346ff19b1b663746dba0d9e8e4bea4f60917ee208c78b3b6f859d177
---

# CHIPSMORE: Compute-in-Interconnect and -Memory Chiplets for Multi-Mode Multi-Request LLM Inference Acceleration

**Authors:** Yue Jiet Chong, Yimin Wang, Zhen Wu, Zixuan Wang, Wei Zhang, Xuanyao Fong
**Affiliations:** National University of Singapore (NUS)
**PDF:** [CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf](CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf)
**arXiv:** [2608.30509](https://arxiv.org/abs/2608.30509)（2026-08-31，cs.AR）

## 问题

CIM 推理加速器常假定固定上下文、单一内存角色或单 batch；多请求靠权重复制抬吞吐，RRAM 面积/泄漏/成本随 batch 涨。Base vs LoRA、长短上下文、KV 容量三者同时变，现有 CIM 设计很难一起扛。

## 方法要点

- 异构 PE：RRAM-ACIM（静态预训练权重 SMAC）+ SRAM-DCIM（LoRA / 动态）；片上可编程 IPCN 2D mesh，路由器内 DMAC（in-network compute）。
- Inter-CT：UCIe（2 endpoints/CT，16 lanes/endpoint）。
- 分层 KV：router scratchpad → SRAM-DCIM（base 模式）/ eDRAM；LoRA 时 SRAM-DCIM 留给 adapter。
- 非复制多请求层流水：每层绑定唯一 weight-bearing CT cluster，请求时间交错，不复制预训练权重。
- State-aware power gating：保留易失 KV/LoRA 状态，关掉空闲 IPCN/算力。

## 摘录数字（仅论文给出）

- Table III：7 nm、1 GHz、cluster 4 chiplets；IPCN 32×32；scratchpad 16 MiB、SRAM-DCIM 16 MiB、eDRAM 64 MiB；UCIe 2 ep × 16 lanes；eDRAM refresh 10 ms。
- vs H100（Mistral-7B INT8，base long 4096/4096，Table V）：BS1 **1112.5 tok/s @ 30.7 W** → **2.38×** 吞吐、**27×** 能效；BS4 **3003.9 tok/s @ 46.4 W** → **1.80×** / **19.04×**。
- UCIe 利用率即使 BS4 仍 **<25%**。
- 短上下文 BS1→4 吞吐增益：Llama3.2-1B **3.91×**、Mistral-7B **2.71×**、Qwen3-14B **2.77×**。
- 周期精确 HW–SW 共仿真 + Design Compiler 7 nm；**无硅**。
