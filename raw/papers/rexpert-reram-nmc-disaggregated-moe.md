---
type: Raw Source
title: ReXpert ReRAM Near-Memory MoE FFN Pool
source_url: https://arxiv.org/abs/2608.13962
arxiv: '2608.13962'
ingested: 2026-08-21
sha256: 935455a5e1e24f45962d5e39c3b533892208117e908ccb5228d8e1c3607bd271
---

# MoE Expert Execution in Disaggregated LLM Serving with a High-Bandwidth ReRAM Near-Memory Architecture

**Authors:** Kunming Shao, Ming Zeng, Xin Yuan, Binbin Liao, Yangming Zhang, Wei Wang, Tim Kwang-Ting Cheng, Chi-Ying Tsui（HKUST + Alibaba Cloud）
**PDF:** [ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf](ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf)
**arXiv:** [2608.13962](https://arxiv.org/abs/2608.13962)（2026-08-14）

## 问题

Attention–FFN 解耦让 MoE 权重可驻留在高带宽 FFN 池，但 decode SLO 限制 run-batch，稀疏路由把激活 expert 并集从 B=1 的 8 扩到 B=64 的 168.6/256，64× batch 只把每 token 权重流量压约 3.0×；热 expert 当 straggler。驻留去掉片外搬权重之后，仍要带宽密度 + 有界共享恢复 occupancy。

## 方法要点

- ReRAM NMC：Unit 4 MiB / 51.2 GB/s / 400 GFLOPS FP8；Core 4×4；Die 20 cores、1.25 GiB、16.4 TB/s、128 TFLOPS；4-die 2.5D UCIe package；Node 8 package。
- 权重不出 Core mesh；热 expert 只在 core 内组播。side-4 是 occupancy–网络代价膝点。
- 实际 MFU = 理想 MFU × occupancy。放置（共激活）+ load-aware fetch 为次级 occupancy 杠杆。
- 归约顺序必须匹配 shard 放置：expert-parallel-first；反向会使 GLM-5.2 包内 D2D 胀 5.7×。

## 摘录数字（仅论文给出）

- occupancy 0.328→0.519（side-2→side-4）；实际 MFU 0.240→0.381；理想 MFU 保持 0.736。
- iso-peak-compute FFN 池延迟相对 H20 **9.5×**、相对 H100/H800 **75.6×**；权重搬运能 **20×**（4.00 vs 0.20 pJ/byte）。
- H20-attn + ReXpert-FFN 相对同质 H20 池 decode TPOT：Qwen3.5-35B **1.25–4.0×**，397B **2.4–10.3×**，GLM-5.2 **2.5–10.4×**。
- 25-die 35B 池约 1.2 kW vs iso-compute 10.8-die H20 4.3 kW TDP（**3.7×** 功耗、约 **35×** 每 token FFN 能量）。
- 建模+轨迹，非 ReXpert 硅。
