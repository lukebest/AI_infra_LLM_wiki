---
type: Paper
title: "TileDRAM: Compiler-Controlled Tile-to-DRAM Layouts for 3D DRAM GPGPUs"
description: "上海科技大学/沐曦 — CU 本地 3D DRAM（混合键合）上把 tile→DRAM 布局做成编译器可见抽象；108 个 MoE FFN 用例行冲突 75.7%→15.2%、几何均值 1.77×；六种 3D DRAM 组织 2.20×；RTX 3090 地址变换开销 0.17%"
tags:
- gpu
- 3d
- hybrid-bonding
- memory
- memory-bandwidth
- dram
- compiler
- moe
- kernel
- inference
created: 2026-10-20
updated: 2026-10-20
timestamp: '2026-10-20T00:00:00Z'
paper_author: [Guangyuan Xu, Lanxuan Zhang, Ziyang Li, Zhaoshi Li, Yajun Ha]
year: 2026
arxiv: '2610.23767'
sources:
  - raw/papers/TileDRAM_Tile_to_DRAM_Layouts_3D_DRAM_GPGPU_2026.pdf
  - raw/papers/tiledram-tile-to-dram-layouts-3d-dram-gpgpu.md
---

# TileDRAM：3D DRAM GPGPU 上由编译器决定 tile 在 DRAM 里的布局

## 一句话结论
3D DRAM 贴在计算单元正上方后，本地带宽很高，但 DRAM 仍是按 bank 和 row buffer 工作的；按惯常地址映射放置 tile，MoE FFN 的结构化 tile 访问会撞出大量行冲突。TileDRAM 把「tile 在 DRAM 地址空间里怎么排」变成编译器可选的布局，只用普通地址运算实现，不改硬件和 ISA。

## 动机
- 架构假设：DRAM 多层堆叠经 face-to-face Cu–Cu 混合键合接到逻辑 die，每个 CU 通过本地内存控制器访问自己上方的 3D DRAM 栈（CU-local），其余地址走常规层级。论文举 OpenAI Jalapeño 的切片式 HBM4 本地视图作为工业对应。
- 带宽差距：Stratum 报告栈内 **19.01–30.34 TB/s**，经 HBM 式封装接口导出每栈约 **0.8–1.2 TB/s**，封装出口窄 **16–38×**，所以要把计算放到栈旁边。
- 强度：MoE 每专家 GEMM（K=4096、N=14336、M=64–128）理想强度 **62.7–123.1 FLOP/B**，低于常规 GPU 的 GDDR/HBM 脊点 **153–295 FLOP/B**，高于本地内存脊点参考 **32.6–52.0 FLOP/B**，说明本地 3D DRAM 理论上能喂饱。
- 问题：惯常放置下请求加权行冲突率 **75.7%**，高本地带宽并不自动变成有效带宽。

## 方案
1. 把 GPU Linear Layout（F2 上的线性映射）从「张量→线程/片上资源」扩展到「tile→DRAM 放置坐标」，得到 tile-to-DRAM 布局。
2. 以 tile 访问签名（tile 形状、staging、warp、操作数属性）为特化单位：不同专家行数 M 的实例共用同一签名和布局，避免对整条 trace 搜索地址映射（整 trace 穷举约 10^14 次评估）。
3. 在固定 DRAM 地址映射下，按有序请求历史模拟 row-buffer 行为来评估候选布局。
4. 选定布局通过普通地址算术实现，无需新的重映射硬件或 ISA。

## 效果（论文数字）
- Accel-Sim + Ramulator2 全 trace 回放，108 个 MoE FFN 用例：行冲突率 **75.7% → 15.2%**，kernel 几何均值 **1.77×**。
- 六条 trace 重定向到六种 3D DRAM 组织：行冲突 **−79.2%**，几何均值 **2.20×**，编译器抽象不变。
- RTX 3090 实机上地址变换相对 identity 的几何均值开销 **0.17%**。

## 与 wiki 的关系
- [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md) — Voxel 已指出 3D 下 row-buffer 冲突让 bus 空转；TileDRAM 从编译器侧给出解法
- [DRAM and Memory System](/concepts/dram-memory-system.md) — bank/row buffer 局部性在 3D 本地栈上仍是一阶约束
- [Voxel](/papers/voxel-3d-stacked-ai-chip-llm-inference.md)、[d-Matrix Raptor 3D DRAM](/papers/hc2026-dmatrix-raptor-3d-dram.md) — 同为 3D DRAM 推理芯片路线
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 混合键合提供本地高带宽前提

## 开放问题
- 结果来自模拟（Accel-Sim/Ramulator2），实机只验证了地址变换开销，3D DRAM 本身没有硅验证。
- 只评测 MoE FFN grouped GEMM；attention/KV 读取的访问签名更不规则，是否同样受益未知。
- 一次分析一个 CU–栈对，跨 CU 访问与远端栈的交互留给常规层级。

# Citations
- Xu et al., "TileDRAM: Compiler-Controlled Tile-to-DRAM Layouts for 3D DRAM GPGPUs", arXiv:2610.23767. [raw](/raw/papers/tiledram-tile-to-dram-layouts-3d-dram-gpgpu.md) · [PDF](/raw/papers/TileDRAM_Tile_to_DRAM_Layouts_3D_DRAM_GPGPU_2026.pdf)
