---
type: Paper
title: "SAGE: Semantic-Aware Geographic Error Recovery for AI Data Movement"
description: 城大香港 — BF16 语义分级×地理检查点；Garnet 相对固定 34-hop 平均延迟 −28%、p99.5 −36%、Ψ_del −30.1%
tags:
- interconnect
- fabric
- protocol
- fec
- retransmission
- communication
- architecture
- noc
- flow-control
timestamp: '2026-09-14T00:00:00Z'
created: 2026-09-14
updated: 2026-09-14
sources:
- raw/papers/SAGE_Semantic_Aware_Geographic_Error_Recovery_AI_2026.pdf
- raw/papers/sage-semantic-aware-geographic-error-recovery.md
---

# SAGE: Semantic-Aware Geographic Error Recovery for AI Data Movement

**Authors:** Patrick S. Y. Hung, Zitong Wang, Zekai Zhang, Yu Hin Chan, Shengzhe Lyu, Ray C.C. Cheung  
**Affiliation:** City University of Hong Kong  
**arXiv:** [2609.10126](https://arxiv.org/abs/2609.10126)（2026-09-09，cs.AR）  
**Venue:** 预印本。  
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.10126)

相对 [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) 把 chiplet SerDes 的 FEC/重传建进延迟模型，SAGE 问的是：**检测到的比特错误该不该重放、从多远的检查点重放**——按数值语义而不是统一 CRC 策略。

## 动机

AI 张量在 NoC / C2C 上移动时，尾数低位翻转≈量化噪声，指数高位翻转可产生离群或非有限值并污染 reduction。文内 DenseNet-121/ESC-50：指数 MSB 故障使准确率跌至 **2.0%**（chance），干净对照 **83.3%**。统一全量重放既贵又可能不必要。

## 方案

1. **语义合同（BF16-like）**：Class-H（灾难）/ Class-M（有界）/ Class-L（精度）；先满足 Class-H 静默投递约束，再按质量归一终端延迟 \(\Psi_{\mathrm{del}}\) 排序可采纳策略。
2. **地理恢复**：源端区域表按故障地理自适应 checkpoint；Class-H 可触发受保护 NACK + 整 flit 段重放；Class-M/L 默认不触发网络重放。
3. **实现**：gem5 **Garnet** 端点与重放协议；综合流水 Class-H/M checker。

## 效果（仅论文数字）

- vs 固定 **34-hop** 恢复（基 BER \(3\times10^{-5}\)，十种子）：平均延迟 **−28.0%**，全结果 p99.5 **−36.0%**，\(\Psi_{\mathrm{del}}\) **−30.1%**（文 Table 3 叙述）。
- Wrapper 表（同 BER）：SAGE 平均延迟 **270.9** vs End-to-end **479.9** / Fixed-34 **328.1**；drop **0.0742** vs End-to-end **0.1508**。
- **SAGE+M**（Class-M 也触发重放）：retry DATA flit-hops/original **×2.30**，drop **7.42%→21.64%**，交付语义质量 **−8.3%**——说明「多触发重放」不等于更好。

## 与 wiki 概念的关系

- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md) — 在链路/传输可靠语义之上加「数值后果」策略层。
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 可靠性从「比特正确」扩展到「任务可接受」。
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — PHY/FEC 代价模型；SAGE 决定哪些错误值得付重传税。

## 开放问题

1. LLM 训练 AllReduce 梯度上 Class-H 边界与 CNN 标定是否可迁移？
2. 与 UCIe/NVLink 现网 FEC 叠加时，语义层放在 NIC 还是协议栈？
3. 在线自适应 Class 边界会不会引入新的静默投递风险？

# Related

- [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md)
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)
- [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md)
- [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md)

# Citations

[1] [arXiv PDF](https://arxiv.org/pdf/2609.10126) — Hung et al., arXiv:2609.10126  
[2] [raw/papers/sage-semantic-aware-geographic-error-recovery.md](raw/papers/sage-semantic-aware-geographic-error-recovery.md) — ingest stub
