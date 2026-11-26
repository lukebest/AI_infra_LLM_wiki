---
type: Raw Source
title: "Mayfly: Lifecycle-Aware High-Bandwidth Flash for Recursive Self-Improvement"
source_url: https://arxiv.org/abs/2611.32264
pdf: Mayfly_Lifecycle_Aware_HBF_RSI_2026.pdf
retrieved: 2026-11-26
ingested: 2026-11-26
org: NUS / HUST
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.32264)

Recursive self-improvement (RSI) lets an LLM improve its agent system by proposing and evaluating candidate variants across tasks. A generation’s sessions grow their KV caches together and release them as they finish, creating a burst followed by a decline. At high concurrency, even the KV of sessions ready to run exceeds the GPU’s HBM. Offloading that KV to host DRAM or SSDs adds capacity but leaves ready sessions waiting for HBM space before execution. HBF can serve the overflow in place, but excessive reads lengthen decode steps and repeated writes consume flash endurance.

Mayfly is lifecycle-guided HBF management for RSI. It bounds per-step HBF reads during overflow and returns KV to HBM as sessions finish and free space. It retains a valid backing copy of each block evicted from HBM to avoid rewrites across state transitions, and forwards session-end signals to the controller to avoid copying dead KV during garbage collection. At 128 sessions per generation on four added HBF sites, Mayfly finishes 34% sooner than parking the same KV on HBF and 23% sooner than reading it from HBF whenever HBM is full; its gain over parking grows with concurrency, to 55% at 256 sessions on eight sites. Keeping one flash copy per block and trimming at announced session ends avoid write amplification.

# Excerpts / key facts

- Authors: Chunlin Tian, Mingjia Fan, Feng Yu, Qingyun Zou, Wenju Zhao, Weng-Fai Wong, Bingsheng He。新加坡国立大学、华中科技大学。arXiv:2611.32264，cs.AR，Wed 25 Nov 2026 公告。
- 评估：离散事件仿真器重实现 vLLM 的 block pool / 调度 / 抢占；步时间与能量在 H200 回放上拟合（含一次把 KV 溢到主机 DRAM，误差 0.5%）；留出回放上，20 GB KV 池的运行时间误差 0.9%、能量 1.6%、抢占 5%。HBF 路径为模型。回放统一用 Qwen3-32B、FP8 权重。
- 硬件模型：H200 六个 HBM 位点共 141 GB，其中 99 GB 给 KV；HBF 为封装上另加位点，每 32 个会话一只 512 GB TLC 堆栈；位点读带宽取 467 GB/s（也跑 202 GB/s 热限制），写为读的十分之一；读/写能量取 20 / 100 pJ/bit，页读 20 µs。
- 主结果（DGM 环，每代 32/64/128/256 会话）：Table 3 运行时间 HBF-Park 为 172 / 279 / 482 / 919 min，Mayfly 为 159 / 235 / 316 / 417 min，即提前 8 / 16 / 34 / 55%。十次任务抽样平均为 8.0 / 17.5 / 36.3 / 53.9%（95% CI ±1.5 / 1.8 / 0.6 / 0.3 个百分点）。128 会话中位 TTFT：Park 89 s，Mayfly 46 s（约 1.9×）；256 会话 187 s 对 73 s（约 2.6×）。相对 HBF-Greedy（HBM 一满就就地读），门控在 32–256 会话上分别节省 29 / 28 / 23 / 11% 运行时间。
- 202 GB/s 热限制下，相对 HBF-Park 仍提前 1 / 7 / 19 / 36%。一块位点留一份拷贝并在会话结束修剪，WAF 为 1.00。
