---
type: Paper
title: "OptiDecode: Free-Space Optical KV Regeneration for Decode Attention"
description: "NUS / Lumai — 架构流水线模型；相对等峰值 HBM 带宽的理想 GPU KV 读取基线，30B–175B 稠密 MHA 在 32K 上下文下 decode 注意力 1.92–1.99×"
tags:
- accelerator
- inference
- decode
- kv-cache
- attention
- photonic
- optical
- hbm
- memory-bandwidth
- llm
- transformer
- energy
- architecture
created: 2026-11-23
updated: 2026-11-23
timestamp: '2026-11-23T00:00:00Z'
paper_author: [Aritra Bagchi, Bin Gao, James Spall, Jakub Pietrak, Weng-Fai Wong, Tulika Mitra]
year: 2026
venue: preprint
arxiv: '2611.19279'
sources:
  - raw/papers/OptiDecode_FSO_KV_Regeneration_2026.pdf
  - raw/papers/optidecode-fso-kv-regeneration.md
---

# OptiDecode：用自由空间光学再生历史 KV，把 decode 注意力的流量减半

## 一句话结论
新加坡国立大学与 Lumai 的 OptiDecode 在 decode 阶段缓存层输入激活，并用自由空间光学（FSO）按 HBM 激活取回速率再生全部历史 KV，再在数字侧做注意力。相对等峰值 HBM 带宽、注意力计算全部被隐藏的理想 GPU KV 读取基线，评测中的 30B–175B 稠密 MHA 在 32K 上下文下达到 1.92–1.99×，逼近流量减半给出的 2× 上界。

## 动机
长上下文稠密 MHA 的 decode 注意力反复读取历史 KV，流量随上下文线性增长。若改为缓存激活（K = XW_K、V = XW_V），历史缓存的存储与读写可以减半，但必须把历史 KV 重新算出来。论文以单卡 Blackwell Ultra（5 PFLOPS 稠密 FP8、8 TB/s HBM）上的单历史 token 为例：读 KV 很快，在 GPU 上再生 KV 需要 121 ns，是激活取回间隔 1.54 ns 的 79×，于是带宽瓶颈转成计算瓶颈。FSO 矩阵–向量乘把投影权重常驻在光学 tile 上，跨历史 token 复用，用来补上这笔再生算力。

## 方案
异构光电解码注意力加速器，按 B200 的 8 TB/s HBM、≥30B 稠密 MHA 做配额（Table 1）：共享 8 TB/s HBM 与 128 token 的 chunk；6 个输入切片、12 个 head group 对应 6×12 的 2,048×2,048 光学 tile（8 GBaud、单波长可扩展）、读出裸片上 2.3 TOPS INT8 QK 与 2.3 TFLOP/s FP32 PV，片上 SRAM 合计 133.5 MiB。读出–规约用 UCIe（有效 76.8 GB/s），规约–softmax 用 PAM4 SerDes（有效 89.6 GB/s）。2,048 维 tile 是与光学技术专家讨论后的设计目标，文中写明它不是某一款商用 DMD 的规格。

三个系统技术让流水线跟上激活取回间隔 t_X：激活重放（一份激活、一套电光转换器按 head group 顺序复用，避免广播）；原位注意力（部分 KV 留在读出裸片，只交换部分分数、概率和部分输出）；chunk 流水线（重叠连续 chunk，用在线 softmax 合并）。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 主对照（理想 GPU KV 读取，等峰值带宽） | 30B 及以上模型在 32K token、A100（2.04 TB/s）–B200（8 TB/s）四档上为 **1.92–1.99×**；128K 时约 **1.98×** 或更高。流水线填充满后，每个 chunk 的完成间隔是 GPU 读该 chunk KV 时间的一半，剩余差距来自填充开销 | Fig. 11 / §6.2 |
| 小模型与短上下文 | 32K 时 LLaMA-7B / OPT-13B 在 A100–H200 为 **1.84–1.97×**，在 B200 为 **1.10× / 1.38×**。OPT-175B 在 B200、1K token 时 batch 1 为 **1.07×**，batch 8 为 **1.80×** | Fig. 11 / §6.2 |
| 整层延迟（OPT-175B，32K，batch 1） | 相对实测 SGLang FlashInfer 路径，注意力为 **1.99–3.30×**；计入权重加载、FFN 取 GPU roofline 时，整层相对 roofline 为 **1.18×** | Fig. 13 / §6.2 |
| 消融（32K，8 TB/s） | 激活重放把 OPT-175B 的电光转换器从 72 降到 6，性能变化不到 1%；原位注意力相对仅重放再提升 **12–14×**；chunk 流水线再提升 **8–12×**，到达 **1.92–1.95×** | Fig. 16 / §6.4 |
| 能量（一阶模型，OPT-175B，32K，batch 1） | 8 / 4.8 / 2.04 TB/s 下为 **3.31 / 3.37 / 3.66 µJ** per historical token per layer，相对 TDP 基线分别低 **23% / 6% / 24%**；相对 A100 PCIe / H200 SXM / B200 SXM 的 NVML 实测再低 **37–43%**。8 TB/s 时 ADC/DAC/TIA 占 67% | §6.6 / Fig. 17 |

速度数字来自按 Table 1 配额建立的架构流水线模型。GPU 侧用 SGLang FlashInfer（FP8 KV、INT8 权重）在 A100/H100/H200/B200 上测每层延迟（CUDA event，100 次中位数）和板级能量（NVML，至少 3 s）。默认一次 decode、一条 query、batch 1；上下文从 1K 扫到 1M。

## 与已有页的增量
[Optical Broadcast Memory](/papers/optical-broadcast-memory-obm.md) 用集成硅光广播把权重送进脉动阵列，评测是大规模系统建模，工作区在训练/推送流。[TPU v4 光可重构](/papers/tpu-v4-optically-reconfigurable.md) 讨论的是机柜级光路交换。本篇把自由空间光学放在 decode 注意力的 KV 再生上，对照是等带宽的理想 GPU KV 读取。三篇的互连层次与对照设定都不同，倍数不宜直接横比。

## 与 wiki 的关系
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 注意力的带宽墙，以及用激活缓存换再生计算
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 历史 KV 与激活两条缓存路径的流量
- [Optical Broadcast Memory](/papers/optical-broadcast-memory-obm.md) — 同属光学进入计算数据通路，机制与评测设定不同
- [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md) — 光学投影与数字注意力的异构数据通路

## 开放问题
- 主速度数字来自架构流水线模型；能量是参数化一阶模型。GPU 对照里的「理想 KV 读取」把注意力计算全部隐藏，实测整层数字需要单独看 Fig. 13。
- 硬件按 ≥30B、8 TB/s 配额，小模型在 B200 上会撞上数字引擎下限。
- 设计保留独立 KV 头与全历史稠密 MHA。作者指出 GQA 会缩小激活缓存的收益，稀疏注意力与潜在向量缓存是后续方向。
- 光学 tile 规格来自设计讨论，文中未对应到某一款已交付的 DMD 产品。

# Citations
- [arXiv:2611.19279](https://arxiv.org/abs/2611.19279) — Bagchi, Gao, Spall, Pietrak, Wong, Mitra（NUS / Lumai Ltd.）
- [raw stub](/raw/papers/optidecode-fso-kv-regeneration.md)
- [PDF](/raw/papers/OptiDecode_FSO_KV_Regeneration_2026.pdf)
