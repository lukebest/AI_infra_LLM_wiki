---
type: Raw Source
title: 'Mixed precision training'
source_path: /home/luke/wiki/raw/papers/Mixed_Precision_Training_2018.pdf
arxiv: '1710.03740'
doi: '10.48550/arXiv.1710.03740'
zotero: G5G3H9XY
ingested: 2026-07-17
sha256: 3bbff2f757abdcfe4c5a4cee338f7b7d888110b9013ec4a934e334016f527c78
---

# Mixed precision training

Authors: Paulius Micikevicius, Sharan Narang, Gregory Diamos, Erich Elsen, Jonah Alben, David Garcia, Boris Ginsburg, Michael Houston, Oleksii Kuchaiev, Ganesh Venkatesh, Hao Wu (NVIDIA, Baidu Research)
Year: 2018 (ICLR)

Structured notes / key excerpts:

- **Goal**: Train deep networks in **IEEE FP16** without accuracy loss or hyperparameter changes — ~halves memory, 2–8× faster math on recent GPUs.
- **Technique 1 — FP32 master weights**: Keep FP32 copy for optimizer updates; round to FP16 for forward/backward; prevents small gradient updates from underflowing in FP16 (~5% of grad exponents < 2⁻²⁴).
- **Technique 2 — Loss scaling**: Scale loss to shift gradient exponents into FP16 representable range; e.g., Multibox SSD needs **×8** scale to match FP32; unscaled training diverges.
- **Technique 3 — FP16 multiply, FP32 accumulate**: Products accumulate in FP32 before rounding to FP16 for storage.
- **Weight update ratio issue**: When |weight| >> |update| (ratio >2048), FP16 addition can zero the update — FP32 master fixes this (Mandarin speech: FP16-only updates → **80%** relative accuracy loss).
- **Memory**: Weights +50% vs pure FP32 weights, but activations/grads in FP16 → **~half** overall training memory (activations dominate).
- **Scope**: CNNs, RNNs, generative, detection, LM, MT, speech — models **>100M** params on large datasets; matches FP32 accuracy across tasks.
- **Contrast**: Prior binary/low-bit work incurred accuracy loss on large models; this keeps full FP16 tensors for fwd/bwd.
