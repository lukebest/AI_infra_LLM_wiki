---
type: Paper
title: "HyPAIC: Personal AI Computer with High Bandwidth Flash for High Performance Trillion-Parameter LLM Inference"
description: "SK hynix HPCA’27 Rev. — PAIC 接入 HBF；1T MoE 单机 vs 8 台无 HBF 基线 E2E 吞吐最高 1.04×、TDP 归一最高 3.59×；小模型 ≥50 tok/s/task 并发最高 4×"
tags:
- inference
- serving
- moe
- hbf
- flash
- lpddr
- memory
- prefetch
- edge
- paic
- sk-hynix
- llm
- throughput
created: 2026-11-06
updated: 2026-11-06
timestamp: '2026-11-06T00:00:00Z'
paper_author: [Minho Ha, Myunghyun Rhee, Euiseok Kim, Hoshik Kim]
year: 2026
venue: HPCA 2027 Revision #545
arxiv: '2611.04144'
sources:
  - raw/papers/HyPAIC_HBF_Personal_AI_Computer_2026.pdf
  - raw/papers/hypaic-hbf-personal-ai-computer.md
---

# HyPAIC：带 HBF 的个人 AI 计算机

## 一句话结论
SK hynix 提出 HyPAIC：在 PAIC 上接入 High Bandwidth Flash，**只读权重放 HBF、可变 KV/激活放 LPDDR**；用预取、只读放置与粗粒度访问缓解延迟/耐久/页粒度。仿真中，1T MoE 上**单台 HyPAIC**相对**八台无 HBF 基线合计**，E2E 吞吐最高 **1.04×**、TDP 归一吞吐最高 **3.59×**；小模型上维持 ≥50 decode tok/s/task 的并发任务数最高 **4×**。

## 动机
- 前沿 MoE（DeepSeek-V4-Pro 1.6T、Kimi K2.5 1T 等）把本地 PAIC（DGX Spark / Ryzen AI Halo）的 LPDDR 统一主存顶满：权重占满后 KV 空间被挤，上下文变短。
- SSD 卸荷带宽过低；多机 scale-out 抬高功耗与成本。
- HBF 相对 HBM 容量 **>10×**，并提供 TB/s 级带宽；延迟、写耐久与页粒度需要与「低 batch、稀疏专家访问」的 PAIC 负载对齐。

## 方案
1. **异构主存**：GPU 侧统一地址空间；两颗 HBF cube（文中假设合计约 1.15 TB / 2 TB/s）与 LPDDR 并存。
2. **放置**：只读权重驻 HBF；KV、激活等可变数据驻 LPDDR，两条物理接口可同时吃满带宽。
3. **缓解**：LHB 预取（稠密权重静态表 + 路由专家预测 hint）、只读放置规避写磨损、专家张量粗粒度对齐页/通道。
4. **评测**：扩展 NVIDIA AIConfigurator；对照多台 DGX Spark（200 GbE）与单台 HyPAIC。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 1T MoE：单 HyPAIC vs 8 台无 HBF 合计 E2E 吞吐 | 最高 **1.04×** |
| 同上 TDP 归一吞吐 | 最高 **3.59×** |
| 小模型：≥50 decode tok/s/task 并发任务数 | 最高 **4×** |
| HBF 相对 HBM 容量（文中陈述） | **>10×**，TB/s 级带宽 |

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 权重走 HBF、KV 走 LPDDR 的双路径预算
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — HBF/闪存容量层相对常规 NVMe 卸荷
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 边缘 PAIC 上的异构存储推理
- [DRAM and Memory System](/concepts/dram-memory-system.md) — LPDDR 作为可变运行时层
- [NORmal](/papers/normal-3d-fenor-lpddr6-main-memory.md) — 同属 LPDDR/闪存主存扩展主题
- [Trillion-param MoE HBF provisioning](/papers/trillion-param-moe-hbf-memory-provisioning.md) — 万亿 MoE × HBF 供给膝点

## 开放问题
- HBF 规格仍在演进；散热与写耐久在更广写路径上仍是落地约束。
- 仿真未细模 wear leveling / GC / ECC 等设备管理开销。

# Citations
- [arXiv:2611.04144](https://arxiv.org/abs/2611.04144) — Ha, Rhee, Kim, Kim, SK hynix, HPCA 2027 Revision #545
- [raw stub](/raw/papers/hypaic-hbf-personal-ai-computer.md)
