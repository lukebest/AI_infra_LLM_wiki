---
type: Paper
title: "L2C2: 在大规模芯粒上做智能体长上下文的稀疏分布式注意力"
description: "北京大学 — ASTRA-sim + NS3 + Ramulator 2.0 + Timeloop，8×8 MCM 与资源对齐的 32 GPU 对照；P=512k、N=512 时 Split-Comm 相对 Ring Attention 部分 prefill 1.45×；交织分配与敏捷缓存均衡合在一起，decode 在 MCM / GPU-basic / GPU-NVL72 上平均 1.53× / 1.32× / 1.36×"
tags:
- chiplet
- interconnect
- attention
- sparse
- kv-cache
- agentic-ai
- inference
- prefill
- decode
- context-parallelism
- hbm
- architecture
- llm
- memory
- nvidia
created: 2026-11-27
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Kanbo Bai, Zhonghua Mu, Hongze Zhou, Tianyu Jia]
year: 2026
venue: ICCAD 2026
arxiv: '2611.33691'
sources:
  - raw/papers/L2C2_Chiplet_Sparse_Distributed_Attention_2026.pdf
  - raw/papers/l2c2-chiplet-sparse-distributed-attention.md
---

# L2C2：用封装上的高带宽互连，换稀疏注意力的访存

## 一句话结论
北京大学提出 L2C2：在大规模多芯粒模块（MCM）上，用上下文并行（CP）部署稀疏注意力，避免沿头维切分带来的 KV 碎片访问。部分 prefill 阶段提出 Split-Comm Attention，利用封装上网络（NoI）的高带宽，用通信换访存，并与 Ring Attention 组成按输入长度切换的 Bi-Mode；decode 阶段用交织 token 分配消除 CP 秩间固有的访存不均，再用敏捷缓存均衡跟踪稀疏选择的漂移。评估用 ASTRA-sim、NS3、Ramulator 2.0 与 Timeloop，稀疏选择来自运行时轨迹。默认 8×8 阵列、每逻辑芯粒 600 TFLOPS（FP8）与两只合计 2 TB/s 的 HBM3。目标模型为 Llama 3.1 405B，稀疏实现取 FSA，块长 64、稀疏比 0.85，batch 为 8。上下文 P=512k、新输入 N=512（接近文中引用的多轮平均部分 prefill 长度）时，MCM 上 Split-Comm 相对 Ring Attention 为 **1.45×**；交织分配与敏捷均衡合在一起，decode 在 MCM、GPU-basic、GPU-NVL72 上平均为 **1.53× / 1.32× / 1.36×**。

## 动机
智能体多轮推理里，每轮是一段部分 prefill 加上多步 decode，上下文会在轮次之间累积。稀疏注意力减少计算，但各 query 选出的 KV 块分散，访存总量仍然大。沿头维的高程度张量并行会把 KV 切碎。CP 按序列切分，每个秩保存完整 KV 块，访问更连续，却引入分布式注意力。Ring Attention 为稠密注意力设计；稀疏比下降后，部分 prefill 更容易变成访存瓶颈，decode 时各 CP 秩的 KV 访问量也不均匀。文中在 Llama-3.1 8B、0.95 稀疏、128k 缓存、CP=8 的轨迹上观察到这一不均。

## 方案
硬件模型以已有大规模 MCM 为模板：逻辑芯粒与本地存储芯粒成对，称为一个 die，die 之间用 mesh 形状的 NoI 相连。并行按行做 CP、按列做头并行（HP），权重与 KV 按此放置。

- **Split-Comm Attention**：在部分 prefill 中，把少量新 query 经 NoI 送到存有对应 KV 的秩上计算，合并重叠选择，降低重复读 KV；与 Ring Attention 按输入长度阈值切换（Bi-Mode）。文中称，得益于 NoI，该阈值在 MCM 上可维持到 N=4k。
- **交织 token 分配**：稀疏注意力下每个 token 关注固定数量的 top-k KV 块，计算量与位置关系弱，因此按 KV 块粒度把 token 交替分给各 CP 秩，使各秩上的 KV 在后续 decode 中有相近的总被选概率。
- **敏捷缓存均衡**：静态交织之后，峰值负载芯粒的缓存访问仍比理想均衡高 **52.8%**。用 Space-Saving 维护热块表（条目数为每芯粒块数的 22.5%），把过载芯粒上已取出的热块迁到同 CP 组的邻接低载芯粒；迁移藏在稀疏注意力的空闲窗口里，并按每个迭代做小额搬运。过载判定示例阈值为实际访问量相对期望均值超过 1.25。文中引用单跳 NoI 端到端延迟可低于 75 ns。

评测配置：默认 MCM 为 8×8 die、HP=8、CP=8；每个 die 含 20 mm × 20 mm 逻辑芯粒（600 TFLOPS FP8、20 MB 片上缓冲）和两只提供 2 TB/s 的 HBM3，逻辑芯粒每边双向 NoI 带宽 1 TB/s。对照 GPU 系统用 32 张卡，每张卡的计算与存储是单个 MCM die 的两倍，使两端总资源对齐。GPU-basic 为 8 卡 NVLink 节点加 InfiniBand；GPU-NVL72 把 32 张卡连到 1.8 TB/s，但每卡配置与 GPU-basic 相同，文中写明没有采用官方 NVL72 规格。

## 量化结果
在默认 MCM、CP=H-TP=8 时，高程度张量并行的 decode 吞吐只有 CP 的 **35.7%**；文中还写，H-TP 提到 4 之后再加并行度，对 KV 访问几乎没有再改善。MCM 上 H-TP 的读延迟达到 CP 的 **7×**。

部分 prefill（P=512k）：

- N=256 时，Split-Comm 相对 Ring Attention 把 KV 访问最多降到 **5.49×**。
- N=512 时，MCM 上端到端部分 prefill 为 **1.45×**。
- GPU-basic 在 N=128 时为 **1.33×**，收益阈值大约落到 N=1k。
- GPU-NVL72 在小 N 上的加速略低于 MCM，文中归因于更高的固定通信延迟。
- N=64k、P=4k 时，即使在 MCM 上 Split-Comm 也会损失 **35%** 效率，因此需要 Bi-Mode。
- 使用 Bi-Mode 后，N<2k 时 MCM 与 NVL72 明显快于 GPU-basic；更大 N 后三套配置同计算能力，延迟趋于接近。

Decode（P=512k）：

- 相对头尾分配，交织分配把各 CP 秩平均 KV 访问方差从 **2.775** 降到 **0.48**，MCM 上 **1.34×**，GPU 两组均为 **1.32×**；相对理想均衡，静态方法仍有 **21.8%** 的改进空间。
- 在交织基础上，CP=8 时敏捷均衡再把 decode 效率提高 **17.7%**，接近理想均衡。固定间隔的基线均衡要么在 I=8 时搬运过重，要么在 I=512 时跟不上稀疏焦点变化。
- GPU-basic / GPU-NVL72 在 CP=8 时，敏捷均衡分别再降延迟 **8.9% / 11.4%**。
- 交织与敏捷均衡合在一起，三套平台平均 decode 加速为 **1.53× / 1.32× / 1.36×**。

## 局限与解读
- 这是 **ASTRA-sim + NS3 + Ramulator 2.0 + Timeloop** 的分布式系统仿真，稀疏选择来自运行时轨迹，不是硅片或整机实测。
- GPU-NVL72 的每卡规格与 GPU-basic 对齐，以便总资源可比，不能当作官方 NVL72 产品数字。
- 主模型是 Llama 3.1 405B 与 FSA 稀疏实现，块长 64、稀疏比 0.85，batch 固定为 8，受 HBM 容量约束。
- 1.45× 对应 N=512 这一接近应用平均的部分 prefill 长度；更长输入上加速会下降。

## 与 wiki 的关系
- [ANOR](/papers/anor-gpu-pnm-sparse-attention.md) — 同样面对稀疏注意力的 KV 访问，把命中放在 GPU、缺失放在 CXL 近存；L2C2 把分布式注意力放到封装上的芯粒阵列
- [IndexerStage](/papers/indexerstage-indexerk-memory-tiers.md) — 在 16+16 张 H800 上为稀疏注意力暂存 Indexer-K；L2C2 优化的是 MCM 上的上下文并行与互连
- [LASH-PAT](/papers/lash-pat-inter-chiplet-routing.md) — 讨论不规则芯粒互连上的路由函数；L2C2 假设 mesh NoI，关注的是注意力通信与访存的互换
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 记录 NoI、HBM3 与按块保存的 KV 在部分 prefill / decode 上的临界路径
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 同一套 CP 在部分 prefill 与 decode 上采用不同的分布式注意力策略

# Citations
- [arXiv:2611.33691](https://arxiv.org/abs/2611.33691) — Bai、Mu、Zhou、Jia（北京大学），ICCAD 2026
- [raw stub](/raw/papers/l2c2-chiplet-sparse-distributed-attention.md)
- [PDF](/raw/papers/L2C2_Chiplet_Sparse_Distributed_Attention_2026.pdf)
