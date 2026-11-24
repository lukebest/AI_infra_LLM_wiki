---
type: Paper
title: "SURMA: On-Die Scale-Up Remote Memory Access for SuperPOD"
description: "清华大学 / 腾讯 / 港科大 — 双 FPGA 原型 + 两台 8-GPU Hopper；512 B 粒度单 SM 吃满可达带宽，NVLink 需超过 14% SM；共享队列把提交从 1.2 µs 降到 400 ns；512-GPU 估计占 GPU 面积不到 0.5%；轨迹回放上四模型推理 1.05–1.26×"
tags:
- accelerator
- gpu
- nvidia
- noc
- interconnect
- scale-up
- nvlink
- rdma
- communication
- inference
- serving
- moe
- kv-cache
- latency
- throughput
- chip-design
- supernode
- fabric
created: 2026-11-18
updated: 2026-11-18
timestamp: '2026-11-18T00:00:00Z'
paper_author: [Haoran Shang, Weifeng Zhang, Mengzhu Li, Huizheng Wang, Sihan Guan, Xinyang Huang, Bowen Liu, Ran Shu, Xinru Tang, Ruoyu Wu, Yinben Xia, Xiang Li, Zekun He, Yachen Wang, Xianneng Zou, Jinyi Deng, Yang Hu]
year: 2026
venue: arXiv preprint
arxiv: '2611.21274'
sources:
  - raw/papers/SURMA_Scale_Up_RMA_SuperPOD_2026.pdf
  - raw/papers/surma-scale-up-rma-engine.md
---

# SURMA：把 SuperPOD 上的细粒度远端访存做到 GPU 片上

## 一句话结论
清华大学、腾讯与港科大提出 **SURMA**，一颗做在 GPU 裸片上的 Scale-Up Remote Memory Access 引擎：SM 只写压缩 WQE、不碰 payload。信用制共享发送队列把提交延迟从门铃路径的 **1.2 µs** 降到约 **400 ns**；融合 write-with-atomic 让多应用共享连接并各自得到完成通知；Network Per Path Ordering（NPPO）保证完成标志落在数据之后，且不用 Sender / Receiver Ordering。双 Agilex 7 FPGA 原型在 200 MHz 上跑到 **47.6 GB/s**（线速 50 GB/s）；同一 RTL 外推到 1.8 GHz 为 **460.8 GB/s**，对得上 Hopper 的 450 GB/s NVLink。在两台 8-GPU Hopper 服务器上，512 B 粒度只需 **1** 个 SM 就能吃满可达带宽，SM 驱动的 NVLink 传输需要超过 **14%** 的计算核。相对 per-QP 直接提交，共享把片上面积减 **96.2%**，在 512-GPU SuperPOD 的估计下占 GPU 面积不到 **0.5%**。用 GPU 轨迹替换重叠阶段后，四个 MoE 模型的 TTFT / TPOT 相对 NVLink 为 **1.05–1.26×**。

## 动机
SuperPOD 的 scale-up 带宽与往返时间一起变大（文中：每 GPU 单向带宽近十年从 NVLink 2 的 150 GB/s 升到 NVLink 6 的 1.8 TB/s；NVL576 还要再加一层交换机）。SM 自己做远端访存会占住 SMEM / 寄存器里的在途数据，并争用 SM 到 NoC 的端口。现成 CopyEngine 能卸载搬运，但在 **7 KB** 粒度下只用到不到 **1%** 的 NVLink 带宽。LLM serving 的传输又细：MLA 的一条 KV 项可小到 **576 B**，MoE dispatch 一个 token 约 4 或 7 KB。在 450 GB/s 链路上，7 KB 只要约 16 ns，而门铃提交约 1.2 µs、把完成标志排到数据之后约 2 µs。直接把 RDMA 搬上裸片还会碰到：门铃慢、每应用连接状态过大（文中 per-QP 队列可到 4.5 GB 量级）、共享连接上的队头阻塞，以及多路径传输的排序代价。

## 方案
1. **分工**：SURMA 做事务层，传输 / 链路 / 物理层留给 scale-up 互连。源端把所有 SM 的请求收进一条共享发送队列，按共享连接调度，用 DMA 从本地 HBM 读 payload，并在每条路径的尾包上附完成原子；目的端把 payload 写入设备内存，等对应写完成后再提交原子。
2. **共享发送队列（SSQ）**：SM 把 WQE 直接写入引擎内的队列，去掉 HBM 门铃往返。多 QP 共用一条 SQ，靠信用与调度避免拥塞控制互相干扰；也接受向量存储一次写入多条 WQE，以维持 576 B 粒度下约 50 GB/s 的请求流。
3. **非阻塞连接共享**：融合 write-with-atomic，让共享连接上的各事务独立通知完成。
4. **NPPO**：按路径保证「数据先于完成标志」，从而不用整条消息的 Sender / Receiver Ordering，把每事务状态从 MB 量级压下去。
5. **数据面**：支持 1D/2D/3D 传输与独立源/目的 stride，融合 kernel 可以直接把算出的矩阵 tile 发出去。

## 效果（论文数字）
评测分三块，都要单独读限定。

**占用（Hopper 两卡点对点，用一组 SM 发 TMA、按 FPGA 测得吞吐模拟 SURMA）**
- 512 B 粒度：**1** 个 SM 吃满可达带宽；256 B 需要 **2** 个 SM。NVLink 曲线近似线性，要超过 **14%** 的计算核才能达到同一带宽。

**FPGA 机制（两块 Agilex 7，背靠背 8 路径，200 MHz、2048-bit 数据通路 51.2 GB/s）**
- 相对门铃 RDMA + Sender Ordering：SSQ 把提交从 **1.2 µs** 降到 **400 ns**；SSQ + NPPO 把 **16 KB 及以下** 传输的完成时间减 **54%**。
- 相对 per-QP 直接提交与连接：共享减片上面积 **96.2%**。原型本身占 51,030 ALM，共享队列 256 KB；512-GPU 配置所需的 2.25 MB QPC 计入面积估计，结论是不到 GPU 面积的 **0.5%**。
- 时钟外推：1.8 GHz 给出 **460.8 GB/s**（引言亦给出按线速比例的 **427 GB/s**）。

**整网推理（在 GPU 上采集 Qwen3-Next-80B、Qwen3-235B、GLM4.5-Air、Ling-flash-2.0 轨迹，把计算–通信重叠阶段换成 SURMA 实测）**
- 所有配置的 TTFT（prefill）与 TPOT（decode）相对 NVLink 为 **1.05–1.26×**。
- Qwen3-235B：prefill 受计算限制，加速几乎恒为约 **1.14×**；decode 受 MoE 通信限制，从 **1.069×** 升到 **1.109×** 后走平。
- Qwen3-Next-80B：两阶段都受通信限制；prefill 从 **1.131×** 降到 **1.053×**（摊还占上风），decode 从 **1.085×** 升到 **1.126×**（通信占比随 batch 上升）。

## 与 wiki 的关系
- [NVLink / NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 把细粒度 RMA 做成 SuperPOD scale-up 路径上的片上引擎
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 通信不再占用超过 14% 的 SM，只留 1–2 个 SM 提交 WQE
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 与集体通信卸载同一条线，粒度下到 576 B 的 KV 项与 MoE token
- [Zero-SM NCCL](/papers/zero-sm-nccl.md) — 用现有 CE + host API 做无 SM 集体；SURMA 是新的片上引擎，针对 CE 吃不满的细粒度
- [T-CCL](/papers/t-ccl-tma-collective-communication.md) — 占用实验里用 TMA 模拟 SURMA 的提交侧

## 开放问题
- 端到端加速来自轨迹回放，不是一颗已经焊上 SURMA 的 GPU。
- SM 占用曲线把 SURMA 模拟成按 FPGA 吞吐发 TMA 的 SM 组。
- 面积不到 0.5% 是 512-GPU SuperPOD 假设下、相对 per-QP 队列的估计；原型本身只为单对目的地持有 8 条路径的连接状态。
- 1.8 GHz 带宽是按时钟线性外推。
- 评测服务器是 Hopper（450 / 200 GB/s NVLink），对 NVL72 / NVL576 的更长 RTT 与更高带宽，文中主要用模型论证必要性。


2026-11-24：[ScaleWire](/papers/scalewire-scale-up-ethernet-simulation.md) 从网卡机制和片上缓存配额的角度仿真 scale-up Ethernet，可与本页的 RMA 引擎对照。

# Citations
- [arXiv:2611.21274](https://arxiv.org/abs/2611.21274) — Shang, Zhang 等；清华大学 / 腾讯 / 香港科技大学
- [raw stub](/raw/papers/surma-scale-up-rma-engine.md)
