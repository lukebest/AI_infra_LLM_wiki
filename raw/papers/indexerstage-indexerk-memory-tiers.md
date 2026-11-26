---
type: Raw Source
title: "IndexerStage: Staging Indexer-K across Memory Tiers for Sparse-Attention LLM Serving"
source_url: https://arxiv.org/abs/2611.28625
pdf: IndexerStage_IndexerK_Memory_Tiers_2026.pdf
retrieved: 2026-11-26
ingested: 2026-11-26
org: Hunan University / Tencent
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.28625)

Long-context sparse-attention serving can remain limited by GPU memory after attention data is offloaded. DeepSeek Sparse Attention retains Indexer-K state to select the tokens that attention will read. Its indexer scans this growing state in full at every layer and decode step. A full scan requires the current layer’s state, however, not simultaneous residency of every layer.

IndexerStage is a serving runtime that externalizes Indexer-K state while preserving native GPU score, top-k, and attention kernels. It stages completed pages through shared execution buffers and preserves new entries locally. Joint memory-and-transfer admission checks storage and each layer’s transfer demand before accepting a growing batch. The backing tier gathers pages; the model-serving GPU controls transfer timing and byte budgets.

The authors implement IndexerStage in SGLang on 16 model-serving and 16 backing H800 GPUs. Across 16K–64K inputs, local streaming storage occupies 0.65–0.70 GiB per model-serving GPU. Relative to host-memory-backed HiSparse, batch size increases by 12.28–23.08% and decode TPS reaches 1.08–1.14×. At 64K with the latent-KV backing path fixed, the larger batch achieves 1.10× decode TPS; enabling streaming at batch size 24 adds 2.42% to time per output token. Mixed-length dynamic serving increases mean generating batch size by 12.07% and delivers 1.31× decode TPS.

# Excerpts / key facts

- Authors: Xin Zhang, Weifeng Zhang, Xianyan Xie, Huijun Shen, Xijin Yin, Zhen He, Yinben Xia, Xiang Li, ZeKun He, Yachen Wang, Xianneng Zou, Guo Chen。湖南大学 / 腾讯。arXiv:2611.28625。
- 平台：四台服务器、每台八张 H800；每台四张跑模型、四张做 backing，经 NVLink/NVSwitch 一对一相连。模型为 61 层 DeepSeek-V3.2、FP8 状态、16 路数据并行注意力。每张模型卡可用 HBM 79.10 GiB。
- 静态（合成 prompt 导入后的纯 decode，最多 512 输出 token）：16K batch 57→64（+12.28%），TPS 11,153.80→12,019.60（+7.76%），TPOT 81.77→85.19 ms（+4.18%）；32K 39→48（+23.08%），TPS 8,704.20→9,913.60（+13.89%），TPOT 71.69→77.47 ms（+8.06%）；64K 24→29（+20.83%），TPS 6,128.10→6,886.70（+12.38%，即约 1.12×，摘要写 16K–64K 范围为 1.08–1.14×），TPOT 62.66→67.38 ms（+7.53%）。
- 64K 时总 HBM 从 78.10 降到 77.11 GiB（−1.26%）；本地流式存储 0.65–0.70 GiB。
- 动态：同一到达序列，12 requests/s，输入 16K/32K/48K/64K、输出 256–1,024，各约四分之一；测量 8,192 个请求。TPS 4,274.97→5,611.49（1.31×），平均 generating batch 24.27→27.20（+12.07%），TPOT p50 91.75→79.86 ms（−12.95%），p95 95.11→83.39（−12.32%），p99 98.91→85.82（−13.23%）。
- 对照 LatentPool-HBM、固定 backing 路径：64K 更大 batch 仍有 1.10× decode TPS；同 batch 24 时流式增加 2.42% TPOT。
