---
type: Raw Source
title: "Expert Coupling in MoE Pretraining: Reducing All-to-All Overhead with Correlated Placement and Token Shuffling"
source_url: https://arxiv.org/abs/2610.09372
pdf: Expert_Coupling_MoE_Pretraining_AllToAll_2026.pdf
retrieved: 2026-10-12
org: Zyphra
---

# Abstract excerpt (verbatim, arXiv:2610.09372)

On a cluster with 8 AMD Instinct MI300X GPUs per node, these collectives can take 45% of the training step at EP32 with top-2 routing and 60% with top-6 routing. ... At top-2, 0.8% of the expert pairs in a layer are selected together by 42% of tokens... Correlated expert placement ... Combined with a dispatcher that sends each token to each GPU once, it removes up to 58% of dispatched rows. Token shuffling ... On one node this raises the share of token–expert assignments served on the token's GPU from 12.5% to 59%. In Megatron-LM, across EP degrees from 8 to 64 with top-2 and top-6 routing, the two methods reduce all-to-all time by 1.16-2.63X and end-to-end step time by up to 1.41X. Neither method changes the models' underlying routing decisions or expert parameters.
