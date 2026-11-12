---
type: Raw Source
title: "Evolving Infra: Agent-Adaptive LLM Serving at Scale"
source_url: https://arxiv.org/abs/2611.12304
pdf: Evolving_Infra_Agent_Adaptive_LLM_Serving_2026.pdf
retrieved: 2026-11-12
ingested: 2026-11-12
org: Georgia Institute of Technology / University of Illinois Urbana-Champaign / University of California, Berkeley / NVIDIA / OpenAI / Massachusetts Institute of Technology
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.12304)

Agentic workloads are a major source of LLM inference demand. Existing prefill–decode (PD) disaggregated serving systems offer limited flexibility for runtime adaptation of compute allocation and KV cache management, and rely on coarse signals that only partly capture the diverse and dynamic agent workload. These limitations lead to load imbalance between prefill and decode nodes and eviction of KV caches that agents will reuse. We present EVOLVING INFRA, an agent-adaptive serving framework that adapts compute allocation to agent workloads and KV cache management to agent context management at runtime. We decouple compute allocation from key–value (KV) cache management, allowing nodes to switch efficiently between prefill and decode. Building on this design, an online planner matches the PD split to workload composition, while an agent-aware distributed KV manager guides cache eviction and transfer with signals from agent context management. Across coding, math, and computer-use tasks with GLM-5.2 and Kimi K2.6 on up to 256 GB300 GPUs, EVOLVING INFRA reduces mean end-to-end request latency and P95 TTFT by up to 4.1× and 14× over Dynamo, NVIDIA’s production framework.

# Excerpts / key facts

- Authors: Hao Kang*, Weili Xu*, Ziyang Li*, Zheng Du*, Hanchen Li, Tian Xia, Song Bian, Tushar Krishna, Huizi Mao, Ion Stoica, Song Han. *Equal contribution. Corresponding: hao.kang.sys@gmail.com. arXiv:2611.12304, 2026-11-09, cs.DC.
- 平台：最多 256×GB300；主实验为 9 个 4×GB300 节点、TP4。模型 NVFP4，FP8 KV，MTP 投机解码。GLM-5.2 用于 Putnam 与 Claude Code（CC），Kimi K2.6 用于 OSWorld 与切换负载。对照 Dynamo v1.5.1，以及整段吞吐最高的 SGLang 静态 PD 拆分。双方都从 6P3D 起步（切换负载 / 消融 / 最低并发另比最佳静态拆分）。
- 方案：对称引擎就地切换 P/D；共享 host-memory KV 池（每节点 L2 可缓存 4× L1 token）；智能体感知的集群 KV 目录；在线 planner 用迭代时间模型匹配 PD 拆分（窗口 Twin=600 s，m=10）；按智能体上下文做驱逐与路由，排队期间异步取远端 KV。
- 稳态（§6.2 / Fig 6 / Appendix C）：吞吐相对 Dynamo **1.10–2.73×**，丢失的 KV 复用减少 **81–95%**，均值 E2E 延迟 **1.15–4.12×**（CC **3.80–4.12×**，OSWorld **2.34–2.69×**，Putnam **1.15–1.23×**），P95 TTFT 最高 **13.92×**（CC 与 OSWorld **3.25–13.92×**）。最低并发下相对最佳静态拆分吞吐 **0.98–1.38×**。相切换平均 **6.2 s**，Dynamo 重启动平均 **754 s**（超过 100×）。
- 切换负载（§6.3 / Fig 7 / Appendix C.4）：相对 Dynamo / 最佳静态，均值 E2E **2.15× / 1.33×**，P95 TTFT **3.58× / 1.88×**，吞吐 **2.14× / 1.28×**。
- 消融（§6.4 / Fig 8，CC 126 并发）：四档初始拆分均值 E2E 最多差 **1.8%**，planner 都收敛到 4P5D。无在线拆分时基础设施+KV 感知路由相对同拆分最佳静态吞吐 **1.37×**；仅异步取 KV 相对上游 SGLang **1.12×**（prefill 空闲 23.6%→14.4%）。相对 cache-aware 路由，丢失 KV 复用 0.7% 对 2.4%，每请求未缓存 prompt token 少 **31%**。在最佳静态拆分上打开在线适应，吞吐只降 **0.3%**。
- 256 GPU（Appendix D.2，CC + GLM-5.2，10 agents/GPU）：静态 PD 的 P95 TTFT 从 36 卡 **142 s** 升到 256 卡 **418 s**；Evolving Infra 的 P95 TTFT 维持 **10–14 s**，均值 E2E 只升 **16%**。256 卡上二分搜索离线画像 **10,752** GPU-hour，是单次服务该 trace **768** GPU-hour 的 **14×**。
- 3,072 GPU 仿真（Appendix D.2，Frontier）：8 个 384 GPU 分区，约 30,720 并发智能体；集群合计 PD 比只变 **7%**，静态拆分下 8 区中 2 区排队可达集群均值 **13.9×**；分区 planner 相对静态拆分吞吐 **1.42×**。
- 开环（Appendix D.3 / Table D.2）：在 36×GB300 上维持 **1.0** agents/min（静态 4P5D 的两倍）；该速率下 P95 TTFT **12.3 s**，相对静态 4P5D / Dynamo 为 **11.3× / 9.9×**。摘要把主实验上界写成相对 Dynamo 均值 E2E **4.1×**、P95 TTFT **14×**（正文为 **4.12×** 与 **13.92×**）。
