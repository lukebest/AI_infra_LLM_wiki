---
type: Paper
title: "Recompute or Restore? Host-Tier KV for Multi-Model Agent Workflows on a Static-Graph NPU Serving Stack"
description: "Korea University 通讯 — ATOM+ 静态图 NPU 上同步宿主 KV；规划器重复 prefill 占已执行 prompt token 的 89.5%；两个过载条件 SLO 从 22.8%/9.4% 升到 100%/99.8%"
tags:
- npu
- kv-cache
- prefix-cache
- agentic-ai
- serving
- serving-system
- inference
- memory
- llm
- latency
created: 2026-11-16
updated: 2026-11-16
timestamp: '2026-11-16T00:00:00Z'
paper_author: [Sungwon Woo, Seyeon Kim]
year: 2026
venue: arXiv preprint
arxiv: '2611.15126'
sources:
  - raw/papers/Host_Tier_KV_NPU_Agent_Workflows_2026.pdf
  - raw/papers/host-tier-kv-npu-agent-workflows.md
---

# 静态图 NPU 上的宿主 KV：恢复还是重算

## 一句话结论
通讯作者标注 Korea University。作者在商业静态图 NPU 栈（Rebellions ATOM+，vllm-rbln 0.10.2）上，用两张卡跑 Qwen3-8B 规划器、一张卡跑 Qwen3-0.6B 执行器，衡量多模型智能体工作流要不要把被赶走的前缀从宿主 DRAM 恢复回来。设备 KV 预算在编译期写死，恢复还走与 prefill/decode 同一条引擎线程，所以收益事先并不确定。崩溃时规划器已执行的 prompt token 里有 **89.5%** 先前已经物化过。加上同步宿主层之后，两个过载条件上的工作流 SLO 达成率从 **22.8% 升到 100%**、从 **9.4% 升到 99.8%**。新种子上的保守负载增益：chain **11.8%**、fork **18.2%**；mixed 与突发负载对种子敏感。fork 工作流的 P99 也会因为这一层升高 **16–18%**。

## 动机
智能体工作流里的多次模型调用共享很长的上下文前缀，服务是否划算，很大程度取决于前缀 KV 能不能复用。在提前编译模型图的 NPU 上，图与 KV 预算在编译期就固定了，运行时布局由厂商栈掌管。完成的请求被挤出之后，后续调用只能重算。从宿主恢复可以避开重算，但拷贝占用与 prefill/decode 同一条引擎线程，所以「恢复一定更快」并不能事先成立。作者要回答两件事：服务崩掉时到底是什么工作在占时间；以及在这种栈上，恢复何时优于重算。

## 方案
测试床：ATOM+（RBLN-CA22），KMD 3.0.0，compiler / optimum-rbln 0.10.2，vllm-rbln 0.10.2.post2。规划器 Qwen3-8B bf16 做两卡张量并行，执行器 Qwen3-0.6B 占用第三张卡。宿主层建在运行时公开的 KV 拷贝接口上，写入与恢复都是同步的。

同时做了一个调度感知的事件模型，在每个测试队列开始前冻结预测，再与实测对照。负载是合成的工作流 DAG：chain、fork、mixed、mixed-burst。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 崩溃时的重复 prefill | 规划器已执行的 prompt token 里 **89.5%** 先前已经物化过 | 摘要 / 引言 |
| 两个过载条件的工作流 SLO 达成率 | **22.8%→100%**，**9.4%→99.8%** | 摘要 |
| 宿主容量扫描（9 GiB，0.65 workflows/s，KV32 mixed-burst） | SLO 达成 **99.9%**，关掉该层为 **28.7%**；同一扫描在 0.80 workflows/s 上各配置降到 21.1%、40.4% 等 | §4.2 |
| 端点确认（新种子，保守口径） | chain 负载增益 **≥11.8%**，fork **≥18.2%**；mixed / bursty 对种子敏感（例：mixed 在 seed 712 上 SLO 达成 27.6%，seed 713 通过） | 摘要 / §4.4 |
| 冻结模型 | 24 个常见负载条件下，中位与 P99 时延都落在 **15%** 容差内，其中包含 fork 上 **16–18%** 的 P99 上升 | 摘要 / §4.3 |
| 模型失准 | 三条策略对比被排错；更便宜存储路径的收益估成 **11%**，实测 **3.1%**（文中另记四次运行级 P99 算术均值 9.83 s→9.53 s，即 −3.1%） | 摘要 / §4.5 |

作者的判断：在这种栈上，恢复是否划算，除了缓存容量，还取决于运行时调度和传输代价。

## 与 wiki 的关系
- [ShadowPrefill](/papers/shadowprefill-per-step-model-routing.md) — 换模型时把前缀预热到另一套权重上，也使用宿主溢出；本篇问的是同一套静态图 NPU 上、被赶走的前缀该恢复还是重算
- [SlackTier](/papers/slaktier-engram-prefetch-deadlines.md) / [HiState](/papers/histate-hybrid-prefix-cache-agent.md) — GPU 或混合模型服务里的宿主 / SSD 前缀层；本篇把对象换成编译期写死 KV 预算的 NPU
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 把「设备 KV 预算固定」记进宿主恢复这条路径
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) — 恢复与 prefill/decode 抢同一条引擎线程，所以时延账会反转

## 开放问题
- 规划器 8B + 执行器 0.6B，规模小于数据中心常见的多模型路由部署。
- mixed 与 bursty 对随机种子敏感，保守负载增益只在 chain 与 fork 上成立。
- 冻结模型能框住常见负载的时延，但会排错策略、高估更便宜存储路径的收益。
- 宿主层给 fork 带来 16–18% 的 P99 上升，说明恢复代价会在某些拓扑上盖住收益。
- 实现绑定 vllm-rbln 0.10.2 与公开 KV 拷贝接口，换厂商栈需要重新标定传输代价。

# Citations
- [arXiv:2611.15126](https://arxiv.org/abs/2611.15126) — Woo, Kim（通讯作者脚注：Korea University；Woo 的机构在作者栏未单独写出）
- [raw stub](/raw/papers/host-tier-kv-npu-agent-workflows.md)
- [PDF](/raw/papers/Host_Tier_KV_NPU_Agent_Workflows_2026.pdf)
