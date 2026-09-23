---
type: Raw Source
title: "SPECTRA: Adaptive Execution of Speculative Decoding on a Runtime-Reconfigurable Tiled Architecture"
description: "Columbia — 运行时可重构瓦片架构跑 speculative decoding；FPGA 20-tile；tile 级最高 2.09×、系统级再 +1.25×。"
timestamp: '2026-09-23T00:00:00Z'
source_url: https://arxiv.org/abs/2609.24847
arxiv: '2609.24847'
ingested: 2026-09-23
sha256: 1f4e9a13e17fb0ea1cde18e611acebed452741cdcd8186346592907528755bd1
---

# SPECTRA: Speculative Decoding on Reconfigurable Tiled Architecture

**Authors:** Gabriele Tombesi, William Baisi, Je Yang, Elisavet Lydia Alvanaki, Kevin Lee, Michael Lippe, Biruk Seyoum, Luca P. Carloni  
**Affiliation:** Columbia University  
**PDF:** [SPECTRA_Speculative_Decoding_Reconfigurable_Tiled_2026.pdf](SPECTRA_Speculative_Decoding_Reconfigurable_Tiled_2026.pdf)  
**arXiv:** [2609.24847](https://arxiv.org/abs/2609.24847)（2026-09-21，cs.AR/cs.AI/cs.DC）

## 问题

Speculative decoding 的 verification 落在 GEMV decode 与 GEMM prefill 之间的中间算术强度区；固定 datapath 难以同时吃满 draft / verify / prefill。

## 方法要点

- 每 tile 内 compute engine 在 **systolic（GEMM）** 与 **vector-lane（GEMV）** 间切换。
- 跨 tile 按 kernel 选择 tile 数、切分轴与通信模式；mapping 由 FPGA 成本模型驱动。
- proFPGA UltraScale+ XCVU19P 上 **20-tile** 原型；含 NoC、CVA6 RISC-V 控制核。

## 摘录数字（仅论文给出）

- 评测对：Pythia-70M→160M、SmolLM2-135M→360M、GPT2-124M→774M。
- Tile 级可重构相对 systolic-only：**1.42× / 2.09× / 1.16×**；相对 vector-only：**3.80× / 5.97× / 8.02×**。
- 系统级 mixed 映射相对最佳固定映射：**1.14× / 1.25× / 1.05×**（摘要概括为再 +**1.25×**）。

**Working page:** [SPECTRA](/papers/spectra-speculative-decoding-tiled.md)
