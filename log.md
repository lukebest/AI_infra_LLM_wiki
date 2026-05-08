# Wiki Log

> 按时间顺序记录所有 wiki 操作。仅追加。
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-16] create | Wiki initialized
- Domain: AI 基础设施（scale-up 网络、加速器架构、确定性执行、推理系统）
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-16] ingest | NVIDIA Groq 3 LPX Blog Article
- Source: raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- Created: entities/nvidia-groq-3-lpx.md, entities/nvidia-vera-rubin-nvl72.md, entities/cerebras-wse.md, concepts/deterministic-execution.md, concepts/lpu-architecture.md, concepts/heterogeneous-inference.md
## [2026-04-16] ingest | MegaScale-Infer + 3 analyses
- Ingest: papers/megascale-infer-2504.02263.md
- Created: analyses/wse-nom-contradiction-analysis.md (矛盾论六步)
- Created: analyses/cerebras-wse-vs-groq-network-comparison.md (全面对比)
- Updated: index.md (10 pages total)
- 使用《矛盾论》六步框架系统性分析 WSE Network-on-Wafer
- Created: analyses/wse-nom-contradiction-analysis.md
- 主要矛盾：物理均匀性 vs 通信异构性（通信异构性是主要方面）
- 关键洞察：color routing 是调和性缓解，非根本解决

## [2026-04-17] ingest | MegaScale-Infer 概念提取
- Created: concepts/disaggregated-inference.md, concepts/m2n-communication.md
- Updated: papers/megascale-infer-2504.02263.md (添加交叉引用)
- Updated: index.md (8 pages total)
## [2026-04-20] ingest | 信息论视角下的 AI Agent 价值模型
- Source: raw/papers/information-theory-ai-agents-2026-04.md
- Created: concepts/information-theoretic-value-model.md
- Updated: index.md (9 pages total)
- Topic: 互信息 I(S;K) 作为 Agent 价值的核心度量，有效性条件 I(S;K)/H(S) > 0.5 (α=2)，悖论区间，工程策略

## [2026-04-17] ingest | AI Tools Weekly Report (manual run)
- Report: notes/projects/ai-tools-weekly-2026-04-17.md
- Email sent: liuyingxyzabc@live.com (Foxmail SMTP, fixed From address)
- Topics: OpenClaw 2026.4.12, Cursor 3, Windsurf/Cognition, Claude Code rebuild, Opus 4.7

## [2026-04-28] ingest | DeepSeek-V4 Technical Report
- Source: DeepSeek_V4 PDF (54 pages)
- Files created:
  - entities/deepseek-v4.md — Model entity page
  - concepts/csa-hca.md — Hybrid attention architecture
  - concepts/mhc.md — Manifold-Constrained Hyper-Connections
  - concepts/muon-optimizer.md — Muon optimizer with Hybrid Newton-Schulz
  - concepts/fp4-qat.md — FP4 Quantization-Aware Training
  - concepts/megamoe-kernel.md — Expert Parallelism communication-computation overlap
  - concepts/tilelang.md — TileLang DSL for kernel development
  - concepts/dsec-sandbox.md — DSec sandbox platform
  - summaries/deepseek-v4.md — Paper summary with wiki cross-links
- Updated: index.md (22 pages total)
- Note: Merged from workspace wiki into ~/wiki/

## [2026-05-08] ingest | SemiAnalysis GTC 2026 – The Inference Kingdom Expands
- Source: raw/articles/GTC 2026 – The Inference Kingdom Expands.md
- Topics: LP30/LP35/LP40 路线图, LPX rack 架构 (FPGA Fabric Expansion Logic), C2C 三级网络拓扑, AFD (Attention FFN Disaggregation), Speculative Decoding on LPU, NVIDIA CPO roadmap (NVL576/NVL1152), Kyber rack 更新 (NVL144/NVL288), Vera ETL256, CMX/STX
- Created:
  - entities/kyber-rack.md — Kyber rack 架构 (144 GPU/rack, NVLink 7, midplane, NVL288/NVL1152)
  - concepts/nvidia-cpo-roadmap.md — CPO 路线图 (Rubin→Rubin Ultra→Feynman)
  - concepts/cmx-stx.md — CMX/STX 推理存储平台 (Tier G3.5, BF-4 DPU)
  - entities/vera-etl256.md — 256 CPU 独立 rack
- Updated:
  - entities/nvidia-groq-3-lpx.md — LP30 规格, LPX rack, C2C 网络拓扑, AFD, speculative decoding
  - concepts/lpu-architecture.md — LPU 世代对比 (Gen1-Gen4), slice 架构, SRAM 权衡
  - concepts/heterogeneous-inference.md — AFD 两种模式 (AFD + speculative decoding)
  - concepts/disaggregated-inference.md — NVIDIA LPX 产品化 AFD
  - entities/nvidia-vera-rubin-nvl72.md — NVL 系统谱系, Kyber 更新
  - index.md (27 pages total)

## [2026-05-08] ingest | 浅谈交换原理（1）——概述
- Source: raw/articles/浅谈交换原理（1）——概述.md
- Created:
  - concepts/switching-principles.md — 交换原理基础（电路交换/分组交换，三对基本概念，交换系统结构）
- Updated: index.md (28 pages total)
- Note: 基础概念文章，单来源，创建一个综合性 concept 页面。关联 deterministic execution、scale-up fabric 设计选择。

## [2026-05-08] ingest | 浅谈交换原理（2）——交换单元
- Source: raw/articles/浅谈交换原理（2）——交换单元.md
- Created:
  - concepts/switching-elements.md — 交换单元（空分S接线器/时分T接线器，开关阵列/共享存储器/共享总线，性能指标）
- Updated: index.md (29 pages total)
- Note: 交换原理系列第2篇。空分交换 ↔ NVLink crossbar，时分交换 ↔ 共享总线，集中型/扩散型 ↔ disaggregated inference M:N 模式。

## [2026-05-08] ingest | 浅谈交换原理（3）——交换网络
- Source: raw/articles/浅谈交换原理（3）——交换网络.md
- Created:
  - concepts/switching-networks.md — 交换网络（单级/多级，阻塞/无阻塞，CLOS 三级网络 (m,n,r)，TST 网络，Banyan 网络）
- Updated: index.md (30 pages total)
- Note: 交换原理系列第3篇。CLOS 是理解 scale-up fabric 多级交换的基础（NVLink switch ≈ CLOS），TST 对应时分+空分组合（C2C 确定性调度）。

## [2026-05-08] ingest | CASSINI (arXiv:2308.00852)
- Source: raw/papers/cassini-network-aware-scheduling-2308.00852.pdf
- Created:
  - entities/cassini.md — Network-aware ML 集群调度器（几何抽象、统一圆、兼容性评分、Affinity 图、time-shift 交错）
- Updated: index.md (31 pages total)
- Key: 利用 DNN 训练周期性通信模式，通过 time-shift 交错不同 job 的 Up/Down 相位。vs Themis 1.5× avg / 2.2× tail，vs Pollux 1.6× avg / 2.5× tail。ECN 标记降低 33×。
