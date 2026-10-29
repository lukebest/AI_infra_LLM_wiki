---
type: Paper
title: "INC-MoE: Overlapping In-Network Collectives and Expert Computation for Expert-Parallel MoE Inference"
description: "EP MoE 的 dispatch/combine 卸到交换机：片内 AllGather 组播 + ReduceScatter 规约，并与专家计算三阶段流水重叠；相对 vLLM 默认环集体 TTFT 最高 −33.1%、prefill 吞吐最高 +49.5%"
tags:
- moe
- expert-parallelism
- collective
- inference
- interconnect
- switch
- networking
- latency
- throughput
- serving-system
created: 2026-10-29
updated: 2026-10-29
timestamp: '2026-10-29T00:00:00Z'
paper_author: [John Stephan, Razvan Puscasu, Xu Yong, Ding Jiutao, Guan Zixuan]
year: 2026
venue: arXiv cs.DC
arxiv: '2610.36339'
sources:
  - raw/papers/INC_MoE_InNetwork_Collectives_MoE_Inference_2026.pdf
  - raw/papers/inc-moe-innetwork-collectives-moe-inference.md
---

# INC-MoE：交换机内集体 + 专家计算重叠的 EP MoE 推理

## 一句话结论
把 Expert-Parallel MoE 的 dispatch / combine 写成交换机侧 **AllGather（组播）** 与 **ReduceScatter（规约）**，并在单个持久 kernel 里按 token band 做 AG–FFN–RS 三阶段流水；因为两条 in-network 集体分别吃满链路的相反方向，重叠后带宽界通信时间相对并发环集体缩短 **(N−2)/(2(N−1))**（N=4 时 **33.3%**，N=8 时 **42.9%**）。在仿真四节点 + 专用 INC 交换机加速器上，OLMoE prefill（EP=4）相对 vLLM 默认环集体路径 TTFT **−20.2–33.1%**、prefill 吞吐 **+25.3–49.5%**，输出一致。

## 动机
- EP 服务里 dispatch 把 token 送到持有所选专家的加速器，combine 把专家输出送回 token 属主；多节点上这两步常占 MoE 层延迟大头。
- 端点环 AllGather / ReduceScatter 并发时，两条集体仍在同向争带宽，重叠几乎不缩短合并后的带宽界时间。
- DeepEP / pplx 等加速 all-to-all，以及 micro-batch / tile 级通信–计算重叠，都没有同时利用「交换机内双向集体」和「device 发起的 band 级流水」。

## 方案
1. **In-network AG / RS**：每 rank 一次有根组播实现 AllGather；有根交换机规约 + 根上本地归约实现 ReduceScatter；主机↔交换机走消息语义。
2. **双向重叠收益**：in-network AG 偏收、RS 偏发，并发时各吃链路一半方向；理论相对并发环集体缩短 **(N−2)/(2(N−1))**，等价带宽最高约 **2(N−1)/N**（N=4 → **1.5×**）。
3. **Band 流水持久 kernel**：token 分 band；稳态下角色分工的 thread block 同时 gather 下一 band、计算当前 band、reduce 上一 band；device 侧同步；尾部 gather 块协助收尾以缩短 drain。
4. **落地**：作为 vLLM MoE 层 drop-in；评测用四节点 scale-out 仿真，第五加速器扮演 INC 交换机。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 理论通信缩短（vs 并发环） | N=4 **33.3%**，N=8 **42.9%** |
| 独立并发 AG+RS 等价带宽 | INC **163–172 Gbps**，相对环 **+25.6–31.8%**（达自身界 **82–86%**） |
| Prefill TTFT vs vLLM 默认 | **−20.2–33.1%**（随 prompt 增大） |
| Prefill 吞吐 vs vLLM 默认 | **+25.3–49.5%**（摘要写最高约 50%） |
| 基线吞吐形态 | 环路径约 **22.5K–23.8K** tok/s/加速器近乎平坦；INC 随 prompt 升至约 **32K** |

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 把 AG/RS 从训练配方推到 **推理 EP**，并强调交换机内集体与端点环的带宽方向差异
- [MCCL](/papers/mccl-measurement-based-collective-communication.md) — 测量闭环换集体算法；INC-MoE 换执行位置（交换机）与重叠结构
- [T-CCL](/papers/t-ccl-tma-collective-communication.md) — 节点内把搬运/规约卸给 TMA；INC-MoE 把 EP dispatch/combine 卸给交换机
- [Zepp](/papers/zepp-distributed-moe-serving-relaxed-balance.md) / [FastEEP](/papers/fasteep-intra-instance-elastic-ep-moe-serving.md) — MoE serving 通信与 EP 拓扑侧优化；INC-MoE 聚焦 in-network 原语 + kernel 流水
- [Switching Elements](/concepts/switching-elements.md) — 交换机侧组播/规约作为交换单元能力

## 开放问题
- 评测是仿真 INC 交换机而非商用 SHArP/可编程交换机硅；真实多跳拓扑与拥塞下 bound 可达性未知。
- 与 DeepEP 风格 all-to-all、dual-batch overlap 的正交叠加未做端到端对照。
- Decode 阶段小消息 / 低带宽利用率时，交换机固定开销是否仍划算未展开。

# Citations
- [arXiv:2610.36339](https://arxiv.org/abs/2610.36339) — Stephan et al., 2026
- [raw stub](/raw/papers/inc-moe-innetwork-collectives-moe-inference.md)
