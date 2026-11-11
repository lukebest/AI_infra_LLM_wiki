---
type: Raw Source
title: "FastAFD: When Does Attention-FFN Disaggregation Pay on Rack-Scale NVLink?"
source_url: https://arxiv.org/abs/2611.07149
pdf: FastAFD_When_Does_AFD_Pay_NVL72_2026.pdf
retrieved: 2026-11-11
ingested: 2026-11-11
org: University of California, San Diego (Hao AI Lab)
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.07149)

Attention–FFN disaggregation (AFD) separates attention from the experts of a mixture-of-experts (MoE) model and has been reported to raise decode throughput over colocated serving. Whether this advantage holds on rack-scale NVLink systems such as GB200 NVL72 remains unclear: prior results were obtained on other hardware, against narrower colocated baselines, or with analytical models, whereas production engines serve large MoE models on these systems with wide expert parallelism (wide EP). We build and carefully tune FastAFD, an AFD inference engine for GB200 NVL72 that overlaps the MoE of one microbatch with the attention of the other, and compare it against the best vLLM wide EP setting (with the EP width tuned per workload). Our experiments show that AFD has a throughput advantage of up to 1.17× over wide EP on Qwen3 and 1.16× on Qwen3.5, and matches it on MiniMax-M2.5. We derive an analytical model that predicts AFD throughput within 3% using only profiles of colocated vLLM, which tells whether switching to AFD would improve throughput before AFD is deployed. Beyond prediction, we turn the model into a concise insight: AFD’s speedup factors into a batch gain (larger batches, since attention GPUs hold no expert weights), an overlap gain (shorter steps, since the MoE runs on the expert GPUs behind attention), and a disaggregation cost (the GPUs given to experts). AFD has the advantage when the two gains outweigh the cost. This view explains which models benefit from AFD, and shows that speculative decoding helps light-expert models most, where the enlarged overlap gain outweighs the larger disaggregation cost and adds a further 8% to AFD’s advantage over wide EP. Looking ahead, serving the experts on accelerators that keep their weights in on-chip SRAM, such as the Groq LPX accelerators that NVIDIA pairs with Vera Rubin NVL72, would remove most of the disaggregation cost, raising the ideal speedup to 2.48× with speculative decoding. FastAFD is open source at https://github.com/hao-ai-lab/FastAFD.

# Excerpts / key facts

- Authors: Yichao Fu*, Yuxuan Zhang*, Minshen Zhang*, Ruitian Wang, Junda Chen, Hao Zhang (UCSD). *Equal contribution. Preprint, arXiv:2611.07149, 2026-11-04, cs.DC.
- Platform: GB200 NVL72；对照为每负载调优的 vLLM wide EP（EP 宽度按负载选）。主度量 Sall 把所有分配的 attention 与 FFN GPU 都计入；Satt 只计 attention GPU。
- 模型（Table A1 / §3）：MiniMax-M2.5（10B active / 229B，256 experts）、Qwen3-235B-A22B（22B / 235B，128 experts）、Qwen3.5-397B-A17B（17B / 397B，512 experts）；均为 FP8 MoE。上下文 4K–16K，输出 OSL=1024。
- Table 1 / Fig 3（标准 decode，d=0）：相对最佳 wide EP 的 Sall：Qwen3 16K **1.17×**（EP32，A:F 11:1，SEP4 1.42，Satt 1.28）；Qwen3.5 4K **1.16×**（EP32，5:1）；Qwen3.5 16K **0.99×**；MiniMax-M2.5 **1.00–1.02×**。相对单节点 EP4 的 SEP4 为 **1.30–2.36×**，被 rack 内调优 wide EP（基线吞吐抬升 22–114%，峰在 EP16–EP32）收窄到 0.99–1.17×。Satt 全负载 **1.08–1.39×**。相对 wide EP 的 batch 优势 **1.06–1.16×**。
- Table 2 / Fig 4（投机 d=3，q=4，接受率 ā≈1.8）：Sall：MiniMax 从持平抬到 4K/16K **1.08×**；Qwen3 **1.10–1.13×**；Satt 最高 **1.70×**（Qwen3 4K）。最优 A:F 收缩过半（MiniMax 9:1–17:1→4:1–8:1，Qwen3 5:1–11:1→2:1–5:1）。摘要称投机给 AFD 相对 wide EP 的优势再加 **8%**。FastAFD 自身 d=3 vs d=0 最高 **1.54×**（Fig 4a）。
- 分解（Eq. 2 / Fig 5）：Sall = (bA/bV)×(TV/TA)×(r/(r+1))，即 batch gain、overlap gain、disaggregation cost。零拟合模型（只吃 colocated vLLM 画像）：65 个部署上到各自最优比，吞吐均值误差 **2.9%**（标准 3.0%、投机 2.6%），单次最高 **7.4%**（Fig 6c）。
- 运行时（Fig 7）：k=2 ping-pong 微批最好；某消融使 E2E 吞吐 −32%（Fig 7c）；相对 peak-tuned CAD，CAD 只有 FastAFD 每 GPU 吞吐的 **0.68–0.78×**（Fig 7d）。
- 异构展望（§6 / Fig 8）：专家放到片上 SRAM 加速器（文中举例 Groq 3 LPX + Vera Rubin NVL72）去掉 GPU 预算上的 disaggregation cost 后，理想 Satt 天花板标准 decode **1.20–1.76×**、投机 **1.38–2.48×**；近持平的 MiniMax 也可到 **1.20–1.26×**。
- 开源：https://github.com/hao-ai-lab/FastAFD
