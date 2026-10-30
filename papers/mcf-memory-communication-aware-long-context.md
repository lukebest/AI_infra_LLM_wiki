---
type: Paper
title: "MCF: Memory- and Communication-Aware Long-Context Inference (MARS + FPGA Compute-NIC)"
description: "Essex — MARS 阶段性 KV 复制/收敛 + FPGA compute-NIC 元数据路由；16K prefill N=16 TTFT 0.62 s，相对 Ring/Zigzag ~3.1×/2.9×；4×KR260 decode 17.3 tok/s"
tags:
- context-parallelism
- kv-cache
- fpga
- inference
- interconnect
- communication
- collective
- serving-system
- hardware
- llm
created: 2026-10-30
updated: 2026-10-30
timestamp: '2026-10-30T00:00:00Z'
paper_author: [Huaizhi Zhang, Jiacheng Zhu, Xuqi Zhu, Junkyu Lee, Klaus McDonald-Maier, Xiaojun Zhai]
year: 2026
venue: arXiv cs.AR (EuroSys'27 header)
arxiv: '2610.34731'
sources:
  - raw/papers/MCF_Memory_Communication_Aware_Long_Context_2026.pdf
  - raw/papers/mcf-memory-communication-aware-long-context.md
---

# MCF：内存与通信感知的长上下文协同框架

## 一句话结论
静态 Ring/Zigzag 式 CP 在长 prefill 反复搬运历史 KV。MCF 用 **MARS** 在早期内存余量下选择性复制高复用 KV、中后期排空副本并收敛到分片 decode 布局，decode 改为 **KV 驻留 + 轻量 query/softmax 状态规约**；FPGA compute-NIC 按元数据做组播/集体/规约。16K prefill、N=16 时 TTFT **0.62 s**，相对 Ring **1.91 s** / Zigzag **1.81 s** 约 **3.1× / 2.9×**。

## 动机
- TP/PP 扩参数，但不直接解决序列维 KV 增长；CP 把序列分片，但静态环传播让历史 KV 反复上链路，带宽受限时 TTFT 陡升。
- Prefill 前段 KV 小、未来复用最高；后段内存紧、需要 decode-ready 紧凑布局——需要阶段自适应，而不是固定 sharding。

## 方案
1. **MARS（Memory-Aware Replication and Scheduling）**：按 chunk 选副本因子；早期复制高复用块以藏传播延迟；压力升高时 drain 冗余副本；prefill 结束保证 owner-only 分片，避免 PD 边界大迁移。
2. **Decode query-centric**：KV shard 不动；节点间只传 query / 局部 max·sum·partial output，NIC 侧 online-softmax 规约。
3. **FPGA 协同**：KR260 上 compute core + packetization + 元数据驱动 NIC（multicast / all-to-all / reduce）；ARM 仅初始化与 MARS 控制。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 16K TTFT vs 节点数 | N=2 **1.68 s** → N=16 **0.62 s** |
| 16K N=16 vs Ring / Zigzag | **0.62 s** vs **1.91 / 1.81 s**（~**3.1× / 2.9×**） |
| 16K N=16 通信量 | MCF **5.12 GiB**（略高于流式基线，换暴露延迟） |
| Prefill ≤8K | TTFT 曲线低于 Ring / Zigzag / PD disaggregation |
| Decode 吞吐 | 4×KR260、Qwen2.5-1.5B **17.3 token/s** |

## 与 wiki 的关系
- [NanoCP](/papers/nanocp-dynamic-context-parallelism-moe.md) — 动态 CP 度；MCF 侧重 **KV 布局阶段机 + 网内集体**
- [INC-MoE](/papers/inc-moe-innetwork-collectives-moe-inference.md) — 交换机内集体；MCF 把路由/规约放进 FPGA compute-NIC
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 长上下文 CP / PD 边界布局转换
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 推理侧元数据驱动组播与规约
- [Remote KV Tier for PCP Prefill](/papers/remote-kv-tier-context-parallel-prefill.md) — CP prefill 锁步与远端 KV；MCF 用复制藏传播

## 开放问题
- 评测以嵌入式 FPGA 集群与 1.5B 模型为主；相对 GPU Ring Attention 的端到端对照未展开。
- 动态链路带宽抖动下的 MARS 在线重调度未系统量化。

# Citations
- [arXiv:2610.34731](https://arxiv.org/abs/2610.34731) — Zhang et al., 2026
- [raw stub](/raw/papers/mcf-memory-communication-aware-long-context.md)
