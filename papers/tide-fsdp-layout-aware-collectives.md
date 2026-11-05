---
type: Paper
title: "TIDE: Zero-Copy Layout-Aware Collectives for FSDP2"
description: "KlingAI/快手 — FSDP2 布局感知零拷贝集体；64 GPU step 相对 Stock −27.1%、相对 SymmMem −6.0%；RS SM 12.5–14.5×"
tags:
- training
- collective
- allreduce
- distributed
- gpu
- llm
- parallelism
- fsdp
- rdma
created: 2026-11-05
updated: 2026-11-05
timestamp: '2026-11-05T00:00:00Z'
paper_author: [Zejian Wang, Yifan Zhao, Kaihui Ren, Xiaoling Zhou, Yubin Wang, Chenhao Guan, Lin Zhang, Yufeng Li, Zhikang Mo, Zhuoru Ma, Yingtong Xiong, Jihu Guo, Yiqiao Liao, Chengru Song]
year: 2026
venue: arXiv
arxiv: '2610.38228'
sources:
  - raw/papers/TIDE_FSDP_Layout_Aware_Collectives_2026.pdf
  - raw/papers/tide-fsdp-layout-aware-collectives.md
---

# TIDE：FSDP2 的布局感知零拷贝集体（FSDP Endgame）

## 一句话结论
FSDP2 参数/梯度按 per-parameter 存放，集体却走 flat rank-major；布局拷贝 alone 在 Llama-3.1 70B、8K tok/GPU 上占 step **6.4%**，默认 NCCL reduce-scatter 还能把本可单波完成的 GEMM 拖慢 **69%**。TIDE 基于公开 **NCCL 2.31+** API，把布局落入集体寻址：AG 经 NVSwitch 组播与 paced recursive-doubling RDMA **零 SM** 直达参数槽；RS 直接吃 bf16 梯度并规约到 fp32 shard（NCCL 无此混合精度模式）。64 GPU 上 step 相对 Stock FSDP2 最高 **−27.1%**、相对 FSDP2+SymmMem **−6.0%**；RS SM 时间少 **12.5–14.5×**。

## 动机
- FSDP2 计算侧与通信侧布局分裂，引发全量 copy-in / pack。
- 通信 kernel 与计算抢 SM：默认 RS CTA 预算可把并发 GEMM 从单波挤成双波。
- SymmMem 等对称内存路径仍留下缓冲与干扰空间。

## 方案
1. **TIDE-AG**：NVSwitch multicast + paced recursive-doubling RDMA，shard 直写参数存储，传输/放置不占 SM。
2. **TIDE-RS**：copy engine + 短命 CTA 做节点内累加，NVSwitch 做跨节点规约；bf16→fp32 混合精度规约。
3. **两阶段流水**：梯度读与网络进度分离；**Slot-Reuse** 可选把梯度暂存到已腾空的 AG 槽。
4. **评测**：64 GPU；Llama-3.1 70B、Wan2.2、Qwen3-30B-A3B；对照 Stock FSDP2 与 FSDP2+SymmMem。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| Layout 转换占 step（70B @ 8K） | **6.4%** |
| 默认 NCCL RS 对单波 GEMM | 拖慢 **69%** |
| Step vs Stock FSDP2（最高） | **−27.1%** |
| Step vs FSDP2+SymmMem（最高） | **−6.0%** |
| Reduce-scatter SM 时间 | **12.5–14.5×** 更少 |
| Backward 缓冲（In-Place / Slot-Reuse） | **3.72𝑁𝑆 / 2.29𝑁𝑆** |
| 相对 SymmMem 缓冲 | 可低约 **4.7 GiB** |

## 与 wiki 的关系
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — FSDP AG/RS 的布局与 SM 账；TIDE 把布局折进集体寻址
- [API-Level Memory Model for GPU Device Communication](/papers/api-level-memory-model-multi-gpu-communication.md) — 同属 GPU 间通信语义与拷贝路径
- [MCCL](/papers/mccl-measurement-based-collective-communication.md) — 测量换算法；TIDE 换布局与 SM 占用
- [Ofan](/papers/ofan-destination-aware-load-balancing.md) — FSDP2 CCT 侧网络 LB；TIDE 在集体内核与缓冲形态

## 开放问题
- 跨厂商 CCL（RCCL 等）与非 NVSwitch 域的可移植性依赖 NCCL 2.31+ 原语集合。
- MoE EP all-to-all 与 TIDE AG/RS 流水的联合调度未覆盖。

# Citations
- [arXiv:2610.38228](https://arxiv.org/abs/2610.38228) — Wang et al., KlingAI Research / Kuaishou, 2026
- [raw stub](/raw/papers/tide-fsdp-layout-aware-collectives.md)
