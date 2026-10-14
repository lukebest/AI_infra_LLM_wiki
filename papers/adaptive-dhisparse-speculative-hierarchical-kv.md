---
type: Paper
title: "Adaptive DHiSparse: Speculative Decoding over a Load-Adaptive KV Hierarchy"
description: "Umans AI — 在 host 卸荷的分层稀疏 KV 上接入 DSpark/DFlash2 投机解码，并让 GPU 驻留历史随负载伸缩；B300、GLM-5.3 100K/C128 每块 decode GPU 793 tok/s（HiSparse 的 1.45×），同延迟约束下并发最高 4×；DeepSeek-V4.1-Flash 500K/C512 达常驻服务 1.85×"
tags:
- inference
- decode
- serving
- serving-system
- kv-cache
- speculative-decoding
- sparse
- attention
- memory
- throughput
- deepseek
- nvidia
created: 2026-10-14
updated: 2026-10-14
timestamp: '2026-10-14T00:00:00Z'
paper_author: [Naji Alazhar, Wassel Alazhar]
year: 2026
arxiv: '2610.13708'
venue: arXiv preprint (cs.AI / cs.CL / cs.DC / cs.LG)
sources:
  - raw/papers/Adaptive_DHiSparse_Speculative_Hierarchical_KV_2026.pdf
  - raw/papers/adaptive-dhisparse-speculative-hierarchical-kv.md
---

# Adaptive DHiSparse：分层稀疏 KV 上的投机解码与按负载伸缩的驻留

## 一句话结论
稀疏注意力让每个 query 只读少量历史，但常规服务仍把全部历史留在 HBM，长上下文下先被 KV 容量卡住准入。HiSparse 把历史放 host、只取被选中的行，但缓存预算固定、也不支持草稿模型投机。Adaptive DHiSparse 补上这两点：低负载时用空闲 HBM 多留历史，高负载时让出；验证期多个 query 共享缺失行的取回。

## 动机（论文数字）
- 固定预算的两难：预算小能多接会话，但 HBM 空闲时也在白白回读 host；预算大少回读，却在压力下占准入容量。
- 卸荷之后 GPU 显存仍是瓶颈：GLM-5.3 100K 每会话需 **0.432 GiB**（带 DFlash2 为 **0.492 GiB**），投机再加每卡 **6.6 GiB** 固定分配；208 个会话只用了 4.3 TB host 中的 **0.93 TB**。

## 方案
| 部件 | 做法 |
|---|---|
| 负载自适应驻留 | 保护必需工作集；HBM 有余时保留更多历史；压力来时释放；其余经精确融合取回恢复 |
| 驻留感知解析 | 区分 KV 来源，验证期多个 query 共享缺失行取回 |
| 有界投机存储 | 草稿 KV 用窗口环形缓冲，验证 staging 跨层组复用；每 GLM 会话只多 **0.060 GiB** 必需状态 |
| 保留原算法 | DSpark/DFlash2 的提议与接受规则不变 |

- 实现在 SGLang；硬件 8×B300 节点（每卡 269 GiB HBM，4.3 TB host 内存经 PCIe）。

## 效果（仅论文数字）
- GLM-5.3 + DFlash2，100K、C128：每块 decode GPU **793 tok/s**，为 HiSparse **1.45×**、非投机自适应 **1.27×**；平均 TTFT 降 **2.1×**，TPOT 降 **29%**。拆解：自适应驻留与拷贝并行度贡献 **1.14×**（prefill→decode 交接 10.4 s→4.0 s），投机再贡献 **1.27×**（一轮验 4 个 query、产出 2.88 token、耗时为非投机步的 2.2×）。
- 同样延迟上限下，并发最高 **4×**、输出 **2.3–3.7×**（取决于 TPOT 上限）。
- DeepSeek-V4.1-Flash + DSpark，500K、C512：为常驻服务 **1.85×**。
- 负载阶跃实验：低负载时从 host 取回的选中行比例 **14.2%→1.4%**。
- 模型设计含义：DeepSeek-V4.1-Flash 每 token 从 host 拉的字节约为 GLM-5.3 的 **1/80**（k 小 4×、选择层少 2.6×、行宽约一半），因而对缓存预算不敏感。

## 与 wiki 的关系
- [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md) — 第一次把 DSpark/DFlash2 搬到 host 卸荷的稀疏 KV 层次上
- [SpecStream](/papers/specstream-resource-efficient-speculative-decoding.md) — 同样把投机与 CPU KV 卸荷放进同一关键路径，SpecStream 卸荷已提交历史，DHiSparse 卸荷稀疏选择的历史
- [Fathom](/papers/fathom-sparse-decoding-offloaded-kv.md)、[Janus](/papers/janus-agentic-ssd-sparse-kv.md) — 稀疏注意力 × 卸荷 KV（host / SSD）的同族工作
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — KV 容量决定准入，这里把 HBM 预算做成随负载变化

## 局限与开放问题
- 评测只覆盖 GLM-5.3、DeepSeek-V4.1-Flash 两款模型和 B300 平台；PCIe host 链路以外（如 NVLink-C2C、CXL）的收益曲线未测。
- C256 时分配等待占 TTFT **85–97%**，作者认为下一步容量来自更小的每会话必需状态和更快回收。
- 两位作者来自同一初创公司，缺少第三方复现（本页判断）。

# Citations
- Alazhar & Alazhar, "Adaptive DHiSparse: Speculative Decoding over a Load-Adaptive KV Hierarchy", arXiv:2610.13708, 2026. [raw](/raw/papers/adaptive-dhisparse-speculative-hierarchical-kv.md) · [PDF](/raw/papers/Adaptive_DHiSparse_Speculative_Hierarchical_KV_2026.pdf)
