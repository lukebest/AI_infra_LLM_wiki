---
type: Paper
title: "IndexerStage: 把 Indexer-K 跨层暂存到内存层次里"
description: "湖南大学 / 腾讯 — 16+16 张 H800、SGLang 实测 DeepSeek-V3.2；相对主机内存 backing 的 HiSparse，静态 16K–64K 上 batch 增加 12.28–23.08%、decode TPS 为 1.08–1.14×；动态混合长度到达下 decode TPS 为 1.31×"
tags:
- gpu
- kv-cache
- sparse
- attention
- inference
- serving
- serving-system
- hbm
- nvlink
- throughput
- latency
- llm
- nvidia
created: 2026-11-26
updated: 2026-11-26
timestamp: '2026-11-26T00:00:00Z'
paper_author: [Xin Zhang, Weifeng Zhang, Xianyan Xie, Huijun Shen, Xijin Yin, Zhen He, Yinben Xia, Xiang Li, ZeKun He, Yachen Wang, Xianneng Zou, Guo Chen]
year: 2026
venue: preprint
arxiv: '2611.28625'
sources:
  - raw/papers/IndexerStage_IndexerK_Memory_Tiers_2026.pdf
  - raw/papers/indexerstage-indexerk-memory-tiers.md
---

# IndexerStage：只让当前层的 Indexer-K 出现在模型卡上

## 一句话结论
湖南大学与腾讯的 IndexerStage 把 DeepSeek Sparse Attention 的 Indexer-K 状态外置：已完成页经共享执行缓冲从 backing 层暂存进来，新条目先留在本地可写区，原生的 score / top-k / attention kernel 保持不变。系统做在 SGLang 上，用 **16** 张模型 H800 加 **16** 张 backing H800 实测 DeepSeek-V3.2（FP8，16 路数据并行注意力）。相对主机内存 backing 的 HiSparse，静态 16K–64K 输入上每卡 batch 增加 **12.28–23.08%**，decode TPS 为 **1.08–1.14×**；混合长度动态到达下，平均 generating batch 增加 **12.07%**，decode TPS 为 **1.31×**。

## 动机
注意力数据卸出模型卡之后，长上下文服务仍可能被 GPU 内存卡住。DSA 要保留 Indexer-K，以便每层、每步扫描并选出注意力要读的 token。完整扫描只需要**当前层**的状态，不必让每一层同时常驻 HBM。把 Indexer-K 也卸到主机路径时，传输预算很快变紧：文中按 32K、batch 39 估计流式 20 层的需求约 **47.80 GB/s**，相对假设可用的 50 GB/s 主机路径只剩 **2.20 GB/s** 给选择性 latent-KV 和扫描前的时序约束。

## 方案
IndexerStage 按层决定放置：流式层把已完成页放在 backing，常驻层留在模型卡 HBM。联合内存-传输准入在接受请求前同时检查存储和每一层的传输需求，并按层序核对字节能否在扫描前到达。Backing 侧负责聚页，模型卡控制传输时机和字节预算。两个固定地址的 HBM 执行缓冲轮流承接暂存页，本地可写区保存新条目；页写满后再刷到 backing，并切换到另一目的地。评测机器为四台服务器、每台八张 H800，每台四张跑模型、四张做 backing，经 NVLink/NVSwitch 一对一相连；每张模型卡可用 HBM **79.10 GiB**。静态实验用合成 prompt 生成的真实 KV 导入后再计时 decode（最多 512 个输出 token），对应预填充-decode 分离部署的 decode 侧。

## 量化结果
静态（各系统跑到自己最大准入 batch，batch 按 DP rank 计，TPS 计模型卡上的生成 token）：

| 输入 | HiSparse batch / TPS / TPOT | IndexerStage batch / TPS / TPOT | batch / TPS / TPOT 变化 |
|---|---|---|---|
| 16K | 57 / 11,153.80 / 81.77 ms | 64 / 12,019.60 / 85.19 ms | +12.28% / +7.76% / +4.18% |
| 32K | 39 / 8,704.20 / 71.69 ms | 48 / 9,913.60 / 77.47 ms | +23.08% / +13.89% / +8.06% |
| 64K | 24 / 6,128.10 / 62.66 ms | 29 / 6,886.70 / 67.38 ms | +20.83% / +12.38% / +7.53% |

16K–64K 的 TPS 范围为 **1.08–1.14×**。64K 时总 HBM 从 **78.10** 降到 **77.11 GiB**（−1.26%），本地流式存储在三个长度上为 **0.65–0.70 GiB**。常驻层 Indexer-K 每请求从 0.51 降到 0.34 GiB（−32.79%）；更大 batch 下该分配仍降 **18.79%**（12.16→9.88 GiB/GPU）。Backing 上的 latent-KV 载荷随 batch 增加 **20.83%**（58.62→70.83 GiB），另有 4.82 GiB 的卸出 Indexer-K 页与元数据。

动态：同一到达序列，12 requests/s，输入 16K/32K/48K/64K、输出 256–1,024 token，各约四分之一；预热 1,440 个请求后测量 8,192 个。

| 指标 | HiSparse | IndexerStage | 变化 |
|---|---|---|---|
| TPS | 4,274.97 | 5,611.49 | 1.31× |
| 平均 generating batch | 24.27 | 27.20 | 1.12×（+12.07%） |
| TPOT p50 (ms) | 91.75 | 79.86 | −12.95% |
| TPOT p95 (ms) | 95.11 | 83.39 | −12.32% |
| TPOT p99 (ms) | 98.91 | 85.82 | −13.23% |

固定 latent-KV backing 路径、只改 Indexer-K 放置时，64K 上更大 batch 仍有 **1.10×** decode TPS；在 batch 24 启用流式会增加 **2.42%** TPOT，开销来自传输控制、就绪检查、可写页保留和共享资源干扰。

## 局限与解读
- 静态数字来自导入后的纯 decode，不包含预填充计算。
- 对照 HiSparse 换了 latent-KV 访问路径；1.10× 这一项把该路径对齐后，增量来自 Indexer-K 流式与更大 batch。
- 默认放置是每隔两层流式一层，用来卡在传输预算内；更多流式层会释放更多 HBM，同时每步增加传输。
- 平台是 H800 加 NVLink backing，结论依赖这条高带宽配对，主机路径的带宽余量在文中已被写得很紧。

## 与 wiki 的关系
- [ANOR](/papers/anor-gpu-pnm-sparse-attention.md) — 同样处理稀疏注意力的容量与缺失，ANOR 把缺失计算放到 CXL-PNM，IndexerStage 把 Indexer-K 本身分页暂存
- [XM-Sparse](/papers/xm-sparse-scale-up-memory-pool.md) — 把 KV 与 K-index 卸到仿真 scale-up 内存池；IndexerStage 在真实 16+16 H800 上测 Indexer-K 暂存，并对齐了 latent-KV 路径
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把「当前层扫描只需当前层状态」写进分层驻留与传输准入
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — backing 与模型卡经 NVLink/NVSwitch 一对一相连

# Citations
- [arXiv:2611.28625](https://arxiv.org/abs/2611.28625) — Zhang 等（湖南大学 / 腾讯）
- [raw stub](/raw/papers/indexerstage-indexerk-memory-tiers.md)
- [PDF](/raw/papers/IndexerStage_IndexerK_Memory_Tiers_2026.pdf)
