---
type: Paper
title: "MeshRT: Compile-Time Governed Wafer-Scale Runtime for Low-Latency High-Throughput Inference"
description: "Edinburgh/MSR SOSP’26 — 在 WSE-3 上把运行时动态编译进每核日程；相对 WaferLLM 吞吐最高约 56×，匹配配置每 token 多 25–40 µs（7.6–9.5%）；相对单实例 SGLang@H200 延迟 4.5–7.0× 更低，功率匹配集群投影 decode 系统吞吐 1.7–13.0×"
tags:
- wse
- cerebras
- inference
- compiler
- serving
- throughput
- latency
- mesh
- noc
- llm
- decode
- prefill
- microsoft
- now
- network-on-wafer
- moe
- batching
- scheduling
- programming-model
- serving-system
created: 2026-11-10
updated: 2026-11-10
timestamp: '2026-11-10T00:00:00Z'
paper_author: [Congjie He, Le Xu, Zhan Lu, Yeqi Huang, Haocheng Xiao, Cheng Deng, Lingxiao Ma, Ziming Miao, Fan Yang, Luo Mai]
year: 2026
venue: SOSP '26
arxiv: '2611.08508'
sources:
  - raw/papers/MeshRT_Wafer_Scale_Runtime_2026.pdf
  - raw/papers/meshrt-wafer-scale-runtime.md
---

# MeshRT：编译期治理晶圆级运行时动态

## 一句话结论
Edinburgh / MSR 提出 **MeshRT**（SOSP’26）：在商品晶圆级加速器（文中为 [Cerebras WSE-3](/entities/cerebras-wse.md) / CS-3）上，把连续批处理、MoE 路由和微批流水等运行时动态**编译进每核日程**，再用安全增量物化在核资源预算内做死锁无关的片上重配。相对静态 [WaferLLM](/concepts/waferllm-system.md)，匹配配置每 decode token 多 **25–40 µs**（**7.6–9.5%**），峰值系统吞吐最高约 **56×**（Table 3 GPT-OSS-120B **55.8×**）；相对实测单实例 SGLang@H200，延迟向每用户吞吐 **4.5–7.0×**；在理想线性缩放到功率匹配 H200 集群的投影下，decode 系统吞吐 **1.7–13.0×**。

## 动机
低延迟推理已成为付费档位，晶圆级加速器用片上 SRAM 与密致 NoC 压低每 token 延迟。现行和高吞吐技术（连续批处理、MoE、稀疏注意力、投机解码）会引入**运行时动态**：具体取值要到执行时才确定。GPU 栈把这类决策交给 host 管理的运行时状态；在晶圆上把决策送出片外，或做朴素的芯片级同步，会同时伤害延迟与吞吐。[WaferLLM](/papers/waferllm-wafer-scale-llm-inference.md) 一类既有晶圆栈难以高效支持这些动态，只能收紧动态特性以保住延迟，导致硬件利用率偏低、低延迟服务成本偏高。

关键观察：LLM 推理的 kernel 类型是封闭集合。动态的**具体值**要到运行时才知道，但其结构——在何处出现、属于哪一类、影响哪些核——可以在编译期完全确定。

## 方案
1. **Dynamism-aware per-core schedule synthesis**：给定计算图与空间映射，编译器按每个 kernel 的功能判断哪些核会接收或产生运行时动态，把控制消息处理逻辑与普通数据处理织进同一套每核日程（覆盖连续批处理、MoE 路由、微批流水）。
2. **Safe incremental materialization**：合成日程可能超出单核路由资源与队列缓冲。先把每核日程切成符合硬件预算的段，再在段边界做死锁无关的片上重配，并利用 collective 的全有或全无完成语义降低同步成本。
3. **实现平台**：商品晶圆级加速器；文中把 WSE-3 写作约 **900,000** PE 的 **762×1172** 阵列、聚合 SRAM **44 GB**、聚合带宽 **21 PB/s**、每 PE 约 **48 KB** 本地 SRAM。评测模型包括 Qwen3.5-9B、GPT-OSS-20B、Qwen3.5-35B-A3B、GPT-OSS-120B。35B 与 120B 的部分结果按 §6.1 投影。
4. **对照设定**：GPU 侧为实测单实例 SGLang@H200；系统吞吐按理想线性缩放到约 **20** 张 H200 / CS-3（DGX H200 按 **10.2 kW** / 八卡）做功率匹配投影。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| vs WaferLLM 匹配配置（Fig 10 / Table 3，4K，micro-bs=1） | Qwen3.5-9B 每 token 多 **40 µs**（**9.5%**）、GPT-OSS-20B 多 **25 µs**（**7.6%**）；单用户吞吐保留 **0.91×** / **0.93×** |
| vs WaferLLM 峰值系统吞吐（Table 3） | 9B **6.3×**、20B **32.7×**、35B-A3B **28.3×**、120B **55.8×**（摘要作最高约 **56×**）；跨工作点 **6.3–55.8×** |
| Prefill 相对 WaferLLM（Fig 9，4K 峰值） | 系统吞吐 **4.0–6.6×** |
| vs 单实例 SGLang@H200 延迟向 decode（Table 2a User） | 每用户吞吐 **4.5–7.0×**（延迟更低）：9B **6.1×**、20B **7.0×**、35B-A3B **4.5×**、120B **6.0×** |
| 功率匹配 H200 集群投影 decode 系统吞吐（Table 2a Sys） | **1.7–13.0×**：9B **13.0×**、20B **8.2×**、35B-A3B **1.7×**、120B **10.6×** |
| 延迟向能效（Table 2a tok/J） | 9B **12.2×**、20B **7.8×**、35B-A3B **1.6×**、120B **10.0×** |
| Decode 策略分解（Table 4） | 流水线并行 **5.5–30.1×**，连续批处理 **1.6–1.7×**，专家并行 **1.2–1.4×** |

吞吐导向设定（Table 2b）下，MeshRT 仍保持 **3.7–8.4×** 每用户优势；三个模型的聚合吞吐为 **1.2–2.3×**，Qwen3.5-35B 为 **0.58×**（文中归因于 micro-bs>2 后每用户吞吐下降）。Prefill 侧 GPU 在延迟向下每用户吞吐高 **1.3–2.3×**，吞吐向下投影系统吞吐高 **9–22×**。

## 与 wiki 的关系
- [Cerebras WSE](/entities/cerebras-wse.md) — 评测平台与 762×1172 / 44 GB / 21 PB/s 口径
- [WaferLLM System](/concepts/waferllm-system.md) — 直接基线；同一作者组在静态 PLMR 栈上补运行时动态
- [WaferLLM 论文页](/papers/waferllm-wafer-scale-llm-inference.md) — 2025 年端到端晶圆 LLM 推理系统
- [Network-on-Wafer](/concepts/network-on-wafer.md) — field-stitch 均匀 mesh 上控制面也必须本地化
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 晶圆 decode 带宽优势与 prefill 算力密度劣势
- [GPU–WSE Complementarity](/papers/gpu-wse-heterogeneity-complementarity.md) — GPU/WSE 异构边界对照

## 开放问题
- GPT-OSS-120B / Qwen3.5-35B-A3B 的部分系统数字按 §6.1 投影；功率匹配 H200 集群采用理想线性缩放。
- 相对 GPU 的 prefill 仍受 WSE-3 算力密度限制；文中用流水线并行部分补偿请求级吞吐。
- 封闭算子空间假设：新的动态机制可能需要新的治理原语。

# Citations
- [arXiv:2611.08508](https://arxiv.org/abs/2611.08508) — He, Xu, Lu, Huang, Xiao, Deng, Ma, Miao, Yang, Mai；Edinburgh / MSR；SOSP’26
- [raw stub](/raw/papers/meshrt-wafer-scale-runtime.md)
