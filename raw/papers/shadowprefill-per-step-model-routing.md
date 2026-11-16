---
type: Raw Source
title: "SHADOWPREFILL: Keeping Your Next Model Warm for Per-Step Model Routing in Agentic LLM Serving"
source_url: https://arxiv.org/abs/2611.13176
pdf: ShadowPrefill_Per_Step_Model_Routing_2026.pdf
retrieved: 2026-11-16
ingested: 2026-11-16
org: Microsoft Azure Research / Microsoft Azure
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.13176)

Per-step model routers send each LLM call of an agent to the cost-optimal model dynamically within each session. However, every model switch discards prefix-cache reuse: KV caches are per model, so the new model must prefill the relevant context before it emits a token. Across representative agentic workloads, including a production coding-agent trace with a mean context of 63K tokens, the prefix hit rate falls from 80–89% on same-model calls to 44–65% after a switch, and a switch call takes 1.5–3.2× as long. We present ShadowPrefill, which prefills the session’s context on the model the router has not chosen, in capacity that instances serving normal traffic leave idle, so the next switch finds its prefix cached. ShadowPrefill harvests the per-iteration SLO slack of requests in flight, protects routed calls, spills shadow KV to host memory, and falls back to a cold switch whenever the shadow is incomplete. With LLMRouter routing 24 model pairs over five agentic benchmark suites, ShadowPrefill cuts switch-call latency by 8.5–21.4%, LLM-call latency by 3.7–17.7%, and routed token cost by 22.5–46.1%, while normal traffic keeps its SLO and energy per request rises by 0.4%.

# Excerpts / key facts

- Authors: Haoran Qiu*, Rohan Mahapatra*, Rodrigo Fonseca（1 Microsoft Azure Research），Mark Russinovich（2 Microsoft Azure）。* 同等贡献。arXiv:2611.13176，cs.DC，2026-11-09 提交。PDF 19 页。摘要与 PDF 均未标注会议。
- 实现于 vLLM；主评估在 Vidur 上，算子剖面来自 H100。另有约 840 行 Python 的 vLLM 原型（未改 vLLM 源码）做测试床验证。
- 路由器：LLMRouter 的 accuracy-per-cost 策略，限定为小模型 S 与大模型 L 的二元组，共 24 对，覆盖 Qwen、Llama、Mistral、Gemma、GPT-OSS、Granite 及同族/跨族组合。
- 五类负载（Table 1）：xRouteBench（切换 19%、均 2.3 次/会话、提示均 19K）、FusionBench（26%、3.1、13K）、Router-R1（33%、4.1、10K）、GHCP-coding（26%、2.0、63K，来自公开 GitHub Copilot 编程智能体轨迹一日）、SWE-bench（26%、10.9、36K）。同模型前缀命中 80–89%，切换后 44–65%。切换调用相对同模型：xRouteBench **3.2×**，GHCP-coding **1.5×**（Fig. 2d）。
- 空闲容量：回放一周 Azure LLM 推理对话轨迹；负载一天内摆动 **3–10×**。代码流量实例在中位小时完全空闲 **72%**、低谷小时 **85%**、高峰 **8%**。高峰时一次迭代大约只用掉 TPOT SLO 的四分之一，**69–79%** 的每迭代时延预算空着（Fig. 3b）。
- 机制：SLO-slack 收割控制器；routed-step 保护；影子 KV 类上限为 KV 池的 **25%**，溢出到宿主 DRAM；按切换可能性排序的增量/流式/粘性影子任务；不完整则冷切换回退。也推广到 PD 解耦集群。
- 对照（Table 2）：No Shadow、Host Tier、Harvest（固定额度 δ=0.1）、Harvest-SLO、Harvest-SLO+Host（主方案）、Predictive（切换概率 ≥0.25 才做影子）、Dedicated（+25% GPU）、Oracle / Oracle+Host。缓存输入按未缓存价的 **10%** 计费。仿真默认正常流量 ρ=0.7（高峰时 90% 请求同时满足两条 SLO 的容量）；SLO 为 TTFT ≤ max(1 s, 5× 孤立 prefill) 与 TPOT ≤ max(25 ms, 5× batch-1 decode)。
- 仿真主结果（Harvest-SLO+Host 相对 No Shadow）：切换调用时延，16 个基准对平均 **−10.4%**，6 个 GHCP 对 **−14.3%**，单对最高 **−21.4%**（Oracle 上界 19.3% / 27.4%，本方案分别达到其上界的 **54%** 与 **52%**，不额外加 GPU）。GHCP 一次冷切换调用 19.0 s，本方案省 3.3 s。切换 TTFT **−44.1%** / **−47.0%**。全部 LLM 调用时延 **−5.0%** / **−9.7%**（Oracle 9.6% / 13.8%）。token 加权命中率：基准 75.0%→82.1%，GHCP 55.4%→76.3%。路由 token 费用基准 **−28.5%**、GHCP **−32.0%**，单对最高 **−46.1%**（Fig. 6e–h）。消融：Harvest 6.9%，Harvest-SLO 8.8%，再加宿主层到 10.4%（基准切换时延）。每请求能量 **+0.4%**；Dedicated 为 +25% GPU 且能量 +11.7%。正常流量 SLO 达成不下降，还升了 0.10–0.40 个百分点。影子 token 里 **63%** 后来没用上。PD 解耦上影子会唤醒本来空闲的 prefill GPU，能量 **+11.5%**。
- 失效与边界：目标超过 50B 时解码占主导，切换时延只降 **3%**；张量并行度加倍后 Harvest-SLO+Host 的 LLM 调用收益降到 **3.5%**；约 0.5 次切换/会话时收益为 **−0.2%**；ρ=0.9 时 Harvest-SLO 只剩 **0.7%**，此时主要靠宿主层。
- 测试床（Section 6 / Fig. 12）：相对各路由器自己的 No Shadow，估计 token 费用平均 **−20.4%**；结论处把切换时延与费用范围概括为 **8.5–21.4%** 与 **22.5–46.1%**（与摘要一致）。
