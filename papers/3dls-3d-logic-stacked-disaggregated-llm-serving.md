---
type: Paper
title: "3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving"
description: KAIST IEEE CAL 2026 — logic-on-logic 3D 把 KVT 与 decode AllReduce 物理隔离；相对共享侧向 D2D 最高 1.49× 吞吐、60.2% 更低 E2E
tags:
- 3d
- chiplet
- hybrid-bonding
- tsv
- interconnect
- disaggregated-inference
- inference
- serving-system
- kv-cache
- communication
- llm
- latency
- throughput
- architecture
timestamp: '2026-08-18T00:00:00Z'
created: 2026-08-18
sources:
- raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf
- raw/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md
---

# 3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving

**Authors:** Jaehun Lee, In-Jun Jung, Joo-Young Kim（KAIST）
**arXiv:** [2607.01617](https://arxiv.org/abs/2607.01617)
**Venue:** IEEE Computer Architecture Letters, 2026。DOI [10.1109/LCA.2026.3709108](https://doi.org/10.1109/LCA.2026.3709108)
**PDF:** [raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf](raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf)

## 中文摘要

现代 LLM serving 同时使用 prefill–decode（PD）解耦与张量并行（TP）。在常规 2D/2.5D chiplet 上，层间 KV-cache 传输（KVT）与 decode 侧 AllReduce 挤在同一条侧向 D2D 上，形成 decode 关键路径的混合流量争用。3DLS 用 logic-on-logic 三维堆叠把 prefill pool 放上层、decode pool 与侧向 D2D 放下层：KVT 走垂直互连（TSV / hybrid bonding / UCIe-3D 类），collectives 留在底层侧向 fabric。相对共享织物平面基线，最高 1.49× 吞吐、60.2% 更低端到端延迟；相对带 VC/带宽预留的优先级平面基线，仍有最高 1.17× 吞吐与 31.4% 延迟下降。论文主张：3D 的价值首先是**物理隔离两类流量**，而不只是加带宽。

## Motivation

PD 解耦把 compute-bound prefill 与 memory-bound decode 分到不同资源池；TP 则在每个 decode 层的 attention 后与 FFN 后各放一次 AllReduce。层间 KVT 与这些 AR 在 2.5D 上共享侧向链路。作者用 OPT-175B、TP=16、512 GB/s D2D 量化（仅论文数字）：

| 设置 | 累计 AR 延迟 | 平均 decode TBT |
|------|--------------|-----------------|
| 无争用，128 out token | 510 ms | 61.11 ms |
| 最高 KV 负载 (16, 16K)，128 out | 16.37 s（**32.1×**） | 184.92 ms（**3.03×**） |
| 同上，1024 out | **22.8×** AR | **2.39×** TBT |

QoS / VC / 静态带宽预留只能**重分配**干扰：优先 AR 会拖慢 KV 交接，优先 KVT 会拖慢 AR。侧向 D2D 还与 HBM 争 shoreline，不能靠无限加带宽解决。这是 [Disaggregated Inference](/concepts/disaggregated-inference.md) 在 **chiplet 封装层** 的缺口。

## Approach

1. **系统层**：上层多个 prefill pool，下层多个 decode pool + decode 侧 D2D（UCIe-like）。请求在上层 prefill，层间 KV 经垂直链路送到对齐的 decode ingress。
2. **池是逻辑分配**：2:1 / 4:1 prefill:decode 比不是“多片堆到一片”；KVT 按 shard 对齐，不是 all-to-one。
3. **封装层**：HBM 仍在 interposer / 底层。底层→顶层方向服务 prefill 的 HBM 读，顶层→底层方向送 KV。顶层多一跳垂直访存，但 **不占底层侧向 D2D**。prefill 算术强度高，可与计算重叠。
4. **对照**：Naive Planar（共享物理链路）；PM-Planar（独立 VC + 静态 KVT:AR 预留 25:75 / 50:50 / 75:25，仍共享物理链路）。iso-bandwidth：侧向与垂直都按 **512 GB/s 总双向（256 GB/s/方向）** 建模，避免把增益归因于 3D 额外带宽。
5. **平台**：Dojo D1 缩放到 16×16；decode-centric 2:1 pool；热包络一阶检查 200 W/cm²。模型 LLaMA3-8B / 70B、OPT-175B；Azure Conv（decode 主导）与 Code（prompt/KV 主导）trace。TP=4/8/16。

## Results（仅论文数字）

系统参数：峰值 **261.12 TFLOPS**，内存带宽 **3.35 TB/s**，D2D **512 GB/s**。

| 对照 | 吞吐 | E2E 延迟 |
|------|------|----------|
| vs Naive Planar | 最高 **1.49×**（Code/LLaMA3-8B）；几何均值 **1.22×** | 最高 **60.2%** 更低（Conv/OPT-175B）；几何均值 **40.6%** 更低 |
| vs PM-Planar | 最高 **1.17×**；几何均值 **1.11×** | 最高 **31.4%** 更低；几何均值 **18.2%** 更低 |

点值：Conv/OPT-175B（scale=1, PB=16, DB=64）E2E 44.99 s → 26.08 s → **17.89 s**。Code/LLaMA3-8B（scale=8, PB=1, DB=4）吞吐 24.32 → 32.92 → **36.30 req/s**。Code/LLaMA3-70B 相对 PM-Planar 的最大吞吐增益：5.55 / 5.24 → **6.15 req/s**。Conv 最优预留 25:75，Code 最优 75:25；错配可差于 Naive Planar。

## Relation to wiki

- [Disaggregated Inference](/concepts/disaggregated-inference.md) — PD 解耦从软件调度延伸到 3D 物理路径隔离
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) / [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 3DLS 是 logic-on-logic，不是 Voxel 那种 DRAM-on-logic
- [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 争用发生在 decode 步内的 AR，被层间 KVT 拉长
- [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md) — 这里是 **推理 TP AllReduce**，但集体仍在关键路径
- [Network-on-Wafer](/concepts/network-on-wafer.md) — 相关工作引用 WSC-LLM / NoW 共设计；3DLS 把隔离做在封装垂直维
- [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md) — 另一条 3D 异构：DRAM vs FeFET 分工，不是 KVT/AR 垂直隔离
- [MOCAP](/papers/mocap-wafer-scale-chunked-pipelining.md) — 晶圆级 prefill-only；3DLS 是 PD 解耦 serving
- [Voxel](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 3D AI 仿真；3DLS 强调流量隔离而非 bank 冲突
- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — 同 KAIST 组；隔离的是 HBF Direct/Relay 投递，不是垂直 KVT/AR
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — AFD 的 FFN 池驻留；3DLS 是 PD+TP 的路径隔离

## 开放问题

1. 垂直链路、键合、PHY、KV ingress、供电的面积/功耗未做完整 PPA，只有 200 W/cm² 一阶热检查。
2. 封装良率：KGD、键合筛查、垂直链路冗余只被点名为约束。
3. 在线混合 Conv+Code 时静态 KVT:AR 预留如何自适应，论文未做。
4. 与晶圆级 serving（WSC-LLM）叠加时，垂直隔离是否仍成立？

# Citations

[1] [raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf](raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf) — Lee, Jung, Kim, IEEE CAL 2026
[2] [raw/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md](raw/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 结构化摘录
