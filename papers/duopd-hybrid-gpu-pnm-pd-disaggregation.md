---
type: Paper
title: "DuoPD: Hybrid GPU and Processing-Near-Memory with Shared DRAM for PD Disaggregation"
description: "SNU — HBM4 逻辑 die 内嵌 PNM 跑完整 decode，GPU 同时跑 prefill，经 TSV 层分时共享带宽；端到端吞吐比常规 PD 分离最高 2.23×；PNM 6.51 mm²（7 nm 折算）放得进 38.6 mm² 空余"
tags:
- disaggregated-inference
- prefill
- decode
- pim
- near-memory-processing
- hbm
- tsv
- 3d
- serving-system
- gpu
- simulator
created: 2026-10-21
updated: 2026-10-21
timestamp: '2026-10-21T00:00:00Z'
paper_author: [Sanghyeok Han, Inseong Choi, Byungkuk Yoon, Gyeonghwan Park, Jae-Joon Kim]
year: 2026
arxiv: '2610.26131'
sources:
  - raw/papers/DuoPD_Hybrid_GPU_PNM_PD_Disaggregation_2026.pdf
  - raw/papers/duopd-hybrid-gpu-pnm-pd-disaggregation.md
---

# DuoPD：GPU 与 HBM 近存计算共享 DRAM 的 PD 分离

## 一句话结论
把 decode 整个搬进 HBM 逻辑 die 上的轻量近存计算单元（PNM），GPU 只做 prefill；两者在 TSV 接口上交错访问同一份 HBM。这样 prefill 吃满算力、decode 吃满带宽，一套 GPU+HBM 同时干两种活，省掉常规 PD 分离里两边各自闲置的资源。

## 动机
- 常规 PD 分离：prefill 实例带宽闲着，decode 实例算力闲着（论文测得 decode 实例与 prefill 实例的带宽利用率差距最高 10.60×）。
- GPU 内 SM 切分（intra-GPU PD）有天然权衡：decode 要很多 SM 才能把带宽吃满，留给 prefill 的算力就少。
- 已有 PIM/PNM 方案靠加大内部带宽（面积、功耗、容量代价大），且只卸载 attention 或 MoE 等部分 decode 算子。

## 方案
1. **紧凑 PNM 微架构**：放进 HBM4 逻辑 die；SIMD PE，1 GHz，16 条 lane × 1,024 个 FP16 乘法器，峰值 32 TFLOPS，1 MB SRAM 缓冲。
2. **TSV 层带宽共享**：GPU 在算前一批已取数据时，PNM 从 HBM 流式取数；内存控制器给 PNM 发同步信号，PNM 缓冲在对齐时刻驱动 TSV，DRAM core die 不改。仲裁策略有 prefill 优先、decode 优先、混合三种，TTFT 对策略更敏感。
3. **分层数据映射**：GPU 级 TP/PP/EP + 单个 GPU-HBM 引擎内的 PNM 级并行；PNM 路径对权重只读以隔离保护。
4. 开源周期级模拟器（GPU+PNM，接 DRAMSim3）。

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| 评测配置 | 8 颗 GPU，每颗 8 个 HBM4 栈（每栈 2 TB/s、48 GB），GPU 2.5 PFLOPS FP16（对标 GB300），PD 间 NVLink5 900 GB/s；输入 8K–32K、输出 32–512 token |
| 端到端吞吐 vs 基线（1:1/3:1 PD 分离、chunked prefill） | GPT3-175B 平均 **1.46–2.23×**，LLaMA2-70B **1.29–1.61×**，Qwen3-235B-A22B **1.45–1.78×** |
| vs SM 切分（B200 实测带宽-SM 关系） | 5:5 切分 TPOT 持平但 TTFT 差 **1.93× / 1.66×**；9:1 切分 TTFT 持平但 TPOT 高 **>5×** |
| 面积 | HBM4 逻辑 die 约 **140.8 mm²**，去掉 TSV/PHY 后空余 **38.6 mm²**；PNM 合计 **6.51 mm²**（28 nm 综合后折算 7 nm；SIMD 3.64、缓冲 1.25、向量单元 1.56） |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 把 PD 分离从「两组 GPU」改成「同一 GPU-HBM 引擎里的两类计算体」
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — 利用 HBM 逻辑 die 的空余面积与 TSV，属于 base-die 定制路线
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 同样用 3D 堆叠逻辑做分离式 serving，可对照 decode 放在哪一层
- [SPIMoE](/papers/spimoe-hybrid-sparsity-reasoning-moe-pim.md) — 典型「只卸载部分算子到 PIM」路线，DuoPD 明确反对这种部分卸载
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)

## 开放问题
- 全部结论来自模拟 + 综合折算，HBM4 base die 能否由 GPU 厂商之外的人定制（JEDEC custom HBM）决定落地路径。
- KV 容量仍受同一 HBM 限制；decode batch 受容量上限约束，长上下文 + 大 batch 时 PNM 的 1 MB 缓冲是否够用论文未展开。
- 与 Duplex 比较时假设 Duplex 无容量损失、DuoPD 另加 4× 带宽/算力变体，需看原文图 13 细读。

# Citations
- [arXiv:2610.26131](https://arxiv.org/abs/2610.26131) — Han et al., 2026
- 模拟器：https://github.com/SNU-VLSI-DRAM/PD-intra-disaggregation-with-HBM-NDP
