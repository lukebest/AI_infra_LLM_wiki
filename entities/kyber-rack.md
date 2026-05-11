---
title: Kyber Rack
created: 2026-05-08
updated: 2026-05-08
type: entity
tags: [nvidia, scale-up, fabric, rack, architecture, cpo]
sources: [raw/articles/GTC 2026 – The Inference Kingdom Expands.md]
---

# Kyber Rack

NVIDIA 第二种 rack 架构（继 Oberon 之后），首次以原型亮相于 GTC 2025，GTC 2026 公布更新设计。支持 NVL144、NVL288、NVL1152 等更大规模 scale-up 域。

## Rubin Ultra NVL144 架构

### Compute Blade
- **4× Rubin Ultra GPU + 2× Vera CPU** / blade（相比 GTC 2025 原型的 2 GPU + 2 CPU 密度翻倍）
- **36 compute blades**（2 canisters × 18 blades）= **144 GPU / rack**
- 液冷

### Switch Blade
- **6× NVLink 7 switch** / blade（高度是 GTC 2025 原型的 2 倍）
- **12 switch blades** / rack = **72 NVLink 7 switch 总计**
- 每 switch 28.8 Tbit/s uni-di（144 lanes × 200G bi-di）
- 6× 152DP connectors / blade，3 connectors 连接每个 midplane board

### Midplane 互联
- 2 块 PCB midplane（1/canister）
- GPU 全连接到 switch blade
- Copper flyover cable 连接 switch 到 connector（距离超 PCB trace 范围）
- 每 GPU 80DP connector（72 DP used × 200G bi-di = 14.4 Tbit/s uni-di scale-up 带宽）

### 生产变更
- GTC 2025 原型使用更低密度 connector（12/blade）
- 量产版预计 6/blade（152DP 高密度 connector）
- Nvidia 评估 co-packaged copper 降低损耗

## NVL288（供应链探索中，未官方发布）

- 2× NVL144 Kyber rack 并置
- Rack-to-rack copper backplane 互联
- 可能需要更高 radix NVLink switch（当前 NVLink 7 最大 144 ports × 200G）
- 或者采用 dragonfly topology + 一定 oversubscription
- 额外 20,736 DP copper cable（上界估计）

## NVL1152（Feynman 世代）

- 8× Kyber rack 互联
- **CPO 连接 rack 间**（rack 内仍 copper）
- Jensen 声称 "all CPO"，但技术博客和供应链信号显示 rack 内仍为 copper POR
- 448G SerDes 挑战（shoreline, reach, power）使得 copper-to-switch 仍为必要

## 相关页面
- [[nvidia-vera-rubin-nvl72]] — Oberon rack 架构
- [[nvidia-cpo-roadmap]] — CPO 路线图
- [[nvidia-groq-3-lpx]] — LPX rack（另一种 rack 架构）
- [[switching-networks]] — Scale-up 互联概念
