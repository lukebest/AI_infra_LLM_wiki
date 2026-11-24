---
type: Paper
title: "FOREST: Coordinating Tree-based HBF, RRAM, and HBM for Efficient Speculative LLM Inference"
description: "紫光国芯 / 北京大学 — 架构模型（A800 投机轨迹 + 22 nm 综合 + 存储器模型）；相对 A800 GPU 投机解码，GLM-4.5-Air 在 4096 输出 token 时端到端 5.5×，decode 吞吐最高 11.46×、decode 能效最高 16.5×"
tags:
- hbf
- hbm
- 3d
- speculative-decoding
- inference
- decode
- kv-cache
- accelerator
- memory
- energy
- architecture
- llm
- design-space-exploration
created: 2026-11-24
updated: 2026-11-24
timestamp: '2026-11-24T00:00:00Z'
paper_author: [Hao Ding, Zheng Shi, Dongxue Zhao, Huiying Bian, Meng Li, Xu Zheng, Kun Wang, Nanjian Wu, Jie Chen, Yimao Cai]
year: 2026
venue: preprint
arxiv: '2611.27701'
sources:
  - raw/papers/FOREST_HBF_RRAM_HBM_Speculative_2026.pdf
  - raw/papers/forest-hbf-rram-hbm-speculative.md
---

# FOREST：用 HBF、RRAM 与 HBM 三棵树分担投机解码

## 一句话结论
紫光国芯微电子与北京大学等单位的 FOREST，按投机解码的三个阶段把存储–计算树分开：HBF 树做目标模型并行校验，3D 堆叠 RRAM 树做草稿模型的低时延自回归起草，HBM 树做两侧的 KV 注意力。评测是把在 NVIDIA A800 上测得的投机轨迹回放到架构模型里，再叠 22 nm 综合与存储器模型。相对 A800 GPU 投机解码，GLM-4.5-Air 在约 8K 输入、4096 输出 token 时端到端 5.5×；各配置 decode 吞吐最高 11.46×、decode 能效最高 16.5×。Llama 3.1-405B 的端到端仍由四卡 A800 的投机解码快 1.32×，作者归到计算密集的 prefill。

## 动机
投机解码把轻量起草、目标模型并行校验和随上下文增长的注意力放在同一次推理里。这三件事对容量、带宽和时延的需求不同。GPU 上它们共用以 HBM 为中心的层次和通用算力，起草阶段容易吃不饱计算，校验和长上下文注意力又会把容量与带宽顶满。

## 方案
三棵存储–计算树协同，权重为 W4A8 DCIM，注意力在 HBM 树上用 16 维块浮点：

- **HBF T 树**：目标模型校验。单栈 512 GB、1.6 TB/s，640 个 W4A8 DCIM PE，峰值 64 TOPS。
- **两棵 RRAM D 树**：草稿模型起草。合计 1 GiB（2 栈 × 8 裸片 × 64 MiB），每树 819.2 GB/s、两树共 1.64 TB/s；根上 2×128 个 SRAM-DCIM PE，峰值 6.55 TOPS。宽而低频的读出，配合时钟解耦接口和与 SRAM-DCIM 重叠的权重回填。
- **HBM KV 树**：两侧注意力。36 GB/栈、2.8 TB/s，512 个 APU，根上 K/V 存储合计 4.25 MiB，等效 192 TFLOPS（K 与 V 各 96）。块缩放的 Q/K/V 预处理放在 HBF 与 RRAM 的根板，注意力在 HBM 树上做流水 softmax 规约。

执行按阶段在共享的 HBM 注意力根上切换草稿 / 目标所有权，并在阶段边界把 KV 工作集回填与独立工作重叠。面积与功率来自 22 nm IX22ULL 标准单元综合、CACTI SRAM 以及 HBF/RRAM/HBM 的带宽–时延–容量–访问能量模型：计算根合计 175.403 mm² / 23.236 W，存储栈 78.117 W，系统估计功率 101.35 W，三树封装投影约 424.92 mm²（Table 3）。

对照是 A800 80 GB：Qwen 用 1 卡，GLM-4.5-Air 用 2 卡 TP+EP，Llama 3.1-405B 用 4 卡 TP。六组目标–草稿配置，batch 1、贪心解码，约 8K 输入，输出长度 128–4096，γ 在 {2,3,4,5,6,8,12,16} 中各自选优，并另报固定 γ=8。GPU 能量用 NVML，跨多卡累加。FOREST 一侧把这些轨迹回放到架构模型。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 端到端加速（约 8K 输入、4096 输出） | GLM-4.5-Air 相对 GPU 投机解码 **5.5×**；Llama 3.1-405B 上四卡 A800 投机解码仍快 **1.32×**（prefill 计算密集） | Fig. 11 / §7.3 |
| decode 吞吐 / decode 能效 | 相对 GPU 投机解码，最高 **11.46×** / **16.5×** | Fig. 11 / §7.3 |
| 端到端能效（γ=8，相对 GPU 投机解码） | Qwen2.5-32B / 72B / GLM-4.5-Air / Llama 3.1-405B 为 **19.19× / 16.46× / 10.51× / 9.14×** | Fig. 12 / §7.3 |
| 接受率（γ=8，4096 输出） | Qwen2.5-32B 上草稿从 0.5B 升到 3B，接受率 38.49%→53.82% | Table 4 / §7.2 |
| 注意力精度敏感性 | 16 维 BFP 代理相对 GPU BF16 注意力，平均接受率最多差 **2.13** 个百分点 | Table 5 / §7.2 |
| 草稿权重放到 RRAM | 相对放到 HBF，0.5B / 1.5B / 3B 草稿的权重访问能量分别降 **97.62% / 92.56% / 85.12%**；系统 decode 能效高 **7.16% / 18.21% / 29.88%** | Fig. 14 / §7.4 |
| 成本效率（tokens/$，文中 TCO 假设） | 相对 GPU 投机解码，四模型为 **6.73× / 3.15× / 6.27× / 2.87×**。假设四年寿命、PUE 1.3、电价 $0.12/kWh、A800 $20,000、FOREST $22,000 | Fig. 15 / §7.5 / §6.2 |

405B 上要越过四卡 A800 的端到端线，T 根算力在 4096 输出时大约需要 128 TOPS，在 1024 输出时大约需要 192 TOPS（Fig. 13）。

## 与已有页的增量
[FLINT](/papers/flint-hbf-llm-inference.md)、[SlipStream](/papers/slipstream-hbf-gpu-prefetch.md) 和 [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md) 讨论 HBF 在 LLM 推理里的放置、预取与是否划算。FOREST 把 HBF 专门交给目标模型校验，并配上 RRAM 起草树和 HBM 注意力树，数字来自 A800 轨迹加 22 nm 投影，需要把「架构模型」和硅测分开读。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBF / RRAM / HBM 分工
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 三树封装与 3D 堆叠存储器
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 405B 上 prefill 仍限制端到端
- [FLINT](/papers/flint-hbf-llm-inference.md) — HBF 推理数据通路
- [SlipStream](/papers/slipstream-hbf-gpu-prefetch.md) — HBF 预取

## 开放问题
- 性能与能量是轨迹回放 + RTL/综合 + 存储器模型，不是流片或板测。
- tokens/$ 依赖文中的购置价与电价假设，Fig. 16 也表明 72B 与 405B 对硬件价格更敏感。
- 全部实验是 batch 1、贪心解码；并发服务下的排队与 KV 容量要另算。
- 3B 草稿需要把 RRAM 容量扩到名义 1 GiB 之外；405B 的端到端仍受 T 根算力与 prefill 限制。

# Citations
- [arXiv:2611.27701](https://arxiv.org/abs/2611.27701) — Ding, Shi, Zhao, Bian, Li, Zheng, Wang, Wu, Chen, Cai（紫光国芯 / 北京大学 / 中科院国家空间科学中心 / 中科院微电子所）
- [raw stub](/raw/papers/forest-hbf-rram-hbm-speculative.md)
- [PDF](/raw/papers/FOREST_HBF_RRAM_HBM_Speculative_2026.pdf)
