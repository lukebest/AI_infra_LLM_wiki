---
type: Paper
title: "SHADOWPREFILL: Keeping Your Next Model Warm for Per-Step Model Routing in Agentic LLM Serving"
description: "微软 Azure — 逐步路由换模型时用正常流量的 SLO 空隙做影子 prefill；24 对模型上切换调用时延基准 −10.4%、编程轨迹 −14.3%（单对最高 −21.4%），路由 token 费用 −28.5%/−32.0%，能量 +0.4%"
tags:
- inference
- serving
- serving-system
- prefill
- kv-cache
- prefix-cache
- agentic-ai
- ai-agent
- disaggregated-inference
- latency
- microsoft
- llm
created: 2026-11-16
updated: 2026-11-16
timestamp: '2026-11-16T00:00:00Z'
paper_author: [Haoran Qiu, Rohan Mahapatra, Rodrigo Fonseca, Mark Russinovich]
year: 2026
venue: arXiv preprint
arxiv: '2611.13176'
sources:
  - raw/papers/ShadowPrefill_Per_Step_Model_Routing_2026.pdf
  - raw/papers/shadowprefill-per-step-model-routing.md
---

# ShadowPrefill：给下一步可能换到的模型预热前缀缓存

## 一句话结论
微软 Azure Research 与 Azure 在 vLLM / Vidur 上做影子 prefill：智能体逐步路由换模型时，KV 按模型隔离，切换会丢掉前缀命中。系统把会话上下文预填到「这次没被选中」的那套模型实例上，只使用正常流量迭代里尚未用掉的 SLO 空隙，并允许把影子 KV 溢到宿主内存。24 对模型、五类智能体负载上，主方案 Harvest-SLO+Host 把切换调用时延平均降低 **10.4%**（基准）与 **14.3%**（GitHub Copilot 编程轨迹），单对最高 **21.4%**；全部 LLM 调用时延降低 **5.0%** / **9.7%**；路由 token 费用降低 **28.5%** / **32.0%**（单对最高 **46.1%**）；每请求能量升高 **0.4%**，正常流量的 SLO 达成没有下降。

## 动机
逐步路由器会给智能体循环里的每一次 LLM 调用选一个更划算的模型。可是 KV 缓存在模型之间不能直接复用，切换之后新模型必须重新 prefill 相关上下文。Table 1 / Fig. 2：五类负载里 **19–33%** 的调用会换模型，每会话平均切换 **2.0–4.1** 次（SWE-bench 平均 10.9 次）。GHCP-coding 切换调用的平均上下文是 **63K** token。同模型调用的前缀命中是 **80–89%**，切换后降到 **44–65%**。切换调用相对同模型：xRouteBench **3.2×**，GHCP-coding **1.5×**，多出来的时间主要花在 TTFT 上。

与此同时，为高峰预留的实例经常有空档。作者回放一周 Azure LLM 推理对话轨迹：负载在一天内摆动 **3–10×**；服务代码流量的实例在中位小时完全空闲 **72%**、低谷小时 **85%**、高峰仍有 **8%**。即使在高峰，一次迭代大约只用掉 TPOT SLO 的四分之一，**69–79%** 的每迭代时延预算是空的。

## 方案
实现于 vLLM，主数字来自 Vidur 仿真（算子剖面来自 H100），另有约 840 行 Python 的 vLLM 原型（未改 vLLM 源码）做测试床核对。路由器采用 LLMRouter 的 accuracy-per-cost 策略，每次在小模型与大模型两套实例之间选择，共 24 对，覆盖 Qwen、Llama、Mistral、Gemma、GPT-OSS、Granite。

五条机制对应五类挑战：

1. **SLO-slack 收割控制器**：按在途请求相对 TTFT/TPOT 的余量决定本迭代还能塞多少影子块。
2. **Routed-step 保护**：带着被路由调用的迭代限制被拉长的幅度。
3. **影子 KV 类 + 宿主溢出**：影子条目最多占 KV 池的 **25%**，被挤出的会话（影子与正常）可溢到宿主 DRAM。
4. **增量、流式、粘性的影子任务**：按切换可能性排序；当前调用的新输入与输出 token 随到随追加。
5. **最低优先级、按迭代抢占，不完整就冷切换**：切换调用不等待影子做完。

方案也推广到 PD 解耦集群。对照包括 No Shadow、只开宿主层、固定额度 Harvest（δ=0.1）、Harvest-SLO、主方案 Harvest-SLO+Host、按切换概率 ≥0.25 门控的 Predictive、多 **25%** GPU 的 Dedicated，以及假设切换前缀免费的 Oracle。缓存输入按未缓存价的 **10%** 计费。仿真默认正常流量 ρ=0.7；SLO 为 TTFT ≤ max(1 s, 5× 孤立 prefill) 与 TPOT ≤ max(25 ms, 5× batch-1 decode)。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 切换调用时延（Harvest-SLO+Host vs No Shadow） | 16 个基准对平均 **−10.4%**，6 个 GHCP 对 **−14.3%**，单对最高 **−21.4%**；Oracle 上界 19.3% / 27.4%，本方案分别达到 **54%** 与 **52%**，不加 GPU | Fig. 4e–h / 正文 §5.2 |
| GHCP 单次冷切换 | 19.0 s，本方案省 **3.3 s** | §5.2 |
| 切换 TTFT | 基准 **−44.1%**，GHCP **−47.0%** | Fig. 5a–d |
| 全部 LLM 调用时延 | **−5.0%** / **−9.7%**（Oracle 9.6% / 13.8%） | Fig. 4a–d |
| token 加权命中率 | 基准 75.0%→**82.1%**，GHCP 55.4%→**76.3%**（Oracle+Host 为 84.4% / 81.3%） | Fig. 5e–h |
| 路由 token 费用 | 基准 **−28.5%**，GHCP **−32.0%**，单对最高 **−46.1%** | Fig. 6e–h / 正文 |
| 消融（基准切换时延） | Harvest **6.9%**，Harvest-SLO **8.8%**，再加宿主层到 **10.4%** | §5.2 |
| 能量与 SLO | 每请求能量 **+0.4%**；Dedicated 为 +25% GPU 且能量 +11.7%。正常流量 SLO 达成不下降，还升了 0.10–0.40 个百分点 | Fig. 8 |
| 影子浪费 | Harvest-SLO+Host 的影子 token 里 **63%** 后来没用上 | 讨论段 |
| PD 解耦 | 影子会唤醒本来空闲的 prefill GPU，能量 **+11.5%** | §5.4 |
| 测试床（vLLM 原型） | 估计 token 费用平均 **−20.4%**（Fig. 12）；摘要把切换时延与费用范围写作 **8.5–21.4%** 与 **22.5–46.1%** | §6 / 摘要 |

摘要里的 LLM 调用时延 **3.7–17.7%** 是跨对范围，正文主数字是上面的平均值。

## 与 wiki 的关系
- [HiState](/papers/histate-hybrid-prefix-cache-agent.md) — 同一模型族里把智能体前缀分层存放；本篇处理的是换模型之后前缀对另一套权重失效。
- [Evolving Infra](/papers/evolving-infra-agent-adaptive-llm-serving.md) — 智能体任务会改 PD 配比与 KV 放置；本篇补的是逐步路由换模型时的缓存预热。
- [SlackTier](/papers/slaktier-engram-prefetch-deadlines.md) — 同样把宿主内存当成推理热路径上的一层；本篇溢的是跨模型影子 KV。
- [Host-Tier KV on ATOM+](/papers/host-tier-kv-npu-agent-workflows.md) — 静态图 NPU 上「恢复还是重算」的实测；与本篇的宿主溢出层相邻，对象是同模型前缀在设备 KV 预算写死时被赶走。
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) / [Disaggregated Inference](/concepts/disaggregated-inference.md) — 本篇在共置与 PD 解耦两种部署上收割空隙，解耦时能量账不同。

## 开放问题
- 目标超过 50B 时解码占主导，切换时延只降 **3%**；把张量并行度加倍后，Harvest-SLO+Host 的 LLM 调用收益降到 **3.5%**。
- 大约 0.5 次切换/会话时，收益为 **−0.2%**。ρ=0.9 时 Harvest-SLO 只剩 **0.7%**，这时主要靠宿主层。
- 长推理输出（文中举例 DeepSeek-R1）会让目标实例几乎没有可收割的空隙。
- 影子工作是投机的：63% 的 token 可能浪费；对能量或功耗设上限的部署需要按切换概率门控，或只对最可能的下一个模型做影子。
- 主数字来自 Vidur + H100 剖面；测试床是对核心路径的核对，不是 24 对全量硅上复现。

# Citations
- [arXiv:2611.13176](https://arxiv.org/abs/2611.13176) — Qiu, Mahapatra, Fonseca（Microsoft Azure Research）；Russinovich（Microsoft Azure）
- [raw stub](/raw/papers/shadowprefill-per-step-model-routing.md)
- [PDF](/raw/papers/ShadowPrefill_Per_Step_Model_Routing_2026.pdf)
