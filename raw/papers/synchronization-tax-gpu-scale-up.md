---
type: Raw Source
title: Understanding the Synchronization Tax in GPU Scale-Up Domains
source_url: https://arxiv.org/abs/2608.22503
arxiv: '2608.22503'
ingested: 2026-08-31
sha256: b2221f3fa71c67ffcb867005da0203d4dd6960189395608d3697ef46f6956054
---

# Understanding the Synchronization Tax in GPU Scale-Up Domains

**Authors:** Arjun Devraj, Lindsey Bowen, Rachee Singh
**Affiliation:** Cornell University
**PDF:** [Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf](Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf)
**arXiv:** [2608.22503](https://arxiv.org/abs/2608.22503)（2026-08-23）

## 问题

Scale-up 域把 NVLink 带宽和域规模一起指数涨（A100 300 GB/s / 8 GPU → B200 900 GB/s / 72 GPU）。集体是 bulk-synchronous：先到 barrier 的 rank 必须等最慢 rank，这段空闲与互连带宽无关。论文称这段等待为 **synchronization tax**。

## 方法要点

- 在 A100 / H100 / H200 上用 PyTorch Kineto 剖析 Llama-3 8B/70B、Qwen-3 32B、DeepSeek-V3 16B 的 SFT（torchtitan），共 **244,710** 次集体。
- 图算法在 barrier-to-barrier 集合上抽 straggler 关键路径，归因跨 rank 计算差异。
- EVT（Gumbel 作下界，经验最佳拟合 Fréchet ξ≈0.15）外推税随域规模增长。
- 增广 Hockney：`T = pα + qS/B + τ`；最优带宽 B* 随 n 下降。

## 摘录数字（仅论文给出）

- 8-GPU 域税可占集体通信时间 **>50%**；中位完成 rank 可把 **>80%** 的 TP 通信花在等待。
- Llama-3 70B @ DGX H200：最快 rank 中位 **40%** TP 等待（最坏几乎全部）。
- GPU 计算差异：GEMM **78%**，FlashAttention **15.4%**，FSDP **4.3%**，Norm **1.2%**，Concat/Split **0.6%**；**93.7%** 的集体 straggler 关键路径纯 GPU。
- 512-GPU vs 8-GPU：最优带宽 **2.06×** 更低；端到端 FLOPS 缩放相对 roofline **−11.7%**。
- εB=−0.5 Gumbel：全连接 n=128 相对基线 **98.69%** 更低 B*；ring n=128 **37.26%**；3D torus n=512 **81.67%**。
- Table 1 NVLink GB/s/GPU：A100 300，H100/H200 450，B200 900；域 8→72。
- DGX H200 ALLREDUCE 测得 α≈**5 µs**。
