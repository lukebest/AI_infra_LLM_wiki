---
type: Paper
title: "Ember: Making Unified Virtual Memory Practical for Discrete-Memory GPUs"
description: "TUM — UVM 超订时缺页驱动放置把互连带宽浪费在搬页上；Ember 让分配先映射在 host、用 GPU 约 256 个硬件访问计数器挑热区上提、按衰减批量回收；1.5× 超订下比 UVM 快 6.8–10.6×，GPU 封顶 16 GB 跑 Qwen 14B/32B 生成快 4.7–16×"
tags:
- gpu
- memory
- memory-bandwidth
- interconnect
- virtualization
- inference
- llm
- nvidia
created: 2026-10-14
updated: 2026-10-14
timestamp: '2026-10-14T00:00:00Z'
paper_author: [Senad-Leandro Lemes Galera, Michail Georgoulakis Misegiannis, Ferdinand Gruber, Jana Giceva, Dimitrios Stavrakakis]
year: 2026
arxiv: '2610.13408'
venue: arXiv preprint (cs.OS / cs.DC)
sources:
  - raw/papers/Ember_UVM_Oversubscription_Discrete_GPU_2026.pdf
  - raw/papers/ember-uvm-oversubscription-discrete-gpu.md
---

# Ember：让 UVM 超订在独立显存 GPU 上可用

## 一句话结论
工作集超过显存后，NVIDIA UVM 的缺页迁移会让「回收—迁入—再缺页」挡在关键路径上，性能断崖式下跌。Ember 把放置策略改成「先映射在 host 内存、只把计数器确认的热区搬上 GPU、冷区后台批量回收」，在不改应用、不做 profiling 的前提下把超订变成可用模式。

## 动机（论文数字与观察）
- 四个障碍：缺页时同步回收导致执行停顿；纯映射访问受互连带宽限制；预取在显存满后变成放大的回收流量；映射与迁移在 stock UVM 里不能按区域混用。
- GPU 自带约 **256** 个硬件访问计数器，统计对 host 驻留内存的访问，越阈值只写通知、不停顿 GPU；默认驱动不用它们迁移，x86 Linux 4 KiB 页下还会丢弃通知。
- 平台的显存与互连带宽比为 **~9×（GH200 NVLink-C2C）到 ~150×（H200 PCIe 5.0 ×8）**。

## 方案
| 机制 | 做法 |
|---|---|
| 混合地址空间 | 分配初始映射在 host，不迁移，GPU 直接按互连速率读 |
| 计数器驱动的区域上提 | 一个通知对应一个 VA block，但上提覆盖可配置的更大区域，以弥补计数器数量不足 |
| 衰减式提前回收 | 后台每 25 ms 把各 chunk 需求减半；占用超 90% 回收到 85%，每轮最多 16 个 chunk；500 ms 内被重新拉回的块累计迁移分以防来回颠簸 |
| 在线重放置 | 运行时跟踪热集变化 |

- 两种实现：改 NVIDIA 开源 UVM 驱动的 Ember-adaptive（需裸机加载内核模块）；在 stock CUDA 上用 `cudaMemAdvise` + 一次前缀预取的 Ember-static（每个托管分配三次调用）。

## 效果（仅论文数字）
- 六个数据密集应用、三块 PCIe GPU（RTX 5080 / A40 / H200）：约 1.5× 超订下比 stock UVM 快 **6.8–10.6×**；数据装得下时 Ember-static 平均也有 **1.9–3.0×**。
- LLM 生成（llama-bench，512 prompt + 128 输出，Qwen2.5 14B / Qwen3 32B，每卡封顶 16 GB）：1.41× 超订下 UVM 与预取只剩 **0.2–0.5 tok/s**；Ember-static 快 **4.7×（RTX 5080）/ 8–13×（A40、H200）**，摘要口径 **4.7–16×**；所有策略都不超过 **3 tok/s**，上限由互连决定。
- GH200（NVLink-C2C，仅 Ember-static）：对 UVM 的几何均值优势收窄到约 **3.5×**；128 token 生成 **62 s**，UVM-mapped 要 **211 s**；只读一遍的负载（pathfinder、radix sort）上 UVM-mapped 反而更快。
- 对 profile 引导的 HELM：端到端平均快 **7.9×**（HELM 的 profiling 占其运行时 18–95%）；只比 kernel 时间平均 **2.1×**，最高 28.0×，bfs 与 gramschm 上更慢。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — GPU 显存与 host DRAM 之间的放置层，与 HBM/HBF/CXL 分层同属「热数据进快层」问题
- [BOOST](/papers/boost-concurrent-host-hbm-llm-inference.md) — 同在 Grace Hopper 上用 host+HBM 并发，BOOST 走推理引擎内的显式波次调度，Ember 走驱动层透明放置
- [CXL Tiered Memory](/concepts/cxl-tiered-memory.md) — CPU 侧页迁移的对应物；Ember 把计数器热度信号用在 GPU 侧
- [WaferTrans](/papers/wafertrans-iommu-free-wafer-scale-gpu.md) — 同样处理 GPU 虚拟内存路径，那篇关注地址翻译

## 局限与开放问题
- 只管 `cudaMallocManaged`；库内部分配（如 Thrust 临时缓冲）看不见。
- 计数器只看 host 驻留区，GPU 驻留区何时变冷只能推断，可能误回收后再搬一次。
- 单 GPU + host 两层；多 GPU 节点上 peer 显存是第三层，论文留作未来工作。
- 对 LLM 推理的意义集中在显存不够、又不能改引擎的场景；与 vLLM/SGLang 这类显式管理 KV/权重的引擎如何组合，论文未评估（本页判断）。

# Citations
- Lemes Galera et al., "Ember: Making Unified Virtual Memory Practical for Discrete-Memory GPUs", arXiv:2610.13408, 2026. [raw](/raw/papers/ember-uvm-oversubscription-discrete-gpu.md) · [PDF](/raw/papers/Ember_UVM_Oversubscription_Discrete_GPU_2026.pdf)
