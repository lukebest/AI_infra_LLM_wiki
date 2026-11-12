---
type: Paper
title: "Relief: A Per-Step Load-Balancing Engine for Expert-Parallel MoE Serving"
description: "HKU / HKUST — EP 逐步负载均衡；双向折半松弛替代逐步 LP；CUDA / PCIe FPGA / 片上引擎三套比特一致部署；硅实现达到逐步最优的 99.5%，相对静态放置最多回收 37.3 个百分点，求解 0.75–0.79 µs"
tags:
- moe
- expert-parallelism
- load-balancing
- serving
- decode
- inference
- fpga
- accelerator
- microarchitecture
- pcie
- hardware
created: 2026-11-12
updated: 2026-11-12
timestamp: '2026-11-12T00:00:00Z'
paper_author: [Jingyuan Li, Maolin Wang, Hayden So]
year: 2026
venue: arXiv preprint
arxiv: '2611.11402'
sources:
  - raw/papers/Relief_Per_Step_EP_Load_Balancing_2026.pdf
  - raw/papers/relief-per-step-ep-load-balancing.md
---

# Relief：按 decode 每一步重拆专家副本负载

## 一句话结论
港大 / 港科大提出 **Relief**：在专家并行（EP）服务里，每层每步重决定同一专家多个副本之间的 token 拆分。算法是双向 pairwise 松弛，对 token 计数做几次整数折半，不必再解逐步线性规划。三套部署——服务 GPU 上的 CUDA kernel、PCIe 上的 FPGA、加速器旁路的固定功能块——给出比特一致的拆分。在三个开源 MoE 族的 decode 路由上，硅实现的有效利用率达到逐步最优的 **99.5%**，相对已部署静态放置最多回收 **37.3** 个百分点；片上求解 **0.75–0.79 µs**。

## 动机
EP 组在最慢的 GPU 上结束。Token 路由每步都变，并且集中到少数专家，于是组里预留的 GPU 时间大量等掉队者。要收回这些时间，必须在每层每步重拆副本负载。精确 LP（如 LPLB）约 **102 µs**（文中亦写 ∼100 µs），对许多层已经比对层本身还长；其工作集按 156G² 字节增长，在 **G=39** 超过现网 GPU 共享内存，部署规模下根本 launch 不了。周期重放置（EPLB）只吃缓慢的统计偏斜，吃不到逐步残差。作者引用近期 ISCA 论文的判断——MoE 的动态性妨碍把激活专家均匀铺到 GPU 上——并用逐步决策频率的测量来回应。

在 Qwen3-30B-A3B（128 experts）的真实路由上，空间利用率（均值/峰值 per-rank 负载）在 G=16 平均 **0.42**，G=64 降到 **0.24**：部署规模下，专家阶段大约四分之三的预留 GPU 时间闲在掉队者后面。

## 方案
1. **Relief 松弛**：把 min-max 拆分写成可在整数上折半的双向 pairwise 过程，若干遍后贴近逐步最优，工作集随 rank 线性增长（文中写 live working set 每 rank 12 字节）。
2. **三套部署**：同一套验证过的引擎，分别落在服务 GPU 的 SM（CUDA kernel）、PCIe 对岸的 FPGA（可现场改），以及加速器旁边的固定功能块（作者类比 Xeon 上的负载均衡器）。输入是 32-bit 定点的 per-expert 计数，输出比特一致。
3. **与放置解耦**：专家放置仍用一次算好的 EPLB 均值放置（D=2 副本）；Relief 只改每步拆分。改放置对 Relief 只是一次 912 字节的重着色。

评测用 Qwen3-30B-A3B（128 experts, top-8, 48 layers）、OLMoE-1B-7B（64 experts, top-8）与 Qwen1.5-MoE-A2.7B（60 experts, top-4），路由来自 GSM8K 与 WildChat；G∈{8,16,32,64}。主度量 **Ueff** 是相对逐步最优的有效利用率。硅实现走 OpenROAD + ASAP7 7 nm 教育 PDK，时钟树阶段最小周期 **2.89 ns**，无 setup/hold 违例。所有曲线把引擎记为完全阻塞、不与层内其他工作重叠。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| 已部署静态放置的 Ueff | 按模型族达到逐步最优的 **66–72%** | 引言 / Table II |
| CUDA kernel 的 Ueff | 三族提到 **93%**；从百微秒层起，在每个组规模上达到或超过所有可部署方案 | 引言 / §V / Table II |
| 硅实现的 Ueff | 族均值 **99.5%**（Table II 中 EPLB + relief (silicon), I* 多列在 98.6–99.9） | Table II |
| 相对静态放置的最大回收 | **37.3** 个百分点 | 摘要 / 引言 / 结论 |
| 三套部署的求解延迟 | **0.75–28 µs**（相对精确 LP 的 102 µs） | Table I |
| 硅实现逐步延迟 | G=8 时 **0.75 µs**，G=64 时 **0.79 µs**，随组规模几乎平坦 | Fig 9 / §V |
| Kernel vs 精确 solver | 每次调用快 **3.7–7.3×**，并在 solver 无法 launch 的规模继续运行 | §I / §IV-A |
| Kernel vs 片上引擎 | 同等 pass 下 kernel 更长 **19–29×** | §V |
| 面积与占比 | 轮廓 **0.35 mm²**，37,434 flip-flops，1.29 M cells / 约一千万晶体管；按晶体管 **0.005–0.021%**，按面积 **0.017–0.022%**，按整块轮廓最多 **0.06%**；文中亦概括为 **0.02%** | §V / 摘要 |

精确 LP 的工作集在 G=39 跨过现网 GPU 共享内存；Relief 的 live working set 按每 rank 12 字节增长，256- 或 1024-expert 模型在 G=64 仍走同一套扫描日程。向量无活动估计在该网表上发散，作者因此未报绝对功耗。

## 与 wiki 的关系
- [GC-MoE](/papers/gc-moe-green-context-expert-parallel.md) — 用 Green Context 拆通信/计算来提高 EP 利用率；Relief 补的是逐步副本拆分这一侧
- [NCCL-EP Dispatch Offload](/papers/nccl-ep-moe-dispatch-offload-dbo.md) — 关心 dispatch 发送何时释放 GPU；Relief 关心专家计算阶段的掉队者
- [MegaMoE](/concepts/megamoe-kernel.md) / [FlashMoE](/concepts/flashmoe-kernel.md) — MoE 核与 EP 通信路径
- [In-Core Nonlinear Operator Acceleration](/concepts/in-core-nonlinear-operator-acceleration.md) — 同属把短决策/短算子做成可在临界路径上承受的硬件块；Relief 针对的是负载均衡决策而非非线性函数

## 开放问题
- 原文与 arXiv 条目均未写会议接收；上轮笔记中的 HPCA’27 未能在 PDF/摘要核实。
- 评测是在固定 EPLB 放置上改拆分，逐步最优本身也受该放置限制（Fig. 2：该两副本放置把最优钉在约 0.67 附近）。
- FPGA 路径带有恒定 PCIe 项，延迟落在 0.75–28 µs 区间的上端；绝对功耗未报。
- 引擎被记为完全阻塞，若与层内其他工作重叠，实际可回收时间还会变化。

# Citations
- [arXiv:2611.11402](https://arxiv.org/abs/2611.11402) — Li, Wang, So（HKU / HKUST）
- [raw stub](/raw/papers/relief-per-step-ep-load-balancing.md)
- [PDF](/raw/papers/Relief_Per_Step_EP_Load_Balancing_2026.pdf)
