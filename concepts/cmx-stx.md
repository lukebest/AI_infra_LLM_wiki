---
type: Concept
title: CMX & STX
description: NVIDIA 推理存储平台：CMX（Tier G3.5 NVMe KV cache）+ STX（BF-4 存储 rack 参考架构）
tags:
- nvidia
- storage
- inference
- kv-cache
- hardware
timestamp: '2026-05-08T00:00:00Z'
created: 2026-05-08
sources:
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
---

# CMX & STX（Context Memory Storage Platform）

NVIDIA 推理存储平台，解决长上下文和 agentic workloads 下 KV cache 快速增长的瓶颈。

## CMX（Context Memory Storage）

### 问题
- KV cache 随 input sequence length × 用户数线性增长
- HBM 容量不足 → Host DRAM 扩展（也有限）→ 需要 NVMe 层
- Prefill 性能（TTFT）直接受限于 KV cache 容量

### 架构："Tier G3.5"
在推理内存层次中新增中间层：
- **G2**: GPU HBM（最快、最贵、最小）
- **G3**: Host DRAM
- **G3.5**: CMX NVMe（BlueField-4 NIC 连接）← 新增
- **G4**: 共享存储（NVMe/SATA/HDD）

### 本质
- 存储服务器通过 BlueField-4 DPU 连接到计算服务器
- 从 Connect-X NIC 换成 BlueField-4
- 品牌演变：ICMS → CMX（2026 CES 首次以 ICMS 名称公布）

## STX（Storage Rack Architecture）

CMX 的 rack 级参考架构，标准化推理集群的存储层设计。

### 硬件配置
- **每 STX box**：2× BF-4 单元
- **每 BF-4**：1× Vera CPU + 2× CX-9 NIC + 2× SOCAMM
- **每 STX rack**：16 box = 32 Vera CPU + 64 CX-9 NIC + 64 SOCAMM

### 生态
NVIDIA 列出所有主流存储供应商支持 STX：
AIC, Cloudian, DDN, Dell, Everpure, Hitachi Vantara, HPE, IBM, MinIO, NetApp, Nutanix, Supermicro, QCT, VAST Data, WEKA

## 战略意义

NVIDIA 逐步标准化集群各层：
- ✅ Compute layer（GPU + LPU）
- ✅ Network layer（NVLink + Spectrum-X）
- 🔄 **Storage layer**（CMX + STX）
- 🔄 Infrastructure operations（BlueField DPU）

## 相关页面
- [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) — 推理计算侧
- [Nvidia Groq 3 Lpx](/entities/nvidia-groq-3-lpx.md) — LPX 推理加速器
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 解耦推理架构

# Citations

[1] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
