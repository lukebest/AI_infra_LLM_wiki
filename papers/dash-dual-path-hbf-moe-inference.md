---
type: Paper
title: "DASH: Dual-Path HBF for MoE LLM Inference"
description: KAIST — GPU–HBF 直连 + HBM 基座中继双路径；五模型几何均值吞吐 1.90× vs RelayOnly；代表负载 1.94× 吞吐 / 1.90× E2E
tags:
- chiplet
- interconnect
- tsv
- through-silicon-via
- hbm
- memory
- moe
- llm
- inference
- packaging
- throughput
- latency
- serving
- kv-cache
- architecture
- physical-layer
- scale-up
- storage
timestamp: '2026-08-21T00:00:00Z'
created: 2026-08-21
sources:
- raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf
- raw/papers/dash-dual-path-hbf-moe-inference.md
---

# DASH: Scalable MoE LLM Inference via High-Bandwidth Flash with Direct GPU and HBM Paths

**Authors:** Seeyeon Kim, Juhyeong Jin, Joo-Young Kim（KAIST）
**arXiv:** [2608.14333](https://arxiv.org/abs/2608.14333)（2026-08-14）
**Venue:** 未标会议。事件驱动 serving 仿真 + H100 实测算子时延，**不是硅**。
**PDF:** [raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf](raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf)

同组 [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) 做 logic-on-logic 流量隔离；本文把问题换成 **HBF 容量层如何接到 GPU**。

## 动机

调研的 MoE checkpoint 权重 **281 GB–1.5 TB**，专家权重占 **94.1–98.8%**，单份就超过 H100 80 GB HBM，还没算 KV。HBF（文引 SanDisk：每 16-die 栈目标 512 GB、1.6 TB/s 读）用 [TSV](/concepts/tsv-3d-physical-layer.md) 把 NAND die 堆在逻辑基座上。

既有组织多半把 HBF 挂在 HBM 后面（级联 Relay），GPU–HBF 直连闲着；或者只直连，丢掉中继带宽。NAND 还有两条延迟：读前 **t_R**（文中扫 1–32 μs，主实验 3 μs），编程 **t_PROG**（主实验 100 μs）。MoE 专家要等路由才知道，常规预取无效；decode KV 太碎，直接 program 会堵读。

## 方案

DASH = Direct Attachment of HBF to the GPU as main memory, plus a Separate path to HBM。

1. **三条 UCIe 3.0 路径**：GPU–HBM、GPU–HBF、HBM–HBF。每条是 4-module UCIe-A（×64 @ **64 GT/s**），原始 2.048 TB/s/向，建模可用流 **1.6 TB/s**（约 22% 余量）。规格点约 0.5–0.6 pJ/bit → 1.6 TB/s 时 **6.4–7.7 W/向**；四模块约 1.6 mm 边宽。
2. **Relay**：HBF 读经 HBM **基座 SRAM** 转到 GPU 侧链路，**不进 HBM 控制器/阵列**。HBF 基座 18 MiB SRAM/栈（16 MiB 可用，两块 8 MiB 交替）；HBM 基座 9 MiB（8 MiB 中继，两块 4 MiB）。整 expert 派给 Direct 或 Relay 之一，不把同一 expert 拆到两条路上。
3. **放置**：专家权重与 write-once prefill KV 在 HBF；QKV/输出投影在 HBM 与 HBF 复制；decode KV 先在 HBM 聚成页波再回写。HBF 内专家切块铺到多 die/plane；权重与 KV **分 erase-block**，GC 不搬权重页。
4. **Lookahead 选专家**：无专家偏置的 router 可写成 P = α(P_base + P_attn)，α 不改排序。P_base 在 attention 前就算完，P_attn 在 attention 输出一出来就算（预存 W_out diag(γ) W_r）。DeepSeek-V3 一类带偏置仍走晚选择。选专家用 FP32。
5. **写调度**：prefill KV 经 GPU–HBF 直写，与 HBM 上取 output 投影重叠；decode 小更新在 HBM 攒满页波，QKV 之后回写，与随后 attention 重叠。

对照：RelayOnly（拆掉直连）、DirectOnly（拆掉 HBF–HBM）、Compact-DASH（单对 HBM/HBF 栈）。主配置 2×512 GB HBF + 2×24 GB HBM。页面 4 KiB；16 die × 32 plane × 4 子阵列假设 → 每栈 8 MiB 页波。

仿真扩 LLMSimulator；H100 PCIe 80 GB 上 1,107 条非 router 算子校验，中位相对误差 **0.51%**，90% < **3.52%**。

## 效果（仅论文数字）

**吞吐 / E2E（固定 batch，L_in/L_out=1K/128）**

- 摘要代表负载：相对 RelayOnly 吞吐 **1.94×**、E2E **1.90×**。
- 五模型 × B∈{1,4,16,64} 几何均值：吞吐 vs RelayOnly **1.90×**、vs DirectOnly **1.84×**；E2E 降 **42.2% / 40.8%**。
- 20 组序列长度组合：吞吐 geomean **1.79× / 1.63×**；E2E 降 **40.1% / 35.6%**。
- Llama 4 Maverick 197.413 GB KV：吞吐 **1.92×**，E2E **−48.0%** vs RelayOnly。

**连续批（Qwen3-235B-A22B，1.6 TB/s/链路）**

| 负载 | DASH P90 E2E | vs RelayOnly | vs DirectOnly |
|------|--------------|--------------|---------------|
| 50% | 20.982 s | −61.2% | −61.0% |
| 75% | 28.847 s | **−53.5%** | **−53.3%** |
| 90% | 31.859 s | −50.5% | −50.4% |

75% 时 P90 TPOT 208.5 ms（相对基线约 −53.9% / −53.8%）。Mixed 相对 Serial 把 DASH 峰值吞吐再抬 10.3%（基线 12.6%）；DASH 仍比单路径高 **34.1%–37.1%**。

**Lookahead（B=1, 4K/128）**

- t_R=3 μs：Qwen3 / DeepSeek-V2 E2E **−3.33% / −1.99%**，TPOT **−3.86% / −2.45%**。
- t_R=32 μs：E2E **−9.50% / −8.69%**，TPOT **−10.88% / −10.53%**。

**其它**

- vs CPU offload / Hybrid oracle：Hybrid 仍比 DASH 慢 **8.22–12.32×**（Qwen3 expert 层，Xeon 8452Y）。
- t_PROG 扫到 500 μs 仍能藏完；5 ms 才在全程加上 19.94 s 暴露 stall。
- 容量/成本参数式：相对 4×24 GB HBM，G(r,δ)=44.67/(2+2r+δ)； illustr. (r,δ)=(1,0) 时 **11.17×** 标称容量/成本。不是厂商报价。
- 耐久投影（Llama 4 Maverick 写压、SLC 100k P/E、A_W=1, u=1）：连续活动 **0.645 年**。作者标明需要器件级 WAF/坏块测量。

## 与 wiki 的关系

- [DRAM and Memory System](/concepts/dram-memory-system.md) / [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — HBF 不是第三层 SSD，而是近 GPU、带 TSV 的 NAND 栈，和 HBM 并列
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — HBF 栈用 TSV；GPU 侧传输是 UCIe 不是垂直逻辑 NoC
- [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md) / [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md) — 同属封装内 C2C/UCIe；本文把链路预算用在 **HBM↔HBF↔GPU** 双路径，而不是 XPU 集体
- [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md) — 同 KAIST 组；3DLS 隔离 KVT/AR，DASH 隔离 Direct/Relay 专家投递
- [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md) — 驻留专家用 ReRAM 带宽密度；DASH 用 HBF 容量 + 双路径带宽
- [Disaggregated Inference](/concepts/disaggregated-inference.md) — 不拆 Attn/FFN 池，拆的是 **专家权重投递路径**
- [PRESERVE](/papers/preserve-prefetch-weights-kv-cache.md) — HBM→L2 prefetch；DASH 是 HBF→GPU 的 t_R 隐藏与 KV 回写

## 开放问题

1. 公开 HBF 规格不全：子阵列并行、价格、封装成本都是假设/参数式。
2. 无硅；GPU 时延来自 H100 算子 profile。
3. DeepSeek-V3 带偏置 router 享受不到 lookahead。
4. 耐久 0.645 年是逻辑写入投影，不是现场老化。

# Citations

[1] [raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf](raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf) — Kim, Jin, Kim, arXiv:2608.14333
[2] [raw/papers/dash-dual-path-hbf-moe-inference.md](raw/papers/dash-dual-path-hbf-moe-inference.md) — 结构化摘录
