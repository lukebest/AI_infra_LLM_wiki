---
type: Raw Source
title: "Deploying RDMA for Large-Scale Inference and Training Workloads (ByteExpress)"
source_url: https://arxiv.org/abs/2610.12815
pdf: ByteExpress_RDMA_Deployment_Inference_Training_2026.pdf
retrieved: 2026-10-13
org: ByteDance / Fudan University
venue: arXiv preprint (cs.DC)
---

# Abstract (verbatim, arXiv:2610.12815)

RDMA can reduce communication overhead in distributed machine learning systems, but realizing these benefits in production requires more than replacing TCP. Variable-size messages, concurrent connections, bursty incasts, and service failures introduce challenges that hardware offload alone cannot address. This paper reports our experience deploying ByteExpress, a software communication layer over hardware RDMA, in ByteDance's parameter-server-based inference and training systems. We present three lessons from the deployment: efficient RDMA requires buffer management across application and transport layers; scalable communication requires coordinated management of connections, receive capacity, and outstanding data; and service availability requires recovery above the transport layer. ByteExpress combines an RDMA-aware allocator, zero-copy transfers, QP multiplexing, receive-credit flow control, a software send window, and RPC-assisted recovery. In production inference, ByteExpress reduces mean and P99 model parameter fetch latency by 35.7% and 43.7%, respectively, and total CPU usage by 10.69% compared with kernel TCP. In training, ByteExpress reduces P99 model parameter push latency by up to 74.0% compared with TCP, with no PFC pauses observed at runtime.
