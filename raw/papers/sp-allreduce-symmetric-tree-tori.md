---
type: Raw Source
title: "SP-Allreduce: Symmetric Tree Schedules for Tori and Beyond"
source_url: https://arxiv.org/abs/2610.16387
pdf: SP_Allreduce_Symmetric_Tree_Tori_2026.pdf
retrieved: 2026-10-15
org: "未在 PDF 首页标注机构（作者 Cherniavskii, Kupavskii, Mironov, Moiseev）"
venue: arXiv preprint (cs.DC)
---

# Abstract (verbatim, arXiv:2610.16387)

Allreduce is a fundamental communication primitive in large-scale distributed training, and torus interconnects remain widely deployed in high-performance systems. We introduce SP-allreduce, a new allreduce algorithm for $d$-dimensional tori that exploits the symmetry of the topology and routes only along shortest paths. We call an allreduce algorithm \emph{fully bandwidth-optimal} if it incurs no bandwidth overhead, no multihop-induced traffic inflation, and achieves perfect per-round load balance. SP-allreduce is based on a family of carefully symmetrized shortest-path trees that guarantees full bandwidth optimality in the $\alpha$--$\beta$ model. We prove that it uses the minimum possible number of rounds among all fully bandwidth-optimal allreduce algorithms on $d$-dimensional tori, and therefore the minimum running time in this class. In this sense, SP-allreduce refines Bucket allreduce: it preserves Bucket's key strengths while reducing the number of rounds by a factor of two. We further extend our approach to broader symmetric topologies and to communication trees of prescribed depths. Experimentally, the resulting algorithms improve over the best compared state-of-the-art algorithms for tori by up to $1.19\times$ on square tori and $1.65\times$ on rectangular tori across the tested configurations. On HyperX and spine-leaf networks, we demonstrate gains of up to $14.82\times$ and $1.72\times$, respectively, over the best evaluated baselines.

# Excerpts (from arXiv PDF v1)

- §1: torus/torus-like fabrics in ML: Google TPU v5/v6/Ironwood 2D/3D tori + optical reconfiguration; AWS Trainium Trn1/Trn2 2D torus; Graphcore IPU-POD; Fujitsu 6D Tofu-D.
- Contribution 2: SP-allreduce completes in 2d⌊n/2⌋ rounds on d-dim n×…×n torus, about half of Bucket's 2d(n−1); optimal among fully bandwidth-optimal schemes for odd n; even n uses one extra round over the 2H−1 lower bound.
- §5: k-SP-allreduce bounds tree depth k (k reduce-scatter + k allgather rounds), trading multihop traffic for fewer rounds.
- §7.1: SST packet-level simulation; 400 Gb/s links, 400 ns per hop (100 ns link + 300 ns router); square tori 8×8–64×64; rectangular 1024-node 64×16, 128×8, 256×4; HyperX 32×32; spine-leaf 16 spines / 32 leaves / 16 hosts per leaf. Baselines Bucket, Swing, Trivance (+Ring, recursive doubling where applicable).
- §7.2: max gain over best of Swing/Bucket/Trivance 8.0% / 19.0% / 17.7% / 18.3% on 8×8 / 16×16 / 32×32 / 64×64 (at 1, 1, 4, 64 MiB); vs Bucket at 64 KiB 1.74× (8×8), 2.00× (64×64).
- §7.3–7.4: gain up to 20.6% at 3.2 Tb/s links (1 MiB); 20.2% at 1600 ns per hop (512 KiB).
- §7.5: rectangular tori at 256 MiB reach ~778 / 764 / 731 Gb/s (97.2% / 95.5% / 91.4% of 800 Gb/s bound); max gains 1.22× / 1.34× / 1.65×; Bucket 706/620/502 Gb/s, Swing 598/509/361 Gb/s.
- §7.6: HyperX 32×32 bound 12.4 Tb/s; SP-allreduce ~11.76 Tb/s (94.9%) vs Swing 0.794 Tb/s → 14.82×; baselines use 4 of 62 links per node per round. Spine-leaf: 199.7 Gb/s (99.8% of 200 Gb/s); max gain 1.72× at 32 KiB (28.4 vs 16.5 Gb/s Trivance).
