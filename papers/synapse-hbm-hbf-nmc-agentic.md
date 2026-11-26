---
type: Paper
title: "Synapse: HBM 协同的 HBF 近存计算，用于流水线多智能体执行"
description: "KAIST — H100 测 GPU 时间、HBF 按 OCP 参数仿真；相对 Passive HBF，三模型端到端延迟降低 48.92–66.60%，吞吐最高 2.98×，建模每 token 能量最高降低 64.48%；磨损仿真寿命大约长 46%"
tags:
- architecture
- hbf
- hbm
- near-memory-processing
- agentic-ai
- moe
- attention
- kv-cache
- llm
- inference
- energy
- memory
created: 2026-11-25
updated: 2026-11-26
timestamp: '2026-11-25T00:00:00Z'
paper_author: [Juhyeong Jin, Hyunjun Cho, Joo-Young Kim]
year: 2026
venue: preprint
arxiv: '2611.29901'
sources:
  - raw/papers/Synapse_HBM_HBF_NMC_Agentic_2026.pdf
  - raw/papers/synapse-hbm-hbf-nmc-agentic.md
---

# Synapse：让 HBF 上的注意力与专家计算与 GPU 跨智能体重叠

## 一句话结论
KAIST 提出 Synapse：在 HBM 与 High Bandwidth Flash（HBF）之间做近存计算，把就绪的注意力和专家计算放到 HBF 上，并与 GPU 上其他智能体的工作重叠。GPU 时间在 H100 上测量，HBF 计算、NAND、传输与争用按 Table 1 仿真。相对「GPU 执行、HBM miss 时从 HBF 取数」的 Passive HBF，三个模型上端到端延迟降低 **48.92–66.60%**，吞吐提到 **1.93–2.98×**，建模的每输出 token 能量降低 **46.13–64.48%**。Fortify 按 wordline 跟踪物理读，同等负载速率下寿命大约长 **46%**。

## 动机
多智能体视频推理里，共享权重加上每智能体 KV 会超出单卡 HBM。以 Qwen3-VL 235B 的 BF16 权重约 **470 GB** 为例，已是 80 GB HBM 的约 **5.9×**，再计入工具停顿期间保留的 KV。多卡切分能凑容量，但又引入通信。HBF 按 OCP 规格提供容量与较高读带宽，只把它当成被动后备存储时，智能体仍会在 GPU 上互相等待：注意力即使 KV 已在 HBM 也可能排在别的智能体后面，专家权重从 HBF 进来也会被其他读取挡住。

## 方案
Synapse 在 HBM–HBF 对上加近存数据通路，并把命令与依赖从 GPU 临界路径上挪开，主要包括：

- **Flow**：就绪的注意力在 HBF 上算，与 GPU 工作重叠。
- **Fuse**：专家计算留在 HBF，避免把专家权重搬进 GPU；共享物理读会计，一次物理读可以服务多个智能体。
- **Forward**：拆成 RWE 与 OIE——所需输入在 HBM 写确认后即可把后继标为就绪，HBF 任务不必等 GPU 空闲再下发。
- **Fortify**：按 bank / wordline 跟踪物理 NAND 读，做局部刷新，替换块级刷新。

QKV 投影与路由仍在 GPU 上。面积估计把 22 nm CACTI SRAM 按 FLINT 的比例（3.9/14.3）投影到 7 nm，MAC / 控制参考 ASAP7，并计入 ECC、摆放边距、10% 缓冲与 70% 标准单元利用率。

## 量化结果
Table 1：5×16 GB HBM2e（80 GB）；5×512 GiB HBF（2.5 TiB）；主机 512 GB DRAM；PCIe Gen5×16，H2D/D2H **55.7 / 46.1 GB/s**；D2D 最大 **1.536 TB/s**（UCIe，OCP Grade 2）；HBF 计算 **2,048** 个 BF16 MAC @ **400 MHz**（1.64 TFLOPS）；片上 **32 MiB**；2,048 个活跃 bank、4 KiB 页；t_R=3 µs，t_PROG=100 µs。GPU 能量用执行时间与 NVML 板卡功率（含 HBM）；主机、HBF 与传输能量为模型。

对照实验重放 Qwen3-VL-235B-A22B-Instruct 在 LongVideoBench 三支验证视频上的轨迹，每支 4 次、共 12 个工作流实例，256 帧；消融用 64 帧，并加入 InternVL3.5-241B-A28B 与 GLM-5.3-Flash（FP8 + FP32 状态）。默认并发 C=6，扫描 C∈{1,3,6,12}。端到端是工作流到达至末智能体完成的平均时间，含排队；吞吐是全部输出 token 除以首个到达至最后完成的墙钟。

- 完整配置相对 Passive HBF：端到端延迟降低 **48.92–66.60%**，吞吐 **1.93–2.98×**，建模每输出 token 能量降低 **46.13–64.48%**。
- 相对 Duplex + passive HBF，Case A 在 C=1、6 上端到端降低 **30.8–32.2%**，吞吐 **1.43–1.48×**，送到 GPU 的中间数据少 **37.0–42.2%**。
- 相对 ReKV、LiveVLM、Hot–Cold（均含检索与传输，C=6、256 帧）：端到端降低 **35.7–61.8%**；固定其选择与专家路由后，仍降低 **38.2–40.2%**。
- Fuse 把累计权重加载时间降低 **75.3–82.3%**（C=1,3,6,12）。在 7,090 个相同的 KV-ready 任务上，就绪到启动的平均等待在 C=3、6、12 降低 **44.9–70.2%**。
- 在已开 Flow/Fuse 的前提下重放 Sarathi-Serve 策略（C=6，命令服务 4 µs）：均值 E2E 从 **157.8 s** 降到 **139.9 s**；再加上 Forward 到 **122.8 s**、**9.51 tok/s**，相对 Sarathi 再改进 **12.2%** 与 **14.0%**。
- Fortify 在 α=1.5、100,000 P/E 预算下，完成的工作量比块级刷新多 **46.04–46.77%**，同等负载速率下寿命大约长 **46%**。
- 新增面积 **72.92 mm²**（HBM **0.120** + HBF **72.801**），相当于五个名义 HBF 封装（**878 mm²**）的 **8.29%**。

## 局限与解读
- 这是 **H100 测得的 GPU 时间 + HBF 架构仿真** 的混合评估，HBF 侧没有硅片校准；能量里的主机 / HBF / 传输部分是模型。
- 默认对照用 256 帧轨迹，完整配置的 48.92–66.60% 来自 64 帧消融、固定 2,048 MAC 与缓冲。
- QKV 与路由仍在 GPU；结论依赖「注意力与专家可以在 HBF 近存执行」这一划分。
- 面积是 22 nm→7 nm 投影，含实现余量，不是流片报告。

## 与 wiki 的关系
- [Hot–Cold HBM/HBF](/papers/hotcold-hbm-hbf-agentic-llm.md) — 同一组把热集留在 HBM、冷池放到 HBF；Synapse 进一步在 HBF 上做注意力与专家计算
- [FOREST](/papers/forest-hbf-rram-hbm-speculative.md) — HBF / RRAM / HBM 上的投机推理层次；Synapse 面向多智能体视频推理的近存重叠
- [FLINT](/papers/flint-hbf-llm-inference.md) — HBF 容量扩展与面积比例的来源之一
- [LaFlash](/papers/laflash-qlc-hbf-coding-agents.md) — QLC-HBF 上的休眠 KV；Synapse 处理的是活跃多智能体的执行重叠
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 HBF 近存计算与 GPU 流水记到同一条数据路径上
- [Mayfly](/papers/mayfly-lifecycle-aware-hbf-rsi.md) — 按 RSI 一代会话的爆发与回落管理 HBF 上的就绪 KV 与写放大
- [HBF-Sim](/papers/hbfsim-extensible-hbf-simulator.md) — GPU–HBF 请求路径仿真底座；本文是应用架构模型

# Citations
- [arXiv:2611.29901](https://arxiv.org/abs/2611.29901) — Jin, Cho, Kim（KAIST）
- [raw stub](/raw/papers/synapse-hbm-hbf-nmc-agentic.md)
- [PDF](/raw/papers/Synapse_HBM_HBF_NMC_Agentic_2026.pdf)
- [arXiv:2609.25782](https://arxiv.org/abs/2609.25782) — Hot–Cold HBM/HBF
- [arXiv:2611.32264](https://arxiv.org/abs/2611.32264) — Mayfly
