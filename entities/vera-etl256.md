---
title: Vera ETL256
created: 2026-05-08
updated: 2026-05-08
type: entity
tags: [nvidia, cpu, storage, hardware, networking]
sources: [raw/articles/GTC 2026 – The Inference Kingdom Expands.md]
---

# Vera ETL256

NVIDIA 256-CPU 独立 rack，应对 AI workloads 日益增长的 CPU 需求。液冷，全 copper 互联。

## 动机
- RL（强化学习）需要 CPU 运行仿真、执行代码、验证输出
- GPU 扩展速度远超 CPU → CPU 成为瓶颈
- 解决方案：极高密度 CPU rack，copper 可达范围内消除 optical transceiver

## 架构

### 物理布局
- **32 compute tray**（上 16 + 下 16，对称排列）
- **4× 1U MGX ETL switch tray**（基于 Spectrum-6）位于中部
- 对称设计：最小化 compute tray 到 spine 的 cable 长度差异，保持全 copper reach

### 计算
- **8× Vera CPU / tray** = **256 CPU / rack**
- 液冷必须

### 网络
- **Rack 内**：Spectrum-X multiplane topology，200 Gb/s lanes
  - 4 switch 分配 lanes，全 all-to-all，单层网络
  - Rear-facing ports → copper spine（intra-rack）
- **Rack 外**：32× front-facing OSFP cage → optical 连接 POD 其余部分

### Switch Tray
- 基于 Spectrum-6
- 管理 compute tray 间全连接

## 设计哲学
与 NVL rack 一致：紧密打包使 copper 可达一切，copper 节省的成本远超额外冷却开销。

## 相关页面
- [[nvidia-vera-rubin-nvl72]] — 同平台 GPU 系统
- [[cmx-stx]] — 推理存储平台
- [[kyber-rack]] — 另一种 rack 架构
