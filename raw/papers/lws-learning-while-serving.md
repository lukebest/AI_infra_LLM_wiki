---
type: Raw Source
title: "Mutable Inference: Architecting LLM Accelerators for Inference-Time Learning"
source_url: https://arxiv.org/abs/2611.18523
pdf: Mutable_Inference_LWS_2026.pdf
retrieved: 2026-11-18
ingested: 2026-11-18
org: University of Virginia
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.18523)

Long-context LLMs must retain growing histories, but full attention makes each new token increasingly expensive. Inference-time learning (ITL) offers another approach. The model keeps training on the context during inference, retaining what it learns in its weights. Recent work shows that ITL can match full-context attention quality while attending only to a recent fixed-size window. This bounds attention costs but adds Learning (backward computation and weight updates) alongside Prediction (the forward pass) costs. Inference accelerators assume fixed weights, while training accelerators target complete training steps. This work identifies two opportunities. Attention's non-matrix operations leave enough idle matrix capacity for Learning, while selected layers can tolerate delayed weight updates with little quality loss. We exploit both with Learning While Serving (LWS), an inference accelerator architecture that shares compute hardware between latency-critical Prediction and deadline-flexible Learning. Hardware-managed per-layer weight versioning allows Learning to publish updates while in-flight computations read older versions. Resumable reduction blocks let Learning kernels span fragmented idle windows and yield to Prediction, while dedicated softmax-gradient units relieve vector contention. On modeled datacenter and edge NPUs, LWS hides Learning within Prediction, sustaining Prediction-only throughput while preserving 99.3% of fully fresh Learning's quality benefit for TTT-E2E 3B at 128K tokens. Across nine models, LWS achieves 1.6x the throughput of serial execution and 1.3x that of the best prior co-execution architecture. RTL synthesis shows that LWS adds 1.5% to NPU core area without another MAC array. By efficiently turning idle inference capacity into learning capacity, LWS establishes inference-time learning as a first-class workload for future LLM accelerators.
