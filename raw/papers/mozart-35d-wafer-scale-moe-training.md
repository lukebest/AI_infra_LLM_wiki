---
type: Raw Source
title: Mozart Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures
source_url: https://arxiv.org/abs/2603.07006
arxiv: '2603.07006'
ingested: 2026-08-18
sha256: efc44f68aca5ddc1a4b364fb8bd55515134606bc4a3d488e2e61db467822f3bc
---

# Mozart: Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures

**Authors:** Shuqing Luo, Han Ye, Pingzhi Li, Jiayin Qin, Jie Peng, Yang (Katie) Zhao, Yu (Kevin) Cao, Tianlong Chen (UNC Chapel Hill / University of Minnesota)
**PDF:** [Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf](Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf)
**arXiv:** [2603.07006](https://arxiv.org/abs/2603.07006)
**Code:** https://github.com/UNITES-Lab/Mozart

## 问题

MoE-LLM 的稀疏专家带来：内存局部性差、All-to-All 通信重、资源利用率低。既有 2.5D/3.5D chiplet 工作多忽略晶圆级，或用稠密均匀的粗粒度划分（如 FRED），不匹配 MoE 细粒度模块性。现代 MoE 中 routed experts 常占 **>90%** 参数。

## 方法要点

- 算法：用指令微调数据剖析专家激活/共激活先验；两阶段聚类+整数规划把常共激活专家放到同/邻 chiplet，降低 token 复制数 C_T；流式 token/expert 调度重叠 DRAM 加载与计算。
- 硬件：3.5D 晶圆级——每 compute chiplet 用 hybrid bonding 做 logic-on-SRAM 3D 堆叠；2.5D **NoP-Tree**（中心 attention、叶专家、带 in-network 聚合的 switch）；16 个 MoE chiplet / 4 组；权重在分布式 DRAM，激活在本地 SRAM。
- 28 nm 综合 + cycle-accurate 仿真；1 GHz；HBM2 256 GB/s vs SSD 15.8 GB/s 对照。

## 摘录数字（仅论文给出）

相对无优化 baseline 的端到端 post-training 加速：
- Qwen3-30B-A3B：**1.92×**
- OLMoE-1B-7B-0924：**2.37×**
- DeepSeek-MoE-16B-Base：**2.17×**

C_T（token 平均复制数）：Qwen3 8 → 5.77；OLMoE 8 → 5.63；DeepSeek 6 → 4.32。
seq=512 时 Mozart-C 相对 baseline **2.34×**；seq=128 为 **1.47×**。
硬件：Qwen3 总面积 14175 mm²、功耗 3.34 kW；OLMoE 10200 mm² / 3.55 kW；DeepSeek 11230 mm² / 3.19 kW。
