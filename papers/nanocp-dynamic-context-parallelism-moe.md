---
type: Paper
title: "NanoCP: Dynamic Context Parallelism for MoE DP-EP Decoding"
description: "上交所/上海 AI Lab ASPLOS'27 — 按请求动态 CP 度解耦 MoE 绑定与 KV 绑定；99% TPOT-SLO 下相对最强 vLLM 可持续请求率最高 3.27×，P99 TPOT 最高降 2.01×"
tags:
- moe
- context-parallelism
- expert-parallelism
- kv-cache
- serving-system
- disaggregated-inference
- parallelism
- llm
- inference
created: 2026-10-23
updated: 2026-10-23
timestamp: '2026-10-23T00:00:00Z'
paper_author: [Jiefei Chen, Binbin Lin, Jinming Ma, Jiangfei Duan, Haojie Duanmu, Hao Liu, Qinxiu Cheng, Xiuhong Li, Zhilin Pei, Hui Wang, Xingcheng Zhang, Dahua Lin]
year: 2027
arxiv: '2605.21100'
sources:
  - raw/papers/NanoCP_Dynamic_Context_Parallelism_MoE_ASPLOS27.pdf
  - raw/papers/nanocp-dynamic-context-parallelism-moe.md
---

# NanoCP：可变长负载下 MoE DP–EP decode 的动态上下文并行

## 一句话结论
DP–EP MoE serving 把每个请求的 attention、MoE 集体与 KV 绑在同一实例上，attention 跟 KV 体量走、dispatch/combine 跟 batch 走，两者无法同时均衡，还会碎片化 KV 造成队头阻塞。NanoCP 用**按请求动态 CP 度**解耦 MoE 绑定与 KV 绑定：长请求跨实例分 KV，短请求留本地。99% TPOT-SLO 下相对最强 vLLM 基线，可持续请求率最高 **3.27×**，P99 TPOT 最高降 **2.01×**。

## 动机
- Attention 延迟随驻留 KV token 升；DeepEP dispatch/combine 随 per-rank batch 升；LeastCache 偏 KV 却扭曲 batch，LeastBatch 偏 batch 却扭曲 KV。
- 实测（32×DeepSeek-V3，Issue 1%，30 req/s）：MoE 通信 straggler 1020.6 µs vs 均值 354.7 µs（完美均衡可砍最大延迟 **65.2%**）；attention straggler 539.5 vs 184.3 µs（**65.8%**）。
- 均匀 CP（Helix 式）强迫短请求也付跨实例通信，并抬高有效 attention batch，损害 FlashMLA 效率。

## 方案
1. **DCP（动态上下文并行）**：每请求独立选 singleton MoE 绑定（均衡 batch）与多实例 KV 绑定（按长度桶选 CP 度 + WaterFill 分 token）。
2. **全局调度器**：跨 DP 实例统一视图；活跃请求可在已有 KV 绑定内重绑 MoE。
3. **AOT 图引擎**：预编译有限 (M,N) 形状桶的 CUDA Graph，运行时选最小可贴合桶。
4. **路由通信后端**：按稀疏 Q-Route / Res-Route 表做点对点直写（NVLink/IB），避开稠密集体与固定 Top-K MoE 库。
5. 开源：https://github.com/nano-infra/NanoEngine/tree/decentral-aug

## 效果（论文数字）
| 项目 | 结果 |
|---|---|
| DeepSeek-V3 Issue 1% / 5%（99% SLO） | 可持续请求率 **3.27×** / **2.11×** vs 最强 vLLM |
| 同工作负载 P99 TPOT | **1.94×** / **2.01×** 改善（在基线达 100 ms P99 的请求率点） |
| Kimi-K2 Issue 1% / 5% | 请求率 **1.88×** / **2.20×**；mean TPOT **1.87–2.07×**；P99 **1.79–2.12×** |
| CP 通信 | 均值 **60.4 µs** vs 均匀 CP8 **629.8 µs**（−**90.41%**） |
| Attention 失衡 | LeastBatch max/median **7.26×**；NanoCP 把最大 attention 压到 267.7 µs，max–median 差距降 **>84%** |
| 图内存 | 48 graphs、**5.32 GiB**/GPU（相对 vLLM 32DP +≈**3.0%** H200 HBM） |
| 峰值跨实例 CP 占比 | 仅 **1.1%** 请求；DCP A2A 峰值 **35.5 µs** |

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 在 DP–EP 内部再解耦「MoE 执行点」与「KV 驻留点」
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 侧 attention vs 集体通信的资源正交
- [FlashMoE Kernel](/concepts/flashmoe-kernel.md) / [MegaMoE Kernel](/concepts/megamoe-kernel.md) — 专家并行通信内核；NanoCP 管的是实例级放置与 CP
- [Remote KV Tiers for Context-Parallel Prefill](/papers/remote-kv-tier-context-parallel-prefill.md) — CP 语境下的远端 KV；NanoCP 面向 decode 可变长混合负载
- [FastEEP](/papers/fasteep-intra-instance-elastic-ep-moe-serving.md) — EP 组弹性；NanoCP 是 CP 度按请求弹性

## 开放问题
- 实现把 KV 绑定限制在单节点内；跨节点 SuperNode 级评估留给后续。
- Bucket(ℓ) 依赖离线扫长与 CP 度，换模型/互连需重标定。
- 与 TBO/NanoFlow 式算子重叠正交；长上下文混合负载上单独开 TBO 可能恶化尾延迟。

# Citations
- [arXiv:2605.21100](https://arxiv.org/abs/2605.21100) — Chen et al., ASPLOS'27
- 代码：https://github.com/nano-infra/NanoEngine/tree/decentral-aug
