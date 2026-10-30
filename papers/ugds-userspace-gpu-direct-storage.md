---
type: Paper
title: "uGDS: User-Space GPU Direct Storage for KV Offload"
description: "HKUST(GZ)/ScaleX-IO — 用户态 NVMe 控制路径 + PCIe P2P 载荷；batch 读/写相对 GDS 最高 12.12×/30.69×；LMCache 中位 TTFT −62.7%、goodput 2.63×"
tags:
- storage
- gpu
- inference
- kv-cache
- serving-system
- latency
- throughput
- hardware
- llm
created: 2026-10-30
updated: 2026-10-30
timestamp: '2026-10-30T00:00:00Z'
paper_author: [Jing Wei, Guanyi Chen, Qi Chen, Chuyu Zhang, Zheng Zhou, Chutian Wang, Jian Zhang]
year: 2026
venue: arXiv cs.DC
arxiv: '2610.30868'
sources:
  - raw/papers/uGDS_UserSpace_GPU_Direct_Storage_2026.pdf
  - raw/papers/ugds-userspace-gpu-direct-storage.md
---

# uGDS：用户态 GPU Direct Storage

## 一句话结论
GDS 去掉了 host staging，但控制路径仍每次进内核，stream-ordered 路径还强制全序。uGDS 把 **NVMe 命令构造 / 硬件队列 / 完成** 全放用户态，载荷仍走 PCIe P2P DMA（`ugds_drv.ko` 仅一次性特权初始化）；A100+990 PRO 上 batch 读/写相对 GDS 最高 **12.12× / 30.69×**，LMCache 中位 TTFT **−62.7%**、goodput **2.63×**。

## 动机
- LLM KV offload、向量检索等把 NVMe 放进关键路径后，SSD↔GPU 微秒级软件开销会直接变成 GPU 空转。
- 商用 GDS：数据路径 P2P，但控制路径仍经 VFS/块层/内核 NVMe；stream-ordered 开销大且强制总序；闭源引擎难诊断与按访问模式调调度。

## 方案
1. **用户态控制**：CPU 构造 NVMe 命令、管理队列与完成；载荷 SSD↔GPU 直达；内核 helper 只做一次性映射/初始化。
2. **队列分区**：同步与 batch 流量分队列；跟踪 in-flight DMA，避免 SSD 仍访问时释放缓冲。
3. **API**：cuFile 风格 sync / batched / stream-ordered async；轮询或中断完成；CUDA + HIP。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Batch 读带宽 vs GDS | 最高 **12.12×**（8-KiB，batch 128） |
| Batch 写带宽 vs GDS | 最高 **30.69×**（4-KiB，batch 128） |
| 4-KiB 同步写延迟（2 线程） | **−84.1%** |
| 单 stream stream-ordered | **5.49 GiB/s**（GDS 仅保留同步带宽的 **40.8%**，约 **2.33×**） |
| LMCache 中位 TTFT | 最高 **−62.7%**（32K：1915→715 ms） |
| LMCache goodput | **2.63×** |
| AMD vs hipFile 同步写 | 最高 **1.19×** |

## 与 wiki 的关系
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — 把 KV tier 的瓶颈从介质带宽推到 **控制路径软件开销**
- [KVStream](/papers/kvstream-parallel-storage-kv-cache.md) — 多存储层并行取前缀；uGDS 优化单层 SSD↔GPU 路径
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM→DRAM→NVMe 数据路径上的用户态 GDS
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — LMCache 等前缀缓存后端可插拔替换 GDS

## 开放问题
- 跨 root-port / IOMMU 拓扑下 P2P 可达性依赖平台；多盘 RAID/文件系统语义未作为主评测。
- 与 Mooncake 等远端 KV 平面的组合未做端到端对照。

# Citations
- [arXiv:2610.30868](https://arxiv.org/abs/2610.30868) — Wei et al., 2026
- [raw stub](/raw/papers/ugds-userspace-gpu-direct-storage.md)
