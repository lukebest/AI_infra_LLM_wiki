---
type: Raw Source
title: "Should You Split Decode? Disaggregation Across Future Models and Accelerators"
source_url: https://arxiv.org/abs/2611.08299
pdf: SiliconForge_Should_You_Split_Decode_2026.pdf
retrieved: 2026-11-10
ingested: 2026-11-10
org: Independent (written in personal time while at d-Matrix and Volantis Semiconductor)
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.08299)

For large language model (LLM) inference, prefill/decode disaggregation (P/D) is deployed in production to isolate phases with different resource demands. Attention/feed-forward network disaggregation (AFD) splits decode again, but adds communication, placement constraints, and another provisioned pool. We ask whether role-specific placement repays this cost as models and accelerator roadmaps change. Infrastructure is committed before future models and hardware can be benchmarked. We present SILICONFORGE, a calibrated model that varies the serving decomposition and hardware assignment independently. We compare P/D and P/D+AFD across four model directions, four accelerator classes anchored to current and announced parts, and two fabrics. We co-optimize each design using the same rules for pipeline overlap and the same power budget. Our main comparisons show no robust deployment-level AFD advantage in service-level objective (SLO) goodput per kW. Most nominal estimates favor P/D. The largest AFD lead comes from fitting one more prefill replica, not from a more efficient decode pool. AFD has a nominal lead in the KV-heavy (key–value) model direction when the co-located expert pool spans several small scale-up domains. Larger domains or a fast fabric for both designs weaken that lead. We therefore find that prefill provisioning, decode memory bandwidth, links, and pool granularity decide deployments more than the split itself. A fixed hardware assignment can lose its advantage as models, fabrics, hardware assumptions, and objectives change. Re-optimizing mappings and pool sizes on the same hardware cuts early commitment’s median normalized goodput loss from 36% to 9%. We recommend adjustable mappings and pool sizes to let boundary and hardware choices follow model demands.

# Excerpts / key facts

- Author: Ramyad Hadidi（独立撰写；供职 d-Matrix / Volantis Semiconductor 期间的个人时间，观点不代表雇主）。
- SILICONFORGE：39 加速器、六种硬件原型、四类（GPU / systolic 等）；四种模型方向（Expert-heavy MoE、KV-optimized MLA、KV-heavy GQA-MoE、Sparse-attention MLA）；电学与光子两种 fabric；主预算 128 kW，规模实验 512 kW。
- 稳健性检验：名义幅度超过 9% 包络且在每个规格角符号保持，才算通过。
- Finding I：SLO goodput/kW 无稳健部署级 AFD 优势；多数名义估计偏向 P/D。Fig 4：单类上加 A/FFN 边界使 goodput/kW 变动 −10.4% 到 +8.1%；八个 AFD+ 里七个落在 9% 包络内；光子 + KV-heavy 最大名义领先 +8.1%。最大 AFD 领先来自多放下一个 prefill replica。
- Finding II：KV-heavy 且共置专家池跨越多个小 scale-up 域时 AFD 有名义领先。映射固定时内存带宽翻倍使 TPOT −39–49%，FLOPs 翻倍最多 −1.8%；评测部署里内存读占 TPOT 的 57–95%。
- Finding III（§IV-D）：提前锁定硬件的中位损失为场景最优 SLO goodput/kW 的 35.7%（摘要作 36%）；同硬件重优化映射与池大小后 9.3%（摘要作 9%）；25% 冗余降到 5.1%。
- 相对 FastAFD：该文报告每 GPU decode 吞吐 1.35–1.45×；在 FastAFD 的 GPU 预算内独立优化两边后模型给出 0.94×（8K 与 16K）。
- AFD 每个 MoE 层每 decode 步跨池交换激活两次；DeepSeek-V3 为 116 次。
