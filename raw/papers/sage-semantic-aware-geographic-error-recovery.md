---
type: Raw Source
title: "SAGE: Semantic-Aware Geographic Error Recovery for AI Data Movement"
source_url: https://arxiv.org/abs/2609.10126
arxiv: '2609.10126'
ingested: 2026-09-14
sha256: 3738e7a3a2b2c5dec92ef879a5f4ac2b6d495c281b64ee4895dc1938dd9c5eed
---

# SAGE: Semantic-Aware Geographic Error Recovery for AI Data Movement

**Authors:** Patrick S. Y. Hung, Zitong Wang, Zekai Zhang, Yu Hin Chan, Shengzhe Lyu, Ray C.C. Cheung
**Affiliation:** City University of Hong Kong
**PDF:** [SAGE_Semantic_Aware_Geographic_Error_Recovery_AI_2026.pdf](SAGE_Semantic_Aware_Geographic_Error_Recovery_AI_2026.pdf)
**arXiv:** [2609.10126](https://arxiv.org/abs/2609.10126)（2026-09-09，cs.AR）

## 问题

AI 互连常对包做统一保护与重放，但 BF16 类数值中指数高位翻转与尾数低位翻转后果天差地别。

## 方法要点

- **语义合同**：Class-H（灾难）/ Class-M / Class-L；是否重放与重放起点（地理检查点）解耦。
- 源端区域表按故障地理自适应 checkpoint 间隔。
- gem5 Garnet 端点/重放协议；合成 Class-H/M checker。

## 摘录数字（仅论文给出）

- DenseNet-121/ESC-50：指数 MSB 故障使准确率跌至 **2.0%**（chance），干净对照 **83.3%**。
- vs 固定 34-hop 恢复（BER \(3\times10^{-5}\)）：平均延迟 **−28.0%**，p99.5 **−36.0%**，质量归一终端延迟 Ψ_del **−30.1%**。
- SAGE+M（也让 Class-M 触发重放）：retry DATA flit-hops/original **×2.30**，drop **7.42%→21.64%**，交付语义质量 **−8.3%**。
