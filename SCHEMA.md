# Wiki Schema

## Domain
AI 基础设施：scale-up 网络、AI 加速器架构、确定性执行、推理系统、光学互联、LLM 模型架构、MoE、训练/推理系统、硬件-软件协同设计。

## Conventions
- 文件名：小写，连字符，无空格（如 `nvidia-groq-3-lpx.md`）
- 每个页面以 YAML frontmatter 开头
- 使用 `[[wikilinks]]` 互相链接（每页至少 2 个出站链接）
- 更新页面时更新 `updated` 日期
- 新页面必须加到 `index.md` 对应分区
- 所有操作追加到 `log.md`

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy
- 架构: accelerator, gpu, lpu, tpu, wse, chiplet, noc, interconnect, isa, pipeline, cache
- 网络: scale-up, scale-out, ocs, tdm, wdm, routing, deterministic, fabric, transport, data-link, physical-layer, link-training, serdes, fec, retransmission, flow-control, congestion-control, switch, protocol, communication
- 推理: inference, decode, prefill, latency, throughput, serving, batching, disaggregated-inference, serving-system, kv-cache, reasoning, capacity-trap, parallelism
- 编译器: compiler, scheduling, spatial-execution, deterministic-execution, programming-model
- 公司: nvidia, cerebras, groq, amd, google, lightmatter, celestial-ai, deepseek, huawei, bytedance, graphcore
- 技术: sram, hbm, photonic, cpo, optical, mesh, memory-bandwidth, memory, rack, cpu, rpc, virtualization, power
- AI系统: agentic-ai, ai-agent, moe, transformer, llm, training, attention, quantization, expert-parallelism
- 方法论: comparison, timeline, benchmark, architecture, information-theory, knowledge-management, formal-analysis
- 模型: model, architecture, benchmark, training-system, inference-system
- 技术: compression, sparse, optimization, routing, parallelism, kernel
- 系统: sandbox, storage, hardware, networking, topology, infrastructure, interconnect

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed, add it here first, then use it.

## Page Thresholds
- **创建页面**：实体/概念在 2+ 来源出现，或对单一来源是核心主题
- **更新已有页面**：新来源提及已覆盖的内容
- **不创建页面**：掠过性提及、细节、领域外内容
- **拆分页面**：超过 ~200 行
- **归档页面**：内容完全被取代

## Entity Pages
每个重要实体一页：概述、关键事实/日期、与其他实体的关系（[[wikilinks]]）、来源引用

## Concept Pages
每个概念一页：定义/解释、当前认知状态、开放问题、相关概念

## Update Policy
新信息与已有内容冲突时：
1. 检查日期——较新来源通常优先
2. 如果确实矛盾，记录两个立场及日期和来源
3. 在 frontmatter 标记：`contradictions: [page-name]`
