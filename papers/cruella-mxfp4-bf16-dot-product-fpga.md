---
type: Paper
title: "Cruella: FPGA 上统一的 MXFP4 / BF16 点积单元"
description: "HyperAccel / KAIST / NTU / Yonsei — Alveo U55C 板测；相对同板 BF16 权重，decode 1.15×–1.87×；相对等吞吐分离单元少 23% DSP、36% LUT；A40 更快，每 token 能量为板卡的 0.92×–2.01×"
tags:
- fpga
- accelerator
- quantization
- numeric-format
- mixed-precision
- llm
- inference
- energy
- hbm
created: 2026-11-25
updated: 2026-11-27
timestamp: '2026-11-27T00:00:00Z'
paper_author: [Jinho Yang, Taehyeong Kim, Mincheol Cha, Hyeoncheol Kim, Donggeun Kim, Nahye Kim, Yujin Lee, Ryeowook Ko, Woong Gyu Park, Jiwoong Park, Junsoo Kim, Tae-Hyoung Kim, Yongjun Park, Seongmin Hong, Joo-Young Kim]
year: 2026
venue: preprint
arxiv: '2611.27323'
sources:
  - raw/papers/Cruella_MXFP4_BF16_Dot_Product_FPGA_2026.pdf
  - raw/papers/cruella-mxfp4-bf16-dot-product-fpga.md
---

# Cruella：在同一套 DSP 阵列上跑 MXFP4×BF16 与 BF16×BF16

## 一句话结论
HyperAccel 与合作者在 Alveo U55C 上实现统一点积单元 UDPU，用一组 DSP 阵列和一条归约流水线同时执行 MXFP4×BF16 与 BF16×BF16。相对等吞吐的分离单元，UDPU 少 **23%** DSP、少 **36%** LUT。板上相对同比特流的 BF16 权重，decode TPOT 为 **1.15×–1.87×**；上下文 512 时平均 **1.54×**，Llama-3.1-8B 最高 **1.87×**。同机上的 A40（vLLM + 扩展 Marlin，读相同 MXFP4 字节）decode 更快，每 token 能量为板卡的 **0.92×–2.01×**。预对齐使 PPL 变化至多 **0.7%**。

## 动机
MXFP4 检查点的层在 MXFP4×BF16（MLP / 专家）与 BF16×BF16（注意力、BF16 层、BF16 KV）之间切换。作者刻画：在 BF16 KV 下，BF16×BF16 占用数据通路时间的 **56%–77%**，此时单独的 MXFP4 单元会闲置。FPGA 可以用比特流接纳新格式，已部署的 FPGA LLM 加速器还缺少把两种乘积放在同一单元里的实现。

## 方案
UDPU 的原则是让两种模式共用从 DSP 乘法到累加的每一级。MX-FP 模式先把每组 4 个 BF16 激活按最大指数预对齐，组内只带一个指数；MXFP4 权重解码成 5-bit 有符号定点，与激活相乘不必等待共享 scale。预加法器打包把两个有符号 MXFP4×BF16 乘积放进同一颗 DSP48E2，并做精确校正。乘积级按组求和并把共享 scale 加到组指数上，随后归约流水线按这些指数对齐累加。FP-FP 模式绕过预对齐，把 BF16 尾数切到同一 DSP 阵列。板上操作数收集器把预对齐放在 UDPU 行之外。单元对照用同吞吐的带宽匹配分离设计，以及 FIGNA / FIGLUT 风格的 FPGA 重实现。

## 量化结果
板测在单块 U55C（16 nm，16 GB HBM2 **460 GB/s**，功率上限 150 W，内核 **185.4 MHz**）上进行，主机为 2× Xeon Silver 4310、256 GB DDR4，软件 XRT 2.15 与自研编译器。单请求、prompt 按 token 预填充、解码 **D=256**，上下文从 512 到 16K。TTFT / TPOT 来自主机时间戳，包含主机运行时；功率为 xbutil 在 decode 窗的板卡均值。每配置 1 次热身 + 5 次测量，TPOT / TTFT 的 95% CI 在 **0.4%** 以内。六个模型：Llama-3.2-1B / 3.2-3B / 3.1-8B，Qwen3-1.7B / 8B，以及专家以 MXFP4 发布的 GPT-OSS-20B（只测 MXFP4）。三个 BF16 配置在 16 GB HBM 上 OOM。

- 上下文 512：MXFP4 相对同板 BF16 权重，TPOT 平均 **1.54×**，最高 **1.87×**（Llama-3.1-8B）；Llama-3.2-1B 为 **1.38×**，Qwen3-1.7B / 8B 为 **1.26× / 1.64×**。TTFT 平均 **1.94×**、最高 **2.19×**。摘要给出的全区间是 **1.15×–1.87×**。
- 16K 上三种双格式模型的平均加速从 512 的 **1.40×** 降到 **1.19×**；FP-FP 字节占比从 512 时至多 72% 升到 16K 时至少 80%。从 512 到 16K，MXFP4 TPOT 在 Qwen3-1.7B 上变长 **1.7×**，在 Llama-3.2-1B 上最高 **2.5×**。
- 权重流速率在每对格式上为 **349–358 GB/s**，约为 32 个 HBM 端口 **380 GB/s** 的 **93%**。512 时固定时间（采样、逐元素 VPU 等）从 Llama-3.2-1B 的 **5.0 ms** 到 Qwen3-8B 的 **14.8 ms**，占 MXFP4 TPOT 的 **27%–67%**。相对 BF16-only 构建，MX 构建在 512 上仍快 **1.23×–1.85×**；Llama-3.2-1B@16K 慢 **9%**。
- 相对等吞吐分离单元：少 **23%** DSP、少 **36%** LUT（Table 5：每车道 17,979 LUT / 136 DSP，对照 27,946 / 176）。单元 P&R 在约 **200 MHz** 收敛。预对齐使 PPL 变化至多 **0.7%**，任务准确率至多 **0.6** 个百分点。
- A40（48 GB GDDR6 **696 GB/s**，300 W，vLLM 0.31.0 + 扩展 Marlin，权重同样按 4.25 bit 打包）：512 时平均快 **2.7×**（最高 **3.6×**），板卡功率平均为 U55C 的 **4.7×**，每 token 能量平均为板卡的 **1.75×**；16K 速度差距平均 **4.2×**，能量比平均 **1.18×**。Llama-3.2-1B@16K 是 A40 能量更低的一例，与摘要区间 **0.92×–2.01×** 一致。
- Table 7：Llama-3.1-8B 在 U55C 上 **36.8 tok/s**、带宽利用率 **54%**、**67.4 W**、**0.55 tok/J**，LUT / DSP 占用 **33% / 26%**。FlightLLM 与 EdgeLLM 在各自板卡与格式上快 **1.4×–1.5×**，按「每 token 字节 × 吞吐」口径利用率至多 **35%**。作者把这张表定位为位置参照，模型与格式并不对齐。

## 局限与解读
- 全部端到端数字是单请求 decode；A40 对照也只比 decode，因为只有这一阶段两边读相同的每 token 字节。
- TTFT / TPOT 含主机运行时；相同时延比例来自 RTL 周期，与板卡墙钟分开书写。
- MX 构建的 VPU 宽度是 BF16-only 构建的一半，固定时间里有一部分来自这条变窄的 VPU。
- 与 FlightLLM / EdgeLLM 的 tok/s 对照跨越不同模型、板卡与格式。

## 与 wiki 的关系
- [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md) — 把已部署 FPGA 上的 MXFP4×BF16 / BF16×BF16 共用单元补进格式账
- [Chimera](/papers/chimera-fpga-llm-decode.md) — 同属 HBM FPGA 上的 decode 加速器，Chimera 在 U280 上走 W4 与多级专家存储
- [Kameleo](/papers/kameleo-bit-serial-activation-precision.md) — 运行时选择激活尾数；Cruella 在板上同时执行两种已发布格式
- [HETEROVLM](/papers/heterovlm-versal-aie-vlm-serving.md) — Versal AIE 上的 VLM 服务，与 U55C 点积单元对照


2026-11-27：[EdgeALM](/papers/edgealm-fpga-audio-language-model.md) 是另一块 HBM FPGA 上的生成加速（U50、音频语言模型）；[ISTS](/papers/ists-bit-slice-steiner-llm-accelerator.md) 则走 ASIC 风格的比特切片数据通路，用 Steiner 点复用部分和。

# Citations
- [arXiv:2611.27323](https://arxiv.org/abs/2611.27323) — Yang et al.（HyperAccel / KAIST / NTU / Yonsei）
- [raw stub](/raw/papers/cruella-mxfp4-bf16-dot-product-fpga.md)
- [PDF](/raw/papers/Cruella_MXFP4_BF16_Dot_Product_FPGA_2026.pdf)
