---
type: Paper
title: "HETEROVLM: Edge Multi-Request VLM Serving on a Heterogeneous Versal SoC"
description: "UC Irvine — Versal VC1902 实测；LFM2.5-VL-3B 单请求 decode 相对 T4 / Orin Nano 为 1.3× / 4.0×，每 token 能量为二者的 61% / 73%、为 3090 Ti 的 51%"
tags:
- soc
- fpga
- edge
- inference
- prefill
- decode
- serving
- energy
- accelerator
- amd
- quantization
- latency
- throughput
- scheduling
created: 2026-11-20
updated: 2026-11-20
timestamp: '2026-11-20T00:00:00Z'
paper_author: [Zhiheng Chen, Yu-An Chou, Yifan Zhang, Ye Qiao, Saptarshi Mitra, Sitao Huang]
year: 2026
venue: preprint
arxiv: '2611.23878'
sources:
  - raw/papers/HETEROVLM_Versal_AIE_VLM_Serving_2026.pdf
  - raw/papers/heterovlm-versal-aie-vlm-serving.md
---

# HETEROVLM：在 Versal AIE + 可编程逻辑上调度多请求 VLM

## 一句话结论
加州大学欧文分校在 AMD Versal VC1902 上实现 HETEROVLM：AIE 阵列跑编码器、prefill 与 attention，可编程逻辑（PL）放小步 decode 的 GEMV 引擎和按类别 / 截止期排序的调度器。并发请求共享一次读权重的 decode 步；紧急请求在工作单元边界抢占，暂停请求从 DDR 中的结果恢复。服务 LFM2.5-VL-3B 时，空闲下 60-token 文本与带一张 512×288 图的 177-token 镜头问题，首 token 分别为 **140 ms** 与 **303 ms**。单请求 decode 相对 Tesla T4 与 Jetson Orin Nano 为 **1.3×** 与 **4.0×**，每 token 能量为二者的 **61%** 与 **73%**，为 RTX 3090 Ti 的 **51%**。

## 动机
车载或机器人边缘节点会同时跑多种视觉–语言问题，安全问题有截止期，聊天可以等待；每个请求又混合计算密集的编码 / prefill 与访存密集的 decode。数据中心 GPU 服务按迭代在主机侧调度，紧急请求要等当前迭代结束，小 batch decode 的每 token 能量也高。先前 Versal AIE 加速器把一个模型映成编译期固定的数据流图、服务单路输入，既没有 autoregressive decode，也没有按截止期的请求调度。

## 方案
HETEROVLM 保持 AIE 图静态，把可调度性放到 PL。阶段按权重字节的复用决定落点：跨许多 token 复用同一字节的阶段占满 AIE；只有少量请求的 decode 步复用不足，放到紧挨 DDR 口的 PL GEMV。调度器把请求切成短工作单元（抢占最多等一个不超过 2 ms 的单元，外加已发出的最多两次 attention），按类别、截止期、到达顺序排列。首 token 之前，decode 步都走 PL，把 GEMM 组留给 prefill；之后，少于主机设定阈值 bthr 的步走 PL，更大的步走 AIE 组，并与 PL 重叠。同一 bitstream 通过加载各自的指令程序与权重，服务同一形状类的其他 VLM。

评测在 VC1902 上，Vitis 2022.1 + TAPA，PL **240 MHz**、AIE **1.25 GHz**。主模型 LFM2.5-VL-3B，用文中的整数运算。对照 GPU 为功耗相近的 Tesla T4、边缘 Jetson Orin Nano，以及高端桌面 RTX 3090 Ti，三者带宽分别为 320 / 102 / 1,008 GB/s，VC1902 的 DDR4 约为 **50 GB/s**；GPU 侧跑同一模型、同一提示与 int8 权重，使用 CUDA graphs 和 torch.compile 的 Triton 核。另有一套全部算子都放在 AIE、PL 只搬数据的对照构建。板级资源：LUT 61.2%、FF 36.9%、BRAM 89.0%、URAM 90.9%、DSP 71.4%；AIE 使用 400 个 tile 中的 272 个（两组 GEMM 160，attention 112）。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 空闲首 token（LFM2.5-VL-3B） | 文本 ➋ **140 ms**（其中 prefill 133 ms）；镜头 ➊ **303 ms**（encoder 130 ms，prefill 165 ms）；三图 ➌ **838 ms**。相对 Orin Nano，镜头 / 文本分别早 **1.7× / 2.0×** | §V-D |
| 单请求 decode（Table IV） | HETEROVLM：**66.5 ms/tok**、15.0 tok/s、**3.56 J/tok**、53.6 W；相对全 AIE 154.4 ms 为 **2.3×**，相对 T4 87.0 ms 为 **1.3×**，相对 Orin 268.2 ms 为 **4.0×**。权重读取 40.6 GB/s，约为 DDR 上限 50 GB/s 的 **81%** | Table IV / §V-G |
| 每 token 能量（单请求） | 为 T4 5.83 J 的 **61%**、Orin 4.91 J 的 **73%**、3090 Ti 6.96 J 的 **51%** | Table IV / §V-G |
| 共享 decode 步 | 两请求共享一次 67.2 ms 的 PL 步，吞吐翻到 **29.8 tok/s**。八请求共享步 **104.8 tok/s**，T4 为 92.3、Orin 为 29.3。每 token 能量在 4 / 8 请求时为 1.22 / 0.62 J，T4 为 1.42 / 0.72 J | §V-D / Fig. 7 |
| 八路 64 输出文本同时到达的完成时间 | 用文中拆分（首 token 前全走 PL，之后 bthr = 3）为 **6.25 s**；固定阈值 7 / 3 为 6.34 / 6.96 s；全 PL 12.44 s，全 AIE 12.85 s | §V-D |
| 抢占（Table V，相对各平台空闲首 token：303 / 156 / 518 / 41 ms） | 紧急镜头问题在前有请求时为 **1.00–1.04×** 空闲时间；插在 4k-token prefill 中途时只比空闲晚 **14 ms**。仅优先级 / 按到达顺序在 4k 前请求后达到 6.63× / 6.75× | Table V / §V-E |
| 负载（泊松 0.05–0.45 req/s，四分之一为 1 s 截止期的紧急镜头） | 0.3 req/s 时（410 紧急 + 1,292 普通）紧急无超时，p99 首 token **0.61 s**；按到达顺序超时 4.2%（1.34 s）。若每十个普通请求里有一个 4k 文本，0.2 req/s 时紧急 p99 为 **0.62 s**，仅优先级 / 按到达为 4.41 / 4.76 s | §V-E |
| 精度 | RealWorldQA 整数运算 69.67%，fp32 为 69.15%（成对 95% CI ±0.63 分）；4,096 上下文上 50 本 PG-19 有 **98.0%** 位置与 fp32 下一 token 相同 | Table II(b) / §V-B |
| 同 bitstream 的另外两个模型 | LFM2.5-VL-1.6B：文本 / 镜头首 token 63 / 209 ms，单请求 PL decode 29.5 ms，1 / 8 请求 33.9 / 215.3 tok/s；SmolVLM2-2.2B：106 / 269 ms，46.6 ms，21.4 / 101.1 tok/s。三模型常驻切换中位 **33 ms** | Table VII / §V-H |

## 与已有页的增量
同一组刚 ingest 的 [Chimera](/papers/chimera-fpga-llm-decode.md) 在 Alveo U280 上做 batch 1 的 LLM decode。本篇换到 Versal AIE + PL 异构 SoC，对象是带截止期的多请求 VLM，并给出抢占与共享权重读的板上数字。两端的能量对照都要连同平台带宽一起读：VC1902 的 DDR4 约 50 GB/s，T4 / Orin / 3090 Ti 为 320 / 102 / 1,008 GB/s；3090 Ti 的单请求 decode 仍明显更快（18.4 vs 66.5 ms/tok）。

## 与 wiki 的关系
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) — 用权重复用决定 AIE 与 PL 的分工，小步 decode 靠近 DDR
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 共享 decode 步一次读权重，暂停请求的状态落在 DDR
- [Chimera](/papers/chimera-fpga-llm-decode.md) — 同一组在 U280 上的 FPGA decode；本篇补异构 SoC 与多请求调度
- [In-core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 归一化、量化、softmax 与 fp32 epilogue 放在 PL，并与 AIE 级联融合

## 开放问题
- 单 bitstream 服务一个形状类；类外模型需要按描述符再出一版 bitstream。
- 作者写明 decode 跟着 VC1902 的 DDR 带宽走，带 HBM 与 AIE-ML tile 的 Versal 型号会提高 decode 与 attention 吞吐，本评测未覆盖。
- GPU 对照是 int8 权重 + CUDA graphs / Triton，平台带宽与功耗档位跨度大，跨平台倍数宜与 Table II(a)、Table IV 的绝对时间、能量一起读。

# Citations
- [arXiv:2611.23878](https://arxiv.org/abs/2611.23878) — Chen, Chou（共同一作）；Zhang, Qiao, Mitra, Huang（University of California, Irvine）
- [raw stub](/raw/papers/heterovlm-versal-aie-vlm-serving.md)
- [PDF](/raw/papers/HETEROVLM_Versal_AIE_VLM_Serving_2026.pdf)
