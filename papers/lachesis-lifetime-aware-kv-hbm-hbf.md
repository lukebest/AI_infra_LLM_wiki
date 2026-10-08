---
type: Paper
title: "Lachesis: Lifetime-Aware KV Cache Placement for Agent Serving across HBM and High-Bandwidth Flash"
description: "SNU/KAIST/UIUC — agent harness 决定 KV 段寿命，按寿命把短命段放 HBM、长命段放 HBF；HBF 寿命 vs HBM-first 1.19–3.13×，达 3.3–12.2 device-years"
tags:
- agentic-ai
- kv-cache
- hbf
- hbm
- memory
- serving
- inference
- llm
created: 2026-10-08
updated: 2026-10-08
timestamp: '2026-10-08T00:00:00Z'
paper_author: [Jaehoon Yang, Jeongmin Lee, Haneul Park, Seung Yul Lee, Nam Sung Kim, Jae W. Lee]
year: 2026
arxiv: '2610.08378'
venue: arXiv preprint (cs.AR)
sources:
  - raw/papers/Lachesis_Lifetime_Aware_KV_HBM_HBF_Agent_Serving_2026.pdf
  - raw/papers/lachesis-lifetime-aware-kv-hbm-hbf.md
---

# Lachesis：按 KV 寿命在 HBM/HBF 间放置

## 一句话结论

HBF（高带宽闪存）容量比 HBM 高一个数量级、读带宽同级，但 NAND 擦写次数有限。Lachesis 的判断是：**选什么写进 HBF 应看 KV 段会活多久，而不是读写比**。短命 KV 放 HBM，HBM 块周转得快，就能替 HBF 吸收更多写入；而 agentic serving 里 KV 寿命由 agent harness（编排智能体的程序）决定，写入那一刻就能知道或预测。

## 动机

- agent 会话把累积上下文作为 KV 长期保留，子 agent 并发运行，活跃 KV 远超常规 serving；全放 HBM 要么加卡、要么降并发。
- 早期 HBF 设计只放只读数据（权重、共享前缀 KV）；近期工作把生成的 KV 也写进 HBF，主要按读写比挑选。作者指出 HBF 寿命取决于 HBM 能吸收多少写入 = HBM 容量 × 块回收次数，所以应按寿命挑。
- harness trace 分析出三条寿命分歧轴：
  - **时间轴**：去掉推理过程的上下文段比带推理段多活中位 **7.6–17.2×**（推理段在回合结束即丢弃）。
  - **结构轴**：lead agent 段长期保留，子 agent 段只把结果并回 lead 后即丢弃；lead 段比 worker 段多活中位 **4.0–6.1×**、比 reviewer 段多活 **4.7–38.3×**，而子 agent 段贡献回合内大部分 KV 写入。
  - **跨 worker 轴**：worker 寿命 p10→p90 相差 **23.6×**，需要从 spawn 记录预测排序。

## 方案

- 放置层位于 harness（OpenHands SDK、AOrchestra、Claude Code 一类）与 serving engine 之间：harness 报段 id、段类别与上下文边界；engine 暴露 `alloc(tier)` / `free(block ids)` 两个调用，每层一个空闲链表。
- 写入时：按段类别（确定性路径）+ worker 寿命预测排序（预测路径，取 HBM 空余容量能放下的 k 个最短命 worker）决定层；边界到达即释放，不等内存压力。
- 评估：模拟 serving engine + 两层内存，回放真实 agent trace（单 agent：τ³-bench、BFCLv4；多 agent：五个 benchmark 混合，含/不含 reviewer），Llama-4-Maverick 与 Qwen3-235B-A22B，8 GPU（attention DP + experts EP）。SLO：TTFT 2 s，P99 TPOT 紧 60 ms / 松 100 ms。HBF 每单元 10 万次 P/E（SLC），每 stack 512 GB，写放大 1.02。基线 **HBM-first**（HBM 有空就放 HBM）。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| HBF 寿命 vs HBM-first（全部 trace） | **1.19–3.13×**，达 **3.3–12.2 device-years** |
| 多 agent，HBM 占 8 槽中 1–4 槽 | Lachesis **3.3–9.3** 年 vs HBM-first **1.9–4.8** 年；紧 SLO **1.50–2.95×**、松 SLO **1.19–1.89×** |
| 紧 SLO 下 5 年保修 | Lachesis 在每种 GPU 内存配置、两种模型下都超过；HBM-first 仅 Qwen3 在 H3 daisy chain 配置下超过 |
| 写入构成 | Lachesis 写入 HBM 的 KV 量是 HBM-first 的 **8.2–19.5×** |
| 两条路径拆分 | 仅确定性路径 **1.11–2.00×**；预测路径再加 **1.33–1.54×**（无 reviewer 时 1.05–1.14×） |
| 单 agent trace | **1.35–3.13×** |

## 与 wiki 的关系

- [Characterizing HBF for LLM Serving](/papers/characterizing-hbf-llm-serving.md) — 同一 HBM–HBF 分层问题，前者用 buffered 调度延寿；Lachesis 把放置依据换成 harness 给的寿命
- [Hot–Cold HBM/HBF Tiering for Agentic Serving](/papers/hotcold-hbm-hbf-agentic-llm.md) — 热/冷按访问划分，Lachesis 按寿命划分，二者可叠加
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — HBF 作为 KV 层的写寿命约束
- [RR-Evict](/papers/rrevict-prefix-cache-eviction-agentic.md)、[Janus](/papers/janus-agentic-ssd-sparse-kv.md) — 同样利用 agent 会话结构做 KV 管理

## 局限与开放问题

- 全部为 trace 驱动模拟；用户回复延迟按对数正态（中位 120 s）采样，工具延迟取公开测量值，真实 HBF 器件与 serving 引擎未验证。
- 依赖 harness 主动上报段边界与 spawn 信息，需要 harness–engine 接口标准化。
- 开放问题：HBM/HBF 槽位比例是封装级设计参数，论文显示加 HBM 槽会减少 HBF stack 与总 P/E 预算，最优点随 SLO 变化，芯片厂如何定配比？

# Citations

[1] [arXiv:2610.08378](https://arxiv.org/abs/2610.08378) — Yang et al., Lachesis
[2] [raw stub](raw/papers/lachesis-lifetime-aware-kv-hbm-hbf.md)
