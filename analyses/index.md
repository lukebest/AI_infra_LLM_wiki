# Analysis

* [Cerebras NoW vs Groq Switched 对比](cerebras-wse-vs-groq-network-comparison.md) - WSE 2D Mesh vs Groq High-radix Switched：拓扑、规模、MoE 场景、矛盾对比
* [WaferLLM Compiler Research Gaps](waferllm-compiler-research-gaps.md) - WaferLLM (OSDI 2025) 作者本人承认但未解决的 3 个 decode 阶段瓶颈（48KB SRAM underutilization、edge cores、K=2 硬编码）→ 编译器视角的 research opportunity：MLIR PLMR-aware dialect + 3 个 pass
* [WSE NoW 矛盾论分析](wse-nom-contradiction-analysis.md) - WSE NoW 矛盾分析：均匀性 vs 异构通信（主要矛盾），附六步框架 + 解决方案
