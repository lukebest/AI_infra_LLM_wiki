---
type: Raw Source
title: "FOREST: Coordinating Tree-based HBF, RRAM, and HBM for Efficient Speculative LLM Inference"
source_url: https://arxiv.org/abs/2611.27701
pdf: FOREST_HBF_RRAM_HBM_Speculative_2026.pdf
retrieved: 2026-11-24
ingested: 2026-11-24
org: Unigroup Guoxin Microelectronics; Peking University; National Space Science Center, CAS; Institute of Microelectronics, CAS
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.27701)

Speculative decoding (SD) accelerates large language model (LLM) inference by combining lightweight token drafting with parallel target-model verification. However, its execution stages impose fundamentally different resource demands: target verification requires high-throughput access to large weight sets, sequential drafting repeatedly executes a compact model under tight latency constraints, and long-context attention processes dynamically growing key-value (KV) caches. Conventional GPU-centric SD systems serve these distinct workloads through a shared HBM-centric memory hierarchy and general-purpose compute resources, creating mismatches between memory capacity, bandwidth, and computational demands. These mismatches constrain deployable model–context configurations and limit the efficiency of both bandwidth-bound and latency-sensitive operations.

To address these challenges, we propose FOREST, a heterogeneous memory-centric architecture that coordinates HBF, 3D-stacked RRAM, and HBM memory–compute trees for efficient SD, featuring: (1) compute-aligned 3D RRAM architecture, combining ultra-wide, low-frequency reads with clock-decoupled interfaces and overlapped SRAM-DCIM weight refills for latency-sensitive drafting; (2) cross-tree numerical co-design, moving block-scaled Q/K/V preprocessing to HBF and RRAM root plates and enabling block-floating-point (BFP) attention with pipelined softmax reduction in the HBM tree; and (3) HBF-aware SD design-space exploration, revealing how bandwidth–compute provisioning and model scale determine performance bottlenecks and performance, energy, and cost trade-offs. Evaluated across six SD configurations spanning 32B–405B target models, FOREST achieves up to 5.5× end-to-end speedup, 11.46× higher decode throughput, and 16.5× higher decode energy efficiency over NVIDIA A800 GPU-based SD baselines. Under a modeled total cost of ownership, FOREST further delivers up to 6.73× higher token-generation cost efficiency.

# Excerpts / key facts

- Authors: Hao Ding, Kun Wang, Nanjian Wu, Jie Chen（紫光国芯微电子）；Zheng Shi, Dongxue Zhao, Meng Li, Yimao Cai（北京大学）；Huiying Bian（中科院国家空间科学中心）；Xu Zheng（中科院微电子所）。arXiv:2611.27701，cs.AR，提交标注 20 Nov 2026。
- 评测是 A800 上测得的投机轨迹 + 22 nm IX22ULL 综合 + CACTI / 存储器模型，不是流片。系统估计功率 101.35 W，三树封装投影约 424.92 mm²。
- GLM-4.5-Air 在约 8K 输入、4096 输出时相对 GPU SD 端到端 5.5×；Llama 3.1-405B 上四卡 A800 SD 仍快 1.32×。decode 吞吐 / 能效最高 11.46× / 16.5×。
- TCO 假设：四年、PUE 1.3、$0.12/kWh、A800 $20,000、FOREST $22,000；tokens/$ 最高 6.73×。
