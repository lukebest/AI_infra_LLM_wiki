---
type: Summary
title: Understanding Silent Data Corruptions in a Large Production CPU Population
description: SOSP 2023 — 阿里云 >100 万 CPU、32 个月 SDC 实测：故障率 3.61‱；提出 Farron 优先测试 + 温控缓解
tags:
- cpu
- infrastructure
- benchmark
- optimization
timestamp: '2026-07-17T00:00:00Z'
created: 2026-07-17
sources:
- raw/papers/Silent_Data_Corruptions_Production_CPU_2023.pdf
---

# Understanding Silent Data Corruptions in a Large Production CPU Population

**SOSP 2023** | DOI [10.1145/3600006.3613149](https://doi.org/10.1145/3600006.3613149)  
Wang, Zhang, Wei（清华）；Wu, Luo（阿里云 Cloud）

首个**超大规模生产 CPU 静默数据损坏 (SDC)** 定量研究：>100 万处理器、32 个月测试，分析脆弱微架构特征、可复现性与缓解策略。

## 核心贡献

1. **Fleet 级 SDC 统计**：整体 **3.61‱** 故障率；产前测试捕获 **90%+** 故障 CPU
2. **脆弱点**：cache coherence、浮点、向量；FP 错误常限于尾数位 → 现有精度检测失效
3. **Farron**：优先测试高可复现 SDC + 温控抑制偶发 SDC；覆盖率和开销优于基线

## 关键数字

| 指标 | 值 |
|------|-----|
| 测试规模 | **>1M** CPU，**32** 个月 |
| 总体 SDC 率 | **3.61‱** |
| 产前 / 定期测试 | **3.262‱** / **0.348‱** |
| Testcases | **633** |

## 与 wiki 交叉

- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md) — CPU 计算路径可靠性
- [DRAM Memory System](/concepts/dram-memory-system.md) — 与存储/内存 corruption 对比

# Citations

[1] [raw/papers/Silent_Data_Corruptions_Production_CPU_2023.pdf](raw/papers/Silent_Data_Corruptions_Production_CPU_2023.pdf)
[2] [raw/papers/silent-data-corruptions-production-cpu.md](raw/papers/silent-data-corruptions-production-cpu.md) — 结构化摘录
