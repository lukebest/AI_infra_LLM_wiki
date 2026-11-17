---
type: Paper
title: "WaferTetris: Efficient Freeform Mapping on Wafer-Scale Accelerators"
description: "Edinburgh / Waterloo / Toronto — 商用 WSE-3 实测；相对重实现 CU.POKer 系统吞吐 3.24–4.42×；相对 WaferLLM per-user 1.04–1.10×，LLaMA3.1-8B 上下文 80k vs 44k（1.8×）"
tags:
- wse
- cerebras
- spatial-execution
- compiler
- inference
- decode
- mesh
- now
- network-on-wafer
- llm
- throughput
- noc
- programming-model
created: 2026-11-17
updated: 2026-11-17
timestamp: '2026-11-17T00:00:00Z'
paper_author: [Dayou Du, Congjie He, Andrew Boutros, Luo Mai, Vaughn Betz, Jianyi Cheng]
year: 2026
venue: arXiv preprint
arxiv: '2611.18527'
sources:
  - raw/papers/WaferTetris_Freeform_Wafer_Mapping_2026.pdf
  - raw/papers/wafertetris-freeform-wafer-mapping.md
---

# WaferTetris：在晶圆上做自由形映射

## 一句话结论
Edinburgh / Waterloo / Toronto 的 **WaferTetris** 去掉晶圆级加速器上矩形 PE island 的几何限制，用复发吞吐模型选择空间并行度，并用带 per-color gate 的架构模型把现有 FPGA 布局布线算法约束到 WSE 路由上，同时保留原有 PE-task 代码。评测在商用 [Cerebras WSE-3](/entities/cerebras-wse.md) 硬件上进行（标为 WSE-2 的配置只是把可用区域限制到 WSE-2 织物尺寸）。对重实现的模板自动映射基线 CU.POKer，LLM 解码系统吞吐为 **3.24–4.42×**（Qwen2.5-7B 在 1k/4k 为 **4.42×**），PE 利用率超过 **93%**（LLaMA 上达 **98.0%**）。对手工优化的 [WaferLLM](/concepts/waferllm-system.md)，在双方都能跑的 WSE-3 配置上 per-user 吞吐为 **1.04–1.10×**，LLaMA3.1-8B 的最大成功上下文从 **44k** 提到 **80k**（**1.8×**）。

## 动机
现有晶圆映射为了生产率采用矩形 PE island 模板（自动系统如 CU.POKer，手工优化如 WaferLLM）。几何约束造成空间碎片：空闲 PE 总数够，但形状对不上所需 island，系统就缩小 island。文中例子：WaferLLM 在 WSE-3 上做 LLaMA3.1-8B 解码时，可用织物预算 862.5k PE 中约 344k 未分配，大约 40% 的峰值浮点算力与本地 SRAM 被闲置。改变 PE 分配还会改变 island 尺寸，往往要重写 PE-task 代码。

## 方案
1. **自由形打包**：在不改提供的 PE-task 代码与逻辑连接的前提下，按 Tetris 方式把计算灵活铺到织物上，并使用 **98% PE 预算**，留 2% 给路由资源。
2. **复发吞吐模型**：把应用变成带时序的图，用最大环平均作为 initiation interval，把分支-汇合依赖纳入稳态流水吞吐预测，用来选择空间并行度。
3. **Per-color gate + FPGA P&R**：把 WSE color 映射为 routing track，在每个 PE 加每 color 一个单位容量门，使同一 color 上进出或穿过该 PE 的流都经过该门，从而把冲突暴露为普通拥塞；实验把织物划分为 **8×4** 网格做布局布线（在 LLaMA3.1-8B、32 层、4K 上比较过多种模板，8×4 最好）。
4. **平台与基线**：WSE-3 约 900k PE、阵列 762×1172，每 PE 约 48 kB SRAM（约 40 kB 留给数据），应用可用 21 个 color。CU.POKer（Jiang et al., 2020）为闭源，作者重实现其已发表的模板算法。与 WaferLLM 比较时，使用其优化过的融合 kernel 作为 mapping unit。

## 效果（论文数字）
§5.2–§5.3 的吞吐与 PE 利用率为商用 WSE-3 上的测量。

**对 CU.POKer（同织物、系统解码吞吐，Figure 9）**

| 模型 | 1k | 2k | 4k | WaferTetris PE | CU.POKer PE |
|---|---:|---:|---:|---|---|
| Qwen2.5-7B | **4.42×** | 4.33× | **4.42×** | 93.2 / 93.2 / 97.4% | 53.7 / 54.3 / 57.1% |
| LLaMA3.1-8B | 3.66× | **3.24×** | 3.36× | 98.0% | 54.5 / 56.0 / 59.8% |
| LLaMA2-13B | 3.91× | 3.72× | CU.POKer OOM；本文 **76.8k tok/s** | 98.0% | 82.4 / 85.0% / — |

**对 WaferLLM（融合 kernel，per-user 吞吐，Figure 11）**：双方都能跑的 WSE-3 配置上为 **1.04–1.10×**。LLaMA3.1-8B 在 WSE-2 与 WSE-3 两种预算下，最大成功上下文均为 **80k vs 44k（1.8×）**。WSE-2 预算下，WaferTetris 能跑 LLaMA2-13B 的 512 与 1k，WaferLLM 在所有测试长度上 OOM。

**Stencil（Figure 10）**：Gray-Scott 约 **1.26×**（PE 利用率 75.0%→96.3%）；弹性波 **1.18–1.21×**（83.3%→97.6%）。

消融（4k、WSE-3）：自由形相对矩形把测量吞吐从 70.1k 提到 94.7k tokens/s（LLaMA3.1-8B）、从 48.2k 提到 76.8k tokens/s（LLaMA2-13B）。按复发模型选出的映射，测量吞吐是按最慢单元选出者的 **1.75–2.49×**。LLaMA2-13B 上，一次共享剖面 90.00 分钟，之后每次映射 **36.84–37.34** 分钟。

## 与 wiki 的关系
- [Cerebras WSE](/entities/cerebras-wse.md) — 评测平台；文中 WSE-3 约 900k PE、762×1172，出货晶圆约 7.2% 物理核未激活
- [WaferLLM System](/concepts/waferllm-system.md) — 手工优化基线；Congjie He / Luo Mai 继续同一条晶圆 LLM 栈
- [WaferLLM 论文页](/papers/waferllm-wafer-scale-llm-inference.md) — 2025 年端到端晶圆 LLM 推理系统
- [MeshRT](/papers/meshrt-wafer-scale-runtime.md) — 同一作者组在运行时动态上的后续；WaferTetris 补的是映射几何
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 把 color 路由约束交给 FPGA 风格 P&R
- [Cerebras Color 机制](/concepts/cerebras-color-mechanism.md) — per-color gate 把冲突暴露为拥塞
- [MOCAP Prefill Pipelining](/papers/mocap-wafer-scale-chunked-pipelining.md) — 晶圆 prefill 流水的另一条线

## 开放问题
- 应用图的算子融合与划分仍由应用给出；自动划分列为开放问题。
- 尚未消费出货 WSE-3 约 7.2% 未激活核的缺陷图；在孔洞周围做自由形放置列为后续工作。
- CU.POKer 为重实现。延迟模型的 LOOCV 评估的是已剖面 kernel 家族内的泛化。

# Citations
- [arXiv:2611.18527](https://arxiv.org/abs/2611.18527) — Du, He, Boutros, Mai, Betz, Cheng；Edinburgh / Waterloo / Toronto
- [raw stub](/raw/papers/wafertetris-freeform-wafer-mapping.md)
