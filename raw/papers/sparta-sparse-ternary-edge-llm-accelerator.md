---
type: Raw Source
title: "SPARTA: A Sparse Ternary LLM Accelerator with Adaptive Attention and Unified Datapath for Long-Context Edge Inference"
source_url: https://arxiv.org/abs/2610.34824
pdf: SPARTA_Sparse_Ternary_Edge_LLM_Accelerator_2026.pdf
retrieved: 2026-10-28
ingested: 2026-10-28
org: Zhejiang University; Veloxis AI
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.34824)

Large language models (LLMs) are increasingly deployed on edge devices, where limited memory capacity and bandwidth constrain both model size and inference efficiency. Recent ternary LLMs with 1.58-bit weights substantially reduce model memory footprint, largely eliminating weight storage as the primary bottleneck. As context lengths grow, however, the bottleneck shifts to the key-value (KV) cache and attention, whose memory traffic increases linearly with sequence length and dominates long-context inference. Existing LLM accelerators mostly handle ternary linear layers and attention with separate datapaths, resulting in inefficient end-to-end execution and costly hardware overhead. To address these challenges, we propose SPARTA, a sparse ternary LLM accelerator for efficient long-context edge inference. SPARTA is built on three key techniques: (1) SPARTA features a phase-aware sparse dataflow that jointly exploits heterogeneous sparsity across compute-bound prefill and memory-bound decode. (2) We design a unified compute fabric in SPARTA to map ternary SpMM/SpMV and bit-serial attention onto a shared processing-element, efficiently exploiting both zero-weight and zero-bit sparsity. (3) To improve the efficiency of long-context inference, we propose an adaptive attention engine with two-stage selection. It first applies coarse-grained page-level Top-k selection to reduce K-cache accesses, and then performs fine-grained token-level Top-p pruning to further minimize V-cache traffic. Across SOTA ternary LLMs, SPARTA reduces KV traffic by 4.1–4.8× over full attention and 1.3–1.5× over a SOTA sparse-attention scheme with task-dependent quality loss. Against an NVIDIA Jetson AGX Orin GPU, SPARTA achieves 3.9× higher generation throughput and 8.3× higher end-to-end energy efficiency on average; against an AMD Ryzen 7 9700X CPU, the improvements are 5.0× and 81.7×, respectively. Against SOTA LLM accelerators, SPARTA achieves 1.6–12.0× higher throughput than FIGLUT, TeLLMe, and MCBP, 2.0–4.2× higher energy efficiency, and 1.3–51.4× higher area efficiency.

# Excerpts / key facts (from PDF)

- Authors: Yanzhen Zhou, Zhengyu Han, Qunyou Liu, Zheyu Yan, Weihong Xu, Cheng Zhuo (ZJU / Veloxis).
- HW (Table II): 28 nm, 1 GHz; 8 Compute Slices × 16 PEs × 32 lanes; 64-entry Top-k window; 64-bin Top-p histogram; HBM2 8×128-bit @2 GHz, 8 GB.
- Area/power: total area **13.9 mm²**, avg on-chip power **1.40 W** (shared fabric 47.6% area / 39.6% power).
- Models: BitCPM-1B/3B/8B, Bonsai (ternary); W1.58/A8; INT4 KV; max seq **32K**.
- Default sparse attn: ρk=1/4 page Top-k, p=0.90 histogram Top-p; ρp retained 2.9–10.9% of Top-k candidates.
- KV traffic: 4.1–4.8× vs full attention; 1.3–1.5× vs SOTA sparse (Twilight-class).
- vs Jetson AGX Orin (50 W): 3.9× throughput, 8.3× energy eff (avg); vs Ryzen 7 9700X: 5.0× / 81.7×.
- vs FIGLUT/TeLLMe/MCBP (same 28 nm flow repro): throughput 1.6–12.0×, energy 2.0–4.2×, area eff 1.3–51.4×.
- Also compared TENET/FACT/Energon/LUT-DLA; PE alone up to 2.2× area / 1.5× energy vs TENET/TeLLMe.
