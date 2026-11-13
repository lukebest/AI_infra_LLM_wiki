---
type: Raw Source
title: "SFU-Sim: Bit-Exact Reverse Engineering of NVIDIA MUFU and Validation of PTX Paths"
source_url: https://arxiv.org/abs/2611.13879
pdf: SFU_Sim_NVIDIA_MUFU_Bit_Exact_2026.pdf
retrieved: 2026-11-13
ingested: 2026-11-13
org: Sun Yat-sen University
venue: arXiv preprint
---

# Abstract (verbatim gist, arXiv:2611.13879)

Reproducing the numerical behavior of a GPU requires predicting the exact output of special function instructions. Vendor documents give only the function semantics and error bounds. These do not fix the output bit pattern. We present SFU-Sim, which builds bit-exact models of NVIDIA multi-function unit (MUFU) instructions by black-box reverse engineering on real GPUs. We first model a single bare MUFU instruction. We then add the surrounding operations found in the disassembly to model full PTX paths. The model covers 12 common MUFU forms and two BF16 forms on the tested Blackwell GPU. Using SIN/COS as a complete case study, we show how we analyze the PTX-to-SASS compilation path and recover the segment structure, the equivalent coefficient tables, and the finite-width arithmetic. On NVIDIA GPUs of three architectures (Ampere, Ada Lovelace, and Blackwell), we exhaustively compare every tested PTX path over its specified input domain. FP16 and FP32 paths cover all 2^16 and 2^32 input encodings, respectively. The model output matches the hardware bit for bit, with zero mismatches. SFU-Sim computes each output directly from its input. It needs neither a lookup table of all inputs nor access to a physical GPU. It can serve as a bit-exact special function component for instruction simulators. It can also serve as an arithmetic reference for hardware design and functional verification that target the same numerical behavior. SFU-Sim and its validation programs are open source at https://github.com/hzX40000000/SFU-Sim

# Excerpts / key facts

- Authors: Haozhi Xie, Tao Su (School of Electronics and Information Technology, Sun Yat-sen University). arXiv:2611.13879, submitted 10 Nov 2026, cs.AR. IEEE-style sections; PDF/abstract do not name a conference. Mark as preprint.
- Devices (§IV): NVIDIA A100 (Ampere, sm_80), GeForce RTX 4060 Laptop (Ada Lovelace, sm_89), RTX PRO 5000 Blackwell (sm_120). Compile targets sm_80 / sm_89 / sm_120.
- Coverage: 12 common MUFU forms on all three devices; two additional BF16 forms (EX2, TANH) on the tested Blackwell only. 14 forms grouped into 7 numerical core families (SIN/COS, EX2, TANH, RCP, RSQ, LG2, SQRT) (Table IV / §III-C).
- Method: black-box reverse engineering. SIN/COS case study recovers period reduction, 64 segments (6+17 bit split), Q37 fixed-point quadratic, truncated partial-product square S15(v) keeping columns m+n≥14 (Fig 3–4). Surrounding PTX ops (e.g. FMUL.RZ prescale by 1/(2π)) modeled separately from the bare MUFU.
- Storage: coefficients of all 8 FP32 functions take less than **10 KB** total; narrow formats reuse them. Storing outputs of these 8 functions for all 2^32 inputs would take about **128 GiB** (§III-C). Contrast with Cankaya (arXiv:2606.00279) GB-scale lookup tables.
- Validation (Table V): 8 FP32 paths (EX2, LG2, RCP, RSQ, SQRT, SIN, COS, TANH) over all 2^32 encodings; 2 FP16 (EX2, TANH) over all 2^16; 2 FP64 high-word (RCP, RSQ) over all 2^32 high words with low word zero; 2 BF16 (EX2, TANH) on Blackwell only. Every listed path: **0 mismatches** on tested devices.
- Extended paths on A100 (Table VI): 7 non-.ftz FP32 approximate, 2 FP16x2, 8 FP32 RCP/SQRT with RN/RZ/RM/RP; each over all 2^32 encodings (FP16x2: all 2^32 half-word combinations); **0 mismatches**. RCP/SQRT rounding-mode paths are validated at the PTX output, not as an independent check of MUFU intermediates.
- Every FP32 NaN output is the fixed encoding 0x7fffffff. Model is functionally equivalent; authors do not claim it is the physical on-chip implementation.
