---
type: Raw Source
title: "p-DCIM: A 28nm Probabilistic SRAM DCIM based Ising Machine for Near-Memory Context Selection in LLM-RAG Pipeline"
source_url: https://arxiv.org/abs/2610.37033
pdf: pDCIM_SRAM_Ising_RAG_Context_Selection_2026.pdf
retrieved: 2026-10-29
ingested: 2026-10-29
org: Georgia Institute of Technology
venue: arXiv cs.AR (2026-10)
---

# Abstract (verbatim, arXiv:2610.37033)

We present a fabricated SRAM DCIM Ising machine that performs set-level context selection for large language model (LLM) with retrieval-augmented generation (RAG). In RAG, the evidence-selection stage is increasingly delegated to repeated language-model reranking, which adds substantial energy to the inference pipeline. We reformulate evidence selection as a quadratic unconstrained binary optimization (QUBO) problem and solve it on a dual-mode digital compute-in-memory (DCIM) macro: the same multiply-and-accumulate datapath computes the embedding-similarity scores that populate the QUBO coefficients and evaluates the per-spin Hamiltonian differences that drive the anneal. The annealing temperature is set by a digital plane-count control along with the SRAM pseudo-read random bit flips, giving graded cooling entirely from on-chip digital configuration. The macro is taped-out in a 28 nm process [0.16 mm2, 0.41 mW] and is proposed to be integrated as part of the logic base-die in hybrid high-bandwidth memory (HBM) and high-bandwidth flash (HBF) stacks in a GPU package, where only the selected passage identifiers return to the host. Replacing the language-model selection pass with the near-memory Ising solver yields a macro-normalized selection-energy estimate more than six orders of magnitude lower than the LLM-based baseline and reduces the evaluated total energy per query by 67%, while maintaining comparable token-level F1 on the evaluated examples.

# Excerpts / key facts (from PDF)

- Authors: Madhav Vadlamani, Rahul Singh, Yuyao Kong, Haomei Liu, Zheng Zhang, Shimeng Yu (Georgia Tech).
- Fabricated 28 nm SRAM DCIM Ising macro: **0.16 mm²**, **500 MHz**, ~**0.41 mW** probabilistic (**0.406 / 0.413 mW** det/prob measured), **32 Kb** SRAM.
- Dual-mode MAC: same datapath builds QUBO coefficients (embedding similarities) and evaluates per-spin ΔH for anneal.
- Cooling: digital magnitude-plane exposure schedule + SRAM pseudo-read bit flips (no analog RNG).
- Integration thesis: logic base-die under hybrid HBM+HBF in GPU package; only selected passage IDs leave memory subsystem; O(N²) pairwise scoring stays near storage (vs HAVEN-style near-storage retrieval).
- Energy: selection ~**0.9 µJ**/query on macro → **>6 orders** below LLM selection pass; evaluated total query energy **536 J → 175 J (−67%)**.
- Quality: comparable to SetR/SetRO baselines on Exact Match / Gold-Contains / token-level F1 (example text cites EM 0.70, Gold-Contains 0.90, token F1 on evaluated examples).
