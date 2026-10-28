---
type: Paper
title: "ZipFusion: Fusing Lossless KV Decompression with Attention for Efficient LLM Decoding"
description: "CUHK — 无损 KV 解压与 attention 融合：FlashInfer 上寄存器内重建，H100 decode attention 1.23–1.25×；8K 下相对未压缩 SGLang 吞吐最高 +26.3%/+25.8%，相对最佳无损基线最高 2.76×"
tags:
- kv-cache
- compression
- serving-system
- inference
- decode
- attention
- latency
- throughput
created: 2026-10-28
updated: 2026-10-28
timestamp: '2026-10-28T00:00:00Z'
paper_author: [Yuetao Chen, Peng Wang, Hong Xu]
year: 2026
venue: arXiv cs.AR
arxiv: '2610.33719'
sources:
  - raw/papers/ZipFusion_Lossless_KV_Attention_Fusion_2026.pdf
  - raw/papers/zipfusion-lossless-kv-attention-fusion.md
---

# ZipFusion：把无损 KV 解压融进 Attention

## 一句话结论
IBP / SplitZip / LZ4 一类无损 KV 压缩先把整层 KV 解压回 GPU，再交给 FlashInfer，解压可占 instrumented decode 时间 **32.7–73.8%**，且 attention 仍按未压缩字节读。ZipFusion 让 attention 直接读压缩页，在寄存器里用位运算还原 BF16；H100 上 decode attention 相对 FlashInfer **1.23–1.25×**（延迟降 **18.5–20.2%**），8K 前缀下相对未压缩 SGLang 最大 batch 吞吐 **+26.3%**（Llama）/ **+25.8%**（Qwen），相对最佳无损基线最高 **2.76×**。

## 动机
- 长上下文 + 高并发下 KV 既占容量又在每步 decode 反复被读，带宽墙与并发上限同时收紧。
- 有损量化 / 丢 token 会动原始 KV 值；无损路线保住 BF16 位型，但现有方案面向 CPU↔GPU 或 prefill↔decode 传输，到 GPU 后仍还原成未压缩副本。
- 适配到 SGLang 后，SplitZip / IBP / LZ4 在 Llama 3.1 8B、batch 32、2048 输入上解压占 instrumented decode 的 **32.7–73.8%**，attention 的重复读并未变少。

## 方案
1. **块内无损格式**：对 BF16（1 符号 + 8 指数 + 7 尾数）按块编码指数偏移；指数落在可压缩范围则压，否则该块保持未压缩。
2. **寄存器内重建**：FlashInfer 风格 attention 读压缩块，线程用简单位运算还原原始值，不写回未压缩缓冲、不做单独解压 pass。
3. **压缩感知内存管理**：压缩腾出的物理空间按层回灌给更多 KV 页；分配器按未压缩页尺寸预留「在跑请求续写」的余量，把剩余容量暴露给调度器接新请求。
4. 实现叠在 FlashInfer 0.6.12 + SGLang（16-token 页、CUDA Graphs）；评测 Llama 3.1 8B Instruct 与 Qwen3-8B，H100 80 GB。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Decode attention vs FlashInfer | **1.23–1.25×**（延迟 **−18.5–20.2%**）；8K / batch 64 Llama **704.6→562.7 µs** |
| 固定 batch 32 吞吐 vs SGLang | Llama **+15.3%**（2044 tok/s）、Qwen **+15.2%**（1882 tok/s） |
| 同 batch vs SplitZip | Llama **2.51×**、Qwen **2.57×** |
| 最大可支撑 batch（mem frac 0.8） | Llama **46→57**，Qwen **40→50** |
| 各方最大 batch 吞吐 vs SGLang | Llama **+26.3%**、Qwen **+25.8%**（约 **2453 / 2042** tok/s，≈**1.26×**） |
| 各方最大 batch vs 最佳无损基线 | Llama 最高 **2.76×**、Qwen **2.61×** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 页式 KV 之上再压一层无损格式，并让调度看见「压缩后的物理余量」
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — decode 重复读 KV 的带宽路径；压缩字节直接进 kernel 才真正减流量
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — IBP/SplitZip 原本服务跨设备传输；ZipFusion 把同一无损收益拉进片上 attention
- [Vortex Extreme Compression](/papers/vortex-extreme-compression-llm-inference.md) — 有损/向量量化加速器路线；ZipFusion 走「保真 + 服务系统」无损路线

## 开放问题
- 评测固定 8K essay 前缀与 256 输出；变长 / 多轮 / 前缀缓存命中场景下压缩率与调度余量如何漂移未给。
- 只覆盖 BF16 KV；与 FP8 KV 或有损量化叠加时格式与 kernel 怎么改未讨论。
- 与 PD 分离 / 远端 KV 层联用时，压缩态跨节点传输与片上直接消费如何统一协议未展开。

# Citations
- [arXiv:2610.33719](https://arxiv.org/abs/2610.33719) — Chen, Wang, Xu, 2026
- [raw stub](/raw/papers/zipfusion-lossless-kv-attention-fusion.md)
