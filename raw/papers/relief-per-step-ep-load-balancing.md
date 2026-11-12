---
type: Raw Source
title: "A Per-Step Load-Balancing Engine for Expert-Parallel MoE Serving"
source_url: https://arxiv.org/abs/2611.11402
pdf: Relief_Per_Step_EP_Load_Balancing_2026.pdf
retrieved: 2026-11-12
ingested: 2026-11-12
org: The University of Hong Kong / The Hong Kong University of Science and Technology
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.11402)

In expert-parallel Mixture-of-Experts serving, a layer finishes only when the most loaded GPU of its group does. Token routing shifts at every decode step and concentrates on a few experts, so most of the group’s reserved GPU time waits on stragglers. Recovering that time means re-deciding, at every layer of every decode step, how each replicated expert’s tokens divide between its copies. The exact linear-program solvers that make this decision optimally take longer than many of the layers they serve, and their working set outgrows GPU shared memory at deployment scale. We introduce Relief, a bidirectional pairwise relaxation that makes the linear program unnecessary, coming within a fraction of a point of the per-step optimum in a few passes of integer halving over the token counts. We build and measure three deployments, CUDA kernels on the serving GPU, the same verified engine on an FPGA over PCIe, and a fixed-function block beside the accelerator. On decode routing from three open MoE families, Relief holds the balance near the per-step optimum at every group size and layer time measured. Scored as effective utilization relative to that optimum, the kernel alone matches or exceeds every deployable scheme at every group size, from the hundred-microsecond layer on. The on-die engine widens that lead at every point, recovering up to 37.3 percentage points over the deployed static placement, while adding 0.02% of a current accelerator’s transistors.

# Excerpts / key facts

- Authors: Jingyuan Li (HKU), Maolin Wang (HKUST), Hayden So (HKU). arXiv:2611.11402, 2026-11-08, cs.AR。PDF 元数据与正文未标注会议；上轮笔记里的 HPCA’27 未能在原文核实，本页按 arXiv preprint 记录。
- 问题：EP 组在最慢 rank 上结束。Qwen3-30B-A3B（128 experts）上，空间利用率（均值/峰值 per-rank 负载）G=16 平均 **0.42**，G=64 降到 **0.24**。精确 LP（LPLB）约 **102 µs**（文中亦写 ∼100 µs），工作集 156G² 字节，在 G=39 超过现网 GPU 共享内存。
- 方案：Relief，双向 pairwise relaxation，对 token 计数做整数折半若干遍；三套部署给出比特一致的拆分：服务 GPU 上的 CUDA kernel、PCIe 上的 FPGA、加速器旁路的固定功能块。副本放置仍用一次算好的 EPLB 均值放置（D=2），Relief 只改每步拆分。
- 评测：Qwen3-30B-A3B（128 experts, top-8, 48 layers）、OLMoE-1B-7B、Qwen1.5-MoE-A2.7B；GSM8K 与 WildChat 路由；G∈{8,16,32,64}。有效利用率 Ueff 相对逐步最优。硅实现走 OpenROAD + ASAP7 7 nm，时钟树阶段最小周期 **2.89 ns**（无 setup/hold 违例）；面积轮廓 **0.35 mm²**，37,434 flip-flops，1.29 M cells / 约一千万晶体管。
- 效果（引言 / Table I–II / §V）：已部署静态放置达到逐步最优的 **66–72%**（按模型族）；kernel 把三族提到 **93%**，硅实现提到 **99.5%**（Table II 中 EPLB + relief (silicon), I* 族均值 99.5）；相对已部署方案最大回收 **37.3** 个百分点。三套部署延迟 **0.75–28 µs**；硅实现逐步求解 **0.75 µs**（G=8）到 **0.79 µs**（G=64）。Kernel 相对精确 solver 每次调用快 **3.7–7.3×**，且在 solver 无法 launch 的规模仍可运行；同等 pass 下 kernel 比片上引擎慢 **19–29×**。晶体管占比 **0.005–0.021%**（按面积 0.017–0.022%，按整块轮廓最多 0.06%），文中亦概括为 **0.02%**。
