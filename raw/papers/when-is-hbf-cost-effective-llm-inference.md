---
type: Raw Source
title: "When Is High-Bandwidth Flash Cost-Effective for LLM Inference?"
source_url: https://arxiv.org/abs/2611.11036
pdf: When_Is_HBF_Cost_Effective_LLM_Inference_2026.pdf
retrieved: 2026-11-12
ingested: 2026-11-12
org: University of California, Merced
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.11036)

Can high-bandwidth flash (HBF) make LLM inference cheaper than adding GPUs? By storing weights closer to the GPU than SSD, HBF may reduce the number of GPUs needed for model capacity. However, this integration is only justified if it meets service targets and its cost is recovered. We simulate this integration using public component data across nine dense and mixture-of-experts (MoE) models, five workloads, two GPU platforms, and 1–100 GPUs. At fixed demand, HBF reduces the minimum GPU count to meet a service target in 98 of 468 comparisons; majority of them are paused and short sessions, 63 remain cost-effective at half a GPU price per HBF stack. For single short-chat users, HBF enables large MoEs, e.g. DeepSeek V3 and Kimi K2, to meet a relaxed service target on one RTX 4090 GPU, where conventional serving fails. At fixed GPU count, HBF improves throughput in 48% of matched comparisons below 16 GPUs and 13% at larger counts. Even at 100 RTX 4090-scale GPUs, cascaded HBF raises offline throughput by 16.4–26.5× for three large MoEs. We found savings and throughput gains arise in different scenarios.

# Excerpts / key facts

- Authors: Zhiyu An, Yiping Li, Wan Du（UC Merced）。arXiv:2611.11036，2026-11-08，cs.AR。4 页短文。工件 https://github.com/ryeii/When-Is-HBF-Cost-Effective。
- 方法：公开器件数据 + NVIDIA AISimulate（H200 表，RTX 4090 用 timing transfer）。两种组织：shared-site（8 个近存位点里换掉 2 或 4 个）与 cascaded（保留近存并外加闪存）。RTX 4090 规模 GDDR 24 GiB / 1.008 TB/s；H200 规模 HBM 141 GiB / 4.8 TB/s。每栈 512 GiB（OCP Table 3）；每 GPU 链路天花板 2 TB/s；每栈 20 W（2 W 静态，8 pJ/read bit）→ 持续读 281.25 GB/s/栈（四栈 1.125 TB/s）；物理写 8 GB/s/栈。节点 8 GPU；流水线有效带宽 H200 315 GB/s、4090 规模 8.4 GB/s；跨节点 35 GB/s + 8 µs/endpoint。
- 九模型、五负载（paused / short chat / long RAG / tool-agent / offline）、两种平台、1–100 GPU，共 468 组对照。服务目标分 responsive / balanced / relaxed / offline（Table II）。
- 固定需求（正文澄清摘要的 98/468）：在双方都通过、且常规方案需要超过 1 张 GPU 的 **224** 组里，HBF 降低最少 GPU 数 **98** 组；其中 82 组最多 4 张带 HBF 的 GPU 就够。两种 HBF 组织同时通过 178 组：123 平、54 级联胜、1 次 shared-site 胜。另有 29 组只有 HBF 通过（覆盖 16 个 DeepSeek V3 / Kimi K2 / Muse 在 4090 规模上的组合）。按负载：paused **40/108**、short chat **39/108**、long RAG **17/108**、tool-agent **0/108**、offline **2/36**（皆为 4090 规模 Llama 3.1-405B，2→1 卡）。79 组 paused/chat 胜里，39 组至少少 9 张 GPU。
- 成本：零溢价的 98 组胜里，每栈价格为 0.5 张 GPU 时仍划算 **63** 组（64%），1 张 GPU 时 **42** 组，4 张 GPU 时 **2** 组（Fig. 4b）。例：H200 规模 balanced short-chat 上 Muse，常规 16 GPU，对两张级联 GPU + 八栈；每栈半价 GPU 时相当于 6 个 GPU 当量，盈亏平衡在每栈 1.75 GPU 当量。
- 例子（Fig. 3）：四用户 balanced short-chat，Qwen3-235B 在 4090 规模从常规 32 卡降到 shared-site 8 或 cascaded 4；H200 规模上 DeepSeek V3 / Kimi K2 / Muse 从常规 16 卡降到 shared-site 4 或 cascaded 2。
- 固定 GPU 数：16 卡以下匹配对照里吞吐提升占 **48%**，16 卡及以上 **41/304（13%）**。100 张 4090 规模 GPU 的离线吞吐，级联 HBF 相对常规：DeepSeek V3 **16.4×**、Kimi K2 **26.5×**、Muse Spark Open **16.5×**（摘要概括为三家大 MoE **16.4–26.5×**；Fig. 6b）。
