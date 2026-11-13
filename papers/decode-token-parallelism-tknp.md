---
type: Paper
title: "Decode Token Parallelism: Memory-Efficient Distributed Attention Parallelism for Scalable LLM Decoding"
description: "NVIDIA / 德州农工 — TKNP 把权重放置与注意力所有权拆开；vLLM 上 Llama 3.1 405B / Nemotron-4 340B，decode 池最多 64×H100，完成吞吐相对 DCP 最高 1.7×、相对 DP 最高 2.06×"
tags:
- decode
- attention
- parallelism
- kv-cache
- disaggregated-inference
- serving
- serving-system
- inference
- nvlink
- throughput
- latency
- nvidia
- prefill
- context-parallelism
created: 2026-11-13
updated: 2026-11-13
timestamp: '2026-11-13T00:00:00Z'
paper_author: [Susav Shrestha, Brad Settlemyer, Narasimha Reddy]
year: 2026
venue: arXiv preprint
arxiv: '2611.13293'
sources:
  - raw/papers/Decode_Token_Parallelism_TKNP_2026.pdf
  - raw/papers/decode-token-parallelism-tknp.md
---

# Decode Token Parallelism：按请求做跨节点注意力

## 一句话结论
NVIDIA 与德州农工的 **TKNP** 观察 decode 里稠密层与注意力的扩展方式不同：MLP / 投影可以在单一 NVLink 域内摊销读权重，注意力则随每条在途请求的 KV 增长。它把一份模型权重按均衡层块放在 decode 池各节点上，持有当前块的节点用节点内张量并行算完整批次的投影与 MLP，每个节点只为自己拥有的请求在本地 KV 上做注意力。实现于 vLLM，在 Llama 3.1 405B 与 Nemotron-4 340B、最多 64 张 H100 的 decode 池上，长上下文高并发的完成吞吐相对 DCP 最高 **1.7×**，相对数据并行最高 **2.06×**。

## 动机
数据并行复制权重，挤占 KV；张量并行把注意力扩展停在 KV head 数，并把稠密集体推到跨节点；decode 上下文并行（DCP）按序列切分以恢复容量，但要跨节点聚合部分注意力。Fig 1 在 Llama 3.1 405B、八张 H100（TP8）、32K 上下文上显示：batch 128 时注意力约占单层 decode 分项延迟合计的 **70%**，MLP 与投影相对平稳。

## 方案
1. **权重放置与注意力所有权分离**：decode 池里只放一份权重，按均衡层块分布。轮到某块时，持有该块的节点成为 active root，在节点内 TP 上为整批做 QKV / 输出投影与 MLP；所有节点（含 root）为各自请求做本地注意力。跨节点只走当前 token 的激活，稠密 all-reduce 留在 NVLink 内，注意力无需合并部分结果。KV 既不迁移也不复制。
2. **双 active-root 微批**（可选，面向 8 节点及以上）：每个节点存两块（约 2/N 的权重），两个 root 交替把注意力叠在对方的稠密计算空隙上。
3. **平台**（§5.1）：Prefill–decode 解耦；两台 prefill 节点固定为 TP8×DP2，decode 池为 4 或 8 节点。每节点 8×80 GB H100、第四代 NVLink、双路 Sapphire Rapids、8×400 Gb/s InfiniBand。Llama 3.1 405B 与 Nemotron-4 340B；FP8（部分参数留 BF16），BF16 KV；vLLM 0.19.0、FlashAttention-3、PyTorch 2.9.1、CUDA 12.9、NCCL 2.27.5。对照在匹配的 decode GPU 数下：DP（N 组独立 TP8）、跨全部 GPU 的 TP、DCP（TP8N+DCPN，vLLM 的 DCP 复用 TP 组）、PP（每阶段 TP8）。完成吞吐计入准入、多波次与收尾。贪心解码下 TKNP 与 DP 输出 token 一致。关闭跨请求前缀共享。Nemotron 在原窗口之外使用线性 RoPE 缩放，结果表征 decode 性能。

## 效果（论文数字）

| 指标 | 结果 | 出处 |
|---|---|---|
| Llama 405B，32 张 H100 decode | 大批次、长序列上完成吞吐相对 DP 最高 **2.06×**；低并发时 DP 更高 | Fig 8 / 摘要 |
| 八节点、64 张 H100、32K | 单份权重相对 DCP 最高 **1.53×**；双 root 微批把优势提到 **1.7×** | Fig 11 / §5.3 |
| 微批本身 | 吞吐最高再加 **11.1%** | §5.3 |
| 4→8 节点扩展（128 请求、32K） | 单份 TKNP **1.81×**（扩展效率 90.5%），DCP **1.37×** | §5.3 |
| Nemotron-4 340B，32 张 H100、64K | 相对 DP 最高 **1.54×**，相对 DCP **1.32×** | Fig 10 / §5.2 |
| 混合长度在线服务 | L-Eval + LongBench v1/v2（8223–126848 token，均值 32898）；1 req/s、100 ms/输出 token 的到达-完成 SLO 上，TKNP 全部达标，DP 与 DCP 低于 90% | Fig 12 / §5.4 |

Fig 9（64K）把已准入请求的 ITL 与含排队的端到端完成时间分开：高并发下 TKNP 靠更大的驻留批次降低排队与平均完成时间；DP/TP 已准入请求的 ITL 可以看起来更好，因为驻留批次更小。

## 与 wiki 的关系
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 在已解耦的 decode 池里继续拆权重放置与注意力所有权
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — decode 阶段稠密层与注意力的扩展速率不同
- [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md) — 稠密集体留在节点内 NVLink，跨节点只走当前 token 激活
- [SiliconForge / Should You Split Decode](/papers/siliconforge-should-you-split-decode.md) — 同属 decode 侧并行边界，对象是是否再拆 A/FFN
- [NanoCP](/papers/nanocp-dynamic-context-parallelism-moe.md) — 动态上下文并行对照；TKNP 用请求本地注意力替代跨节点部分结果合并

## 开放问题
- 小批次或短上下文时，通信与同步可能盖过分布式注意力的收益（§6）。
- 评测平台是 H100 + InfiniBand；更大的 NVLink 域会改变节点内 / 节点间通信的平衡。
- 与专家并行、以及把同样的层块放置用到 DCP（稠密集体留在节点内、序列仍分片）的组合，作者列为后续工作。

# Citations
- [arXiv:2611.13293](https://arxiv.org/abs/2611.13293) — Shrestha, Settlemyer, Reddy（NVIDIA / Texas A&M）
- [raw stub](/raw/papers/decode-token-parallelism-tknp.md)
- [PDF](/raw/papers/Decode_Token_Parallelism_TKNP_2026.pdf)
