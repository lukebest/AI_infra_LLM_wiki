---
type: Raw Source
title: "From Seed to BLOOM: Autonomously Growing a Better Out-of-Order Core"
source_url: https://arxiv.org/abs/2611.26517
pdf: BLOOM_MiracleGro_OOO_Core_2026.pdf
retrieved: 2026-11-25
ingested: 2026-11-25
org: University of California, Berkeley
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.26517)

Improving microprocessor performance while meeting ASIC implementation constraints like area and frequency is a complex and labor-intensive task that requires expertise across computer architecture, hardware design, and performance analysis and profiling. While large teams in industry can afford the engineering resources to target this problem across performance modeling, RTL design, and ASIC implementations, small teams of researchers and engineers cannot take on this huge engineering burden while keeping up with the pace of advancement in processor microarchitecture. Recent advancements in large language model (LLM) agents present a promising substrate to accelerate this traditionally human-intensive process.

In this work, we build and evaluate MiracleGro, an agentic AI-based system that, without human intervention, analyzes cycle-level RTL behavior and synthesis results, identifies performance bottlenecks, and translates architectural ideas into RTL implementation in a leading open-source out-of-order superscalar application core, the Berkeley Out-of-Order Machine (BOOM). Taking into account cycle-exact performance, area, and critical path, MiracleGro automatically produces improved BOOM designs that drastically increase the human-optimized BOOM’s performance on substantial workload suites such as SPEC CPU2017 with full reference inputs.

MiracleGro achieves an 85% IPC speedup and a frequency improvement of 27% in SkyWater 130nm, resulting in a 2.34x wall-clock time speedup on the full SPEC CPU2017 intspeed benchmarks (30 trillion instructions). This result demonstrates the enormous opportunity to harness frontier models to improve state-of-the-art RTL-driven platforms for implementation-grounded microarchitecture research across hardware designs.

# Excerpts / key facts

- Authors: Angela Cui, Ferran Hermida-Rivera, Jack Toubes（共同一作），Jim Fang, Chengyi Lux Zhang, Borivoje Nikolić, Christopher W. Fletcher, Sagar Karandikar。UC Berkeley。arXiv:2611.26517，提交标注 Monday 23 November 2026 公告窗。
- 循环框架为 CHIA；最终 Loop v2-p4 每轮分析并实现 4 个结构相关特性，并行跑 2 轮。最佳设计 BLOOM 出现在第 34 轮。
- 软件 RTL（GSIM）在 SPEC CPU2017 checkpoint 上 geomean IPC 2.23，SkyWater 130nm 综合频率 88.37 MHz（关键路径 11.32 ns），面积 120.94 mm²，相对基线 90.60 mm² 大约 +33%；checkpoint 墙钟 2.28×。
- FireSim 跑完整 SPEC CPU2017 intspeed 参考输入（约 30 万亿条指令；657.xz 因 FPGA 约束使用 16GB swap）：基线频率 69.85 MHz，BLOOM 88.37 MHz；geomean IPC 加速 85%（1.85×），墙钟 2.34×。
- 只优化 IPC 时，合并步 m16c0 的 IPC 相对基线 +74%，关键路径变为 2.5 倍。墙钟优化大约从第 300 小时开始。墙钟优化流单轮大约 41 小时。
- 循环外在商业 16 nm PDK 上综合：BLOOM 关键路径比基线 BOOM 大约长 14%，面积大约多 21%。该 PDK 受许可限制，无法向 agent 提供 QoR 反馈。文中给出同一基线 SoC 在现代 16 nm 上为 4.75 mm²、1.02 GHz，作为对照刻度。
