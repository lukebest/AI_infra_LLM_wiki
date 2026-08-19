---
type: Raw Source
title: C2C-Explorer Chip-to-Chip Interconnect LLM
source_url: https://arxiv.org/abs/2608.08611
arxiv: '2608.08611'
ingested: 2026-08-19
sha256: d72754d7382b69826f3e9b89092de9d855fd85a4ed90a6fd901342b570921b4c
---

# C2C-Explorer: An Exploration Framework for Chip-to-Chip Interconnect Architectures in LLM Cloud Computing Systems

**Authors:** Jiayi Li, Di Wu, Qingxu Li, Hongxiao Zhao, Jiaqi Yang, Anjunyi Fan, Wenbin Zhang, Boqiang Wu, Shuting Liu, Shifeng Fang, Jianbo Dong, Dimin Niu, Bonan Yan
**PDF:** [C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf](C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf)
**arXiv:** [2608.08611](https://arxiv.org/abs/2608.08611)
**Venue:** 文内写 accepted DAC 2026（2026-07-26 Long Beach）
**Code:** https://github.com/Selinaee/C2C-Explorer

## 问题

LLM 训练通信可占 iteration >90%、推理 >50%。SimAI 等只给 GPU-to-GPU 流，到不了物理 C2C 路径；BookSim/Garnet 是片上，ns-3 是 scale-out。缺 scale-up 域 C2C 的硬件级仿真 + DSE。

## 方法要点

- Traffic generator：SimAI P2P → 按拓扑拆到 C2C 口 → chunk + 滑动窗口/credit → AXI burst。
- Simulator：AXI + Ethernet PHY；switch / full-mesh；端口 cycle-accurate + 交换机 event-driven 混合；最多数百 XPU。
- AB-DSE：硬件可行性剪枝（如 chunk_size ≥ 2·MAC_frame）+ LHS + GP/EI。
- 验证：1×400Gbps 交换机 + 4 FPGA C2C host，对照 ODCC ETH-X。

## 摘录数字（仅论文给出）

- 时序误差：One→All **4.39%**、All→One **2.46%**、All↔All **8.23%**。
- 混合模型相对纯 cycle：最多 **7.8×** 仿真加速（128 KB、4→512 XPU All↔All）。
- 32-XPU DeepSeek-R1-671B combine：goodput **+44.1%**、P50/P99 **-30.4%**、buffer **-98.4%**（相对最差可行点）。
- LLaMA3.1-405B inference AR：goodput **+51.7%**、延迟 **-68.7%**、buffer **-75%**。
- Qwen3-30B training AR：goodput **+50.5%**、延迟 **-64.3%**、buffer **-96.9%**。
- 可行空间 2394 → 1152；约 20 次迭代收敛。
