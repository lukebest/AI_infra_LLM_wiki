---
type: Paper
title: "TripleKV: Predict, Prefetch, Protect – KV Cache Management for AI Agents"
description: "UIUC / IBM Research / NTUA — 单卡 H100 NVL + vLLM 实测；相对带 DRAM/SSD 层的 vLLM，P95 TTFT 在四套智能体负载上最高降 49%；临界路径 SSD 读取从 45–76% 降到 10% 以下"
tags:
- kv-cache
- serving
- serving-system
- ai-agent
- agentic-ai
- prefetch
- inference
- latency
- ssd
- memory
- llm
- hardware
created: 2026-11-24
updated: 2026-11-24
timestamp: '2026-11-24T00:00:00Z'
paper_author: [Shashwat Jaiswal, Chloe Alverti, Mengmei Ye, Chen Wang, Hubertus Franke, Fan Lai, Tianyin Xu, Josep Torrellas]
year: 2026
venue: preprint
arxiv: '2611.25112'
sources:
  - raw/papers/TripleKV_Predict_Prefetch_Protect_2026.pdf
  - raw/papers/triplekv-predict-prefetch-protect-agent-kv.md
---

# TripleKV：用工具时延预测，把智能体 KV 提前取回 DRAM

## 一句话结论
伊利诺伊大学厄巴纳-香槟分校、IBM Research 与雅典国立技术大学的 TripleKV，在智能体「推理–工具」循环里，用工具时延预测器在工具执行期间把下一轮所需的 KV 块从 SSD 预取到主机 DRAM，并保护这些块不被提前驱逐。相对扩展了 DRAM/SSD 层的 vLLM，四套数据/网页/编程智能体负载上，需要在临界路径读 SSD 的请求从 45–76% 降到 10% 以下，P95 TTFT 最高降低 49%；相对 TokenCake、Continuum 等智能体感知系统，P95 TTFT 可到 1.5–7× 更低。

## 动机
ReAct 风格智能体会把不断变长的上下文反复送回推理引擎。Qwen3-30B-A3B 大约 96 KiB/token，一条 50K token 的上下文约 4.6 GiB；H100 NVL 在权重与运行开销之后大约只剩 32 GiB 给 KV，只能同时放下约六条这样的上下文。工具调用期间 KV 可能闲置上百秒，并发智能体把块驱逐到 DRAM 乃至 SSD。LRU 在中等负载下就会把这些块提前清掉：实验里最多 76% 的推理请求发现先前缓存已落到更慢层或被丢弃，50K 上下文从 SSD 取回可能要数秒，否则就要重新 prefill。

智能体场景里，下一轮推理需要哪些 KV 块事先已知，不确定的只是工具何时返回。预取目标因此可以放到主机 DRAM：不必预占稀缺的 GPU 显存，也不会和正在进行的推理争用 GPU。

## 方案
三层 KV：L1 为 GPU HBM，L2 为主机 DRAM，L3 为 SSD。三个组件配合：

- **Predict**：在智能体 harness 里用工具感知的时延预测器估计工具完成时间，按这个时点从 L3 发起预取。
- **Prefetch**：异步、低优先级地把所需块读进 L2；与 GPU 上的推理路径分开。
- **Protect**：L2 用保护类别与牺牲者缓存式的 watch list。预取时仍留在 L1 的块（实验里最多约 30% 的 prompt token）被加入 watch list，一旦从 L1 驱逐且 L2 还没有副本，就从 L3 回填到受保护的 L2 槽位。L2 还保留一小段空闲（文中 256 块 / 1.5 GiB）给层间在途块。驱逐优先级为 CACHED > BACKUP > PREFETCHED。

实现是在 vLLM 的 offloading connector 上大约 3000 行代码，预测器不足 300 行 Python，每个工具调用发一次预取。评测用 64-token 块（6 MiB）和每 GPU 64 GiB L2（约 10,900 块），超时 120 s。

平台（Table 3）：单卡 NVIDIA H100 NVL（94 GB HBM），Qwen3-30B-A3B（BF16 约 60 GiB），L1 32 GiB、L2 64 GiB、L3 为 1 TiB RAID 并以 `O_DIRECT` 读取；vLLM v0.24（2026 年 6 月）。负载为 DRB、GAIA、TB4、BC+ 四套，各从现场跑出的 50 条任务轨迹回放，并发 12 / 16 / 20 个智能体线程。对照为带 L3 的 vLLM、TokenCake、Continuum+LMCache，以及用轨迹真实工具时延替换预测的 Oracle。各组 L2 都固定 64 GiB。作者把 L2 收在 64 GiB，是为了在 50 个智能体会话可产生 200–500 GiB 上下文的高度占用场景里观察行为。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 临界路径 SSD 读取 | 从 45–76% 降到 **10% 以下** | Abstract / §3.2 |
| P95 TTFT vs 带 L3 的 vLLM | DRB / GAIA / TB4 / BC+ 上分别最高降 **35% / 49% / 23% / 33%**；中位持平或最多低 32% | Fig. 15 / §6.2 |
| vs 智能体感知系统 | 摘要：P95 TTFT 为 1.5–7× 更低。正文：尾部相对 TokenCake 最多优 **77%**，相对 Continuum 最多优 **86%** | Abstract / §6.2 |
| 请求吞吐 vs 带 L3 的 vLLM | DRB / GAIA / BC+ / TB4 上分别最多 **+18% / +40% / +31% / 持平**；相对 TokenCake / Continuum 请求吞吐最多为其 2.9× / 3.5× | Fig. 16 / §6.2 |
| prefill / decode 吞吐 | 相对带 L3 的 vLLM，四套负载合计最多 **+40%** token/s；相对 TokenCake 与 Continuum 最多 **3.5×** | Fig. 17 / §6.2 |
| 相对 Oracle | 时延与吞吐都落在 **5%** 以内 | §6.2 |
| 平均请求等待 | 20 个智能体时，相对带 L3 的 vLLM 最多少等 **78%**；后者平均最多花 1.6 s 读 L3，TripleKV 在 16 个智能体及以下最多 0.05 s，20 个时最多 0.45 s | Fig. 18 / §6.2 |
| 覆盖 / 精度 / 及时性 | 覆盖 96–100%，GAIA 20 为 87%、BC+ 20 为 60%；精度 97–100%；预取在入队前完成的请求占 96–100%，与 Oracle 相差在 1% 以内 | Fig. 19–21 / §6.3 |
| 受保护需求 | 12 个智能体时 4–23 GiB，20 个时 27–83 GiB；GAIA 20 与 BC+ 20 碰到 64 GiB 上限，分别有 13% 与 38% 的预取块在使用前被驱逐 | Fig. 22 / §6.3 |

消融（Fig. 23，20 个并发）：工具一开始就天真预取，仍有 21–45% 的请求在临界路径读 L3；加上 Protect 再加 Predict，这个比例与尾延迟随组件递进下降。

## 与已有页的增量
[ASK](/papers/ask-tool-progress-agent-kv-serving.md) 读工具进度来决定服务侧动作。[Evolving Infra](/papers/evolving-infra-agent-adaptive-llm-serving.md) 按智能体自适应放置 PD 与 KV。[Host-Tier KV](/papers/host-tier-kv-npu-agent-workflows.md) 在静态图 NPU 上同步宿主 KV。TripleKV 把预取目标放在 DRAM 而不是 GPU，用工具时延预测把 SSD 读隐藏在工具执行里，并在单卡 H100 上对着带三层存储的 vLLM 报出 P95 TTFT。

## 与 wiki 的关系
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — GPU / DRAM / SSD 三层 KV 与预取
- [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — L3 RAID、`O_DIRECT` 与临界路径读盘
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 归队智能体的 TTFT 被 L3 读取拉长
- [ASK](/papers/ask-tool-progress-agent-kv-serving.md) — 同样利用工具执行信息
- [Evolving Infra](/papers/evolving-infra-agent-adaptive-llm-serving.md) — 智能体感知的 KV 放置

## 开放问题
- L2 固定 64 GiB。GAIA 与 BC+ 在 20 个并发时受保护需求碰到或超过这个上限，覆盖分别降到 87% 与 60%。
- 评测回放现场轨迹，以保证输入、输出和工具时延一致；在线轨迹漂移要另看。
- L3 配置为足够大、不会驱逐；更小的盘或写压力不在本文范围。
- 实现是 vLLM offloading connector 上的约 3000 行扩展，预测器在 harness 侧。

# Citations
- [arXiv:2611.25112](https://arxiv.org/abs/2611.25112) — Jaiswal, Alverti, Ye, Wang, Franke, Lai, Xu, Torrellas（UIUC / NTUA / IBM Research）
- [raw stub](/raw/papers/triplekv-predict-prefetch-protect-agent-kv.md)
- [PDF](/raw/papers/TripleKV_Predict_Prefetch_Protect_2026.pdf)
