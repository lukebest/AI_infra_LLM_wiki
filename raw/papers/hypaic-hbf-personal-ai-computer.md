---
type: Raw Source
title: "HyPAIC: Personal AI Computer with High Bandwidth Flash for High Performance Trillion-Parameter LLM Inference"
source_url: https://arxiv.org/abs/2611.04144
pdf: HyPAIC_HBF_Personal_AI_Computer_2026.pdf
retrieved: 2026-11-06
ingested: 2026-11-06
org: SK hynix Inc.
venue: HPCA 2027 Revision #545
---

# Abstract (verbatim gist, arXiv:2611.04144)

Large language models (LLMs) have undergone rapid adoption, expanding from simple chatbots and reasoning tasks to agentic AI… To achieve better problem-solving capabilities, most modern frontier LLMs adopt a mixture-of-experts (MoE) architecture, pushing model sizes into the trillion-parameter regime… GPU manufacturers have introduced personal AI computers (PAICs). However, existing PAICs equipped with LPDDR-based unified main memory suffer from severe capacity limitations…

In this paper, we propose HyPAIC (Hyper-PAIC), a PAIC architecture that incorporates high bandwidth flash (HBF) into PAICs… store read-only model weights in HBF and mutable runtime data in LPDDR. HBF provides over 10× the capacity of high bandwidth memory (HBM) alongside comparable TB/s-scale bandwidth. HyPAIC addresses HBF’s access latency, limited write endurance, and page-level access granularity through prefetching, read-only weight placement, and coarse-grained weight accesses… a single HyPAIC improves end-to-end (E2E) system throughput by up to 1.04× and TDP-normalized throughput by up to 3.59× during 1T MoE model inference, compared with the aggregate performance of eight baseline systems without HBF… For small model inference, HyPAIC increases the maximum number of concurrent tasks that maintain at least 50 decode tokens per second per task by up to 4×…

# Excerpts / key facts

- Authors: Minho Ha, Myunghyun Rhee, Euiseok Kim, Hoshik Kim (SK hynix). HPCA 2027 Revision #545.
- HBF >10× HBM capacity, TB/s-scale BW；权重只读放 HBF，KV/激活放 LPDDR。
- Prefetch + read-only placement + coarse-grained access。
- 1T MoE：单 HyPAIC vs 8 基线合计 E2E **1.04×**，TDP-normalized **3.59×**。
- 小模型：≥50 decode tok/s/task 并发最高 **4×**。
