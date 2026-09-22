---
type: Paper
title: "Weave: MoE Megakernel 内的细粒度动态 SM 调度"
description: "把 MoE dispatch/GEMM/combine 融入 persistent megakernel，层内联合选择通信 SM 与 chunk，并用 bubble stealing 回收空闲 SM。"
tags:
- architecture
- inference
- llm
- moe
- expert-parallelism
- interconnect
- gpu
- kernel
- scheduling
created: 2026-09-22
updated: 2026-09-22
timestamp: '2026-09-22T00:00:00Z'
paper_author: [Ziyu Huang, Yangjie Zhou, Chenhao Zhu, Zihan Liu, Jinyu Liu, Shulai Zhang, Xingxun Tang, Hongzhe Yan, Xinhao Luo, Minyi Guo, Xiu Lin, Yinghao Yu, Guodong Yang, Liping Zhang, Shixuan Sun, Jingwen Leng]
year: 2026
arxiv: '2609.21483'
sources:
  - raw/papers/Weave_Dynamic_SM_MoE_Overlap_2026.pdf
  - raw/papers/weave-dynamic-sm-moe-overlap.md
---

# Weave：MoE Megakernel 内的细粒度动态 SM 调度

## 一句话结论

Weave 将 MoE 的 dispatch、两次 GEMM、activation、combine 放进一个 persistent megakernel，再按层/按 GPU 联合选择通信 SM 和 chunk，空闲通信 SM 还能“偷”GEMM tile。4×H100、EP=4 上，MoE 层相对五个基线的几何平均加速为 **1.95–4.76×**，端到端为 **1.12–1.70×**；摘要跨基线汇总分别为 **2.89× / 1.33×**。

## 动机：固定 SM 切分跟不上 routing skew

Expert parallel 把 token 先 All-to-All dispatch 到 expert，再 combine 回原 GPU。通信 kernel 与 GEMM 都争夺 SM；SM 给通信太少会饿网络，给太多又会拖慢 GEMM。论文在 DeepSeek-V2-Lite 的连续层观察到，最佳通信 SM 数可在 **12–36** 间变化，而且不同 GPU 因 token routing 不均衡也需要不同配置。已有方案要么固定切分，要么只在 iteration 边界调整，无法处理层内 phase 变化。

## 方案

### 1. 五阶段 persistent megakernel

Weave 在一个 kernel 内执行 dispatch、GEMM0、activation、GEMM1、combine。通信路径采用 RDMA read，SM 完成 gather/scatter；GEMM 使用分层 tile 与 FP8/FP16 Tensor Core。持久化 kernel 避免阶段间 launch/synchronization，也让 SM 可以跨角色重分配。

### 2. cost model 联合选 SM 与 chunk

每层为每 GPU 根据 local/remote token 数、hidden size、expert shape 等统计量估计通信与计算时延。它联合搜索通信 SM 数 `c` 与 chunk 数 `K`，既覆盖层间 routing skew，又为层内 pipeline 选择粒度。在线决策平均只花 **0.54 μs**，所选配置与穷举最优平均差 **8.2%**。

### 3. chunk pipeline 与 bubble stealing

GEMM 分 chunk 后，combine 可以在某个 chunk 完成时立即开始。遇到通信 chunk 因 RDMA 未到达而等待，通信 SM 原地领取 GEMM tile；去重协议保证 tile 不会被两边重复执行。该机制把计算-通信并发活跃比例从 DeepEP 的 **14.1%** 提至 **47.1%**（DSv2-Lite 案例）。

## 量化结果

4×H100 SXM、NVLink 互连、EP=4，六个模型（DeepSeek-V2-Lite/V3、Mixtral、Qwen3、GLM-4.5、Kimi-K2）：

- **MoE layer**：相对 DeepEP、EPS-MoE、Comet、MegaMoE、Entwine 的几何平均加速范围 **1.95–4.76×**；论文摘要汇总为 **2.89×**。
- **端到端**：将真实 MoE layer 时间与合成 attention 时间组合后，几何平均加速范围 **1.12–1.70×**；摘要汇总为 **1.33×**。
- **消融**：在 layer-wise dynamic SM scheduling 上依次加入 fine-grained pipeline 与 bubble stealing；完整设计相对只做 dynamic scheduling 的平均提升为 **22.8%**。

## 局限与解读

- 实验只有 4×H100、EP=4、单机 NVLink；跨节点 RDMA、更多 GPU 和网络拥塞下的可扩展性尚未证明。
- 端到端结果把实测 MoE layer 与合成 attention 时间组合，而非完整模型服务 trace；需要谨慎解读 **1.33×**。
- cost model 假设 layer 级统计可在运行前快速取得，长期负载抖动和多租户干扰未覆盖。

Weave 延伸了 [LLM Distributed Training Collectives](../concepts/llm-distributed-training-collectives.md) 中的计算-通信重叠，但焦点是 MoE inference 的 **SM 这一共享资源**；相较 [FlashMoE](flashmoe-fast-distributed-moe-single-kernel.md) 的单 kernel 路径，它新增层内动态角色切换与 bubble stealing，也可与 [GEMM vs. GEMV](../concepts/gemm-vs-gemv.md) 一起理解不同 batch 下的 tile 可用性。

# Citations

1. Huang, Z., Zhou, Y., Zhu, C., et al. “Weave: Fine-Grained Dynamic SM Scheduling in an MoE Megakernel for Compute-Communication Overlap.” arXiv:2609.21483, 2026. [arXiv](https://arxiv.org/abs/2609.21483)
2. [本地原文 PDF](../raw/papers/Weave_Dynamic_SM_MoE_Overlap_2026.pdf)；[原始来源记录](../raw/papers/weave-dynamic-sm-moe-overlap.md)
