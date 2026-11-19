---
type: Raw Source
title: "Chimera: A Configurable LLM Decode Accelerator Architecture with Compute-Memory-Floorplan Co-Design for HBM-Equipped Multi-Die FPGAs"
source_url: https://arxiv.org/abs/2611.21677
pdf: Chimera_FPGA_LLM_Decode_2026.pdf
retrieved: 2026-11-19
ingested: 2026-11-19
org: University of California, Irvine
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.21677)

GPUs are widely used for LLM inference, but single-request decoding is memory-bound, leaving their compute underutilized while they draw substantial power. HBM-equipped FPGAs are well suited to LLM decoding: their customizable datapaths use memory bandwidth more energy-efficiently than GPUs. However, high memory bandwidth alone does not ensure high decode performance: exploiting it requires parallel compute and memory interfaces, whose resource costs and placement on the chip can limit the throughput. We present Chimera, a configurable LLM decode accelerator architecture that co-designs compute, memory access, and floorplan. Specifically, HBM Proxy Ports extend HBM access to compute lanes on every super logic region (SLR) die, and tiered expert storage holds mixture-of-experts weights beyond the HBM capacity. In addition, a unified configuration analysis estimates per-token latency and per-SLR resource use and guides the design of each configuration within resource budgets. On an AMD Alveo U280, we build ten designs for eight dense, mixture-of-experts, hybrid linear/standard-attention, and ternary LLMs, up to an 80B-parameter mixture-of-experts LLM on four memory tiers. Chimera's designs achieve a geometric mean of 1.6× the token throughput of prior state-of-the-art FPGA implementations and 3.0× and 1.5× the energy efficiency of the RTX 3090 and A100 GPUs, setting a new benchmark for LLM decoding on HBM-equipped FPGAs.

# Excerpts / key facts

- Authors: Zhiheng Chen, Yifan Zhang, Yu-An Chou, Ye Qiao, Sitao Huang（University of California, Irvine）。arXiv:2611.21677，cs.AR，2026-11-18 公告（提交标注 14 Nov 2026）。预印本。Demo：https://anonymous.4open.science/r/chimera_fpga_llm_demo-0658/ （正文链接）。
- 平台：AMD Alveo U280，工具链 TAPA + Vitis/Vivado 2023.1。十个设计、八个模型：稠密 Llama-3.2-1B / Llama-3.1-8B；MoE Qwen1.5-MoE-A2.7B / Qwen3-Coder-30B-A3B；混合 Granite-4.0-H-1B 与混合 MoE Qwen3-Next-80B-A3B；三元 BitNet b1.58-2B 与 Ternary-Bonsai-27B。全部 A8 激活，KV 与循环状态放在 HBM；上下文最长 4K。吞吐是 WikiText-2 上墙钟 decode token 速率，三次中位数，U280 上三次相差不到 1%。板卡功率是 U280 供电轨在另一次 decode 上的平均；GPU 基线是 vLLM、batch 1、CUDA graphs，权重位宽与板上一致，功率来自 NVML。
- 同板同模型对照：Llama-3.2-1B W4，Chimera **301.1 tok/s**，FlexLLM 为 **144.7**，**2.08×**（在 FlexLLM 的全部 8 个上下文/decode 长度上为 2.04–2.09×）。内核 200 MHz，FlexLLM 为 292 MHz，HBM 带宽相同。
- 与先前 FPGA 发表数字的几何均值（作者口径，四项）：相对 FlexLLM、FlightLLM（U280、LLaMA2-7B W3.5A8 sparse，55 tok/s）、EdgeLLM（VCU128、ChatGLM2-6B W4A16KV16，51.4 tok/s）、LUT-LLM（V80、Qwen3-1.7B W2A3，约 196 tok/s，且为单 decoder block 无 LM head 的 RTL 共仿真）为 **1.6×**。另：U280 上 4-bit Llama-3.1-8B 相对 FlightLLM / EdgeLLM 发表速率为 **1.36× / 1.45×**；BitNet-2B 为 **249.4 tok/s**，相对 PENSA 在 U50 上的 58.1 约为 **4.3×**。这五篇先前设计都没有跑 MoE 或混合模型。
- Table III(a)，上下文 512、decode 256 token 的部分数字（U280 tok/s / W / tok/J；括号内为 3090、A100 的 tok/s 与 tok/J）：Llama-3.2-1B W4 301.1 / 61.5 / 4.90（492.8 / 1.55，575.4 / 3.05）；Llama-3.1-8B W4 74.7 / 76.3 / 0.98（150.1 / 0.44，197.2 / 0.70）；Qwen3-Coder-30B-A3B FP8 26.8 / 58.0 / 0.46（24.8 / 0.12，158.4 / 0.87）；Qwen3-Next-80B-A3B W4 29.3 / 65.2 / 0.45（39.4 / 0.17，49.0 / 0.36）；同模型 FP8 24.5 / 64.3 / 0.38（16.0 / 0.11，22.0 / 0.19）。U280 板卡 58–76 W，两块 GPU 117–348 W。
- 几何均值：能量效率（tok/J）相对 RTX 3090 **3.0×**、相对 A100 **1.5×**。U280 带宽约为 3090 的 49%、A100 的 30%（Table I），吞吐几何均值分别为这两块 GPU 的 **70%** 与 **52%**。八个上下文/decode 长度上，各设计最低吞吐为其最高值的 **71–95%**。
- 分层专家存储：Qwen3-Coder 在 U280 / 3090 上专家超出 HBM/显存，U280 从板上 DDR4 与主机内存读，decode 快于 3090（3090 经 PCIe 从主机 DRAM 读）。FP8 Qwen3-Next 的专家存储延伸到 NVMe，U280 经 PCIe 做 bus master 读主机内存，decode 快于两块 GPU。专家未命中等待占 Qwen3-Coder 时间的 32%、FP8 Qwen3-Next 的 27%、4-bit Qwen3-Next 的 13%。较早的 Qwen3-Coder 设计提前拷贝下一层专家，使驻留 HBM 的已选专家从 81% 升到 92%，上下文 ≤512 时吞吐 +19.9%。
- 协同设计消融（Llama-3.1-8B W4）：早期 HLS lane 原型 22 道，完整协同设计 30 道跑通并达到 **74.7 tok/s**，比上一档高 11.6%（估计增益 12.0%），为 HLS 原型的 **1.7×**。去掉 Proxy Ports 时 HBM2 从 450 降到 342 MHz，30 道从 74.2 降到 65.7 tok/s；15 个伪通道共享时 42.3 tok/s。
- 配置分析：用测得的存储路径速率时，八个上下文/decode 长度平均误差 6.4%；改用标称峰值则平均误差 14.0%，专家在 HBM 之外的三个设计为 23–35%。
- 量化质量（Table IV）：与所实现的量化 Hugging Face 模型相比，WikiText-2 PPL 平均差 0.17%，MMLU 平均差 0.3 分。
