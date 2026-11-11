---
type: Raw Source
title: "flash-comm: Self-Synchronizing Collective Communication for LLM Decoding"
source_url: https://arxiv.org/abs/2611.06634
pdf: flash-comm_Self_Synchronizing_Collective_2026.pdf
retrieved: 2026-11-11
ingested: 2026-11-11
org: ScitiX.AI
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.06634)

We present flash-comm, a communication library that achieves efficient transport for LLM decoding by fusing readiness synchronization with data movement. flash-comm introduces self-synchronizing transfers in which each data block carries evidence of its readiness, allowing receivers to directly validate the blocks they need without separate inter-GPU barriers. Based on this principle, a cost-guided protocol selector adapts the readiness encoding to message size and the number of participating GPUs, balancing synchronization overhead against additional data-transfer cost. flash-comm further decouples transport order from reduction order to preserve result consistency across GPUs under asynchronous data arrivals. On a server with eight NVIDIA B300 GPUs, flash-comm reduces all-reduce latency by a median of 28.8% and up to 43.7% compared with custom AR v2 (the state-of-the-art all-reduce implementation). In end-to-end decoding, flash-comm reduces time per output token (TPOT) by 1.7–6.8%. Note that all-reduce accounts for 11.4% of the baseline decoding time, which bounds the latency reduction possible from optimizing this operation alone. The same mechanism also supports standalone all-gather, reducing latency by a median of 23.8% and up to 58.9% across eight B300 GPUs.

# Excerpts / key facts

- Authors: Carrie Wang, Jack Li, Jason Zhao (ScitiX.AI). arXiv:2611.06634, 2026-11-04, cs.DC.
- 动机（Table 1）：跨 GPU barrier 成本可与整次小消息 all-reduce 相当。CUDA Graph 下净 barrier：H100 2.66 µs / H200 1.87 µs / B300 **4.33 µs**；1 KB all-reduce：2.54 / 2.46 / **3.33 µs**。B300 上 barrier 是 1 KB AR 的 **1.30×**。画像负载里 all-reduce 占基线 decode **11.4%**（1.68 ms / 14.73 ms）。
- 方案：自同步传输（块自带就绪证据）；代价引导协议选择器（就绪编码、one-hop 与分片 two-hop）；传输顺序与归约顺序解耦。Table 3：two-hop 核去掉两端 bookend barrier（对照 NCCL symmetric window 与 SGLang custom AR v2 各 2 个 barrier）。
- Table 4 / Fig 3（八卡 B300 all-reduce vs custom AR v2，µs）：1 KB 3.49→3.33（−4.6%）；128 KB 4.92→4.74（−3.7%）；512 KB 9.45→6.58（−30.4%）；1 MB 12.36→7.08（−42.7%）；4 MB 20.70→14.78（−28.6%）；16 MB 53.43→42.48（−20.5%）。188 个消息尺寸中位 **−28.8%**，最高 **−43.7%**；小消息最弱点大约在 1% 内，4–16 KB 有小幅落后。
- Table 5（八卡 B300 all-gather，对每尺寸最快基线）：1 KB 3.36→2.56（−23.8%）；512 KB 8.44→3.47（−58.9%）；1 MB 9.34→4.24（−54.6%）；16 MB 31.70→28.91（−8.8%）。45 个 size×GPU 组合全部改进；八卡中位 **−23.8%**，最高 **−58.9%**。
- Table 6（188 尺寸中位 AR 降幅 vs custom AR v2）：H100 2/4/8 GPU：8.6% / 11.8% / 24.3%；H200：4.9% / 9.5% / 22.3%；B300：4.2% / 9.8% / **28.8%**。
- Table 7（E2E，DeepSeek-V4-Flash-0731，八卡 B300 张量并行 decode，TPOT ms）：concurrency 16：2.99→2.94（−1.7%）；32：4.38→4.08（**−6.8%**）；64：6.49→6.18（−4.8%）；192：13.60→12.89（−5.2%，绝对最多 0.71 ms）。十个并发点全部领先，范围 **1.7–6.8%**。
- 范围：单节点 NVLink/NVSwitch 上 2/4/8 GPU；Hopper/Blackwell；bf16/fp32。作者计划把同一原理扩到 all-to-all / EP。
