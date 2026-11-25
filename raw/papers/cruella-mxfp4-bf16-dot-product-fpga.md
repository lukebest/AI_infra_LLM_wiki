---
type: Raw Source
title: "Cruella: A Unified Microscaling and Floating-Point Dot-Product Unit for LLM Inference on FPGAs"
source_url: https://arxiv.org/abs/2611.27323
pdf: Cruella_MXFP4_BF16_Dot_Product_FPGA_2026.pdf
retrieved: 2026-11-25
ingested: 2026-11-25
org: HyperAccel; KAIST; Nanyang Technological University; Yonsei University
venue: preprint (TRETS CCS listed on arXiv page)
---

# Abstract (verbatim gist, arXiv:2611.27323)

The number formats that accelerators execute natively are fixed at fabrication, yet large language model (LLM) checkpoints are released with MXFP4 weights in the Microscaling (MX) formats standardized in 2023. FPGAs adopt new formats through bitstreams. However, to the best of our knowledge, no deployed FPGA LLM accelerator executes MXFP4 weights alongside BF16 products. We characterize the decoding of MXFP4 checkpoints, whose layers alternate between MXFP4×BF16 products and BF16×BF16 products of attention and BF16 layers. With a BF16 KV cache, BF16×BF16 products take 56%-77% of the datapath time, during which a separate MXFP4 unit idles. We present Cruella, whose unified dot-product unit (UDPU) executes both product types on one DSP array and reduction pipeline. First, per-group pre-alignment keeps this pipeline at the BF16 width and changes perplexity by at most 0.7%. Second, pre-adder packing places two signed MXFP4×BF16 products in one DSP48E2 multiplier with an exact correction. On an Alveo U55C, the UDPU needs 23% fewer DSP slices and 36% fewer LUTs than separate MXFP4 and BF16 units of equal throughput. On this board, MXFP4 weights speed up decoding by 1.15×-1.87× over BF16 weights, and an NVIDIA A40 GPU decodes faster but spends 0.92×-2.01× the board’s energy per token.

# Excerpts / key facts

- Authors: Jinho Yang, Taehyeong Kim, Mincheol Cha, Hyeoncheol Kim, Donggeun Kim, Ryeowook Ko, Woong Gyu Park, Jiwoong Park, Junsoo Kim, Seongmin Hong, Joo-Young Kim（通讯，HyperAccel）；Nahye Kim（KAIST）；Yujin Lee, Tae-Hyoung Kim（NTU）；Yongjun Park（Yonsei）。arXiv:2611.27323，cs.AR，Monday 23 November 2026 公告窗。
- 板测：单块 Alveo U55C（16 nm，16 GB HBM2，460 GB/s，150 W 限制，内核 185.4 MHz），XRT 2.15；单请求、prompt 按 token 预填充、D=256，上下文 C=P+D 从 512 到 16K。TTFT/TPOT 含主机运行时；功率为 xbutil 在 decode 窗的板卡均值。每配置 1 次热身 + 5 次测量，TPOT/TTFT 的 95% CI 在 0.4% 以内。
- 六模型：Llama-3.2-1B / 3.2-3B / 3.1-8B，Qwen3-1.7B / 8B，GPT-OSS-20B（仅 MXFP4，因专家以该格式发布）。KV 为 BF16。三个 BF16 配置在 16 GB HBM 上 OOM。
- 上下文 512：MXFP4 相对同板 BF16 权重，TPOT 平均 1.54×、最高 1.87×（Llama-3.1-8B）；Llama-3.2-1B 为 1.38×，Qwen3-1.7B / 8B 为 1.26× / 1.64×。TTFT 平均 1.94×、最高 2.19×。16K 上三种双格式模型平均加速从 512 的 1.40× 降到 1.19×。摘要给出的全区间为 1.15×–1.87×。
- 相对带宽匹配的分离 MXFP4+BF16 单元（同等吞吐）：UDPU 少 23% DSP、少 36% LUT。单元 P&R 在约 200 MHz 收敛。
- A40（vLLM 0.31.0 + 扩展 Marlin MXFP4，48 GB GDDR6 696 GB/s，300 W）：512 上下文平均快 2.7×（最高 3.6×），板卡功率平均为板卡的 4.7×，每 token 能量平均为板卡的 1.75×；16K 速度差距平均 4.2×，能量比平均 1.18×。Llama-3.2-1B@16K 是 A40 能量更低的一例。摘要区间 0.92×–2.01×。
- Table 7：Llama-3.1-8B 在 U55C 上 36.8 tok/s、带宽利用率 54%、67.4 W、0.55 tok/J、LUT/DSP 占用 33%/26%。FlightLLM / EdgeLLM 在各自板卡与格式上快 1.4×–1.5×，按同样字节×吞吐口径利用率至多 35%。
- 预对齐使 WikiText-2 PPL 变化至多 0.7%，任务准确率变化至多 0.6 个百分点（仿真器，与 RTL 点积对齐）。
