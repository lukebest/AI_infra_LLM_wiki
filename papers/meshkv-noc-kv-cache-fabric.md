---
type: Paper
title: "MeshKV: NoC KV Cache Fabric for Tiled Decode"
description: UCLA/Columbia — 片上 KV 当 NoC 流量；FPGA 8×8 互连流量最高 −58%、KV 利用率 2.1×、多流吞吐 1.9×
tags:
- noc
- mesh
- kv-cache
- llm
- inference
- decode
- accelerator
- interconnect
- architecture
- sram
- memory-bandwidth
timestamp: '2026-09-21T00:00:00Z'
created: 2026-09-21
updated: 2026-09-21
sources:
- raw/papers/MeshKV_NoC_KV_Cache_Fabric_2026.pdf
- raw/papers/meshkv-noc-kv-cache-fabric.md
---

# MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators

**Authors:** Dong Liu*, Yanxuan Yu*（* equal contribution）
**Affiliation:** University of California, Los Angeles; Columbia University
**arXiv:** [2609.19207](https://arxiv.org/abs/2609.19207)（2026-09-16，cs.AR）
**PDF:** [arXiv PDF](https://arxiv.org/pdf/2609.19207)

相对压缩/驱逐（KIVI、KVQuant、H2O）与 DRAM/CXL 放置（PagedAttention、FlexGen、CXL-SpecKV），MeshKV 不先减字节，而是把**驻留 SRAM 上的 KV 块**改成片上 NoC 上的分组流，专治瓦片加速器 decode 的 gather 热点。与 [Budgeted Express-Mesh](/papers/budgeted-express-mesh-noc.md) 改拓扑链路不同，本文改的是 **KV 流量类与多播路由**。

## 动机

- Prefill 可摊销 tile 跳数；decode 每步用一行 query（\(d_h\approx128\)）去 gather 不断增长的 KV slab。
- 集中式注入把长上下文 KV 压在同一条 bisection：论文 Fig.1 在 T=32K、LLaMA-2-7B、B=1 下，CENT 约 **41%** 链路周期花在背压上。
- FP16 LLaMA-2-7B 在 T=32 768 时 KV 约 **16 GiB**（\(2 L H d_h T\)），每步几乎通读。

## 方案

1. **TaKV（仿射条带）**：home \(\pi(\ell,s)=(\ell \bmod W,\ (a\cdot\ell+s)\bmod H)\)，一层一周期占位交换，摊平热点。
2. **Mare（多播 + 去重）**：XYM 生成树；16-entry exact tag + 256-bit bloom（\(W_b=96\)）抑制重复；VN0=单播 PART（XY），VN1=KV_FETCH/KV_DATA 多播（Turn Model 限制转弯）。
3. **Pad**：段级预取 / tile 乘 / FlashAttention-2 在线 softmax，FIFO 深度 48 覆盖 RTT；\(W_{coal}=12\) 周期合并约 **78%** 的 head 请求。
4. **实现**：Alveo U280 **8×8**，512-bit wormhole，每 tile 四 bank KV SRAM + \(d_h=128\) 脉动 PE；对照 CENT / SHARED / TaKV-only / 完整 MeshKV。

## 效果（仅论文数字）

| 指标 | 数字 |
|------|------|
| 互连流量 vs CENT（T=32K,B=1） | LLaMA **0.42×**（−58%）；Mistral **0.40×** |
| 二分 KV 利用率（LLaMA T=32K） | MeshKV **61%** vs SHARED **29%**（约 **2.1×**）；T=8K 为 71% vs 38% |
| Decode 吞吐 vs CENT（T=32K LLaMA） | B=1 **1.35×**；B=8 **1.90×** |
| 链路能量 / 每 token 净能量 vs CENT | **−48%** / **−17%**（活动估计；SRAM 能量 **+7%**） |
| Ablation（B=8，相对完整） | −Mare 吞吐 **0.62×**、流量 **1.55×**；−PAD **0.78×**；−bloom **0.82×** |
| U280 资源（8×8，一层 attention） | LUT 47%、URAM 53%、DSP 64%（瓶颈） |

**口径：** 同平台 FPGA 硬件实测（吞吐 95% CI <3%，五次运行）；相对 DFX / FlightLLM / CXL-SpecKV **不做跨平台绝对延迟对比**。8×8 多流 **1.9×**，16×4 因多播树变长仅约 **1.4×**。

## 与 wiki 关系

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)：XY / Turn Model 在 **KV 多播** 上的落地。
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)：把 KV 瓶颈从 off-chip 挪到 **片上 bisection 背压**。
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)：流量类（KV_FETCH / KV_DATA / PART）驱动 VC 与路由分区。
- 对照 [Budgeted Express-Mesh](/papers/budgeted-express-mesh-noc.md)（加 express 边）与 [Fathom](/papers/fathom-sparse-decoding-offloaded-kv.md) / [HBFlex](/papers/hbflex-flexible-memory-hbf-llm.md)（减字节或换介质）。

## 开放问题

- 仅一层 attention datapath；完整 FFN+norm 端到端未报。
- 多播树在更大 mesh（如 16×4）收益回落；chiplet / 晶圆尺度是否仍成立未验证。
- 与软件侧量化/驱逐正交，组合增益未测。

# Related

- [Mesh and Torus Topology](/concepts/mesh-torus-topology.md)
- [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md)
- [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)
- [Budgeted Express-Mesh](/papers/budgeted-express-mesh-noc.md)
- [FlashAttention-2](/concepts/flashattention-2.md)
- [PagedAttention / vLLM](/concepts/pagedattention-vllm.md)

# Citations

[1] [arXiv:2609.19207](https://arxiv.org/pdf/2609.19207) — MeshKV PDF
[2] [raw/papers/meshkv-noc-kv-cache-fabric.md](/raw/papers/meshkv-noc-kv-cache-fabric.md) — ingest stub
