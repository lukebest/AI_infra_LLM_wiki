---
type: Raw Source
title: "CAMP: Context-Aware Mapping and Placement for LLMs on 3D-IMC Arrays"
source_url: https://arxiv.org/abs/2611.07707
pdf: CAMP_3D_IMC_Mapping_Placement_2026.pdf
retrieved: 2026-11-10
ingested: 2026-11-10
org: IBM Research
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.07707)

Large Language Models (LLMs) incur severe memory-access overheads due to the cost of loading large weight matrices and Key-Value (KV) caches. Analog In-Memory Computing (AIMC) is an emerging solution that enables computation directly on static weights stored in memory, substantially reducing energy and latency. 3D-IMC further stacks memory arrays into vertical tiers, increasing capacity but revealing a new challenge: how weights are placed in memory determines which Matrix-Vector Multiplications (MVMs) can execute concurrently, affecting latency and throughput. The concurrency aspect of 3D-IMC weight-mapping remains underexplored in the literature, leading to sub-optimal utilization of compute resources on 3D-IMC chips.

In this context we propose Context-Aware Mapping and Placement (CAMP), an inference-context-aware weight mapping algorithm for 3D-IMC-based LLM accelerators. CAMP captures the potential resource contention resulting from the architecture, targeted network, and runtime context in a conflict matrix, enabling throughput-optimized weight mapping. This mapping is refined through a profiling-driven feedback loop that efficiently prunes the search space and returns optimized mappings within practical runtimes. CAMP is an offline, software-based solution requiring no hardware changes and improving 3D-IMC compute utilization from 42.4% to 60.3%, delivering up to 2.0× higher 3D-IMC throughput and 1.74× higher end-to-end throughput over state-of-the-art mapping algorithms.

# Excerpts / key facts

- Authors: Orhun Görkem, Athanasios Vasilopoulos, Georgios Pagonis, Victoria Clerico, Hadjer Benmeziane, Irem Boybat, Hsinyu Tsai, Abu Sebastian, William Andrew Simon（IBM Research）。
- 三阶段：profiling 得到冲突矩阵 → 初始映射（冲突高的 MVM 放到不相交资源）→ profiling 驱动的剪枝束搜索细化 TP/BP/EP 平衡。
- 仿真配置（§5.1）：512×512、320-tier AIMC tile；容纳 Llama-3.1-70B / Mixtral-8×7B 需 1,024 tile；单 tile MVM 延迟 100 ns；64 LG、每组 4 leaf、4 条 H-tree 通道。
- 基线：Greedy-Util [5]（主基线，最大化 TP）；3D-aCortex [3]；Full-compute 理想上界。
- 3D-IMC 利用率：摘要 42.4% → 60.3%（Fig 1 均值约 42% / 60%；贡献段亦写 42% increase）。
- 3D-IMC 吞吐 vs Greedy-Util：Llama-3-8B 1.95×、Llama-3-70B 1.91×、Qwen-72B 2.0×；Mixtral 平均 1.71×、最高 1.84×。
- E2E：摘要相对 SOTA mapping 最高 1.74×。Fig 11 例：A100 attention + seq=128 时 CAMP 相对 GPU 基线 5.5×（Greedy-Util 4.4×）；综合策略下 seq=4096 相对 GPU 16.3×（Greedy-Util 12.7×）。长上下文 attention 主导时映射收益有限。
