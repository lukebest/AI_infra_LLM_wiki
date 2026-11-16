---
type: Paper
title: "SlipStream: Enabling HBF for GPU Systems by Mitigating the Latency and SRAM Overheads"
description: "Georgia Tech / NVIDIA / Stanford，HPCA’27 — 按需求节奏给 HBF 做页级预取；40 MB 缓冲达到理想 HBF 的 92.4%，H3 即使用 320 MB 也只有 43.1%；16 MB 相对 40 MB 只差 4%"
tags:
- hbf
- flash
- hbm
- prefetch
- gpu
- sram
- memory
- inference
- serving
- moe
- nvidia
- dram
- llm
created: 2026-11-16
updated: 2026-11-16
timestamp: '2026-11-16T00:00:00Z'
paper_author: [Anish Saxena, Hritvik Taneja, Christos Kozyrakis, Aamer Jaleel]
year: 2026
venue: HPCA 2027
arxiv: '2611.14776'
sources:
  - raw/papers/SlipStream_HBF_GPU_Prefetch_HPCA2027.pdf
  - raw/papers/slipstream-hbf-gpu-prefetch.md
---

# SlipStream：按需求节奏给 GPU 上的 HBF 做页级预取

## 一句话结论
Georgia Tech、NVIDIA Research 与 Stanford 在 HPCA 2027 提出 SlipStream：把 HBF 预取做成由需求定速的生产者–消费者流水。软件先给数据无关的 LLM kernel 记下一份可重复的权重页需求顺序，再插入 staging warp，用非阻塞 STAGE 指令按这个顺序预取；硬件上，STAGE 表项要等到需求第一次碰到该页才退役，缓冲槽也等到页从 HBF 返回才分配。七个 16–800 GB 的稠密模型上，**40 MB** 暂存缓冲达到「延迟像 HBM 的理想 HBF」性能的 **92.4%**；先前的张量流式设计 H3 即使用 **320 MB** 也只有 **43.1%**。把缓冲缩到 **16 MB**（H3 的 1/20）后，相对 40 MB 只再丢 **4%**。两个 MoE（Qwen3-30B / 235B）在 40 MB 上达到理想性能的 **91.2%**。

## 动机
HBF 用 NAND 替换 HBM 的 DRAM 层，容量大约可到 16 倍，读带宽可与 HBM 相当，但读延迟接近 **20 µs**，大约是 HBM 的 20 倍。按需访问会把推理拖慢到最高 **12.8×**。按缓存行跟踪的预取器要把在途状态扩大约 20 倍才能盖住这段延迟。按虚地址顺序流式送数的 H3，跟 kernel 真正的需求顺序不一致，往往需要几百 MB 的缓冲。

## 方案
软件–硬件协同：

1. **Stream Profiler** 在模型与 kernel 库首次托管时，记录数据无关 kernel 里各 CTA 可重复的 4 KB 权重页需求顺序。
2. 运行时插入 **staging warp**，用非阻塞 STAGE 按这份顺序把页从 HBF 送进暂存缓冲；工作 warp 是消费者。
3. 关键约束：STAGE 跟踪项在需求首次访问该页时才退役，让需求给预取定速，限制预取超前的距离。
4. 按 **4 KB 页** 跟踪，页返回时才分配缓冲槽，从而把缓冲大小与在途流量分开。

仿真栈是 Accel-Sim v1.3 + Ramulator2。Table III：L2 40 MB，HBM/HBF 峰值读带宽各 2 TB/s，容量 80 GB / 1280 GB，HBF 延迟 20 µs。稠密模型、batch 64：Llama-8B、Mistral-24B、Qwen2.5-32B、DeepSeek-67B、Llama-70B、Qwen2.5-72B、Llama-405B（更大模型的 FP16 权重可达 800 GB 量级，评估走 INT4 等压缩路径）。MoE 用 TensorRT-LLM 持久 kernel，评估 Qwen3-30B 与 Qwen3-235B；batch 8/64 时平均激活 31 与 87 / 128 专家。staging warp 在 A100 / H100 / RTX PRO 6000 上的端到端 decode 开销为 **0.76–2.96%**（几何均值 2.1% / 2.4% / 1.2%）。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 稠密模型、40 MB vs 理想 HBF | 平均 **92.4%**（逐模型 78.0–107.2%；Llama-70B 与 Qwen2.5-72B 超过理想 HBF） | §VI-A |
| 稠密模型、16 MB | 平均 **88.8%**（74.1–102.7%），相对 40 MB 差 **4.0%** | §VI-A |
| H3 | 40 MB 只有理想性能的 **10.6%**（减速 4.8–11.5×）；320 MB 也只有 **43.1%** | §VI-A / 摘要 |
| HBF 读带宽（归一到 2 TB/s） | SlipStream-40MB 持续 **49.2–81.2%** 峰值 | Fig. 10 |
| MoE（Qwen3-30B/235B，几何均值） | 40 MB **91.2%**，16 MB **87.3%**；Qwen3-30B batch 8 为 83.7%，Qwen3-235B batch 64 为 97.1% | Fig. 14 / §VII-B |
| 系统对照 | Llama-70B 在四张已能放下权重的 HBM GPU 上，吞吐 **1.17×**。Llama-405B：十六张 HBF GPU + SlipStream 相对十六张 HBM 给出 **2.27×** 吞吐、**0.52×** 每 token 能量、**0.23×** EDP；按需序 H3 的 TPOT 为 602 ms（纯 HBM 的 10×），吞吐 0.55× | 讨论段 |
| 面积与功率（CACTI 22 nm） | SlipStream 增加约 0.39 mm²，相当于 826 mm² GA100 的 **0.02%**。在测得利用率下大约加 24.5–32.0 W（相对装 HBF 后系统功率 3.7–4.9%）。H3-320MB 面积 42.7%（22 nm），功率 +18–22% | Table IV / §VI |

## 与已有 HBF 页的增量
已有页面主要讨论 HBF 何时划算、KV/专家如何在 HBM–HBF 之间放置，以及层级带宽本身，例如 [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md)、[Characterizing HBF](/papers/characterizing-hbf-llm-serving.md)、[HBFSim](/papers/hbfsim-hbm-hbf-llm-memory-hierarchy.md)、[FLINT](/papers/flint-hbf-llm-inference.md)、[HyPAIC](/papers/hypaic-hbf-personal-ai-computer.md)。本篇补的是 **GPU 侧如何把近 20 µs 的读延迟藏住**，并且把暂存缓冲从数百 MB 压到 16–40 MB。对照对象是张量流式的 H3；数字来自 Accel-Sim + Ramulator2，与上述工作的 AISimulate / HBFSim 不宜直接横比。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把 HBF 从「容量层」接到 GPU 上可部署的预取通路
- [When Is HBF Cost-Effective](/papers/when-is-hbf-cost-effective-llm-inference.md) — 问装机是否收回成本；本篇问延迟被藏住之后吞吐与能量能否接近理想 HBF
- [Memory Hierarchy / Cache](/concepts/memory-hierarchy-cache.md) — 页级、由需求定速的 staging 缓冲

## 开放问题
- 主结果是周期级仿真；硅上只测了 staging warp 的开销，没有在真实 HBF 器件上跑端到端。
- 数据相关结构（如 embedding 表）仍留在 HBM；动态派发 tile 的 kernel 需要 CTA 至少提前 20 µs 认领工作。
- 20 µs 的逐层冷启动要靠跨 kernel staging 或持久 megakernel 才能摊掉。
- Llama-405B 的系统对照依赖「八张 HBF GPU 就能放下整份副本」这一容量假设，以及所建模的互连与能量模型。

# Citations
- [arXiv:2611.14776](https://arxiv.org/abs/2611.14776) — Saxena, Taneja（Georgia Tech）；Kozyrakis（NVIDIA Research & Stanford）；Jaleel（NVIDIA Research）。HPCA 2027
- [raw stub](/raw/papers/slipstream-hbf-gpu-prefetch.md)
- [PDF](/raw/papers/SlipStream_HBF_GPU_Prefetch_HPCA2027.pdf)
