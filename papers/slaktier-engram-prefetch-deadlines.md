---
type: Paper
title: "Placing LLM Lookup Tables by Per-Layer Prefetch Deadlines"
description: "Microsoft — SlackTier 按层预取窗口放置 Engram 表；V4.1 两层窗口 0.27 vs 9.35 ms；四盘 NVMe 上相对未改 SGLang 均值 TPOT 最多 +1.4%，宿主内存 212→34 GiB；省下的内存做 host KV 时中位吞吐 +36%，p90 TTFT 38.1→24.1 s"
tags:
- memory
- prefetch
- kv-cache
- serving
- serving-system
- inference
- decode
- storage
- ssd
- flash
- rdma
- microsoft
- deepseek
- latency
- throughput
created: 2026-11-13
updated: 2026-11-13
timestamp: '2026-11-13T00:00:00Z'
paper_author: [Wen Huang, Jack Liu]
year: 2026
venue: arXiv preprint
arxiv: '2611.13413'
sources:
  - raw/papers/SlackTier_Engram_Prefetch_Deadlines_2026.pdf
  - raw/papers/slaktier-engram-prefetch-deadlines.md
---

# SlackTier：按层预取期限放置查找表

## 一句话结论
微软的 **SlackTier** 把 DeepSeek-V4.1 的 Engram n-gram 表（203 GB）按各层预取窗口放到 NVMe 或远端内存，并在短窗口层优先提交 I/O、把小块 GPU 行缓存分给窗口不够的层。V4.1 两层窗口实测为 **0.27 ms** 与 **9.35 ms**（约 30 倍）。四张盘、缓存均分时，相对未修改 SGLang，agent / chat 回放的均值每输出 token 时间最多高 **1.4%**，服务进程宿主内存从 **212 GiB** 降到 **34 GiB**。在 GPU KV 预算收紧的 agent 负载上，把省下的内存交给 host KV cache，中位吞吐提高 **36%**，中位 p90 TTFT 从 **38.1 s** 降到 **24.1 s**。

## 动机
今日服务栈把这两张表放在宿主 DRAM，4×H200 节点上一个服务进程用 **223 GiB**，其中表本身 **190 GiB**；未修改 SGLang 进程为 **212 GiB**。行号只取决于输入 token，因此一步之内的读取可以从 step 开始就与更早的层重叠。两层能重叠的时间差很大：第 14 层前面有约 9 ms，第 1 层只有约 0.3 ms。朴素把两张表都放到本地 NVMe，在 128 并发会话下 decode 慢 **6–7%**；只缓存第 14 层的热行，开销仍从 6.4% 降到 4.9%。放置既取决于谁热，也取决于各层的读期限。

## 方案
1. **按窗口选层与缓存**：表可以放在读时间落进该层窗口的任何一级；缓存优先给窗口不够的层。第 14 层可以无缓存走 NVMe，第 1 层需要缓存或留在 DRAM / 走更快的 RDMA。
2. **SlackTier（SGLang 插件）**：step 开始就发出全部查找，先读短窗口层；GPU 行缓存跨层划分；I/O 与拷贝走 decode CUDA graph 里的旁路流。输出与原 gather 逐比特一致（V4.1 上 790K 次查找、Qwen PLE 上 1.1M 次，含驱逐，均无 mismatch）。
3. **平台**（§6）：DeepSeek-V4.1-Flash，SGLang 0.5.22，TP4/EP4、4×H200，FP8 KV，bounded SWA 回放。表在本地 3.5 TB NVMe 裸设备。负载为 OpenHands agent（留出仓库）与 WildChat。B 表示并发会话。另用探针在 Gemma 4 E4B 上测窗口随深度的增长，并在 Qwen3.8-Flash-Next 的层 1 PLE 表上复用同一路径。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 预取窗口 | W₁=**0.27 ms**，W₁₄=**9.35 ms**；联合注入延迟的预测 RMSE **0.12 ms** | §6.3 / Table 3 |
| 仅第 14 层上 NVMe、无缓存（B=128） | 相对宿主表 agent **−0.0%**、chat **−0.1%**，p99 不变 | Table 2 |
| 两张表一块盘、无缓存 | agent **+6.4%**，chat **+7.2%** | Table 2 |
| 四盘 + 1M 行/卡均分缓存 | agent **+0.7%**，chat **+1.7%**；RSS **34 GiB**（宿主表路径 223 GiB） | Table 2 |
| 客户端 vs 未修改 SGLang（B=128） | 四盘均分：agent TPOT **−0.5%**，chat **+1.4%**（摘要：最多 +1.4%）；进程 **34 vs 212 GiB** | Table 6 / 摘要 |
| 缓存分配 | 全部给第 14 层（f=0）agent **+4.9%**；f=0.25–1 为 **+1.3–1.9%**。四分之一预算均分仍为 **+1.8%** | §6.2 / Fig 3 |
| RDMA 远端内存 | 无缓存一步读 **0.21–0.25 ms**（约 600–740 页/卡/层）；B=128/256 相对宿主表 **−0.7% 到 +0.0%**。两实例共享一份拷贝，TPOT 相对单实例本地 DRAM 表在 **2.2%** 以内 | §6.8 |
| 省下的内存做 host KV | 256 agent、GPU KV 固定 1.5M token：前缀命中 **63%→76%**，p90 TTFT **38.1→24.1 s**，吞吐 **702→956** token/s（**+36%**）。同样 host KV 但表仍在 DRAM 需要 **408 GiB** RSS | Table 5 |
| Qwen3.8 PLE | 四盘 + 1M 行缓存：decode agent **+3.4%**、chat **+2.4%**；命中 93% / 57% | Table 7 |

Gemma 4 上，窗口约为一步时长的 **0.85–0.92 k/L**，H200 / MI300X / GB10 归一化后接近重合（Fig 4）。GPU KV 池放到 3M token 时，不加 host KV 已有 77% 的 prompt 命中，再加 host KV 不再改变命中率与吞吐（§6.5）。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 203 GB 查找表从宿主 DRAM 下沉到 NVMe / RDMA，并按层窗口决定哪一级需要缓存
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode CUDA graph 内的旁路预取；客户端数字同时含 prefill
- [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md) — 同属「用更便宜的存储层级换 GPU / DRAM」的部署判据
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 远端内存上一份表供给两个服务实例

## 开放问题
- 同一方法不适用于稠密或专家权重：一步几乎读完全部非 Engram 权重（约 307 GB），即使四条 PCIe 5 x16 也要约 1.2 s，远长于 11–43 ms 的 decode 步（§7）。
- 宿主 KV 的收益依赖偏紧的 GPU KV 预算；H200 节点有 1.8 TiB DRAM 时，只在池子收紧时才划算。
- 评测在 4×H200 单节点与一份远端表上；更大规模的盘阵争用与跨机架放置仍待展开。

# Citations
- [arXiv:2611.13413](https://arxiv.org/abs/2611.13413) — Huang & Liu（Microsoft / Independent Researcher）
- [raw stub](/raw/papers/slaktier-engram-prefetch-deadlines.md)
- [PDF](/raw/papers/SlackTier_Engram_Prefetch_Deadlines_2026.pdf)
