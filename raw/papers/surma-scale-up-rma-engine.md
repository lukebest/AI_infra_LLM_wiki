---
type: Raw Source
title: "SURMA: Efficient Fine-Grained Communication Offload for SuperPOD"
source_url: https://arxiv.org/abs/2611.21274
pdf: SURMA_Scale_Up_RMA_SuperPOD_2026.pdf
retrieved: 2026-11-18
ingested: 2026-11-18
org: Tsinghua University / Tencent / HKUST
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.21274)

GPU SuperPODs underpin large language model (LLM) serving, but growing bandwidth and round-trip times make inter-GPU communication consume increasing compute resources. SM-driven remote memory access occupies shared memory or registers for in-flight data and competes for SM-to-NoC bandwidth. Dedicated engines can free these resources, but must handle fine-grained transfers, down to a 576 B KV-cache entry. NVIDIA's CopyEngine uses less than 1% of NVLink bandwidth at 7 KB granularity. We present SURMA, an on-die Scale-Up Remote Memory Access engine. Adapting RDMA requires overcoming slow doorbell submission, excessive per-application connection state, head-of-line blocking of completion notifications on shared connections, and costly ordering for multipath transfers. SURMA uses a credit-based shared send queue to reduce submission latency from 1.2 µs to 400 ns; fused write-with-atomic semantics to share connections while independently notifying each transaction; and Network Per Path Ordering to ensure data arrives before the completion flag without Sender or Receiver Ordering. We implement SURMA in RTL on a two-FPGA prototype and evaluate it with two 8-GPU NVLink servers. At 512 B granularity, SURMA saturates attainable bandwidth with a single SM, whereas NVLink needs over 14% of the SMs. SURMA occupies under 0.5% of GPU area and accelerates inference on four models by 1.05-1.26x over NVLink.
