---
type: Paper
title: "KVStream: Adaptive Parallel Storage Management for KV Caching in Large-Scale LLM Serving"
description: "Argonne/RIT/IIT — 长上下文前缀 KV 溢出到存储时，把节点 NVMe 和闲置的并行文件系统一起用：批量读、写后置、每块全层复制、空闲层抢下一块；离线吞吐比 LMCache 最高 1.49×，突发负载均值 TTFT 最高降 6.1×"
tags:
- kv-cache
- prefix-cache
- storage
- serving-system
- inference
- memory
- latency
created: 2026-10-27
updated: 2026-10-27
timestamp: '2026-10-27T00:00:00Z'
paper_author: [Avinash Maurya, Jaiaid Mobin, Jie Ye, M. Mustafa Rafique, Franck Cappello, Bogdan Nicolae]
year: 2026
venue: arXiv cs.DC
arxiv: '2610.31827'
sources:
  - raw/papers/KVStream_Parallel_Storage_KV_Cache_2026.pdf
  - raw/papers/kvstream-parallel-storage-kv-cache.md
---

# KVStream：多存储层并行的 KV 前缀检索

## 一句话结论
agentic、代码、长文档服务的前缀 KV 会超出 GPU 和主机内存，存储 I/O 进入推理关键路径。KVStream 把前缀检索当成「跨存储层聚合带宽调度」：每块在所有层都存一份，哪层空闲就去取下一块未读的块，无需预测或调参就贴近聚合带宽上界（差距 5% 以内）。

## 动机（论文在两套 HPC 测试床上的观测）
- 卸载 KV 再读回依然划算：磁盘读只有 6.2–13 GB/s，LMCache 存取前缀仍比在 H100 上重算快最多 2.2×；但服务一个数据集要读 5–32 TB（逐出导致读放大），检索占 LMCache 时间 80–88%。
- LMCache 按请求串行取前缀，磁盘→主机和主机→GPU 交替，流水打不满。
- 节点本地 NVMe 单独读只比共享并行文件系统（PFS）快 2.2×（VAST）/ 3.2×（Lustre），而推理期间 PFS 除了加载模型几乎没流量；同一设备读写并发比分开跑慢 6% / 27%。
- 每块延迟重尾、各层带宽随共享负载漂移，任何静态比例切分都会偏离最优。

## 方案
1. **批量读**：一个 step 的所有前缀读合并发起。
2. **写后置**：新 KV 的写回推迟到前向计算之后，避开读写干扰。
3. **多路复制 + 完成驱动路由**：每个 chunk 在 NVMe 和 PFS（或云文件存储）都放一份，哪层完成上一块就领取下一块未读 chunk；性能模型证明可达聚合带宽上界，静态切分的差距随带宽波动增大。
4. 作为 LMCache 后端插入，透明服务 vLLM/SGLang；附带 trace 驱动模拟器 kvsim。

## 效果（论文数字）
测试床：4×H100-80GB 与 4×A100-40GB 节点，2×1.6 TB NVMe RAID-0，PFS 为 4 PB VAST 与 100 PB Lustre；vLLM v0.15.0、LMCache v0.3.14；4 个模型（14B–110B）、6 个数据集、最多 128 GPU。

| 指标 | 结果 |
|---|---|
| 检索带宽 | 距聚合带宽上界 **5% 以内** |
| 离线吞吐 vs LMCache | 最高 **1.49×**（vs 重算 **3.22×**） |
| 在线均值 TTFT（突发到达） | 最高降 **6.1×** |
| 不占优场景 | 主机内存或到达顺序已保住复用时 **0.98–1.05×**；复用稀疏时 **0.81×** |

数据集与 trace 中 81–96% 的 prompt token 命中缓存前缀；多路复制使存储占用翻倍。

## 与 wiki 的关系
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — NVMe 读写干扰、RAID-0 与 io_uring 在 KV 卸载中的实际表现
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 前缀缓存块向主机/存储延伸的又一层
- [Remote KV Tier for PCP Prefill](/papers/remote-kv-tier-context-parallel-prefill.md) — 同为 LMCache 存储层；那篇给出远端命中的盈亏带宽，KVStream 给出多层并行把带宽做大的办法
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — 内存分层之外的「存储分层」对应物
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — PD 分离中 KV 传输与存储层的衔接

## 开放问题
- 复制带来 2× 容量与写带宽开销，在 PFS 被训练任务或 checkpoint 占满时的退化未系统量化。
- 测试床是 HPC 节点（VAST/Lustre）；云上 FSx/对象存储的尾延迟形态不同，论文只做了类比。
- 复用稀疏时反而 0.81×，部署端需要按工作负载判定是否启用。

# Citations
- [arXiv:2610.31827](https://arxiv.org/abs/2610.31827) — Maurya et al., 2026
- [raw stub](/raw/papers/kvstream-parallel-storage-kv-cache.md)
