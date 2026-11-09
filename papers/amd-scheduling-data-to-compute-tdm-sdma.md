---
type: Paper
title: "Scheduling Data to Compute: Hierarchical Data Pipelining for LLM Training on AMD GPUs"
description: "AMD Primus/Primus-Turbo — 首个吃满 TDM/transpose-load/SDMA/RDMA 的 AMD LLM 训练系统；TDM CSA 几何均值 1.88×（峰 2.74×），transpose 1.19×，SDMA 重叠区 1.16×，分层 SDMA+RDMA 相对 CU 集体 1.33×"
tags:
- amd
- gpu
- training
- attention
- kernel
- rdma
- sdma
- cdna
- collective
- llm
- memory-bandwidth
- parallelism
created: 2026-11-09
updated: 2026-11-09
timestamp: '2026-11-09T00:00:00Z'
paper_author: [Gengyu Rao, Ghadeer Ahmed H Alabandi, Su Ann Chong, Thomas Huber, Kailash Gogineni, Subhajit Dutta Chowdhury, Saleel Kudchadker, Suchita Pati, Zirui Zhang, Zhen Huang, Yanyuan Qin, Xiaoming Peng, Lihuan Zhang, Botao Hu, Wei Huang, Yang Bo, Wen Xie, Xiangyu Zhao, Ruibin Zhang, Xiaobo Chen, Vidushi Goyal, Anshu Raina, Claire Songhyun Lee, Jiakun Yan, Yao Fu, Nusrat Islam, Ravi Dwivedula, Jie Zhang, Maria Garzaran, Zhenyu Gu, Emad Barsoum]
year: 2026
venue: arXiv preprint
arxiv: '2611.05751'
sources:
  - raw/papers/AMD_Scheduling_Data_to_Compute_TDM_SDMA_2026.pdf
  - raw/papers/amd-scheduling-data-to-compute-tdm-sdma.md
---

# Scheduling Data to Compute：AMD GPU 上的分层数据流水

## 一句话结论
AMD（Primus / Primus-Turbo）给出**首个吃满全部 GPU 数据流水特性**的 AMD LLM 训练系统：片内 **TDM**（MI455）+ **transpose-load**，跨 GPU **SDMA / RDMA**。TDM 使 DeepSeek V4 风格 **CSA**（Compressed Sparse Attention）kernel 训练步几何均值 **1.88×**（最高 **2.74×**）；transpose-load 平均 **1.19×**（排除 spill 最高 **1.21×**）；SDMA 重叠区平均 **1.16×**；分层 SDMA+RDMA 让 16/32 GPU 上重叠 GEMM 相对 CU 集体平均 **1.33×**。开源：https://github.com/AMD-AGI/Primus-Turbo 、https://github.com/AMD-AGI/Primus 。

## 动机
- 训练规模上升后，CU 常因数据仍在慢存或他卡而空转；小幅利用率损失在超大规模下代价巨大。
- 传统「多线程藏延迟」与 CU 驱动通信会占用计算资源（文中称 RCCL 可占到 MI355 约 25% CU）。
- AMD 已提供显式数据搬运 ISA/引擎，需要内核与框架协同把数据持续喂给计算。

## 方案
1. **TDM**：Tensor Data Mover 把张量从 HBM 搬入片上，并与 CSA attention kernel 的细粒度 KV tile 流水对齐。
2. **Transpose-load**：加载时完成布局转置，去掉寄存器级显式转置。
3. **SDMA / RDMA**：用专用 DMA 做机内 scale-up 与跨机 scale-out，减少 CU 被通信内核占用。
4. **分层集体**：rail 上先 RDMA、再本地 SDMA，让重叠 GEMM 相对 CU 集体更快。
5. **落地**：集成进开源 Primus / Primus-Turbo。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| TDM × CSA（几何均值） | 训练步 **1.88×**；最高 **2.74×** |
| Transpose-load（排除 spill） | 平均 **1.19×**；最高 **1.21×** |
| SDMA 重叠区 | 平均 **1.16×** |
| 分层 SDMA+RDMA vs CU 集体（16/32 GPU） | 重叠 GEMM 平均 **1.33×** |
| 系统定位 | **首个**利用全部 GPU 数据流水特性的 AMD LLM 训练系统 |

## 与 wiki 的关系
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — CDNA 侧显式数据流水相对「多线程藏延迟」
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — SDMA/RDMA 相对 CU 集体的重叠路径
- [FlashAttention](/concepts/flashattention.md) — CSA kernel 继承 FlashAttention 式片上状态 + 流式 KV
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBM→片上→跨 GPU 的分层供给
- [Meta × AMD MI350X 共设计](/papers/meta-amd-mi350x-training-codesign.md) — 同属 AMD 训练软硬协同脉络

## 开放问题
- 分层 SDMA+RDMA 集体仍在集成；更大集群上的可扩展性与故障路径待补。
- Transpose-load 在 VGPR spill 配置下收益会回落，需要寄存器预算感知的调度。

# Citations
- [arXiv:2611.05751](https://arxiv.org/abs/2611.05751) — Rao et al., AMD；lorrirao@amd.com
- [raw stub](/raw/papers/amd-scheduling-data-to-compute-tdm-sdma.md)
- https://github.com/AMD-AGI/Primus-Turbo
- https://github.com/AMD-AGI/Primus
