---
type: Raw Source
title: "ARK: Avoiding Routing Collisions for KV Cache Transfer in Disaggregated LLM Inference"
source_url: https://arxiv.org/abs/2610.41160
pdf: ARK_KV_Path_Reservation_Disagg_Inference_2026.pdf
retrieved: 2026-11-05
ingested: 2026-11-05
org: Georgia Institute of Technology
venue: ACM SIGCOMM NAIC ’26
---

# Abstract (verbatim gist, arXiv:2610.41160)

Disaggregated LLM inference separates the prefill and decode phases across GPU pools, generating massive KV-cache transfers. Because these transfers last hundreds of milliseconds to seconds, they behave as mega elephant flows that dominate link bandwidth utilization. In this regime, stateless ECMP can perform poorly: hash collisions may overload one spine link while leaving others idle, stretching transfer times by seconds. Yet this same persistence makes coordination practical. Since these flows are long-lived, even lightweight one-to-all coordination can be amortized over their lifetime. We present ARK, a distributed elephant-flow path reservation mechanism. ARK coordinates senders to choose source ports whose hashes map concurrent flows onto distinct spines, without requiring switch changes or receiver-side packet reordering. Packet-level RDMA simulations show that ARK reduces mean and P95 FCT by up to 27.3% and 34.0% under moderate load, and further reduces mean TTFT by up to 12.9%.

# Excerpts / key facts

- Authors: Hung-Chun Lin, Ting-Wei Hsu, Chung-En Ho, Ahmed Saeed (Georgia Tech). NAIC ’26.
- LLaMA-3.1-405B 100K-token KV ≈ 48 GB; 400 Gbps 上可占满约 960 ms。
- 软件端路径预留：选 source port 使 hash 落到不同 spine；不改交换机、不需接收侧重排。
- QPS=25：mean FCT **−27.3%**，P95 FCT **−34.0%**；mean TTFT 最高 **−12.9%**。
