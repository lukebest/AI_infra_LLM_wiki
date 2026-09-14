---
type: Summary
title: AI Infra Book Ch.9 Distributed Inference
description: 第9章分布式推理—PD/AF 配比、GQA vs MLA 交接、专家 CPU/GPU 交点、共享 KV
tags:
- book
- disaggregated-inference
- inference
- serving
- moe
- kv-cache
- parallelism
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/articles/bojieli-ai-infra-book.md
---

# Ch.9 分布式推理（优先章）

对接 [Disaggregated Inference](/concepts/disaggregated-inference.md)、[Heterogeneous Inference](/concepts/heterogeneous-inference.md)、[M2N](/concepts/m2n-communication.md)、[Prefill/Decode](/concepts/prefill-decode-divergence.md)。

章首题：4×A100 + 4×H20，3.5 req/s，8K in / 1025 out，Qwen3-8B BF16。共置上限 **3.02 req/s**，低于到达率。

稳定条件：\(\lambda d_r < n_r\)。共置 \(\mu_{\mathrm{co}}=N/(d_P+d_D)\)。

## 四种组织

| 方式 | 收益 | 新约束 |
|------|------|--------|
| 完整副本 | 独立请求 | 复制权重、缓存分散 |
| **PD 分离** | 阶段各配资源 | KV 交接、两端同时占内存、双队列 |
| **AF 分离** | 算子对硬件 | 逐层激活往返 |
| 共享 KV | 省重复 prefill | 标识、失效、多一次搬移 |

## PD：KV 与配比

\(V_{KV}=2n L h_{kv} d_h b\)。Qwen3-8B：144 KiB/token，8K = **1.125 GiB**。25 GB/s 交接 **48.3 ms**（启动可忽略）。MLA（V3 紧凑）：68.6 KiB/token，549 MiB，**23.0 ms**；展开保存会大 71×。双缓冲交接期间两端各留一份。

峰值（书取 50% 效率）：

| 卡 | BF16 | HBM | P | D（bs=32） |
|----|------|-----|---|------------|
| A100 | 312 TFLOP/s | 2039 GB/s | 0.856 s/req | 1.764 GPU·s |
| H20 | 148 | 4096 | 1.81 s | 0.878 GPU·s |

- **同构 8×A100**：分离按整数卡划分上限 2.83 < 共置 3.05。价值是隔开排队。分块 prefill 理想捎带可到 4.50。
- **异构 A100×4 P + H20×4 D**：4.67 与 4.55 req/s，网卡 20.7 → \(\mu_{PD}\approx4.55\)（共置的 **1.51×**）。角色对调只剩 2.22。分块捎带共置 4.17 < 分离。
- 前缀命中 6K：应把 A100 调去 D（5.69）。短输出 129 tok：分离只比共置高 8.5%。
- 链路成为约束当 \(B_{\mathrm{net}}<\mu V_{KV}\)；4.55 req/s 时 GQA 需 ≥5.5 GB/s，MLA ≥2.6。

## AF / 专家

传权重 vs 传激活。Qwen3-235B 专家 36 MiB。KTransformers 机：CPU AVX-512 1.8 / AMX 21.3 TFLOP/s，DRAM 220 GB/s。8 专家各 1 token：CPU ~1.46 ms vs 搬 GPU ~12.5 ms。各 128 token：AVX 交点约 **72 行**，AMX 推迟到 **689 行**。

跨机专家分离：attention 池 ↔ expert 池，每层 dispatch+combine All-to-All；skew 经「等齐」放大。扩大 EP 不自动增大每专家 batch（均匀仍是 \(nk/E\) 行）。MegaScale-Infer：micro-batch 乒乓，\(t_A+t_F+(q-1)\max(t_A,t_F)\)；论文同构 80GB Ampere 上 Scaled-MoE vs TRT-LLM decode **1.90×**（含放置/流水/库，不是「只开 EP」）。

稠密 AF 逐层：Qwen3-8B 一步 72 次 8 KiB @ 25 GB/s，载荷 23.6 μs，启动 360 μs → **0.384 ms**（启动主导）。

## 共享 KV 与综合（9.7）

直传搬 1×；经池 2×（+48.3 ms）。无前缀复用时选 **直传 PD**。有一次后续复用：读 48.3 ms 替代重算 856 ms。启动 10 s 积压 35 req，要在 60 s 内清空需 \(\mu\ge4.2\)；直传 4.55 约 43 s 清空，共置持续积压。

顺序：请求→资源秒 → 整数池配比 → 传输与双端内存 → \(\mu-\lambda\) 排空。瓶颈在 D 时加 P 无用；瓶颈在通道时加副本只让更多人等取回。

# Citations

[1] [Ch.9](https://github.com/bojieli/ai-infra-book/blob/main/manuscripts/09-分布式推理.md)
[2] [PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book.pdf)
[3] [raw stub](/raw/articles/bojieli-ai-infra-book.md)
