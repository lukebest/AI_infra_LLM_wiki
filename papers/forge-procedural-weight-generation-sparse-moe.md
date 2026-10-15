---
type: Paper
title: "FORGE: Procedural Weight Generation for Sparse MoE Inference"
description: "UW-Madison/NVIDIA ASPLOS'27 — 专家权重改成 O(log²d) 旋转角种子，SM 内 0.032 mm² 的 RGU 现场生成权重 tile 直写 SMEM；替换 30% MoE 层，专家 FFN kernel 2.3–3.2×，KV 容量 1.2–2.6×，系统吞吐 1.3–2.8×，代价是下游精度低于同预算 LoRA"
tags:
- gpu
- accelerator
- moe
- hbm
- memory-bandwidth
- inference
- decode
- expert-parallelism
- compression
- kv-cache
- nvidia
created: 2026-10-15
updated: 2026-10-15
timestamp: '2026-10-15T00:00:00Z'
paper_author: [Chanyoung Moon, Travis Pence, Daisuke Yamada, Jiaqi Mo, Yanxin Zhang, Vikas Singh, Karthikeyan Sankaralingam]
year: 2026
arxiv: '2610.16890'
venue: ASPLOS 2027
sources:
  - raw/papers/FORGE_Procedural_Weight_Generation_Sparse_MoE_2026.pdf
  - raw/papers/forge-procedural-weight-generation-sparse-moe.md
---

# FORGE：MoE 专家权重在 SM 内现场生成

## 一句话结论
短上下文 MoE decode 的瓶颈在于每步都要把专家权重从 HBM 搬进来，而且专家权重占满 HBM、逼出跨节点 EP。FORGE 把被替换层的每个专家离线拟合成一组 Clifford 代数旋转角（rotor seed），推理时由每个 SM 里一个固定功能单元 RGU 现场生成权重 tile 写进 Shared Memory，直接喂 Tensor Core。权重路径从「搬」改成「算」，与量化正交。

## 动机（论文数字）
- 五个目标 MoE（DeepSeek-v3.2、GLM-5、Qwen3-235B、Qwen3-30B、Qwen3-Coder-Next）在 FP8 下，专家参数占总参数 **94–98%**。
- DeepSeek-v3.2（K=8, E=256）批 32 时每个专家只分到 1 个 token，FFN 退化成 GEMV；H100 上 cuBLASLt FP8 专家投影要到每专家约 **512** token（Qwen3-30B 约 **4,096**）才达到 50% SM 计算利用率，对应服务批 **16,384 / 65,536** token，远超交互式 decode 的批大小。
- 量化缩小了每参数字节，但每步仍要读全部激活权重并占用 HBM 容量；论文的 FP8 基线已是 H100 Tensor Core 原生最窄格式。

## 方案
| 部件 | 做法 |
|---|---|
| Rotor 投影 | 线性层拆成三段：d_in→chunk、m=2 个 rotor 映射、chunk→d_out；每 chunk 2ⁿ×2ⁿ 块对角，n∈{9,10,11}，每 chunk 只存 C(n,2) 个角度 |
| 并行执行模型 | 外层旋转轴顺序执行；内层按列（64 宽 SIMD）、行对（静态无冲突）、k 块三个轴并行；Supertile 对齐 GEMM thread-block tile，可跨多个 K 迭代复用 |
| 为何需要硬件 | 纯 SIMT 软件生成比整个基线专家 GEMM 慢 **25.8–45.1×**，指令数 **76–149×**，SMEM bank 冲突多 2–5 个数量级 |
| RGU 微架构 | 地址生成器（0.5 KB Base ROM + 9 KB Mapping ROM + 离线最大匹配得到的无冲突调度 ROM）、4-bank 1R1W 的 28.875 KB Supertile SRAM、0.43 KB 参数缓冲、双 64 宽 PE 道、2 周期一对；输出端直接做 Tensor Core 需要的 Phase-XOR swizzle 写 SMEM |

## 效果（仅论文数字；H100 实测基线 + RTL/周期模型 + 解析 decode 模拟器）
- 专家 FFN kernel（每专家 8 token）：**2.28–3.23×**；16 token 时降到 **1.13–1.67×**。Qwen3-235B 单专家延迟 **14.58 → 4.52 µs**。
- 全模型单 token decode（B=1，替换 30% MoE 层）：T=4K 时 **1.10–1.15×**，T=128K 时 **1.07–1.11×**。
- 容量：释放的权重 HBM 占总参数内存 **28–29%**；最大并发用户 T=4K **1.2–2.6×**、T=128K **1.1–3.5×**；同 GPU 数系统吞吐 **1.3–2.8×**。DeepSeek-v3.2 / GLM-5 最小装载 GPU 数从 **10/11 降到 7/8**，单个 NVLink 节点即可装下。
- 替换比 0.7 时吞吐 **2.0–6.1×**，但论文明确未评估该点精度，只作 what-if。
- PPA（ASAP7 7 nm）：每 SM **0.032 mm²**（约 SM 的 0.9%），**1.80 GHz**；132 个 SM 合计约 **4.2 mm²、5.1 W**（H100 die 0.5%、TDP 0.7%）。
- 精度（r=0.3，同为 rank-8 LoRA 恢复）：Qwen3-30B WikiText 困惑度 LoRA-only **6.53**、FORGE **7.65**；ARC-C 55.72→51.36，HellaSwag 60.88→57.10。三个模型族都低于 LoRA-only。

## 与 wiki 的关系
- [GEMM vs GEMV](/concepts/gemm-vs-gemv.md) — 每专家 token 少使 FFN 落入 GEMV 区；FORGE 用「片上生成」把带宽受限改成计算受限
- [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md) — 在 SM 内加一个与 Tensor Core 并行的固定功能单元，SIMT 发射口与 SMEM bank 被证明是软件路径的瓶颈
- [DRAM and Memory System](/concepts/dram-memory-system.md) — 权重从 HBM 驻留负载变成种子，释放的容量转给 KV
- [ThunderEP](/papers/thunderep-pcie-consumer-gpu-moe.md)、[Zepp](/papers/zepp-distributed-moe-serving-relaxed-balance.md) — 同样处理 MoE 容量逼出的 EP all-to-all；FORGE 从减少需装载的字节入手，让模型缩回单节点
- [HBM power 实测](/papers/hbm2-power-characterization-real-chips.md) — 同日入库；HBM 读是 HBM 最耗电的操作，减少权重读取也省 HBM 功耗（本页推断，论文未测功耗收益）

## 局限与开放问题
- 基线实测、设计为模拟；端到端数字经解析模拟器，不含改造后 SM 内的争用与占用效应；面积只算 RGU 本体，不含接入 SM 的连线；工艺是预测性 7 nm 对比商用 4 nm。
- 精度代价真实存在，替换比越高收益越大但精度未验证；能否用更好的恢复方法撑住高替换比是关键。
- 只评估了 H100；对 FP4/Blackwell 这类更窄原生格式，搬运收益与生成成本的平衡点会移动（本页判断）。
- 训练侧需额外 rotor 拟合步骤，对已发布开源权重的部署流程有门槛。

# Citations
- Moon et al., "FORGE: Procedural Weight Generation for Sparse MoE Inference", ASPLOS 2027, arXiv:2610.16890. [raw](/raw/papers/forge-procedural-weight-generation-sparse-moe.md) · [PDF](/raw/papers/FORGE_Procedural_Weight_Generation_Sparse_MoE_2026.pdf)
