---
type: Paper
title: "TranSAGE: Automating Spatial Accelerator Generation for Large-Scale Transformer Models"
description: "ASPLOS'27 — 上交/华南理工；以「多算子流水簇」为执行单元的 MLIR 空间加速器生成器，DP 图划分 + 簇内数据流 DSE + 架构原语出 RTL；decode 比 A100 吞吐 1.62×、能效 8.57×，比 Gemmini/LEGO 最高 11.33×"
tags:
- accelerator
- dataflow
- compiler
- spatial-execution
- design-space-exploration
- chip-design
- transformer
- llm
created: 2026-10-27
updated: 2026-10-27
timestamp: '2026-10-27T00:00:00Z'
paper_author: [Chi Zhang, Yi Sun, Weichuang Zhang, Quan Chen, Jieru Zhao]
year: 2026
venue: ASPLOS 2027
arxiv: '2610.32279'
sources:
  - raw/papers/TranSAGE_Spatial_Accelerator_Generation_ASPLOS2027.pdf
  - raw/papers/transage-spatial-accelerator-generation.md
---

# TranSAGE：面向大模型 Transformer 的空间加速器自动生成

## 一句话结论
现有加速器生成器（Gemmini、LEGO 等）按单个算子生成硬件，TranSAGE 把若干算子组成流水簇当作执行单元，联合搜索「怎么融合」和「每簇用什么数据流」，再自动吐出 RTL。收益主要来自把 LayerNorm/激活等辅助算子流水进矩阵乘，以及 decode 阶段融合减少访存。

## 动机
- 空间加速器片上带宽和能效占优，但为大模型手工设计代价高；单算子生成器做不了跨算子融合与流水，只能支持固定模式融合（如 GEMM+激活）。
- 融合粒度难选：融合不足浪费复用，融合过度会让 PE 分配不整除（64 PE 跑 FLOP 比 2:1 的两个算子无法全用满）、每算子 SRAM 变小、复用下降；最优融合随 prefill/decode 变化。
- 簇内数据流（分块、展开、循环序）与簇间生产-消费访问顺序耦合，设计空间爆炸。

## 方案
1. **前端**：PyTorch → Torch-MLIR → Linalg 规范化。
2. **DSE 引擎**：DP 图划分（以 EDP 为目标，cutIndex 回溯）决定算子簇；簇内分解为 L2 分块与 L1 展开/循环序两级搜索，用「维度关系网络」由输入推导输出分块，保证上下游访问顺序一致可直接流水。
3. **空间架构原语（SAP）**：算术、存储（DataNode/FIFO）、路由（Decompose/Compose/Mux/Demux）原语池；各簇共享同一套硬件资源，靠多路选择器运行时重配置，每簇编码成二进制存入 dispatch table。
4. **RTL 生成**：SAP 图中每个原语替换为 RTL 模板或硬件宏。

## 效果（论文数字）
评测模型 Llama3-8B（附录）、Qwen3-8B、Gemma-7B、Llama3-70B、Qwen3-235B-A22B；TranSAGE 按 1 GHz、45 nm 模型估算，能耗用 DeepScaleTool 缩放到 8/7 nm 再与实测设备比较。

| 对比 | prefill 平均吞吐 | decode 平均吞吐 | prefill 能效 | decode 能效 |
|---|---|---|---|---|
| vs Orin NX | 2.05× | **2.41×** | 1.78× | 3.65× |
| vs A100 | 1.65× | 1.62× | 3.46× | 8.57× |
| vs Ascend 910B3 | 1.42× | 2.12× | 3.69× | **13.04×** |

- vs 生成器（Gemmini-OS / Gemmini-WS / LEGO，Timeloop+Accelergy 建模）：prefill edge 1.58× / 2.22× / 1.82×，server 4.14× / 3.28× / 5.50×；decode edge 3.13× / 1.46× / 1.46×，server **11.33×** / 3.37× / 3.37×；decode 能效最高 1.73×（edge）/ **6.07×**（server）。
- BF16 利用率：prefill 最高 96.15%（edge）/ 90.20%（server）；decode 只有 3.16% / 3.05%，受内存带宽所限。
- 重配置面积开销最高 0.11%；最大簇规模 6 时 DSE 在数十分钟内完成，搜索时间近线性增长。

## 与 wiki 的关系
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — WS/OS 等单算子数据流的上一层：跨算子流水簇 + 自适应数据流
- [Plasticine](/concepts/plasticine-accelerator.md) — 同属空间/可重构数据流路线；TranSAGE 走「每模型生成专用硬件」
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 最优融合随阶段变化；decode 利用率 ~3% 再次印证带宽墙
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — decode 的 GEMV 化解释了为何融合对能效贡献远大于对吞吐

## 开放问题
- 对比口径混合：设备基线是实测（PyTorch 原生 kernel，未用 vLLM/TensorRT-LLM 等优化栈），TranSAGE 是 45 nm 模型缩放估算，生成器基线是 Timeloop 建模；绝对倍数需打折看待。
- 摘要写 decode 吞吐「up to 2.41×」，贡献列表一处写 2.42×，以正文表述为准。
- 生成后物理资源固定，模型结构演进需重生成；只做单芯片，多芯片通信感知 DSE 列为未来工作。
- decode 利用率 3% 说明真正瓶颈在 HBM/片外带宽，与近存/3D DRAM 路线结合的空间还未讨论。

# Citations
- [arXiv:2610.32279](https://arxiv.org/abs/2610.32279) — Zhang et al., ASPLOS 2027
- [raw stub](/raw/papers/transage-spatial-accelerator-generation.md)
