---
type: Entity
title: NVIDIA Groq 3 LPX
description: NVIDIA rack-scale 低延迟推理加速器，256 LPU，LP30 Samsung SF4，AFD，C2C 三级拓扑
tags:
- nvidia
- groq
- lpu
- accelerator
- inference
- deterministic
- scale-up
timestamp: '2026-05-08T00:00:00Z'
created: 2026-04-16
sources:
- raw/articles/nvidia-groq3-lpx-blog-2026-04.md
- raw/articles/GTC 2026 – The Inference Kingdom Expands.md
---

# NVIDIA Groq 3 LPX

Rack-scale 低延迟推理加速器，NVIDIA Vera Rubin 平台的第七颗芯片。256 个 Groq 3 LPU（LP30）互联，专注确定性、低延迟的 agentic 推理。

## Groq 收购背景

NVIDIA 以 $20B 向 Groq 授权 IP 并聘用大部分团队（法律结构上非完整收购，规避反垄断审查）。交易宣布后不到 4 个月，NVIDIA 已有系统概念集成进 Vera Rubin 推理栈。

## LP30 芯片规格

| 指标 | LP30（LPU Gen 3） | LPU Gen 1 |
|------|-------------------|-----------|
| 制程 | Samsung SF4（Austin fab，美国制造） | GF 14nm |
| SRAM | 500 MB on-chip | 230 MB |
| FP8 算力 | 1.2 PFLOPs | 750 TFLOPs (INT8) |
| 封装 | 单片 monolithic die（无需先进封装） | — |
| C2C SerDes | Groq C2C（非 NVLink） | — |

### LPU Gen 2 跳过原因
- 设计用于 Samsung SF4X（Austin fab）
- C2C SerDes 无法达到 112G → 芯片功能异常
- 从未量产

### 路线图
- **LP35**：LP30 小改版，仍 SF4，新增 NVFP4 格式支持
- **LP40**：TSMC N3P + CoWoS-R，**首次采用 NVLink 协议**（替代 Groq C2C）
  - NVIDIA 自主导入更多 IP
  - Hybrid bonded DRAM（SK Hynix 供应）扩展片上存储
  - 与 Feynman 平台深度协同设计

### 供应链优势
- SF4 不受 TSMC N3 产能限制（AI 芯片生产瓶颈）
- 无 HBM（另一产能瓶颈）
- 对 NVIDIA 而言是**增量收入和产能**，不侵蚀 TSMC/HBM 分配

## LPX Rack 系统

### Compute Tray
- **16× LP30 / tray**（belly-to-belly 封装：上 8 + 下 8）
- **2× Altera FPGA**（"Fabric Expansion Logic"）
- **1× Intel Granite Rapids host CPU**
- **1× BlueField-4** front-end module（超大规模客户可用自选 NIC）

### Fabric Expansion Logic（FPGA）角色
1. **NIC 功能**：C2C → Ethernet 协议转换，连接 Spectrum-X scale-out fabric（LPX ↔ GPU）
2. **PCIe bridge**：C2C → PCIe，LPU 通过 FPGA 连接 host CPU（LPU 无 PCIe PHY）
3. **Backplane 通信**：FPGA 间通过 backplane 互联，管理控制流和时序
4. **扩展 DRAM**：每个 FPGA 最多 256 GB DDR5 → 可用于 KV cache
5. **Speculative decoding**：256 GB DDR5 足以部署 draft model 或 MTP layer

### Front Panel
- 8× OSFP cage：cross-rack C2C
- 2× QSFP-DD（预计）：→ Spectrum-X switch（连接 GPU）

## LPU C2C 网络拓扑

Rack 总 scale-up 带宽：256 LPU × 90 lanes × 112G / 8 × 2 directions ≈ **640 TB/s**

### Intra-Tray（node 内）
- 16 LPU **all-to-all mesh**（PCB trace）
- 每 LPU 连接其他 15 个 LPU：4×100G C2C
- Belly-to-belly 减少 PCB trace 长度
- 每 LPU 1×100G → FPGA（8 LPU / FPGA）

### Inter-Node / Intra-Rack
- 每 LPU 连接其他 15 node 中各 1 个 LPU：2×100G/link
- Copper cable backplane
- FPGA 间：15×25G/50G per FPGA
- Backplane：**8,160 差分对**

### Inter-Rack
- 每 LPU 4×100G → OSFP cage → 跨 rack LPU
- Daisy chain 拓扑，100G AEC reach 内可实现

## Attention FFN Disaggregation（AFD）

LPX 的核心使用模式，源自 [Megascale Infer 2504.02263](/papers/megascale-infer-2504.02263.md) 和 Step-3：

- **Attention → GPU**（stateful，动态 KV cache）
- **FFN / MoE Expert → LPU**（stateless，确定性架构适配静态工作负载）
- Token routing：dispatch（All-to-All GPU→LPU）+ combine（反向 All-to-All）
- **Ping-pong pipeline**：micro-batch 在 GPU 和 LPU 之间乒乓传递，掩盖通信延迟

## Speculative Decoding on LPU

另一种 LPX 使用模式：
- Draft model 或 MTP layer 部署在 LPU
- 利用 LPU 低延迟加速 draft token 生成
- 主模型只需一次 warm prefill 验证 k 个 draft tokens
- 通常提升 1.5-2× output tokens per decode step
- 与 AFD 区别：draft model 需要 KV cache（数 GB 级）→ 利用 FPGA 附加的 256 GB DDR5

## 相关页面
- [Nvidia Vera Rubin Nvl72](/entities/nvidia-vera-rubin-nvl72.md) — 同平台 GPU 系统
- [Deterministic Execution](/concepts/deterministic-execution.md) — 确定性执行模型概念
- [Lpu Architecture](/concepts/lpu-architecture.md) — LPU 架构概念
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 解耦推理概念
- [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — 异构推理概念
- [Kyber Rack](/entities/kyber-rack.md) — Kyber rack 架构
- [Megascale Infer 2504.02263](/papers/megascale-infer-2504.02263.md) — AFD 技术来源

# Citations

[1] [raw/articles/nvidia-groq3-lpx-blog-2026-04.md](raw/articles/nvidia-groq3-lpx-blog-2026-04.md)
[2] [raw/articles/GTC 2026 – The Inference Kingdom Expands.md](raw/articles/GTC 2026 – The Inference Kingdom Expands.md)
