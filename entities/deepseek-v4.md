---
type: Entity
title: DeepSeek-V4
description: V4 模型系列：1.6T/284B MoE，百万 token 上下文，CSA+HCA 混合注意力
tags:
- model
- architecture
- training
- inference
- quantization
- attention
- moe
- compression
timestamp: '2026-04-28T00:00:00Z'
created: 2026-04-28
sources:
- DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf
- raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf
---

# DeepSeek-V4

## Overview
DeepSeek-V4 是 DeepSeek-AI 于 2026 年 4 月发布的预览版 LLM 系列，核心目标是**打破超长上下文的效率瓶颈**，实现百万 token 上下文的工程实用性。包含两个模型：

| | DeepSeek-V4-Flash | DeepSeek-V4-Pro |
|---|---------|--------|
| 总参数 | 284B | 1.6T |
| 激活参数 | 13B | 49B |
| 层数 | 43 | 61 |
| 隐藏维度 d | 4096 | 7168 |
| 专家数 | 1 shared + 256 routed | 1 shared + 384 routed |
| 激活专家 | 6 | 6 |
| 训练数据 | 32T tokens | 33T tokens |
| 序列长度 | 4K → 16K → 64K → **1M** | 同 |

## Key Innovation: 效率突破 (vs V3.2, 1M context)

| 指标 | V4-Pro | V4-Flash |
|------|--------|----------|
| 单 token 推理 FLOPs | **27%** of V3.2 | **10%** of V3.2 |
| KV Cache 大小 | **10%** of V3.2 | **7%** of V3.2 |

KV cache 缩到原来的 1/10 ~ 1/14。

## Architecture

继承 DeepSeek-V3 的 Transformer + MoE + MTP 框架，三大升级：

1. **Hybrid Attention**: [Csa Hca](/concepts/csa-hca.md) — 交替使用 Compressed Sparse Attention 和 Heavily Compressed Attention
2. **[Mhc](/concepts/mhc.md)** (Manifold-Constrained Hyper-Connections) — 升级残差连接
3. **[Muon Optimizer](/concepts/muon-optimizer.md)** — 替代 AdamW，更快收敛

### MoE Changes (vs V3)
- 激活函数：Sigmoid → **Sqrt(Softplus)**（计算 affinity scores）
- 前 3 层用 Hash Routing 替代 dense FFN
- 去掉路由目标节点数限制
- [Fp4 Qat](/concepts/fp4-qat.md): expert weights + indexer QK path 用 FP4 (MXFP4)

### Attention 配置

| | V4-Flash | V4-Pro |
|---|---------|--------|
| CSA m (压缩率) | 4 | 4 |
| CSA top-k | 512 | 1024 |
| HCA m' (压缩率) | 128 | 128 |
| Query heads | 64 | 128 |
| Head dim c | 512 | 512 |
| Query compression dim | 1024 | 1536 |
| Output projection groups | 8 | 16 |
| Sliding window | 128 | 128 |
| mHC expansion factor | 4 | 4 |

## Infrastructure

- [Megamoe Kernel](/concepts/megamoe-kernel.md): 单一 fused kernel 实现专家并行通信-计算重叠，1.5-1.96× 加速
- [Tilelang](/concepts/tilelang.md): DSL 用于 kernel 开发，平衡开发效率与运行时性能
- **Batch-invariant + deterministic** kernels: 用 DeepGEMM 替代 cuBLAS，端到端 bitwise 一致
- [Dsec Sandbox](/concepts/dsec-sandbox.md): 生产级沙箱平台，4 种执行基板，管理数十万并发实例
- **On-disk KV cache**: 共享前缀复用，3 种 SWA 缓存策略
- **[DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md)**：生产 serving 层 speculative decode（替代 MTP-1 单 token baseline），per-user 生成 +57–85%

## Training Stability

两个实用但理论不清的技巧：
- **Anticipatory Routing**: 用历史参数计算路由索引，仅在 loss spike 时激活
- **SwiGLU Clamping**: 线性分量 [-10, 10]，gate 上限 10

## Post-Training

两阶段范式：
1. **Specialist Training**: SFT → RL (GRPO)，每领域独立
   - Generative Reward Model (GRM) 替代标量奖励模型
   - 三种推理模式：Non-think / Think High / Think Max
2. **On-Policy Distillation (OPD)**: 全词表 logit 蒸馏，10+ 教师

其他：Interleaved Thinking（工具调用保留完整推理历史）、Quick Instruction（复用 KV cache 做辅助任务）

## Evaluation Highlights

| 维度 | V4-Pro-Max 表现 |
|------|-----------------|
| 知识 | SimpleQA 57.9（开源最强），落后 Gemini-3.1-Pro (75.6) |
| 推理 | Codeforces 3206（首次开源匹配闭源），HMMT 95.2 |
| Agent | SWE Verified 80.6，Terminal Bench 67.9 |
| 长上下文 | MRCR 1M 83.5（超越 Gemini-3.1-Pro 76.3）|
| 形式推理 | Putnam-2025 hybrid: **120/120 满分** |

## Limitations
1. 架构复杂度高（CSA + HCA + mHC + MTP + MoE + SWA），未来需精简
2. 训练稳定性技巧（Anticipatory Routing, SwiGLU Clamping）有效但理论不清
3. 缺少多模态
4. 长上下文交互延迟待优化
5. 未探索 embedding 稀疏等新维度

## Relations
- Predecessor: DeepSeek-V3
- Key technique: [Csa Hca](/concepts/csa-hca.md), [Mhc](/concepts/mhc.md), [Muon Optimizer](/concepts/muon-optimizer.md), [Fp4 Qat](/concepts/fp4-qat.md)
- Infra: [Megamoe Kernel](/concepts/megamoe-kernel.md), [Tilelang](/concepts/tilelang.md), [Dsec Sandbox](/concepts/dsec-sandbox.md)
- Serving: [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md)

# Citations

[1] [DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf](DeepSeek_V4---d45f7f3c-196b-473d-8faa-8645ce91ea2f.pdf)
