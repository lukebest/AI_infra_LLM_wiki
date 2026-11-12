---
type: Paper
title: "Evolving Infra: Agent-Adaptive LLM Serving at Scale"
description: "Georgia Tech / UIUC / Berkeley / NVIDIA / OpenAI / MIT — 智能体自适应 PD 与 KV；最多 256×GB300，相对 Dynamo v1.5.1 均值 E2E 最高 4.12×、P95 TTFT 最高 13.92×；吞吐最高 2.73×；相切换 6.2 s 对 Dynamo 重启动 754 s"
tags:
- disaggregated-inference
- prefill
- decode
- serving
- serving-system
- kv-cache
- agentic-ai
- ai-agent
- inference
- latency
- throughput
- scheduling
- nvidia
- openai
created: 2026-11-12
updated: 2026-11-12
timestamp: '2026-11-12T00:00:00Z'
paper_author: [Hao Kang, Weili Xu, Ziyang Li, Zheng Du, Hanchen Li, Tian Xia, Song Bian, Tushar Krishna, Huizi Mao, Ion Stoica, Song Han]
year: 2026
venue: arXiv preprint
arxiv: '2611.12304'
sources:
  - raw/papers/Evolving_Infra_Agent_Adaptive_LLM_Serving_2026.pdf
  - raw/papers/evolving-infra-agent-adaptive-llm-serving.md
---

# Evolving Infra：按智能体工作负载在线调整 PD 与 KV

## 一句话结论
Georgia Tech、UIUC、Berkeley、NVIDIA、OpenAI 与 MIT 提出 **Evolving Infra**：把节点的计算角色与 KV 管理拆开，用对称引擎就地切换 prefill/decode，再用在线 planner 与智能体感知的分布式 KV 目录去跟负载。在 coding / 计算机使用 / 数学智能体上服务 GLM-5.2 与 Kimi K2.6，主实验 36×GB300，扩展到 **256×GB300**。相对 Dynamo v1.5.1，稳态均值 E2E 延迟 **1.15–4.12×**（上界出现在 CC），P95 TTFT 最高 **13.92×**，吞吐 **1.10–2.73×**；摘要把这两项上界写成 **4.1×** 与 **14×**。

## 动机
已有 PD 解耦系统把节点上的 KV 绑在该节点当时的相位上。改 PD 拆分就要重启动节点或丢掉它的 KV；路由也要在负载均衡与缓存局部性之间取舍。智能体负载本身又会变：OSWorld 这类计算机使用任务每步追加截图，偏 prefill；Putnam 这类数学任务生成长推理轨迹，偏 decode；Claude Code 轨迹还夹着子智能体、压缩与长暂停。粗粒度信号（队列深度、KV 利用率）只部分反映这些变化，于是 prefill/decode 节点失衡，仍会被复用的 KV 也被驱逐。

## 方案
1. **对称引擎**：节点就地切换 prefill/decode，不必重启动，切换中继续服务正在跑的请求。
2. **共享 host-memory KV 池**：每个节点的 KV 对其他节点可读；节点上 host 内存（L2）可缓存 GPU 内存（L1）**4×** 的 token。请求在排队时异步取远端 KV，路由按预测最短 TTFT 选 prefill 节点。
3. **智能体感知的集群 KV 目录**：先驱逐已无活跃分支引用的替换历史、已结束子智能体的上下文，以及转移留下的重复副本。
4. **在线 planner**：用区分已缓存 / 未缓存 token 的迭代时间模型，按窗口（Twin=600 s，m=10）匹配 PD 拆分。

主实验：9 个 4×GB300 节点、TP4；模型 NVFP4、FP8 KV、MTP 投机解码。GLM-5.2 跑 Putnam 与 Claude Code（CC），Kimi K2.6 跑 OSWorld 与切换负载。对照 Dynamo v1.5.1，双方从偏 prefill 的 **6P3D** 起步；切换负载、消融与最低并发还对照整段吞吐最高的 SGLang 静态 PD 拆分。各跑 30 分钟预热后计入。稳态并发：Putnam 224/256/288，CC 90/108/126，OSWorld 128/144/160。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 稳态吞吐 vs Dynamo | **1.10–2.73×**；丢失的 KV 复用减少 **81–95%** | §6.2 / Fig 6 / Appendix C.4 |
| 稳态均值 E2E vs Dynamo | 全负载 **1.15–4.12×**；CC **3.80–4.12×**，OSWorld **2.34–2.69×**，Putnam **1.15–1.23×** | §6.2 / Fig 6 中行 |
| 稳态 P95 TTFT vs Dynamo | 最高 **13.92×**；CC 与 OSWorld **3.25–13.92×** | §6.2 / Fig 6 底行 |
| 最低并发 vs 最佳静态拆分 | 吞吐 **0.98–1.38×** | Appendix D.1 |
| 相切换耗时 | Evolving Infra 平均 **6.2 s**（含等待在跑请求）；Dynamo 重启动平均 **754 s**，全程退出服务（超过 **100×**） | Appendix C.1 |
| 切换负载（Putnam→混合→OSWorld） | 相对 Dynamo / 最佳静态：均值 E2E **2.15× / 1.33×**，P95 TTFT **3.58× / 1.88×**，吞吐 **2.14× / 1.28×** | Fig 7 / Appendix C.4 |
| 初始拆分敏感度（CC 126 并发） | 3P6D 到 6P3D 四档，均值 E2E 最多差 **1.8%**，都收敛到 4P5D | Fig 8a / Appendix C.2 |
| 组件贡献（同一 4P5D） | 基础设施+KV 感知路由，相对最佳静态吞吐 **1.37×**；仅异步取 KV 相对上游 SGLang **1.12×**（prefill 空闲 23.6%→14.4%） | Fig 8b / Appendix D.6 |
| 相对 cache-aware 路由 | 丢失 KV 复用 **0.7%** 对 **2.4%**；每请求未缓存 prompt token 少 **31%** | Appendix D.5 |
| 在线适应本身的吞吐代价 | 在已是最佳的静态拆分上打开，吞吐只降 **0.3%** | Fig 8b |
| 256×GB300（CC，10 agents/GPU） | 静态 PD 的 P95 TTFT 从 36 卡 **142 s** 升到 256 卡 **418 s**；本文 P95 TTFT 维持 **10–14 s**，均值 E2E 只升 **16%** | Appendix D.2 / Fig D.1 |
| 离线画像成本（256 GPU，3 小时 CC） | 二分搜索 **10,752** GPU-hour，是单次服务该 trace **768** GPU-hour 的 **14×**；穷尽搜索 **56,448** GPU-hour | Appendix D.2 |
| 3,072 GPU 仿真（Frontier，8×384） | 集群合计 PD 比只变 **7%**；静态拆分下 8 区中 2 区排队可达集群均值 **13.9×**；分区 planner 相对静态拆分吞吐 **1.42×** | Appendix D.2 |
| 开环到达（36×GB300，CC） | 维持 **1.0** agents/min，为静态 4P5D 的两倍；该速率下 P95 TTFT **12.3 s**，相对静态 / Dynamo 为 **11.3× / 9.9×**。目标为 P50/P95 TTFT ≤5/15 s、P50 E2E ≤10 s | Appendix D.3 / Table D.2 |

Planner 在 CC 上选 3P6D–4P5D，在 OSWorld 上选 8P1D，与 SGLang 下的最佳静态拆分（4P5D / 6P3D）不同，因为对称引擎会移动最佳拆分点（Appendix D.1）。在偏 decode 的 Putnam 上，planner 只留 1–2 个 prefill 节点换吞吐，224 与 288 并发时 P95 TTFT 会高于 Dynamo，均值 E2E 仍然更低。Putnam 上打开在线适应仍有收益，因为对称引擎改变了最佳拆分。

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 把 PD 拆分做成可在线、可保留 KV 的相切换
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 不同智能体（截图追加 vs 长推理）需要不同 P/D 比，而且会随时间移动
- [SiliconForge](/papers/siliconforge-should-you-split-decode.md) / [FastAFD](/papers/fastafd-attention-ffn-disaggregation-nvl72.md) — 前者问要不要再拆 decode，后者给 NVL72 上 AFD 的实测；本文处理的是智能体负载下 P 与 D 节点之间的在线分配与 KV
- [ARK](/papers/ark-kv-path-reservation-disagg.md) — 同校组（Georgia Tech）在解耦推理上的 KV 路径预留，关注点是网络大象流

## 开放问题
- 3,072 GPU 结果来自扩展后的 Frontier 仿真，远端 KV 取回被假定在 prefill 开始前完成、不计时。
- 开环实验中 planner 在 0.75 agents/min 上因一次切到 2P7D 而错过目标，1.0 agents/min 反而达到；作者记录了这次开关。
- 未与 SGLang 运行时角色切换对照，因为该路径拒绝本文模型使用的投机解码。Llumnix 无法在 GB300 的 Arm CPU 上运行，H200 对照放在 Appendix A.1。

# Citations
- [arXiv:2611.12304](https://arxiv.org/abs/2611.12304) — Kang, Xu, Li, Du, Li, Xia, Bian, Krishna, Mao, Stoica, Han
- [raw stub](/raw/papers/evolving-infra-agent-adaptive-llm-serving.md)
- [PDF](/raw/papers/Evolving_Infra_Agent_Adaptive_LLM_Serving_2026.pdf)
