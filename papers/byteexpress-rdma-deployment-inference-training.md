---
type: Paper
title: "Deploying RDMA for Large-Scale Inference and Training Workloads (ByteExpress)"
description: "字节跳动/复旦 — 参数服务器式推荐推理/训练里两年多的 RDMA 生产经验：RDMA 感知分配器+零拷贝、QP 复用、接收 credit、软件发送窗口、RPC 层恢复；推理 fetch 平均/P99 延迟 −35.7%/−43.7%、CPU −10.69%；训练只靠 DCQCN 时 P99 反而劣于 TCP，加软件窗口后 push P99 −74.0% 且无 PFC 暂停"
tags:
- rdma
- bytedance
- rpc
- flow-control
- congestion-control
- training
- inference
- infrastructure
created: 2026-10-13
updated: 2026-10-13
timestamp: '2026-10-13T00:00:00Z'
paper_author: [Yibo Huang, Yi Cui, Yukai Huang, Huaping Zhou, Jiancong Tong, Zhaoyu Wu, Gen Miao, Haoran Wei, Boyan Ding, Zhuo Jiang, Jianxi Ye, Yibo Zhu, Chuanxiong Guo, Yang Xu, Jie Wu]
year: 2026
arxiv: '2610.12815'
venue: arXiv preprint (cs.DC / cs.NI)
sources:
  - raw/papers/ByteExpress_RDMA_Deployment_Inference_Training_2026.pdf
  - raw/papers/byteexpress-rdma-deployment-inference-training.md
---

# ByteExpress：把 RDMA 用进生产 ML 服务，靠的是硬件之上的那层软件

## 一句话结论
在字节跳动参数服务器架构（今日头条/TikTok 推荐、搜索、广告）里，把 TCP 换成 RDMA 只是开始：变长消息、大量并发连接、突发 incast 与服务故障都需要 RNIC 之上的软件层来管理。ByteExpress（BE）挂在既有 RPC 框架 Archon 下面，用 RC 传输，给出三条经验：缓冲管理要跨应用层与传输层；连接、接收容量、在途数据要分层分别管控；可用性要在传输层之上恢复。

## 方案
| 问题 | 机制 |
|---|---|
| 零拷贝需要应用缓冲可被 RNIC 访问 | 基于 rpmalloc 的 `bemalloc`：大块注册、摊薄 MR 开销，接收缓冲所有权直接交给应用线程 |
| 连接状态与驱动锁争用 | 同目的地 socket 共享 engine（一个 RC QP）做 QP 复用；线程域隔离共享驱动结构 |
| 发送方耗尽对端 posted receive | 接收 credit：SEND / WRITE_WITH_IMM 消耗 credit，接收端批量补充 |
| incast 下 DCQCN 不够 | 每 engine 软件发送窗口限制在途字节，配合分片调度；DCQCN 与 PFC 继续保留，各管一层 |
| 故障恢复需要服务上下文 | 保留 RPC 级超时、重试、副本选择与 TCP 回退，加连接监控 |

- 选 RC 的依据：100 Gbps、1,024 B MTU 下 RC 达 **92.26 Gbps**、UD 只有 **48.29 Gbps**；200 Gbps、4,096 B MTU 下 RC **191.36** vs UD **114.70 Gbps**。

## 效果（仅论文数字）
- 生产推理（300 参数服务器 + 124 ranker，25 Gbps ConnectX-5）：参数 fetch 平均延迟 **−35.7%**、P99 **−43.7%**；峰时总 CPU 从 **57.45%** 降到 **51.31%**（相对 **−10.69%**）。
- 生产训练（124 参数服务器 + 346 trainer）：只用硬件拥塞控制时 P99 fetch/push 均高于 TCP 且出现 PFC 暂停；加软件窗口后 P99 fetch **1.04 s → 338 ms**，P99 push **268 ms**（相对 TCP **−74.0%**），测量期间无 PFC 暂停。
- RDMA 系统已支撑生产推荐服务**两年以上**。

## 与 wiki 的关系
- [Network Interface & System Design](/concepts/network-interface-and-system-design.md) — credit 流控与拥塞控制分层的生产实例
- [PCM](/papers/pcm-programmable-congestion-management-rdma-nic.md) — 同周的 RDMA 拥塞管理工作：PCM 把策略下沉到 NIC，BE 在主机软件层补窗口
- [MRC](/entities/mrc.md) — 训练集群 RDMA 传输的另一条路线（多路径+选择性重传）
- [GPU-Initiated Communication Dissected](/papers/gpu-initiated-communication-dissected.md) — NI 边界上队列/完成语义的工程细节

## 局限与开放问题
- 负载为推荐系统参数服务器、25 Gbps NIC，与 LLM 集合通信（大消息、GPU 直连、400–800G）差别明显；可迁移的主要是分层控制的原则。
- 论文未量化节省的 CPU 被应用如何利用，也未直接测训练端到端吞吐（用 P99 作代理）。

# Citations
- Huang et al., "Deploying RDMA for Large-Scale Inference and Training Workloads", arXiv:2610.12815, 2026. [raw](/raw/papers/byteexpress-rdma-deployment-inference-training.md) · [PDF](/raw/papers/ByteExpress_RDMA_Deployment_Inference_Training_2026.pdf)
