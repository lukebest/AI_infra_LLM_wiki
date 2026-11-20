---
type: Paper
title: "XM-Sparse: High-Throughput Sparse-Attention LLM Serving over Scale-up Memory Pools"
description: "Netpreme / 港科大 / 新加坡国立 — SGLang 上稀疏注意力卸载到仿真 scale-up 内存池；相对 PCIe 上的 ECHO / HiSparse，decode 吞吐最高 4.98× / 4.52×，相对同平台朴素接入最高 1.34×"
tags:
- inference
- decode
- serving
- serving-system
- kv-cache
- sparse
- attention
- hbm
- scale-up
- memory
- gpu
- nvidia
- throughput
- pcie
- nvlink
created: 2026-11-20
updated: 2026-11-20
timestamp: '2026-11-20T00:00:00Z'
paper_author: [Yijun Sun, Xudong Liao, Zhuobin Huang, Kai Chen, Nikita Lazarev, Zhizhen Zhong]
year: 2026
venue: preprint
arxiv: '2611.22280'
sources:
  - raw/papers/XM_Sparse_Scale_Up_Memory_Pool_2026.pdf
  - raw/papers/xm-sparse-scale-up-memory-pool.md
---

# XM-Sparse：在 scale-up 内存池上卸载稀疏注意力的 KV 与索引

## 一句话结论
Netpreme、港科大与新加坡国立大学的 XM-Sparse 把稀疏注意力的完整 KV 与 indexer key（K-index）缓存都卸到 scale-up 内存池，只在 HBM 里保留紧凑的热 KV 缓冲、K-index 暂存和一部分 K-index 页。系统做在 SGLang 上。实验用 X-Mem VM 在八张 B300 上仿真内存池（四张跑 decode，四张当内存节点）：相对 PCIe 上的 ECHO / HiSparse，DeepSeek-V3.2 与 GLM-5.3 在 16K–1M 上下文上的 decode 吞吐分别最高为 **4.98×**（对 ECHO，GLM-5.3）与 **4.52×**（对 HiSparse，GLM-5.3）；相对同一 X-Mem 平台上的朴素 HiSparse 接入最高 **1.34×**。

## 动机
DeepSeek-V3.2、GLM-5.3 这类生产模型用紧凑的 K-index 选出历史 token，但服务系统仍需保留完整 KV 历史，HBM 容量限制并发。已有卸载系统（HiSparse、ECHO）把完整 KV 放到主机内存，K-index 和热 KV 仍常驻 HBM；PCIe 带宽和主机容量会卡住 decode。作者指出，即便换到更高带宽、更大容量的 scale-up 内存池（文中以 X-Mem 为例，Table 1 写单向 900 GB/s、节点内数十 TB），热 KV 与整份常驻 K-index 仍会占满 HBM，decode 吞吐继续受容量约束；两类缓存的访问形态也不同，不宜用同一种 I/O。

## 方案
XM-Sparse 把 KV 与 K-index 都主动外置，用织物带宽换 HBM 容量、做更大 batch。对动态选出的 KV 缺失项，它把基于 TMA 的取回与 attention 融进同一 kernel，按 Split-K 的 tile 流水：先算已在片上的 tile，同时把后续 tile 取进共享内存，再合并部分结果，省掉 attention 前单独的 swap-in。对可预测的 K-index 访问，用只占 1 个 SM 的 GPU 发起 DMA 预取，门铃在 CPU 上批量更新，数据走 copy engine；并在 DMA 命令流的信号量检查点暂停 copy engine，让按需 KV 取回和模型 collective 优先，避免预取抢带宽。

评测机器：两路 Intel Xeon 6767P、2 TB 主机 DRAM、八张 NVIDIA B300（各 268 GiB HBM），每卡单向 NVLink 5.0 为 900 GB/s，PCIe 5.0 ×16 为每向 64 GB/s。四卡跑 decode 实例，另外四卡作为 X-Mem VM 的内存节点；超过 1 TB 物理内存的容量，通过把同一段物理内存反复映射到更大的虚拟地址空间来仿真。模型为 DeepSeek-V3.2（671B）与 GLM-5.3（744B），FP8 权重，注意力 DP4、MoE EP4，top-k=2048；请求来自 LongBench v2，输入 16K–1M，输出固定 128 token。默认每请求 4K-token 热 KV 缓冲，平均缺失率约 15%；每张 decode GPU 给常驻状态 60 GiB 预算。对照：PCIe 上的 ECHO、SGLang 中的 HiSparse，以及把 HiSparse 的主机 KV 后端换成 X-Mem 的朴素接入。延迟（mean TBT）在真实轨迹、相同 batch 下比较；为在物理内存限制下评吞吐，吞吐实验使用固定 15% 缺失率与 round-robin 专家路由。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 相对 PCIe ECHO 的 decode 吞吐 | DeepSeek-V3.2 **1.72–2.50×**；GLM-5.3 **3.14–4.98×**（16K–1M） | §5.2 / Fig. 9b |
| 相对 PCIe HiSparse 的 decode 吞吐 | DeepSeek-V3.2 **1.57–1.75×**；GLM-5.3 **2.05–4.52×** | §5.2 / Fig. 9b |
| 相对同平台 HiSparse + X-Mem | DeepSeek-V3.2 **1.10–1.34×**；GLM-5.3 **1.06–1.29×**。例：GLM-5.3 @128K，选中 batch 从 109 增到 209/GPU，吞吐 1437.9→1849.3 tokens/s/GPU | §5.2 |
| 真实轨迹上的 mean TBT | 相对 ECHO：DeepSeek **−30.0–56.0%**，GLM **−39.6–66.6%**；相对 HiSparse：DeepSeek **−7.4–35.8%**，GLM **−9.5–45.8%** | §5.2 / Fig. 9a |
| 组件（GLM-5.3） | 融合核在 16K、batch 1、关闭卸载时 mean TBT 25.93→21.86 ms（**−15.7%**）；K-index 卸载在 128K 上吞吐 **+28.6%**（1437.9→1849.3） | Table 3 / §5.3 |
| I/O 机制（K-index 卸载时） | GPU 发起 DMA + 优先级调度 1849.3 tokens/s/GPU，相对 CPU 提交 DMA 的 33.5、基于 SM 卸载的 1128.7（相对后者 **+63.8%**）。16 KiB 上 GPU 发起 DMA 624.0 GB/s，对 CPU 提交 DMA 的 22.4 GB/s；1 MiB 时两者都接近 830 GB/s | §5.3 |
| 缺失率敏感性 | 缺失率 0%→40%，XM-Sparse mean TBT 72.09→84.98 ms（**+17.9%**），HiSparse 72.36→250.17 ms；40% 缺失时 TBT 相对 HiSparse **−66.0%** | §5.3 |

## 与已有页的增量
新闻早读已提过 XM-Sparse 与 X-Mem 硅片未到、用 B300 HBM 模拟外存这一点。本页按论文补上机制（TMA 融合取回、GPU 发起 DMA 与优先级调度）、同平台朴素接入对照，以及「吞吐数字使用固定 15% 缺失率与 round-robin 专家路由」这一评测边界。Wiki 里已有 [Adaptive DHiSparse](/papers/adaptive-dhisparse-speculative-hierarchical-kv.md)、[Fathom](/papers/fathom-sparse-decoding-offloaded-kv.md) 等把稀疏 KV 卸到主机或分层存储的路径；本篇的增量在于面向更高带宽的 scale-up 内存池，并把 K-index 也卸出去。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 用 scale-up 织物带宽换 HBM 容量，热 KV 与 K-index 分层驻留
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) — 长上下文 decode 的容量与取回延迟
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 评测用每卡 900 GB/s 的 NVLink 5.0，并与 PCIe / CXL / NVLink-C2C 对照
- [Adaptive DHiSparse](/papers/adaptive-dhisparse-speculative-hierarchical-kv.md) — 主机卸荷稀疏 KV 的前序路线

## 开放问题
- 内存池是 X-Mem VM 仿真：四张 B300 充当内存节点，超过 1 TB 的容量靠反复映射物理内存；硅上的 X-Mem 尚未纳入本评测。
- 最高吞吐数字使用固定 15% 缺失率与 round-robin 专家路由；真实轨迹上的比较主要是相同 batch 下的 mean TBT。
- Table 1 中 X-Mem 的 900 GB/s / 数十 TB 是作者给出的池规格，实验里能直接观察的是这套仿真平台上的带宽与容量行为。
- 对照系统 ECHO、HiSparse 尚未单独建页，跨论文数字需回到各自原文。

# Citations
- [arXiv:2611.22280](https://arxiv.org/abs/2611.22280) — Sun, Liao, Huang, Chen, Lazarev, Zhong（Netpreme / HKUST / NUS；Sun 与 Huang 在 Netpreme 实习期间完成）
- [raw stub](/raw/papers/xm-sparse-scale-up-memory-pool.md)
- [PDF](/raw/papers/XM_Sparse_Scale_Up_Memory_Pool_2026.pdf)
