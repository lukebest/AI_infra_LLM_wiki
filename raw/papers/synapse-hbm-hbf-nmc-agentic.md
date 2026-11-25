---
type: Raw Source
title: "Synapse: An HBM-Coordinated HBF Near-Memory Computing Architecture for Pipelined Agentic AI Execution"
source_url: https://arxiv.org/abs/2611.29901
pdf: Synapse_HBM_HBF_NMC_Agentic_2026.pdf
retrieved: 2026-11-25
ingested: 2026-11-25
org: KAIST
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.29901)

During multi-agent video reasoning, model weights and per-agent key–value caches can exceed high-bandwidth memory (HBM) capacity. High-bandwidth flash (HBF) adds capacity, but agents still wait for GPU execution. Synapse, an HBM-coordinated near-memory computing architecture, overlaps HBF attention and expert execution with GPU computation across agents. It also reduces dispatch delays and unnecessary refreshes. Across three models, Synapse achieves 48.92–66.60% lower end-to-end latency, up to 2.98× throughput, and up to 64.48% lower modeled energy per output token than GPU execution with passive HBF. Wear simulations project 46% longer HBF lifetime than block-wide refresh at equal workload rates.

# Excerpts / key facts

- Authors: Juhyeong Jin, Hyunjun Cho, Joo-Young Kim。KAIST。arXiv:2611.29901，cs.AR，Tue 24 Nov 2026 公告。
- 方法：GPU 执行时间在 NVIDIA H100 上测量；HBF 计算、NAND 访问、传输与争用按 Table 1 仿真。能量：GPU 用执行时间与 NVML 板卡功率（含 HBM）；主机、HBF 与传输能量为模型。
- Table 1：5×16 GB HBM2e（80 GB）；5×512 GiB HBF（2.5 TiB）；CPU 内存 512 GB DRAM；PCIe Gen5×16，H2D/D2H 55.7/46.1 GB/s；D2D 最大 1.536 TB/s（UCIe，OCP Grade 2）；HBF 计算 2,048 个 BF16 MAC @ 400 MHz；片上 32 MiB；2,048 个活跃 bank、4 KiB 页；t_R=3 µs，t_PROG=100 µs。
- 模型：Qwen3-VL-235B-A22B-Instruct（与先前工作对照）；消融另含 InternVL3.5-241B-A28B、GLM-5.3-Flash（FP8 + FP32 状态）。负载为 LongVideoBench 验证视频轨迹；对照实验 256 帧、消融 64 帧。默认并发 C=6。
- 相对 Passive HBF（GPU 执行，HBM miss 时从 HBF 取权重与状态）：完整配置把端到端延迟降低 48.92–66.60%，吞吐提到 1.93–2.98×，建模的每输出 token 能量降低 46.13–64.48%。
- 相对 Duplex + passive HBF：Case A 在 C=1/6 上端到端降低 30.8–32.2%，吞吐 1.43–1.48×，送到 GPU 的中间数据少 37.0–42.2%。相对 ReKV / LiveVLM / Hot–Cold，256 帧时端到端降低 35.7–61.8%。
- 在 Flow/Fuse 上叠加 Sarathi 策略后，C=6 的均值 E2E 从 157.8 s 降到 139.9 s；再加 Forward 到 122.8 s、9.51 tok/s，相对 Sarathi 再改进 12.2% 与 14.0%。
- Fortify 按 wordline 跟踪物理读：在 α=1.5 下完成的工作量比块级刷新多 46.04–46.77%，同等负载速率下寿命大约长 46%。
- 面积估计（22 nm CACTI 按 FLINT 比例投影到 7 nm，MAC/控制参考 ASAP7）：新增 72.92 mm²（HBM 0.120 + HBF 72.801），相当于五个名义 HBF 封装（878 mm²）的 8.29%。
