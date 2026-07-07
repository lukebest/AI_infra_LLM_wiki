---
type: Raw Source
title: WaferLLM Large Language Model Inference at Wafer Scale
source_path: /home/luke/snap/zotero-snap/common/Zotero/storage/JNESI2NR/He 等 - 2025 - WaferLLM large language model inference at wafer scale.pdf
arxiv: '2502.04563'
ingested: 2026-07-07
sha256: b51cedb55d7e461770c11a27be62679620fa00fd72d1c2af370fed16dc7698e2
---

# WaferLLM: Large Language Model Inference at Wafer Scale

**Authors:** Congjie He, Yeqi Huang, Pei Mu (Edinburgh); Ziming Miao, Jilong Xue, Lingxiao Ma, Fan Yang (Microsoft Research)  
**PDF:** [WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf](WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf)  
**arXiv:** [2502.04563v3](https://arxiv.org/abs/2502.04563) (May 2025) | **Code:** https://github.com/MeshInfra/WaferLLM

## 问题

晶圆级加速器（Cerebras WSE-2：85 万 core、40 GB 片上 SRAM、~22 PB/s 带宽）采用 **massive-scale mesh NoC + 分布式 local memory**，与 GPU/TPU 的 **shared memory** 假设根本不同。现有 LLM 推理栈（vLLM、SGLang、Ladder 等）与 T10（GraphCore IPU 分布式编译器）无法充分利用 PLMR 硬件 → 利用率极低。

## PLMR 设备模型（pronounced "Plummer"）

| 字母 | 属性 | WSE-2 含义 |
|------|------|------------|
| **P** | Massive Parallelism | 百万级 core，需极细粒度 partition/replicate |
| **L** | non-uniform Latency | mesh 远端访问延迟可达本地 **~1000×**；α（per-hop）< β（per-routing 软件转发） |
| **M** | constrained local Memory | 每 core ~48 KB SRAM；须 O(1/N²) 分块 |
| **R** | limited Routing | WSE-2 每 core **5-bit 地址码 → ≤25 条路由路径** |

## 系统贡献

1. **Wafer-scale LLM parallelism**
   - **Prefill**：BLyEx 双维 partition → 百万 core GEMM；**dist-GEMM-T** 避免 mesh 上 costly transpose
   - **Decode**：BEyLx 序列维 **replicate** + dist-GEMV；prefill/decode 间 KV/权重 **NoC reshuffle**
   - **KV cache shift**：替代 GPU 式 concat，平衡各行 core 利用率（vs concat 导致末行 M/P 违反）

2. **MeshGEMM**（prefill）
   - **Cyclic shift** + **INTERLEAVE** → **two-hop** 关键路径 O(α)，O(1) 路由/core，O(1/N²) 内存
   - vs AllGather/SUMMA O[(α+β)N]；vs Cannon O(αN)

3. **MeshGEMV**（decode）
   - **K-tree allreduce** 聚合局部 GEMV；实现选 **K=2**，在 R 与 L 间折中
   - vs pipeline/ring allreduce O[(2α+β)N]

## 实现

~7k 行 CSL（parallelism + MeshGEMM/MeshGEMV）+ ~2k 行 Python（checkpoint、launch、autotune core grid）。离线 autotune 为 prefill/decode 选不同 core 规模（如 LLaMA3-8B：660×660 prefill / 360×360 decode）。

## 评测摘要（WSE-2 vs A100 7nm 同代）

| 对比 | 结果 |
|------|------|
| vs **T10** on WSE-2 | 平均 **160×** TPR（短 seq 最高 180×；长 seq 平均 36×） |
| vs **Ladder** on WSE-2 | 平均 **625×**（短 seq 最高 677×） |
| **MeshGEMM** vs SUMMA/Cannon | **2–3×** |
| **MeshGEMV** vs Cerebras demo GEMV | **4–8×**；vs **单 A100** **606×**、**16×** 能效 |
| **KV shift** vs GPU PagedAttention 可扩展性 | 最高 **~400×** token capacity |
| **E2E** vs SGLang A100 集群（NVLink+IB 最优） | **10–20×** TPR、**2.5×** 能效 |
| vs 单 A100 SGLang | **30–40×** |

模型：LLaMA3-8B、LLaMA2-13B 全模型；CodeLLaMA-34B、Qwen2-72B 子层（超 WSE-2 40 GB 容量）。

## 定位

首个 **PLMR-compliant** 晶圆级 LLM 推理系统；与 [SpaDA](/concepts/spada-programming-language.md)（通用 SDA 语言/编译）互补——WaferLLM 专注 **LLM operator + parallelism policy**。PLMR 的 **R** 约束与 WSE **24 color / ≤25 路径** 直接相关（见 [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md)、[Cerebras WSE](/entities/cerebras-wse.md)）。
