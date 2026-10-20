---
type: Paper
title: "ArchAgent: Agentic AI for Heterogeneous System Design Across Chip, Scale-Up, and Scale-Out Domains"
description: "Argonne/UIUC — LLM 规划器把系统设计拆成芯片/scale-up/scale-out 三个子问题交给专家 agent，确定性解析模型打分；1 MW 等功耗混合 AI+HPC 负载下异构设计加权几何均值 1.93×，第 18 次评估超过爬山法 100 次的 1.65×"
tags:
- agentic-ai
- ai-agent
- architecture
- chip-design
- design-space-exploration
- scale-up
- scale-out
- interconnect
- power
- llm
created: 2026-10-20
updated: 2026-10-20
timestamp: '2026-10-20T00:00:00Z'
paper_author: [Murali Emani, Kashyap R Manjusha]
year: 2026
arxiv: '2610.23724'
sources:
  - raw/papers/ArchAgent_Heterogeneous_System_Design_2026.pdf
  - raw/papers/archagent-heterogeneous-system-design.md
---

# ArchAgent：跨芯片、scale-up、scale-out 的多智能体异构系统设计

## 一句话结论
系统级设计空间（芯片类型、分区大小、每分区互连、scale-out 网络）组合爆炸，LLM 适合做「按瓶颈提方案」的规划，性能数字全部交给确定性解析模型算。这样在少量评估内就能找到比同构 GPU 更好的异构配置。

## 动机
- 计算（GPU、数据流处理器、RISC-V 加速器）、存储（HBM、GDDR、SRAM）、互连（NVLink、UALink、Infinity Fabric、InfiniBand、Slingshot、Ultra Ethernet）都在分化。
- LLM 训练受 GEMM 与 all-reduce 支配，prefill 偏算力、decode 偏访存，HPC 求解器又有 FP64 与小消息 all-reduce；没有一种芯片–网络组合在所有阶段都好。

## 方案
1. 分层多智能体：LLM 规划器把设计拆成芯片、scale-up、scale-out 三个子问题；三个专家子 agent 分别给出 roofline 推理、域大小与 α–β 推理、集体通信映射等参数级建议与批评。
2. 每个候选先过 schema 校验，再进确定性解析评估器（roofline 芯片模型 + α–β 通信模型，按 MLPerf 与厂商数据校准），返回混合负载得分、分负载性能与瓶颈归因，规划器据此迭代。
3. LLM 不产生任何性能数字，只决定下一步评估什么。

## 效果（论文数字，1 MW 设施级等功耗，含网络端口功耗）
- 最佳设计（gpt-oss-120b 规划器）混合负载加权几何均值 **1.93×**（相对同构 GPU 基线）：训练 **1.72×**、推理服务 **1.67×**、HPCG **4.76×**、AI+HPC 耦合 **2.61×**，FFT **1.37×** 是约束项。
- 搜索效率：第 **18** 次评估超过爬山法 100 次评估的终值 **1.65×**，约第 36 次达到 1.93；随机搜索需 48 次评估才超过 1.5。
- 规划器能力影响结果：gemma-4-31B-it 在 50 次评估内只到 **0.87**（低于同构基线），出现 7 个 schema 无效和 4 个不可行设计；gpt-oss-120b 为 5 个 schema 无效、0 个不可行。
- 搜索结果常把 **2–10%** 功耗预算分给专门的 decode 或求解器分区。

## 与 wiki 的关系
- [DSA Processor Design Trade-offs](/concepts/dsa-processor-design-tradeoffs.md) — agentic 设计流从 HLS/RTL 层（AHRR）上移到系统组成层
- [AHRR](/papers/ahrr-agents-hls-chip-design.md) — 同为 agent 驱动的芯片设计，层级更低
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — scale-up/scale-out 拓扑与带宽选型正是被搜索的维度
- [Prefill–Decode Divergence](/concepts/prefill-decode-divergence.md) — 小比例 decode 专用分区的收益来自两阶段瓶颈不同

## 开放问题
- 结论受解析模型保真度限制：不建模交换机级拥塞，计算/通信重叠用固定系数，未计 PD 分离中的 KV 传输。
- 晶圆级原型被近似为可组合切片，可能低估片内带宽。
- 作者计划用 ASTRA-sim 等更高保真模型复核选中设计并跑多随机种子；目前主表为单次结果。

# Citations
- Emani & Manjusha, "ArchAgent: Agentic AI for Heterogeneous System Design Across Chip, Scale-Up, and Scale-Out Domains", arXiv:2610.23724. [raw](/raw/papers/archagent-heterogeneous-system-design.md) · [PDF](/raw/papers/ArchAgent_Heterogeneous_System_Design_2026.pdf)
