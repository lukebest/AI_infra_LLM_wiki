---
type: Paper
title: "Tideway: Phase-Aware Tiered Memory Management for MoE Inference on Consumer Devices"
description: "Duke — RTX 5090 实测；270 个固定形状端到端平均 1.97×、最高 3.18×；TraceLab TTFT 平均 2.40×（1.15×–9.04×），decode 吞吐平均 1.61×（1.20×–2.28×）"
tags:
- moe
- inference
- memory
- ssd
- dram
- edge
- prefill
- decode
- serving
- pcie
- kv-cache
- flash
- llm
- throughput
- latency
- serving-system
created: 2026-11-17
updated: 2026-11-17
timestamp: '2026-11-17T00:00:00Z'
paper_author: [Yifei Wang, Tsun-yu Yang, Yechen Xu, Hancheng Ye, Qinsi Wang, Baijun Zhou, Tingjun Chen, "Hai \"Helen\" Li", Danyang Zhuo, Yiran Chen]
year: 2026
venue: arXiv preprint
arxiv: '2611.14848'
sources:
  - raw/papers/Tideway_Phase_Aware_Tiered_MoE_2026.pdf
  - raw/papers/tideway-phase-aware-tiered-moe.md
---

# Tideway：消费级电脑上给 MoE 分阶段管内存

## 一句话结论
Duke 的 **Tideway** 把消费级 PC 上的 GPU VRAM 与主机 RAM 收成统一内存池，为 MoE 的 prefill 与 decode 切换阶段感知布局，并在专家缺页时仍重放分段 CUDA Graph。在一块 **32 GB RTX 5090** 桌面上，用 Qwen3.6-35B-A3B、Gemma4-26B-A4B、DeepSeek-V4-Flash 对比 FreeToken v0.1.2、llama.cpp（commit `67a17c1`）以及在 FreeToken 后端复现的 SSD-LLaMA 与 FlashMoE：**270** 个固定形状配置上，相对各设定下最快基线，端到端平均 **1.97×**、最高 **3.18×**（Gemma4、32 GiB RAM）；TraceLab 八段编程代理会话上端到端 **1.20×–3.14×**。TTFT 平均 **2.40×**（**1.15×–9.04×**），decode 吞吐平均 **1.61×**（**1.20×–2.28×**）。结果为该桌面上的实测。

## 动机
本地部署大规模 MoE 要在 GPU VRAM、主机 RAM 与 SSD 之间溢出权重。现有系统常把各层当成独立缓存，溢出时发生抖动：FreeToken 假定完整专家池常驻主机 RAM；llama.cpp 把分页交给 OS mmap，粒度是页而不是专家；FlashMoE 的学习替换在全模型 prefill 扫描下仍会抖动；SSD-LLaMA 跨阶段共用同一布局，会产生可避免的搬移。

## 方案
1. **统一内存池**：VRAM 与主机 RAM 抽象为统一池，SSD 作为盘外只读后备；专家可只在 VRAM、只在 RAM、或两层都有，跨层去重，并利用双向 PCIe 把被驱逐的 GPU 专家写回主机 RAM。
2. **阶段感知布局**：Prefill Layout 在主机 RAM 中锚定可复用专家，用小的 streaming window 吸收扫描流量，并以双缓冲重叠第 \(l+1\) 层送达与第 \(l\) 层计算。转到 decode 时收回借出的 VRAM 作为固定地址专家槽，主机 RAM 作 LRU 缓存。
3. **缺页仍可重放的 CUDA Graph**：每层 warmup 捕获 attention / router / experts 三段 piecewise graph，绑定到固定地址的持久 GPU 缓冲；缺页在段与段之间由主机 handler 处理，然后在同一 CUDA stream 上重放 experts graph。
4. **实现与平台**：Python + C，约 11.8K 行；代码 https://github.com/Afterglow231/Tideway。硬件为 32 核 AMD CPU、按模型把主机 RAM 上限封到 16–128 GiB、32 GB RTX 5090、PCIe 5.0、8 TB WD BLACK SN850X；测得 pinned PCIe 57.6 / 57.3 GB/s H2D/D2H，SSD 读 6.8 GB/s。

## 效果（论文数字）
模型：Qwen3.6-35B-A3B（BF16，67 GiB）、Gemma4-26B-A4B（BF16，48 GiB）、DeepSeek-V4-Flash（原生 FP4，155 GiB）。加速比相对该 model–RAM 设定下最快的基线。Figure 7(b) 图注标明 TTFT 与 decode 吞吐来自 TraceLab。PDF 摘要把 1.61× 写成 TPOT 加速，正文写成更高的 decode 吞吐。

| 指标 | 范围 | 平均 / 峰值 | 来源 |
|---|---|---|---|
| 端到端（270 个固定形状） | 1.13×–3.18× | 平均 **1.97×**；峰值 Gemma4 @ 32 GiB **3.18×** | Figure 7(a)，§6.1 |
| 端到端（TraceLab 8 段） | 1.20×–3.14× | 峰值 Qwen3.6 @ 48 GiB **3.14×** | Figure 7(a) |
| TTFT（TraceLab） | 1.15×–9.04× | 平均 **2.40×**；峰值 Qwen3.6 @ 48 GiB **9.04×** | Figure 7(b) |
| Decode 吞吐（TraceLab） | 1.20×–2.28× | 平均 **1.61×**；峰值 Gemma4 @ 16 GiB **2.28×** | Figure 7(b) |

最高 RAM、专家已能装进统一池时，仍有 1.13×–1.58× 端到端加速。DeepSeek-V4-Flash、64 GiB、32K 输入上的消融：Cross-tier Memory Manager、异步专家送达与 piecewise decode graphs 叠到总体 E2E **2.28×**；其中 decode graphs 把 TPOT 一步从 1.37× 抬到 2.04×。持久缓冲与 Residency Table 占用不到 32 GB VRAM 的 3%。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 VRAM、主机 RAM 与 SSD 收成统一池，并按阶段改布局
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — prefill 扫描与 decode 驻留是两套访问模式
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — SSD 只作只读后备，writeback 走 PCIe 上的 VRAM↔RAM
- [ThunderEP](/papers/thunderep-pcie-consumer-gpu-moe.md) — 同为消费级 GPU 上的 MoE；ThunderEP 攻 PCIe 通信，Tideway 攻分层内存
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) — 文中 FlashMoE 基线在 FreeToken 后端复现其替换预测器
- [UMLoad](/papers/umload-unified-memory-model-loading.md) — 统一内存装载的另一条线，对象偏模型加载

## 开放问题
- 评测在单机 RTX 5090 上进行，主机 RAM 为人为封顶的预算；SSD-LLaMA 与 FlashMoE 的机制在 FreeToken 后端上复现。
- KV 作为竞争租户：Tideway 先为 KV 预留容量再分配专家槽，上下文变长会挤占专家驻留；把 KV block 与专家一并纳入池，文中列为开放方向。
- 与投机解码、系统级 GPU 复用器、以及多会话共享本地模型的协同，同样列为后续方向。

# Citations
- [arXiv:2611.14848](https://arxiv.org/abs/2611.14848) — Wang, Yang, Xu, Ye, Wang, Zhou, Chen, Li, Zhuo, Chen；Duke University
- [代码](https://github.com/Afterglow231/Tideway)
- [raw stub](/raw/papers/tideway-phase-aware-tiered-moe.md)
