---
type: Raw Source
title: 'Unlocking reasoning potential in large langauge models by scaling code-form planning'
source_path: /home/luke/wiki/raw/papers/Code_Form_Planning_Scaling_LLM_Reasoning_2024.pdf
arxiv: '2409.12452'
doi: '10.48550/arXiv.2409.12452'
zotero: P6ISUKQ8
ingested: 2026-07-17
sha256: 025c56090d59d6ed531ed34c2e8c2901b485d5b0bca5bf9673309b46ecfa57b4
---

# Unlocking reasoning potential in large langauge models by scaling code-form planning

Authors: Jiaxin Wen, Jian Guan, Hongning Wang, Wei Wu, Minlie Huang (Tsinghua University, Ant Group)
Year: 2024

Structured notes / key excerpts:

- **CODE PLAN**: Scalable framework — LLMs generate and follow **code-form plans** (pseudocode blueprints) before final response.
- **Motivation**: Multi-step reasoning fails (repetition, incoherence, focus drift, early answering); pretraining corpora lack explicit planning structure.
- **vs prompting (CoT, Plan-and-Solve)**: Requires strong inherent capability + brittle prompts; poor cross-task generalization.
- **vs task-specific fine-tuning (AMOR FSM, latent plans)**: Limited domains or opaque latent codes.
- **Code advantages**: Structured control flow — functions, for-loops, if-branches; interpretable; auto-extractable from web corpora at scale.
- **Training data**: **2M** examples ⟨prompt, code-form plan, response⟩ from existing corpora — no curated task-specific datasets.
- **Results**: **25.1%** relative improvement vs direct response generation, averaged over **13** reasoning benchmarks (math, symbolic, instruction-following, multi-hop QA, decision-making).
- **Models**: Mistral, Llama 7B–13B; gains increase on more complex tasks; strong data efficiency from generalization.
- **Efficiency**: Minimal extra compute at train and inference vs latent-plan methods.
