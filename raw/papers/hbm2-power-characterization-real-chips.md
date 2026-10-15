---
type: Raw Source
title: "Understanding the Power Consumption of Modern High Bandwidth Memory: Experimental Analysis and Modeling Using Real HBM2 DRAM Chips"
source_url: https://arxiv.org/abs/2610.14244
pdf: HBM2_Power_Characterization_Real_Chips_2026.pdf
retrieved: 2026-10-15
org: ETH Zurich / NYU (SAFARI)
venue: MICRO 2026 extended version (arXiv cs.AR)
---

# Abstract (verbatim, arXiv:2610.14244)

We perform the first comprehensive experimental characterization of power consumed by real HBM2 DRAM chips. Our extensive characterization yields 1) the empirical basis for developing new, accurate HBM power models or validating existing power models and 2) key insights into structural and data-pattern-dependent variation of power in HBM2 chips. Out of our 13 new findings and 6 key takeaway messages, we highlight: 1) a read operation consumes significantly higher current than any other operation and 2) the toggled data bus signals in a data transfer burst significantly affect current draw where toggling all HBM2-internal bank group bus signals causes 29.4% higher power consumption than keeping them constant. Leveraging our empirical insights into HBM2 power consumption, we engineer an access pattern that yields 23.6% higher power consumption on average across 36 tested HBM2 chips than the highest-power-consuming JEDEC-specified current measurement loop. Our results have important implications for HBM-based system design and validation. Relying solely on JEDEC- or vendor-specified test loops to bound HBM power could cause system failures and/or thermal throttling in real-world high-power AI/ML workloads. To improve 3D-stacked DRAM power modeling in open source architectural simulation infrastructures, we develop a new HBM power model. Our model predicts the power of 36 real HBM2 chips across diverse workloads (including a real LLM decode workload) with 7.6 -- 8.1% mean absolute percentage error, substantially more accurately than state-of-the-art HBM power models. The power consumption predicted by our model for a power-intensive microbenchmark closely matches (with 2.4% to 5.3% error across HBM3E's specified supply voltage range) the average HBM3E memory power consumed by three tested NVIDIA H200 GPUs. We publicly release our power model at this https URL.

# Excerpts (from arXiv PDF v1)

- §1: HBM3E GPU memory power measured up to 248 W on average across three NVIDIA H200 GPUs, ~35% of 700 W budget.
- Setup: 36 HBM2 chips in 18 AMD Alveo U55C FPGA boards (DRAM Bender-based testing infrastructure); highest clock 600 MHz (1200 MT/s); temperature range 48–86 °C.
- Takeaway 2 / §5.1: read draws 3.1× higher current than refresh (planar DDR3L: refresh is highest); measured all-0s IDD4R 1716 mA vs 1079 / 966 mA used by existing HBM2 models.
- Finding / Takeaway 3: current rises linearly with temperature, 6.7 mA per 1 °C on average.
- Takeaway 4: read current varies 8.1% across bank groups and 5.3% across banks on average.
- Finding 11 / Takeaway 5: toggling all bank-group bus signals → 29.4% higher power than constant; engineered access/data pattern ("0110" with BG bus toggle) → 23.6% average (35.4% max) more power than IDD4R, the highest JEDEC loop.
- §6 Ayna model (on DRAMPower): MAPE 8.1% (all-0s) / 7.6% (random) across workloads; Llama workloads 7.3% / 5.2%; DRAMSim3 predicts 2235 mW vs measured 4201 mW for Llama3.1-8B decode batch 8 (46.6% MAPE); prior models 20–42% error; separate TSV + BG-bus toggle terms cut read energy/bit error from 11.4% (FGDRAM calibrated) to 2.3%.
- §6.2 H200: model matches high-read microbenchmark power with 5.3% / 2.4% / 4.5% error at min / nominal / max VDD; idle power error 20.3% / 17.7% / 12.0%; modeled trace throughput 4.50 TB/s.
- §6.3 HBM4 projection: read energy rises with data rate (6.24 → 6.73 pJ/bit from 4.8 to 8.0 Gbps/pin at VDDC=1.05 V / VDDQ=0.9 V); HBM4 @8.0 Gbps within 0.1% of HBM3E @6.4 Gbps at same voltages; 1.5% and 6.0% lower at (1.05 V, 0.7 V) and (1.00 V, 0.7 V).
- Model released at https://github.com/CMU-SAFARI/HBM-Power and in Ramulator 2.1.
