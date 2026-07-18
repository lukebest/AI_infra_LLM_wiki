---
type: Raw Source
title: 'Multi-branch self-drafting for LLM inference acceleration'
source_path: /home/luke/wiki/raw/papers/Multi_Branch_Self_Drafting_LLM_Inference_2025.pdf
arxiv: ''
doi: '10.1609/aaai.v39i22.34567'
zotero: ARC5DHFW
ingested: 2026-07-17
sha256: eff60f89cb891c9488d75a78b662220d64a12d8684f554cdfb321b41ab161c2e
---

# Multi-branch self-drafting for LLM inference acceleration

Authors: Zipeng Gao, Qingrong Xia, Tong Xu, Xinyu Duan, Zhi Zheng, Zhefeng Wang, Enhong Chen (USTC + Huawei Cloud)
Year: 2025

Structured notes / key excerpts:

- **Self-Draft**: Extends autoregressive decoding to **multi-branch drafting** — LLM generates draft sequences via parallel draft branches (attention masks), no separate draft model or fine-tuning.
- **Draft-and-verify**: Verify multiple candidate tokens in one forward pass; preserves target model parameters and output quality.
- **Motivation vs external drafters**: Small draft models add serial comm/compute overhead and alignment training cost; architecture modifications (Medusa etc.) need fine-tuning.
- **vs pre-built cache (PIA)**: Cache from corpus suffers domain mismatch — PIA throughput drops **>30%** when GSM-8K cache used on Dolly-15K; Self-Draft updates cache with contextual drafts from branches.
- **Padding robustness**: Random prompt padding still yields **>20%** BLEU/ROUGE overlap with vanilla decode — motivates in-context branch drafts.
- **Cache maintenance**: Combines corpus common expressions + contextual drafts from drafting branches.
- **Results**: **2.0–3.2** accepted tokens per forward step; **~2×** end-to-end throughput vs autoregressive baseline across open benchmarks.
- **Code**: github.com/ZipECHO/Self-Draft
