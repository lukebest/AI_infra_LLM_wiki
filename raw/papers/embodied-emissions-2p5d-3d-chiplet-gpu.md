---
type: Raw Source
title: "Embodied Emissions of 2.5D and 3D Scaling in Chipletized GPUs for Low-Carbon AI"
source_url: https://arxiv.org/abs/2610.32830
pdf: Embodied_Emissions_2p5D_3D_Chiplet_GPU_2026.pdf
retrieved: 2026-10-27
org: imec (Cambridge UK, Leuven BE); Vrije Universiteit Brussel
venue: arXiv cs.AR (2026-10), short paper
---

# Abstract (verbatim, arXiv:2610.32830)

GPU compute resources are scaling to support growing AI workloads, leading to further rises in the climate change impact of hyperscale data centers that rely on high-performance GPUs. To model how packaging decisions impact the carbon footprint we have estimated the embodied emissions (EE) of a chiplet-based GPU that has been scaled in 2.5D and 3D using the imec.netzero modelling platform. We doubled the number of compute units and high bandwidth memory (HBM) capacity in the 2.5D and 3D scaled systems and found that 3D scaling results in an 89% increase in EE, as compared to an increase of 141% for 2.5D scaling, positioning 3D scaling as an attractive solution to limit the embodied emissions due to GPU scaling.

# Excerpts / key facts (from PDF)

- Baseline inspired by AMD MI300X: passive Si interposer (3 metal layers), 4 IOD (5 nm, TSV, micro-bump), 8 XCD hybrid-bonded on IOD (5 nm +4 metal), 8 stacks 12-Hi HBM3 (28 nm logic die, DRAM1z). Baseline EE: DRAM dies 53.2%, logic dies 28%.
- Yield: Murphy model, 0.1 defects/cm²; critical area 100% logic, 15% passive interposer; 99% packaging yield per die/subpackage attach. Reticle stitching, warpage, extra DRAM thinning excluded.
- 2.5D scaled: package +100% (~7× reticle), 16 XCD on 8 IOD, 16×12-Hi HBM3; interposer yield 43.5%, GPU package assembly yield 78.6%; EE +141%.
- 3D scaled: 8 extra XCD hybrid-bonded on top, 12×16-Hi HBM (HBM4-like), package +25% (~4× reticle); interposer yield 58.5%, IOD-XCD subpackage 95.1%, HBM subpackage 84.3%, assembly 85.1%; EE +88.5%.
- 2.5D EE 28% higher than 3D; final assembly losses add 18% (3D) vs 27% (2.5D); 2.5D interposer 60% larger; interposer EE +83% at 100% yield, +168% with yields.
- Iso-FLOPs, iso-HBM capacity; 2.5D has more HBM bandwidth but two switched 4-IOD groups vs fully connected 4 IOD in 3D; Hespas training sims: 2.5D only 6.8–13.5% faster.
- Caveats: HBM stack-height yield and thermal management may bottleneck 3D. Funded by ARIA.
