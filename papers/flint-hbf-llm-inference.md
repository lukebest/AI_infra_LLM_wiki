---
type: Paper
title: "FLINT: Workload-Driven HBF Substrate for LLM Inference"
description: Huawei/ETH — HBF 基座 burst-buffer + phantom-plane refresh + 只读 FTL；decode 吞吐 vs SSD/HBM-only/H3 为 1205×/2.2×/6.2×（仿真）
tags:
- hbf
- hbm
- memory
- tsv
- through-silicon-via
- chiplet
- interconnect
- physical-layer
- moe
- llm
- inference
- decode
- kv-cache
- serving
- throughput
- latency
- storage
- packaging
- architecture
- huawei
timestamp: '2026-08-28T00:00:00Z'
created: 2026-08-28
updated: 2026-08-28
sources:
- raw/papers/FLINT_HBF_LLM_Inference_2026.pdf
- raw/papers/flint-hbf-llm-inference.md
---

# FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration

**Authors:** Geraldo F. Oliveira*, Arash Tavakkol*（共一）, Xiangyu Zhu, Ahmet Caner Yüzügüler, Vamanan Arulchelvan, Lukas Cavigelli, Renzo Andri, Mohammad Sadrosadati, Jia Xinglei, Onur Mutlu, Zhou Ke, Shai Bergman, Ji Zhang
**Affiliation:** Huawei Technologies Switzerland AG / Huawei / ETH Zürich / HUST
**arXiv:** [2608.25062](https://arxiv.org/abs/2608.25062)（2026-08-25）
**Venue:** 预印本。文内未另报会议。
**PDF:** [raw/papers/FLINT_HBF_LLM_Inference_2026.pdf](raw/papers/FLINT_HBF_LLM_Inference_2026.pdf)

同主题 [DASH](/papers/dash-dual-path-hbf-moe-inference.md) 改的是 **GPU–HBF 怎么接**（三条 UCIe，Direct∥Relay）。本文改的是 **HBF 基座怎么读、怎么 refresh、怎么翻译地址**：级联仍走 HBM→HBF D2D，不新增直连。

## 动机

权重已经超过单封装 HBM。文给的例子：DeepSeek-V3 BF16 约 **1.3 TB**，Llama 3.1-405B 约 **810 GB**；Kimi K2 原生精度仍 **1.0 TB**，DeepSeek-V4-Pro **795 GB**，还没算 KV。小 batch 单卡/小节点不能靠加卡凑容量：min-fit 多卡在 bsz=1–4 把 **52–85%** 的每 token 时间花在跨封装通信+同步（层 barrier **51–79%**），算力只占 **0.1–1.9%**。容量解掉之后，oracle 在 bsz=1 用 1 封装就能过 50 ms TPOT，min-fit 却要 4–8 封装（平均超配 **4.6×**）。

既有 HBF（H3 / KAIST 幻灯）把权重放进 HBF，用 HBM 基座 SRAM LHB + 编译器层前 prefetch 藏 t_R。文里 H3 在 MoE 上浪费 **86–96%** 的 HBF 流量（专家路由和 cache 交错让静态 hint 对不上）；通道上 refresh 一块要 **54.2 ms**（t_ERASE=3 ms + 1024×50 μs），对齐计数器一次能堵 **26 s–22 min**，打散后每个 decode 步仍平均插 **0.7 s**（0.09–1.8 s）。SSD 级 FTL 的写路径对只读权重是浪费。

## 方案

封装：xPU、HBM、HBF 同 interposer。xPU↔HBM 一条 D2D，HBM↔HBF 再一条，**daisy-chain**，共用 xPU shoreline。权重预装进 HBF，KV/激活留 HBM。HBF 经 HBM 基座地址译码对加速器透明。

评测点（Table 2）：B200 级；HBM3e **192 GB**、8×1 TB/s；HBF Gen-1 SLC **4 TB**、8×(512 GB, 1 TB/s)；16 die × 32 plane；页 **4 kB**；burst **2 MB**（512 plane 同坐标）；D2D **1 TB/s/栈**。评测表 t_R/**t_PROG**/**t_ERASE** = **2 μs / 50 μs / 3 ms**。正文另写现代 SLC t_R **12 μs**——两个数不要混用。

1. **Burst-buffer controller**（HBF 基座）：LLC miss 进队列，按 (page, block) 聚成 plane-parallel burst。当前 burst 从 page buffer 泄到 cache buffer 再走 D2D 时，下一 burst 已经 sense。用 NAND 自带双缓冲，**去掉** HBM 侧 LHB 和编译器 prefetch。
2. **Phantom-plane refresh**：每 die N+1 物理 plane，1 个离线当 phantom。读出的 ECC 副本 fork 一份去 phantom 编程；migration bitmap 去重。冷页由 scrubber 补。T_rot ≥ C_plane / BW_prog = **12.5 s**，整圈约 **7 min**。热块最坏 **0.86 GB/s/栈**，16 个 phantom 编程口 **1.28 GB/s** 够用。
3. **Read-only FTL**：burst 粒度 L2P。512 GB / 2 MB → 256 K 项，约 **1 MB** SRAM + relocation/计数器，合计约 **1.8 MB/栈**。掉电当干净重装（erase+reload ≈ **6.7 min**），不保驻留权重。

基线：HBM+SSD（PCIe Gen5×4, 14 GB/s）；HBM-only min-fit 多卡；H3（两槽 LHB + 层前 hint）。轨迹来自华为 WSE workload generator（不是 Cerebras WSE）+ 实测 MMLU expert 分布。**仿真，不是硅。**

## 效果（仅论文数字）

**摘要 / 主结论**

| 对照 | decode 吞吐 | 能耗（降） |
|------|-------------|------------|
| HBM+SSD | **1,205×** | **408×** |
| HBM-only | **2.2×** | **1.1×** |
| H3（HBM+HBF 静态预取） | **6.2×** | **6.8×** |

50 ms TPOT：相对 HBM-only **3.1×** 更少 GPU 封装（最高 **8×**）。面积：HBF die **+3.1%**（多 1 plane）；基座 **3.9 mm² @ 7 nm**（CACTI 22 nm 再缩）。

**带宽（128K ctx）**

- FLINT 吃掉所取 HBF 流量 **90–97%**；MoE 有用带宽 **1.9–3.6 TB/s**，相对 H3 **4.0–14.3×**（六模型平均 **6.2×**）。
- H3 在 MoE 上重取 **80–95%**；dense Llama 3.1-405B 两边都到 **2.6 TB/s** 有用带宽（层序读一遍）。

**每 GPU decode 吞吐（相对 HBM-only）**

- 六模型 **1.5–3.1×**（平均 **2.2×**；bsz=1 最高 **3.7×**）。HBM-only 在 bsz=1 把 **74–85%** 时间耗在层 barrier。
- MoE vs H3：**4.0–14.3×**（平均 **6.2×**）。
- phantom-plane（FLINT+R）与无 refresh 吞吐相同。
- HBM+SSD 比 HBM-only 慢 **396–885×**。

**能耗**

- MoE 五模型相对 HBM-only：**0.72–0.90×**/token；bsz=1 为 **0.45–0.73×**（DSv4-Pro **2.2×** 节能）。
- dense Llama：**1.64×**（HBF 每 bit 读能比 HBM 高）。
- refresh 编程最多再加 **0.31%**。
- vs H3：MoE **4.2–15.7×** 更低。
- HBM+SSD 相对 HBM-only：**215–692×** 更高。

**封装数（50 ms TPOT, 128K）**

- bsz=1：五个 MoE 各 1 个 FLINT 封装；HBM min-fit 要 4–8。
- bsz=4：四个 MoE 仍 1 封装，Qwen3 要 2；dense Llama 4（bsz=1）/ 8（bsz=4）。
- bsz=64：Maverick 2 vs 4，Qwen3 32 vs 64，Kimi-K2 16 vs 96，DSv3 16 vs 128。DSv4-Pro 在 50.7 vs 50 ms 硬阈值下 FLINT 被推到 16 封装，min-fit 只要 6。

**Refresh / 寿命**

- 通道内 refresh 平均罚 **20×**（13–24×）；对齐突发在当 token 上 **3,700×**（303–6,771×）。
- 无 refresh 的 always-on 块约 **25 s** 坏。FLINT：P/E **10⁵** 连续 decode 平均 **29 天**（MoE 7–33 天，Llama 1.0 年）；**10⁶** 平均 **0.8 年**；**10⁷** 平均 **8.0 年**。

## 与 wiki 的关系

- [DASH](/papers/dash-dual-path-hbf-moe-inference.md) — DASH 加 GPU–HBF 直连 + HBM 基座中继；FLINT 仍是 HBM→HBF 级联，增量在控制器/refresh/FTL
- [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md) — 系统账：HBF 只赢低 I·b；FLINT 把级联 HBF 的有效带宽从 H3 的浪费态拉回来
- [DRAM and Memory System](/concepts/dram-memory-system.md) / [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md) — HBF 近封装容量层，不是 PCIe SSD
- [Through-Silicon Via (TSV) Physical Layer](/concepts/tsv-3d-physical-layer.md) — 16 die NAND 靠 TSV；封装侧是 D2D，不是 3D logic NoC
- [3D Stacking Technologies](/concepts/3d-stacking-technologies.md) — 仍是 TSV-HBF，不是 HB logic-on-logic
- [PRESERVE](/papers/preserve-prefetch-weights-kv-cache.md) — 软件层 HBM→L2 prefetch；FLINT 把 burst 时机收进 HBF 基座硬件

## 开放问题

1. 评测 t_R=2 μs，正文现代 SLC 写 12 μs。带宽–延迟积和 2 MB burst 都跟 t_R 走，换 12 μs 要重算。
2. 无硅。HBM 用 Ramulator 校准到 67.8–69.9% 持续带宽；算力按 MFU 0.5 解析。
3. 基线 H3 是 CAL 2026 静态预取，不是 DASH 双路径。不能把 6.2× 读成「相对 DASH」。
4. 寿命是 P/E 扫描，不是厂商 HBF 耐久规格。
5. 掉电重装 6.7 min，不保非易失驻留。

# Citations

[1] [raw/papers/FLINT_HBF_LLM_Inference_2026.pdf](raw/papers/FLINT_HBF_LLM_Inference_2026.pdf) — Oliveira, Tavakkol et al., arXiv:2608.25062
[2] [raw/papers/flint-hbf-llm-inference.md](raw/papers/flint-hbf-llm-inference.md) — 结构化摘录
