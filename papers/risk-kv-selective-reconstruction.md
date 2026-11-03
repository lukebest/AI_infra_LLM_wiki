---
type: Paper
title: "RISK-KV: Quality-Aware Selective KV Cache Reconstruction"
description: "哈工大 — 跨层 ridge 重建目标层 KV；省略 18.2%–33.3% 历史 KV，困惑度变化 <0.5%；512-token 本地恢复相对 Token Replay 1.51–3.31×"
tags:
- inference
- kv-cache
- serving-system
- decode
- latency
- memory
- llm
- distributed
- gpu
created: 2026-11-03
updated: 2026-11-03
timestamp: '2026-11-03T00:00:00Z'
paper_author: [Wang Yuekai]
year: 2026
venue: arXiv
arxiv: '2610.29544'
sources:
  - raw/papers/RISK-KV_Selective_KV_Reconstruction_2026.pdf
  - raw/papers/risk-kv-selective-reconstruction.md
---

# RISK-KV：质量感知的选择性历史 KV 重建

## 一句话结论
分布式推理里迁移/恢复请求若整份搬历史 KV 开销大、整段 Token Replay 又偏慢。RISK-KV 用**目标层两侧精确 KV 作锚点 + 跨层 ridge 回归**预测缺失层的 attention 投影输入，再**折叠原模型 KV 投影矩阵**；以 **NLL 增量**度量重建风险，配合拓扑搜索与质量门控。代表性配置可省略 **18.2%–33.3%** 历史 KV，困惑度变化 **<0.5%**；512-token 本地恢复相对全量 Token Replay **1.51–3.31×**。

## 动机
- 分布式与边缘场景下，请求迁移与中断恢复依赖历史 KV；整份保留/传输代价高，丢弃后重放前缀又增加恢复时延。
- 仅用数值重建误差或层位置排序，未必反映对语言模型预测的真实损伤；多层联合重建的风险也不是单层风险的简单相加。

## 方案
1. **跨层锚点重建**：在 GQA Transformer 中，保留目标层两侧的精确历史 KV；轻量 ridge 回归预测目标层归一化 attention 输入，再用冻结的 K/V 投影生成缺失 cache。
2. **仿射折叠**：预测映射与 KV 投影可代数折叠，在线阶段直接从锚点状态生成重建 KV，减少额外参数与中间表示。
3. **功能风险 + 拓扑搜索**：以 teacher-forced 下的均值 NLL 变化为风险；先测各组独立风险再沿排序做联合配置搜索（G 组约评 2G 配置），bootstrap 质量门控卡住质量预算。
4. **评测模型**：Qwen2.5-0.5B/1.5B-Instruct、TinyLlama-1.1B-Chat-v1.0；本地恢复实验用 512-token 历史。

## 效果（论文数字）
| 指标 | 结果 |
|---|---|
| 省略历史 KV 比例（代表性恢复配置） | **18.2%–33.3%** |
| 相对全精确 KV 的困惑度变化 | **<0.5%** |
| 本地请求恢复（512-token 历史）vs 全量 Token Replay | **1.51–3.31×** |

## 与 wiki 的关系
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md) — 服务侧 KV 管理；RISK-KV 补「可省略层的重建」而非页表分配
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 迁移/恢复场景与 PD 解耦下的状态搬运成本
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — 历史 KV 存储与重算之间的带宽/计算折中
- [UlaCache](/papers/ulacache-unified-logical-sparse-kv-serving.md) — 同属历史 KV 可达性优化，侧重稀疏选择的逻辑地址；RISK-KV 侧重跨层重建

## 开放问题
- 时延实验尚未覆盖真实无线跨节点迁移；后续 decode 仍可能物化完整 KV。
- 质量门控偏保守时可减少预算违规，同时会牺牲部分 cache 节省；跨更大模型族的风险校准未系统报告。

# Citations
- [arXiv:2610.29544](https://arxiv.org/abs/2610.29544) — Wang Yuekai, HIT, 2026
- [raw stub](/raw/papers/risk-kv-selective-reconstruction.md)
