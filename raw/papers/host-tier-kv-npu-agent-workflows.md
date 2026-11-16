---
type: Raw Source
title: "Recompute or Restore? Host-Tier KV for Multi-Model Agent Workflows on a Static-Graph NPU Serving Stack"
source_url: https://arxiv.org/abs/2611.15126
pdf: Host_Tier_KV_NPU_Agent_Workflows_2026.pdf
retrieved: 2026-11-16
ingested: 2026-11-16
org: Korea University（通讯作者脚注；Woo 的机构原文未单独列出）
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.15126)

Agent workflows issue dependent model calls that share long context prefixes, so serving them efficiently depends on reusing the key-value (KV) cache of those prefixes. On accelerators that compile model graphs ahead of time, however, the device KV budget is fixed, and prefixes evicted under load must be recomputed. Restoring them from host memory avoids this recomputation, but the transfer occupies the same engine thread as prefill and decode, so its benefit is not guaranteed. In this paper, we study when restoring beats recomputing on a commercial static-graph neural processing unit (NPU) stack (Rebellions ATOM+, vllm-rbln 0.10.2) that serves a Qwen3-8B planner on two cards and a Qwen3-0.6B executor on one. We first show that repeated prefill dominates planner work when default serving collapses: 89.5% of the executed planner prompt tokens had been materialized before. We then build a synchronous host-DRAM tier on the runtime’s public KV copy calls, together with a scheduler-aware event model whose predictions are frozen before each test cohort. Experimental results show that the host tier raises workflow service-level objective (SLO) attainment from 22.8% to 100% and from 9.4% to 99.8% in the two tested overload conditions, and endpoint confirmation on two new seeds supports conservative load gains of 11.8% (chain) and 18.2% (fork), while mixed and bursty workloads remain seed-sensitive. The frozen model predicts median and 99th-percentile (P99) latency within its 15% tolerance in all 24 common-load conditions, including the 16-18% P99 increase that the tier causes for fork workflows, but it misorders three policy contrasts and overestimates the benefit of a cheaper store path (11% predicted against 3.1% measured). The trade-off therefore depends on runtime scheduling and transfer cost as well as cache capacity.

# Excerpts / key facts

- Authors: Sungwon Woo、Seyeon Kim（通讯作者；脚注写 Korea University。Woo 的机构在 PDF/HTML 作者栏未单独写出；arXiv 提交者是 Woo）。arXiv:2611.15126，cs.DC，2026-11-11 提交、2026-11-13 公告。PDF 14 页。摘要与 PDF 均未标注会议。
- 测试床：Rebellions ATOM+（RBLN-CA22），KMD 3.0.0，compiler / optimum-rbln 0.10.2，vllm-rbln 0.10.2.post2。规划器 Qwen3-8B bf16 用两张卡做张量并行，执行器 Qwen3-0.6B 占用第三张卡。宿主层建在运行时公开的 KV 拷贝接口上，与 prefill/decode 同步占用同一引擎线程。
- 负载：回放合成的工作流 DAG（chain / fork / mixed / mixed-burst）。默认服务在过载崩溃时，规划器已执行的 prompt token 里有 **89.5%** 先前已经物化过，重复 prefill 占主导。
- 效果：两个过载条件上，工作流 SLO 达成率从 **22.8%→100%**、**9.4%→99.8%**。宿主容量扫描（F6、KV32 mixed-burst、seed 506）：9 GiB 在 0.65 workflows/s 时达成 **99.9%**（无该层为 **28.7%**）；0.80 workflows/s 时各配置降到 21.1%、40.4% 等，容量仍不够。新种子的端点确认给出保守负载增益：chain **≥11.8%**、fork **≥18.2%**；mixed 与 bursty 对种子敏感（例如 mixed 在 seed 712 上 SLO 达成 27.6%，seed 713 通过）。
- 冻结的调度感知事件模型：在全部 24 个常见负载条件下，中位与 P99 时延预测落在 **15%** 容差内，其中也包括宿主层给 fork 工作流带来的 **16–18%** P99 上升。模型把三条策略对比排错，并把更便宜存储路径的收益估成 **11%**，实测只有 **3.1%**（文中另有四次运行级 P99 算术均值从 9.83 s 降到 9.53 s，即 −3.1% 的测量）。
- 作者判断：在静态图 NPU 上，恢复是否优于重算，除了缓存容量，还取决于运行时调度和传输代价。
