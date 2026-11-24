---
type: Raw Source
title: "ScaleWire: An End-to-End Scale-Up Ethernet Simulation Framework for LLM Systems"
source_url: https://arxiv.org/abs/2611.26086
pdf: ScaleWire_Scale_Up_Ethernet_Simulation_2026.pdf
retrieved: 2026-11-24
ingested: 2026-11-24
org: Institute of Information Engineering, CAS; Institute of Microelectronics, CAS; University of Chinese Academy of Sciences
venue: preprint
---

# Abstract (verbatim gist, arXiv:2611.26086)

LLM training and inference rely on scale-up networks for high-bandwidth, low-latency memory-semantic communication among accelerators (XPUs). Ethernet is emerging as an open interconnect for scale-up systems. In Ethernet systems, network-interface (NI) mechanisms across transport, network, and link layers interact, jointly shaping communication performance and on-chip resource requirements. We present ScaleWire, an end-to-end scale-up Ethernet simulation framework for LLM systems. It couples packet-level simulation of cross-layer NI mechanisms with a resource exploration engine that combines analytical estimates and simulation to size on-chip resources. We validate ScaleWire against hardware measurements and nine analytical checks, and evaluate six NI designs across four LLM communication workloads. For DeepSeek-R1 dispatch, NI design choices lead to a 4.5× difference in per-XPU on-chip storage budget. In grid-comparison experiments, the exploration engine uses 6–19% of the simulations required by exhaustive search. Using vLLM prefill traces with kernel times measured on GH200 GPUs, ScaleWire further guides resource provisioning under a completion-time constraint for inference execution. ScaleWire thus helps designers select NI mechanisms and provision on-chip resources to balance communication performance and resource cost.

# Excerpts / key facts

- Authors: Kai Ma, Quanfeng Lv, Jingguo Ge, Kefan Ruan, Ruoqi Li（中科院信息工程研究所 / 国科大 / 网络空间安全防御全国重点实验室）；Bowei Dai（中科院微电子研究所）。arXiv:2611.26086。
- ETH-X 四主机、400 Gb/s 交换机对照：全互连吞吐 MAPE 3.0%，约 345 Gb/s/主机饱和；一对全 MAPE 7.3%。
- DeepSeek-R1 dispatch：六种 NI 设计每 XPU 存储 862–3,858 KiB（4.5×）。探索引擎用穷举 6–19% 的仿真次数。
- 推理配额回放 GH200 kernel 时间：Llama-3.1-70B（8 XPU）Default / LLR+E2E 为 421 / 893 KiB，DeepSeek-V3.1（16 XPU）为 267 / 502 KiB。
