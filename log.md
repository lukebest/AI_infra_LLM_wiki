# Bundle Update Log

## 2026-09-07

### Watch (morning)
* **Watch**: 2026-09-07 Asia/Shanghai AI infra 论文巡检。cs.AR/cs.DC recent 列表到 Fri 9/4（周一美东新稿上海早晨尚未放出；Labor Day 窗口）。已 ingest 的 Photonic Prefill/AInfer-PD/LEAP/DynaNDE/CHIPSMORE/Sync Tax 等不重复。
* **Ingest**: BASP PDF → `raw/papers/BASP_Batch_Aware_Sequence_Parallelism_2026.pdf` + stub `raw/papers/basp-batch-aware-sequence-parallelism.md`（arXiv:2609.03151, 2026-09-04, cs.DC）。
* **Ingest**: CREDIT PDF → `raw/papers/CREDIT_DSMEM_Inter_CTA_Tiling_2026.pdf` + stub `raw/papers/credit-dsmem-inter-cta-tiling.md`（arXiv:2609.01864, 2026-09-02, cs.DC）。
* **Ingest**: Einsummable PDF → `raw/papers/Einsummable_Multi_GPU_Parallelism_2026.pdf` + stub `raw/papers/einsummable-multi-gpu-parallelism.md`（arXiv:2609.03905, 2026-09-04, cs.DC）。
* **Creation** (papers): [BASP](/papers/basp-batch-aware-sequence-parallelism.md)（Ulysses 子组 A2A；1.17–1.32×）；[CREDIT](/papers/credit-dsmem-inter-cta-tiling.md)（DSMEM reduction-reuse；5090/H100 1.466×/1.318×）；[Einsummable](/papers/einsummable-multi-gpu-parallelism.md)（自动 join-agg；LLaMA block 8.97 vs 13.65/14.87 ms）。
* **Update**: [LLM Collectives](/concepts/llm-distributed-training-collectives.md)（SP/Ulysses 子组 + 自动分解），[NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)（训练侧关 NVLink 域），[GPU SIMT](/concepts/gpu-simt-architecture.md)（DSMEM 一行）。
* **Indexes**: 手动同步 `papers/index.md`（+3）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: Para-Pipe (2609.04168, 边缘异构 SoC 算子流水，非 LLM fabric)；FlowTT (2609.03459, DLRM TT embedding GPU kernel)；Analog Photonic Interposer (2609.03125, 视觉 sensor↔模拟加速器)；Latency-Aware Multi-Agent LLM on Heterogeneous GPUs (2609.03335, serving 编排)；Einsummable 同窗 Barnacle/JuPyLive/区块链/FL/5G 等出范围；Sep 4 已跳过 AceSpec/Atlas/NOVA/CREDIT 当时仅扫过标题——今日全文入库；Characterizing multi-tenancy (2609.00817) 仍表征文。BusyBarn 仍无公开全文 PDF。先验跳过 Beacon/AXI4/survey 2608.28048 等仍适用。

## 2026-09-04

### Watch (morning)
* **Watch**: 2026-09-04 Asia/Shanghai AI infra 论文巡检。cs.AR recent/new = Thu 9/3 提交（含 cross）；已 ingest 的 LEAP/DynaNDE/CHIPSMORE/Sync Tax/FLINT/Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart 与全部 hc2026-* 不重复。
* **Ingest**: Photonic Prefill PDF → `raw/papers/Scaling_Inference_Prefill_High_Radix_Photonic_2026.pdf` + stub `raw/papers/scaling-inference-prefill-photonic.md`（arXiv:2609.01821, 2026-09-01, cs.DC/cs.AR）。
* **Ingest**: AInfer-PD PDF → `raw/papers/AInfer_PD_InPlace_Prefill_Decode_MoE_2026.pdf` + stub `raw/papers/ainfer-pd-inplace-prefill-decode-moe.md`（arXiv:2609.00993, 2026-09-01, cs.DC）。
* **Creation** (papers): [Photonic Prefill](/papers/scaling-inference-prefill-photonic.md)（3D 光子 4× SU BW / 1152 pod；高 batch 2.1–3.2×、跨 pod 2.2–4.5×）；[AInfer-PD](/papers/ainfer-pd-inplace-prefill-decode-moe.md)（Ant；turnstile+DeepEP 相位隔离；vs Normal −7.1–22.5%、vs SGLang −24.8–32.9%）。
* **Update**: [Disaggregated Inference](/concepts/disaggregated-inference.md)（同池 P/D 复用一行 + 光学 DES），[NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)（光学 1152 pod 对照），[NVIDIA CPO Roadmap](/concepts/nvidia-cpo-roadmap.md)（推理 prefill 量化）。
* **Indexes**: 手动同步 `papers/index.md`（+2）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: AceSpec (2609.02514, edge-cloud WAN speculative，出 WSE/NoC/NoW)；Atlas 3DGS VR (2609.02352)；NOVA eNVM on-chip training (2609.01948)；RunSoC automotive (2609.01614)；Batch Before You Time EDA (2609.02470)；H3DNAS / FORGE MCU / GadIR / HDL repair；CREDIT DSMEM；MeanField GPU scheduling；Characterizing multi-tenancy AI training (2609.00817, 表征)；Just Talk Once split FL (2609.01457)。先验跳过仍适用：Block-Diffusion/VARA/HBQ、Beacon、AXI4、LLM-H、survey 2608.28048、Gen-TAS、SNN、MeshReduce-U、Redwood、Ankhdjet、TerraceMoE、FPGA Transformer survey。BusyBarn 仍无公开全文 PDF。

## 2026-09-03

### Watch (morning)
* **Watch**: 2026-09-03 Asia/Shanghai AI infra 论文巡检。cs.AR new/recent = Wed 9/2 提交（12+cross）；Thu 9/3 美东列表上海早晨可能尚未放出。已 ingest 的 CHIPSMORE/Sync Tax/FLINT/Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart 与全部 hc2026-* 不重复。
* **Ingest**: LEAP PDF → `raw/papers/LEAP_IMC_NoC_LLM_Inference_2026.pdf` + stub `raw/papers/leap-imc-noc-llm-inference.md`（arXiv:2609.00857, 2026-09-01, cs.AR；ICCAD'25 扩展）。
* **Ingest**: DynaNDE PDF → `raw/papers/DynaNDE_Near_Data_Expert_Scheduling_2026.pdf` + stub `raw/papers/dynande-near-data-expert-scheduling.md`（arXiv:2609.00407, 2026-09-01, cs.AR）。
* **Creation** (papers): [LEAP](/papers/leap-imc-noc-llm-inference.md)（NUS；IMC+NMC+INC；LEAP-D 片上 PD；vs A100 ≥2.55×/≥71.94×，vs H100 1.52×/24.91×）；[DynaNDE](/papers/dynande-near-data-expert-scheduling.md)（IIT；NPU–NDP 分析模型调度；vs MoNDE prefill/decode 2.6×/2.2×）。
* **Update**: [Disaggregated Inference](/concepts/disaggregated-inference.md)（LEAP-D 片上行），[Heterogeneous Inference](/concepts/heterogeneous-inference.md)（IMC/NMC/INC；NPU–NDP），[Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)（IRCU INC），[Collective-Capable NoC](/concepts/collective-capable-noc.md)（对照 LEAP IRCU），[CXL Tiered Memory](/concepts/cxl-tiered-memory.md)（MoE CXL-NDP）。
* **Indexes**: 手动同步 `papers/index.md`（+2）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: Block-Diffusion edge (2609.01084, LPDDR/systolic 压缩，无 NoC/NoW/chiplet 互连增量)；VARA ReRAM (2609.00421, 通用激活稀疏 IMC)；HBQ (2609.00450, MICRO 量化)；SPEC CPU 2026 EPYC (2609.01527)；FPGA Transformer survey (2609.01212)；Analog-DB / FALCON / JENGA / energy-law / version-space / SILK replace。先验跳过仍适用：Beacon 2608.30932、AXI4 monitor、LLM-H、survey 2608.28048、Gen-TAS、SNN、MeshReduce-U、Redwood、Ankhdjet、TerraceMoE。BusyBarn（ISCA 2026）仍仅 artifact/Zenodo，无公开全文 PDF。3DLS 已入库不重复。

## 2026-09-02

### Watch (morning)
* **Watch**: 2026-09-02 Asia/Shanghai AI infra 论文巡检。cs.AR new 页 = Tue 9/1 提交；Wed 9/2 美东列表上海早晨可能尚未放出。已 ingest 的 Sync Tax/FLINT/Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart 与全部 hc2026-* 不重复。
* **Ingest**: CHIPSMORE PDF → `raw/papers/CHIPSMORE_CIM_Chiplets_LLM_Inference_2026.pdf` + stub `raw/papers/chipsmore-cim-chiplets-llm-inference.md`（arXiv:2608.30509, 2026-08-31, cs.AR）。
* **Creation** (papers): [CHIPSMORE](/papers/chipsmore-cim-chiplets-llm-inference.md)（NUS；RRAM-ACIM+SRAM-DCIM + IPCN in-network DMAC；分层 KV；非复制多请求层流水；vs H100 Mistral-7B INT8 最高 2.38× 吞吐 / 27× 能效）。
* **Update**: [Disaggregated Inference](/concepts/disaggregated-inference.md)（层流水共享权重一行），[Heterogeneous Inference](/concepts/heterogeneous-inference.md)（CIM PE 异构），[Interconnection Network Design Space](/concepts/interconnection-network-design-space.md)（IPCN compute-in-interconnect）。
* **Indexes**: 手动同步 `papers/index.md`（+1）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: Beacon (2608.30932, LLM multi-agent chiplet HW-DSE，方法文、无新 fabric PHY/拓扑数，与 HYDRA 域重叠)；AXI4 transaction monitoring (2608.30435, Benini mixed-crit SoC)；LLM-based HW development hierarchical IRs (2608.30659, EDA)；Clock-gating MSP430 (2608.30954)；FABO routing (2608.30268)；adiabatic systolic (2608.30058)；SNN memory (2608.30444)；genomic storage thesis (2608.31004)；KORD (2608.30379)。先验跳过仍适用：survey 2608.28048、Gen-TAS、TerraceMoE gate-fail、VPP、CE-MoE、Blackwell CC、MeshReduce-U、edge Hydra 2608.25053、Intelligent Network WAN 2608.26453（出 WSE/NoC/NoW 范围）。BusyBarn（ISCA 2026）仍无公开全文 PDF。

## 2026-09-01

### Watch (morning)
* **Watch**: 2026-09-01 Asia/Shanghai AI infra 论文巡检。**无增量**。cs.AR recent/new 到 Mon 8/31（5 条；Tue 9/1 美东列表上海早晨尚未放出）。已 ingest 的 Sync Tax/FLINT/Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart 与全部 hc2026-* 不重复。
* **Indexes**: 无 papers 变更。未跑 `generate_indexes.py`。
* **Considered not ingested**: AI Hardware Accelerators survey (2608.28048, 综述无新一作互连数)；Gen-TAS (2608.28160, FPGA-GPP 任务分配)；Neuromorphic numerical solvers (2608.28387)；DeepSeq3 (2608.28188, EDA GNN)；RVV 1.0 HPC (2608.28097)；TerraceMoE (2608.27874, MoE 分层 A2A 代价模型，step-level gate 失败、实测未进 hierarchical 区)；VPP (2608.26523, Ascend chunked-prefill 软件流水)；CE-MoE layer reconfig (2608.28511, 减 A2A 的模型层型，非 fabric)；Blackwell CC TEE (2608.26575)；LLM energy token/request (2608.28044)；cache LAH/S4-FIFO (2608.27975)。Fri 8/28 已跳过项（MeshReduce-U/SNN/Redwood/Ankhdjet/HOLMES/LLM-EDA 等）仍跳过。BusyBarn（ISCA 2026）仍仅 artifact/IEEE，无公开全文 PDF。

## 2026-08-31

### Watch (morning)
* **Watch**: 2026-08-31 Asia/Shanghai AI infra 论文巡检。cs.AR recent 到 Fri 8/28；Mon 8/31 美东列表上海早晨可能尚未放出。已 ingest 的 FLINT/Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart/Iff 与全部 hc2026-* 不重复。
* **Ingest**: Synchronization Tax PDF → `raw/papers/Synchronization_Tax_GPU_Scale_Up_Domains_2026.pdf` + stub `raw/papers/synchronization-tax-gpu-scale-up.md`（arXiv:2608.22503, 2026-08-23, cs.DC）。
* **Creation** (papers): [Synchronization Tax](/papers/synchronization-tax-gpu-scale-up.md)（Cornell；8-GPU 域集体 >50% 是 barrier 等待；增广 Hockney T=pα+qS/B+τ，B* 随域规模下降）。
* **Update**: [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md)（带宽缩放 vs 域规模张力），[LLM Collectives](/concepts/llm-distributed-training-collectives.md)（墙钟含与 B 无关的 τ）。
* **Indexes**: 手动同步 `papers/index.md`（+1）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: MeshReduce-U (2608.26220, GNN/不规则 mesh NoC 编译器，非 LLM fabric)；SNN multicast (2608.26223)；Redwood (2608.26418, AI 设计加速器 EDA)；Ankhdjet (2608.26206, 三值 CiROM)；HOLMES yield (2608.26758)；LLM EDA orchestration (2608.27184)；DNA storage；SILK TOCTOU；vision generative edge。3D-IC Benchmark (2608.25155) 与 edge Hydra (2608.25053) 已于 8/28 跳过。BusyBarn 仍无公开 arXiv PDF。2603.22774 CPU slowdowns 替换版在窗口外。昨日跳过的 Simthesizer/NOVA/FlashAccel/TMR/SPICE 仍跳过。

## 2026-08-28

### Watch (morning)
* **Watch**: 2026-08-28 Asia/Shanghai AI infra 论文巡检。cs.AR new/recent 到 Thu 8/27（7 篇新稿 + 替换）；Fri 8/28 列表尚未放出。已 ingest 的 Maia/光互连/HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart/Iff 与全部 hc2026-* 不重复。2608.24637 v2 数字未变（2.7×/3.8×/3.3×），不重入库。
* **Ingest**: FLINT PDF → `raw/papers/FLINT_HBF_LLM_Inference_2026.pdf` + stub `raw/papers/flint-hbf-llm-inference.md`（arXiv:2608.25062, 2026-08-25）。
* **Creation** (papers): [FLINT](/papers/flint-hbf-llm-inference.md)（HBF 基座 burst-buffer / phantom-plane / 只读 FTL；级联不是 DASH 双路径）。
* **Update**: [DASH](/papers/dash-dual-path-hbf-moe-inference.md)，[OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md)，[TSV](/concepts/tsv-3d-physical-layer.md)，[DRAM](/concepts/dram-memory-system.md)，[3D Stacking](/concepts/3d-stacking-technologies.md)。
* **Indexes**: 手动同步 `papers/index.md`（+1）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: 3D-IC Benchmark Suite (2608.25155, UCLA Gupta，CATCH→3Dblox 物理设计测试集，无 LLM/NoC/NoW)；edge Hydra 表征 (2608.25053, AGX SoC + llama.cpp，与已入库 HYDRA 2608.19395 不是同一篇)；APT DiT 剪枝 (2608.25380)；BOOSTEDSOSA (2608.25346)；Syn2Logic (2608.25536)；Ising anneal (2608.26100)。cs.NI 近窗 5G/UAV/IoT/BGP/SlimTCP，无 LLM 互连。昨日跳过的 Simthesizer/NOVA/FlashAccel/TMR/SPICE/FIBER/HyperCut 与 2608.24637 v2 仍跳过。BusyBarn 仍无公开 PDF。

## 2026-08-27

### Watch (morning)
* **Watch**: 2026-08-27 Asia/Shanghai AI infra 论文巡检。cs.AR new/recent 到 Wed 8/26（Tue 8/25 提交；API 最新 2608.24664 15:05 UTC）。Thu 8/27 列表尚无更新提交。cs.NI 近窗多为 5G/量子/IoT；MemChannel CXL pooling 与 WiCi 无线 GPU 不入库。已 ingest 的 HYDRA/ReXpert/HCCL/DASH/DICE/Fovea/C2C/ThAME/3DLS/Mozart/Iff 与全部 hc2026-* 不重复。
* **Ingest**: Maia 200 全文 PDF → `raw/papers/Maia_200_Software_Defined_Dataflow_2026.pdf` + stub `raw/papers/maia-200-sdla.md`（arXiv:2608.24664, 2026-08-25）。
* **Ingest**: 晶圆级光互连热调谐 PDF → `raw/papers/Thermal_Tuning_Wafer_Scale_Optical_Interconnect_LLM_MoE_2026.pdf` + stub `raw/papers/wafer-scale-optical-interconnect-moe-thermal.md`（arXiv:2608.24637, 2026-08-25）。
* **Creation** (papers): [Maia 200 SDLA](/papers/maia-200-sdla.md)（归档全文，链到 HC 幻灯页，不重复峰值 TOPS）；[晶圆级光互连热 stall](/papers/wafer-scale-optical-interconnect-moe-thermal.md)。
* **Update**: [HC Maia 200](/papers/hc2026-microsoft-maia-200.md)（加归档指针；幻灯 <1 µs 与全文 ~4 µs 不混用），[Network-on-Wafer](/concepts/network-on-wafer.md)（光 interposer 近亲），[LLM Collectives](/concepts/llm-distributed-training-collectives.md)，[Protocol Stack](/concepts/interconnection-network-protocol-stack.md)（ATLv2），[3D Stacking](/concepts/3d-stacking-technologies.md)。
* **Indexes**: 手动同步 `papers/index.md`（+2）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Considered not ingested**: Simthesizer (2608.24650, serving 仿真器+agent，无互连架构)；Pipeline-Native Transformers (2608.23841, CPU decode 带宽)；Elastic KV (2608.23658)；MemChannel CXL (2608.21731, cs.NI pooling transport)；WiCi (2608.24204)。昨日跳过的 NOVA/FlashAccel/TMR/SPICE/FIBER/HyperCut/VIPER/M3D SRAM/MCM GPU/SYNTLOG/Optalysys 仍跳过。BusyBarn 仍无公开 PDF。NVHBM 是新闻博客，不是论文。

## 2026-08-26

### Hot Chips 2026 ingest
* **Ingest**: Day1/Day2 KEEP 幻灯 PDF → `raw/papers/HC2026_*.pdf` + Raw Source stub。数字只取 extract notes。**未**拷贝 Micron Confidential。
* **Creation** (papers): [Rubin](/papers/hc2026-nvidia-rubin.md), [MI455X](/papers/hc2026-amd-instinct-mi455x.md), [Helios UALoE](/papers/hc2026-amd-helios-ualoe.md), [Crescent Island](/papers/hc2026-intel-crescent-island.md), [Vera CPU](/papers/hc2026-nvidia-vera.md), [CS-4](/papers/hc2026-cerebras-cs4.md), [MTIA 400](/papers/hc2026-meta-mtia-400.md), [Maia 200](/papers/hc2026-microsoft-maia-200.md), [TPU 8](/papers/hc2026-google-tpu8.md), [SN50](/papers/hc2026-sambanova-sn50.md), [BlueField-4](/papers/hc2026-nvidia-bluefield-4.md), [Groq 3 LPX](/papers/hc2026-nvidia-groq-3-lpx.md), [Spectrum-X Multiplane](/papers/hc2026-nvidia-spectrum-x-multiplane.md), [Jalapeño](/papers/hc2026-openai-jalapeno.md), [Thor Ultra](/papers/hc2026-broadcom-thor-ultra.md)。教程/海报 7 页见同日上一小节。
* **Update**: [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md), [Groq 3 LPX](/entities/nvidia-groq-3-lpx.md), [Cerebras WSE](/entities/cerebras-wse.md), [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md), [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md)（MTIA 400 2D mesh / 1.2 TB/s SU）, [CXL Tiered Memory](/concepts/cxl-tiered-memory.md)（Diamond Rapids CXL 3.0 1LM/Flat2LM 三行）, [TPU v4 OCS](/concepts/tpu-v4-ocs-reconfigurable-fabric.md)（链 TPU 8）。
* **Schema**: 公司加 `microsoft / openai / broadcom / intel / sambanova`；网络加 `ualink / ualoe`。
* **Indexes**: 手动同步 `papers/index.md`（+15）、`entities/index.md`、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Skip as full papers**: Micron Confidential；Opticore；LUTs and Bolts；RISC-V / Canonical / Infineon；Day1 Arm AGI / IBM Z / Diamond Rapids（仅 CXL 三行）/ welcome / awards / Waymo / BosSemi / Fujitsu / Wildcat；Day2 Samsung LPDDR5X-PIM / XCENA MX1 / closing / Versal RF / Versal Premium Gen2。

### Hot Chips 2026 tutorials / posters ingest
* **Ingest**: Handy / Samsung / SK hynix / d-Matrix / OXMIQ / NVIDIA Fusion 教程 PDF + Pistil 海报 PDF → `raw/papers/HC2026_*.pdf` + Raw Source stub。**未**拷贝、未 ingest Micron Confidential 教程。
* **Creation** (papers): [Handy HBM 开场](/papers/hc2026-handy-hbm-tutorial.md), [Samsung B-die / zHBM](/papers/hc2026-samsung-hbm-base-die.md), [SK hynix packaging](/papers/hc2026-skhynix-hbm-advanced-packaging.md), [d-Matrix Raptor](/papers/hc2026-dmatrix-raptor-3d-dram.md), [OXMIQ HBF](/papers/hc2026-oxmiq-hbf.md), [NVIDIA NVLink Fusion](/papers/hc2026-nvidia-riscv-nvlink-fusion.md), [Pistil](/papers/hc2026-pistil-20-chiplet-slm.md)。
* **Update**: [3D Stacking](/concepts/3d-stacking-technologies.md)（SK HyB vs HBM4E；Samsung zHBM WoW+HCB）, [Hybrid Bonding](/papers/hybrid-bonding-3d-integration-recent.md), [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md)（Raptor 1-Hi logic-on-top）, [DRAM](/concepts/dram-memory-system.md), [TSV](/concepts/tsv-3d-physical-layer.md), [Network-on-Wafer](/concepts/network-on-wafer.md)（zHBM 不是晶圆级 NoW）, [DASH](/papers/dash-dual-path-hbf-moe-inference.md)（OXMIQ 对照）, [NVLink fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md), [Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md)。
* **Schema**: 公司标签加 `samsung / sk-hynix / d-matrix / oxmiq`；技术加 `hbf`。未加 intel / microsoft / openai。
* **Indexes**: 手动同步 `papers/index.md`（+7）、`raw/papers/index.md`。未跑 `generate_indexes.py`。
* **Skip**: Micron Confidential；Opticore（photonic compute）；LUTs and Bolts（edu ring NoC）；RISC-V / Canonical / Infineon。


### Watch (morning, no increment)
* **Watch**: 2026-08-26 Asia/Shanghai AI infra 论文巡检。cs.AR new/recent 聚焦 Tue 8/25（Wed 8/26 列表尚未出）；扩展核对 FlashAccel 替换版（2607.10186v2, replaced 2026-08-22）。已 ingest 的 HYDRA/ReXpert/HCCL/DASH 等不重复。
* **No increment**: 本轮无 WSE/NoC/NoW/3D/chiplet/LLM 互连合格全文。不硬凑入库。
* **Considered not ingested**: NOVA (2608.22613, 4F² VCT + peri-over-cell 两层 NMP，HB/TSV 仅作 DRAM 堆叠带宽，无 NoC/chiplet/NoW 拓扑增量)；FlashAccel (2607.10186v2, GPU 内 HBF 权重+KV 布局/SRAM 预取/管理软件，相对已 ingest 的 DASH 双路径 UCIe 无互连架构增量)；SYNTLOG FSM FPGA (2608.23288)；systolic PE approx (2608.22378)；NoTB RTL (2608.21962)；FPGA compression survey (2608.21657)；Optalysys photonic compute-in-transit (2608.21536)；M3D 6T SRAM 2nm (2608.22741)；VIPER PIM DSE (2608.23404)；MCM GPU cycle simulator (2608.22602)；TherMapNet (2608.21887)。昨日跳过的 TMR/SPICE/FIBER/HyperCut/FPGA NoC CAD/DTX/SLA/H100 load/HBM reliability/MAGMA/TokenPowerSandbox/HCRMap 仍跳过。BusyBarn 仍无公开 PDF。WATOS (2512.12279) 在窗口外。

## 2026-08-25
* **Watch**: 2026-08-25 Asia/Shanghai AI infra 论文巡检。cs.AR pastweek 最新到 Mon 8/24（6 篇）；Tue 8/25 列表尚未出。昨日已 ingest 的 HYDRA（2608.19395）不重复。
* **No increment**: 本轮无 WSE/NoC/NoW/3D/LLM 互连合格全文。不硬凑入库。
* **Considered not ingested**: TMR wide-link NoC router (2608.21288, Benini 组，512-bit/2-cycle/7nm TMR，偏 SEE 可靠性而非 LLM 互连拓扑)；SPICE MoE prefetch (2608.21240, PCIe expert offload 投机预取，软件编排)；FIBER (2608.19628)；HyperCut (2608.19296, tiled NoC 层间调度，唯一偏 LLM 的是 GPT-2 decode)；FPGA NoC CAD / DTX / SLA / H100 load / HBM reliability / MAGMA / TokenPowerSandbox / HCRMap 仍跳过。BusyBarn 仍无公开 PDF。

## 2026-08-24
* **Watch**: 2026-08-24 Asia/Shanghai AI infra 论文巡检。近 7 天 cs.AR（8/17–8/21）仍多 FPGA/RTL/GPU SIMT；WSE/NoC/NoW/3D/LLM 互连增量里只选出 1 篇有架构实质的全文。已 ingest 的 ReXpert/HCCL/DASH（08-21）、DICE（08-20）、Fovea/C2C-Explorer/ThAME（08-19）、Iff/3DLS/Mozart（08-18）不重复。
* **Ingest**: HYDRA PDF → `raw/papers/HYDRA_Heterogeneous_Chiplet_DSE_Hybrid_LLM_2026.pdf` + stub `raw/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md`（arXiv:2608.19395, 2026-08-19）。
* **Creation** (papers): [HYDRA](/papers/hydra-heterogeneous-chiplet-dse-hybrid-llm.md)。
* **Update**: [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md), [Disaggregated Inference](/concepts/disaggregated-inference.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md), [Network-on-Wafer](/concepts/network-on-wafer.md)。
* **Indexes**: 手动同步 `papers/index.md`（+1）、`raw/papers/index.md`。
* **Considered not ingested**: FPGA NoC CAD (2608.17266)；DTX (2608.16953)；SLA scheduling (2608.16336)；H100 global load (2608.15764)；FIBER (2608.19628, GPU SIMT/寄存器)；HBM reliability (2608.19471)；MAGMA (2608.18366, FPGA GMM 视觉)；TokenPowerSandbox (2608.18149, 能耗 serving)；HCRMap (2607.11586, 3.5D MoE 映射，先前跳过、与 Mozart 重叠)。BusyBarn 仍无公开全文 PDF。本周合格增量只有 HYDRA，不硬凑 2–4 篇。

## 2026-08-21
* **Watch**: 2026-08-21 Asia/Shanghai AI infra 论文巡检。近 7–14 天 cs.AR 仍多 GNN/RTL/FPGA/SNN；WSE/NoC/NoW/3D/LLM 互连增量里选出 3 篇有架构实质的全文。已 ingest 的 Iff/3DLS/Mozart（08-18）、Fovea/C2C-Explorer/ThAME（08-19）、DICE（08-20）不重复。
* **Ingest**: ReXpert PDF → `raw/papers/ReXpert_MoE_ReRAM_Near_Memory_Disaggregated_Serving_2026.pdf` + stub `raw/papers/rexpert-reram-nmc-disaggregated-moe.md`（arXiv:2608.13962, 2026-08-14）。
* **Ingest**: HCCL PDF → `raw/papers/HCCL_Collective_Communication_Meta_MTIA_300_2026.pdf` + stub `raw/papers/hccl-meta-mtia-300-collective-communication.md`（arXiv:2608.00358；abs 自称 SC '26，未核程序册）。
* **Ingest**: DASH PDF → `raw/papers/DASH_Dual_Path_HBF_MoE_LLM_Inference_2026.pdf` + stub `raw/papers/dash-dual-path-hbf-moe-inference.md`（arXiv:2608.14333, 2026-08-14）。
* **Creation** (papers): [ReXpert](/papers/rexpert-reram-nmc-disaggregated-moe.md), [HCCL](/papers/hccl-meta-mtia-300-collective-communication.md), [DASH](/papers/dash-dual-path-hbf-moe-inference.md)。
* **Update**: [Disaggregated Inference](/concepts/disaggregated-inference.md), [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md), [DRAM and Memory System](/concepts/dram-memory-system.md), [TSV Physical Layer](/concepts/tsv-3d-physical-layer.md), [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)；交叉 [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md)、[3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md)、[C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md)、[Meta RDMA](/papers/rdma-over-ethernet-meta-training.md)。
* **Schema**: `SCHEMA.md` 公司标签加 `meta`。
* **Indexes**: 手动同步 `papers/index.md`（+3）、`raw/papers/index.md`。
* **Considered not ingested**: FPGA NoC CAD (2608.17266, FPL 2024 投稿窗口、FPGA 布局布线，无 LLM 架构增量)；DTX (2608.16953, 训练脉动/VLIW，无互连/3D/chiplet)；Dryas (2608.12934, Enzian ECI 跟踪引擎)；HBF Sucks / Potential Applications of HBF / Beyond Capacity 的姊妹短文 (2608.11668/13127/13868, 表征或短 CAL，架构增量已被 DASH 覆盖)；Hardware Design and Security (2608.05063, 安全)；SLA scheduling (2608.16336)；H100 global load (2608.15764)；BusyBarn 仍无公开全文 PDF（仅 artifact/IEEE）；先前跳过的 SHIFT/HCRMap/SiFAR/CLIP-3D/Chiplet-Contiguous/DeepStack/3D-Flow/DyPNet-MSC/Trivance/200mm InOx/2608.15118 仍无新全文增量。

## 2026-08-20
* **Watch**: 2026-08-20 Asia/Shanghai AI infra 论文巡检。近 7–14 天 cs.AR 多为 GNN/RTL/FPGA CAD，WSE/NoC/NoW/3D/LLM 互连增量很少。已 ingest 的 Iff/3DLS/Mozart（08-18）与 Fovea/C2C-Explorer/ThAME（08-19）不重复。
* **Ingest**: DICE PDF → `raw/papers/DICE_Detailed_Inter_Chiplet_End_to_End_PHY_Modeling_2026.pdf` + stub `raw/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md`（arXiv:2607.24221；PDF 页眉仍为 ISCA 2026 submission draft）。
* **Creation** (papers): [DICE](/papers/dice-detailed-inter-chiplet-end-to-end-phy-modeling.md)。
* **Update**: [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md)（chiplet PHY/FEC/PAM4）、[C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md)、[Network-on-Wafer](/concepts/network-on-wafer.md)、[UB 物理层](/concepts/ub-physical-layer.md)。
* **Indexes**: 手动同步 `papers/index.md`（+1）、`raw/papers/index.md`。
* **Considered not ingested**: Collective Communication for Distributed LLM Systems (2608.15118, 集群级 AR/RS/AG/A2A 教程，与已有 collectives 概念重叠、非 WSE/NoC/NoW/3D)；200 mm M3D InOx (2608.09508, 器件/工艺)；BusyBarn (ISCA 2026 晶圆级 LLM 映射+BALD，IEEE 付费、无公开 PDF，数字无法核)；Ouroboros / FlatAttention / ELMoE-3D / ATLAS 等 3–5 个月前工作超出 1–2 月窗口。先前跳过的 SHIFT/HCRMap/SiFAR/CLIP-3D/Chiplet-Contiguous/DeepStack/3D-Flow/DyPNet-MSC/Trivance 仍无新全文增量。

## 2026-08-19
* **Watch**: 2026-08-19 Asia/Shanghai AI infra 论文巡检。检索近 7–14 天并扩展到约 2 个月：WSE / NoC / NoW / 3D IC / LLM 加速器互连。昨日已 ingest 的 Iff/3DLS/Mozart 未重复。
* **Ingest**: Fovea PDF → `raw/papers/Fovea_Physical_Implication_Aware_Wafer_Scale_DSE_2026.pdf` + stub `raw/papers/fovea-physical-implication-aware-wafer-scale-dse.md`（arXiv:2608.03285, 2026-08-04）。
* **Ingest**: C2C-Explorer PDF → `raw/papers/C2C_Explorer_Chip_to_Chip_Interconnect_LLM_2026.pdf` + stub `raw/papers/c2c-explorer-chip-to-chip-interconnect-llm.md`（arXiv:2608.08611, DAC 2026 自称）。
* **Ingest**: ThAME PDF（v2）→ `raw/papers/ThAME_3D_Memory_Enabled_Heterogeneous_MoE_2026.pdf` + stub `raw/papers/thame-3d-memory-enabled-heterogeneous-moe.md`（arXiv:2607.17074；昨日仅摘要、今日全文）。
* **Creation** (papers): [Fovea](/papers/fovea-physical-implication-aware-wafer-scale-dse.md), [C2C-Explorer](/papers/c2c-explorer-chip-to-chip-interconnect-llm.md), [ThAME](/papers/thame-3d-memory-enabled-heterogeneous-moe.md)。
* **Update**: [Network-on-Wafer](/concepts/network-on-wafer.md)（Fovea 可行域/DSE）, [3D Stacking Technologies](/concepts/3d-stacking-technologies.md)（CBA+HB）, [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md), [Cerebras WSE](/entities/cerebras-wse.md), Mozart / WoW / 3DLS 论文页交叉引用。
* **Indexes**: 手动同步 `papers/index.md`（+3）。
* **Considered not ingested**: SHIFT (2606.28754, 计算搬迁 vs 数据搬迁，对比「晶圆级 LLM 服务」但主贡献偏 runtime)；HCRMap (2607.11586, 3.5D MoE 映射，与 Mozart 重叠且偏调度)；SiFAR (2607.08973, 软件同步-free AllReduce)；HyNoC (FPGA VLIW NoC, LLaMA 只作负载)；CLIP-3D (2607.12788, 通用 3D-IC 热/布局, 非 LLM)；200 mm M3D InOx (2608.09508, 器件/工艺为主)；Chiplet-Contiguous Layout / locality simulator (2606.11718/11716, 多 chiplet GPU GEMM)；DeepStack / 3D-Flow / DyPNet-MSC / Trivance 仍缺相对 wiki 的新增量或全文无新实质。无增量条目不单列「无增量」，因本轮有三篇 ingest。

## 2026-08-18
* **Watch (first-run)**: 2026-08-18 Asia/Shanghai 首轮 AI infra 论文巡检。检索 2025–2026（偏近 2–8 周）WSE / NoC / NoW / 3D IC / LLM 加速器。已有页未重复 ingest：FlooNoC collectives、Cerebras/WSE、Voxel、WaferLLM、MOCAP、hybrid bonding 综述。
* **Considered not ingested**: ThAME (arXiv:2607.17074, ESWEEK-26, 15.7×/9.8× 仅摘要级)；DeepStack (2604.04750, 与 Voxel DSE 重叠)；3D-Flow FlashAttention hybrid-bond (2602.11016)；DyPNet-MSC photonic NoW (ISPASS 2026)；Trivance AllReduce (2602.17254)；RPU (2602.18568)；CHIME (2601.19908)。
* **Ingest**: Iff et al. WoW NoW PDF → `raw/papers/Network_Design_Wafer_Scale_WoW_Hybrid_Bonding_2026.pdf` + stub `raw/papers/network-design-wafer-scale-wow-hybrid-bonding.md`（arXiv:2603.05266）。
* **Ingest**: 3DLS PDF → `raw/papers/3DLS_3D_Logic_Stacked_Disaggregated_LLM_Serving_2026.pdf` + stub `raw/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md`（arXiv:2607.01617, IEEE CAL 2026）。
* **Ingest**: Mozart PDF → `raw/papers/Mozart_35D_Wafer_Scale_MoE_Training_2026.pdf` + stub `raw/papers/mozart-35d-wafer-scale-moe-training.md`（arXiv:2603.07006）。
* **Creation** (papers): [WoW Network Design](/papers/network-design-wafer-scale-wow-hybrid-bonding.md), [3DLS](/papers/3dls-3d-logic-stacked-disaggregated-llm-serving.md), [Mozart](/papers/mozart-35d-wafer-scale-moe-training.md)。
* **Creation** (concepts): [Network-on-Wafer](/concepts/network-on-wafer.md) — 三条 WSI 物理路线 + 放置即拓扑。
* **Update**: [3D Stacking Technologies](/concepts/3d-stacking-technologies.md), [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Disaggregated Inference](/concepts/disaggregated-inference.md), [Cerebras WSE](/entities/cerebras-wse.md), [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md), [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md), `SCHEMA.md`（加 `now / network-on-wafer / wafer-on-wafer`）。
* **Indexes**: 手动同步 `concepts/index.md`（+1）、`papers/index.md`（+3）。

## 2026-08-13
* **Ingest**: Corner To Corner Route 交互可视化 → `raw/articles/corner-to-corner-route.html` + 摘录 `raw/articles/corner-to-corner-route.md`（6×8 AIC 折叠多环、RBRG 转弯服务、相位约束最短路）。
* **Creation**: [AIC Folded Multi-Ring NoC](/concepts/aic-folded-multi-ring-noc.md) — floorplan 常量、微边周期表、H→V→H 合法性、对角 194 cyc / 53.7 mm 复现。
* **Update**: [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md), [Topology Optimization Variants](/concepts/topology-optimization-variants.md) — 折叠多环/几何 DOR 交叉引用。
* **Indexes**: 手动同步 `concepts/index.md`（+1 条）。

## 2026-07-31
* **Layer 1 Ingest (New Study Series)**: 3D NoC 研究 Phase 1（Layer 1 物理层）开篇，4 raw 学记 → `raw/articles/3d-noc-study-{01-tsv-process-tech,02-monolithic-vs-tsv,03-hybrid-bonding,04-3d-mesh-baseline}.md`（侧重 TSV 物理 + 三路线对比 + 商业现实 + Feero baseline）。
* **Creation** (papers): [Katti TSV 2010](papers/katti-tsv-technology-roadmap-2010.md) — TSV 综述原典入口；[Batude Monolithic 2011](papers/batude-monolithic-3d-review-2011.md) — Monolithic 综述入口；[Hybrid Bonding Recent](papers/hybrid-bonding-3d-integration-recent.md) — Cu-Cu 直接键合综述；[Feero 3D Mesh Stan 2008](papers/feero-3d-mesh-noc-stan-2008.md) — 3-D Mesh NoC 拓扑 baseline。
* **Creation** (concepts): [TSV Physical Layer](concepts/tsv-3d-physical-layer.md) — TSV 工艺 + KOZ + 寄生 + 热 + 良率 五约束概念页；[3D Stacking Technologies](concepts/3d-stacking-technologies.md) — TSV / Monolithic / Hybrid Bonding 三路线对比 + 对 3D NoC 设计含义。
* **Update**: [3D-Stacked AI Chip](concepts/3d-stacked-ai-chip.md) + [Post-Moore Architecture Frontiers](concepts/post-moore-architecture-frontiers.md) 反向链接在 #5 步补。`SCHEMA.md` tag taxonomy 加 `3d / tsv / monolithic / hybrid-bonding / through-silicon-via / microbump / cu-cu / packaging / integration / sequential-integration`（既有 `chiplet / physical-layer` 等保留，无重复）。
* **Indexes**: 手动同步 `concepts/index.md`（+2 条）、`papers/index.md`（+4 条）。

## 2026-07-30
* **Ingest**: Ali (@waterloo_intern) '22580: From GPT2 to Kimi3, Explained' (2026-07-27 X 长文) → `raw/articles/22580 From GPT2 to Kimi3, Explained.md`（551 行，已存）。
* **Creation** (entities): [Moonshot AI Kimi K3](/entities/moonshot-ai-kimi-k3.md) — K3 模型实体 + 架构骨架 + 与 GPT-2 尺度对照。
* **Creation** (concepts): [Linear Attention Evolution](/concepts/linear-attention-evolution.md) — GPT-2 → Linear Attn → DeltaNet → Gated DeltaNet → KDA 七年演化主线；[Attention Residuals](/concepts/attention-residuals.md) — AttnRes 深度方向选择性残差检索；[Stable Latent MoE](/concepts/stable-latent-moe.md) — K3 MoE 框架（latent-space + Quantile Balancing + 898 expert/16+2 active）。
* **Creation** (papers): [Ali 22580 From GPT2 to Kimi3](/papers/ali-22580-from-gpt2-to-kimi3.md) — 论文摘要页（含全部章节结构 + 关键代码 + 数学公式）。
* **Update**: [WaferLLM System](/concepts/waferllm-system.md) — 新增 §"与 Kimi K3 的同构关系" + 相关概念交叉引用，frontmatter sources/updated 同步；[Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 新增 Linear Attention Evolution 与 K3 交叉引用（KDA 改变 decode bandwidth 格局），frontmatter 同步。
* **Update**: [SCHEMA.md](/SCHEMA.md) tag taxonomy 实际未改动（新页 tags 全部命中既有 taxonomy：attention/moe/llm/architecture/moonshot/optimization/kernel/inference 等）。
* **Indexes**: 手动同步 `concepts/index.md`（+3 条）、`entities/index.md`（+1 条）、`papers/index.md`（+1 条）。

## 2026-07-24
* **Ingest**: 金观涛、华国凡《控制论与科学方法论》→ `raw/books/控制论与科学方法论-金观涛-华国凡.mobi` + 结构化摘录 `raw/books/cybernetics-and-scientific-methodology.md`（源：`/home/luke/下载/控制论与科学方法论.mobi`）。
* **Creation**: [Cybernetics and Scientific Methodology](/concepts/cybernetics-and-scientific-methodology.md), [Black-Box Epistemology](/concepts/black-box-epistemology.md)。
* **Update**: [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md), [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md), [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md), [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md) — 黑箱/负反馈方法论交叉引用。

## 2026-07-22
* **Ingest**: 论文精读专项 paper-deepdive Day 1–8 + OVERVIEW → `raw/articles/paper-deepdive-day-01.md` … `day-08.md`、`paper-deepdive-overview.md`（源：`openclawdata/.../paper-deepdive/`）。
* **Creation**: [CMP NoC Pareto Design Tradeoffs](/concepts/cmp-noc-pareto-design-tradeoffs.md), [High-Radix Clos Adaptive Routing](/concepts/high-radix-clos-adaptive-routing.md), [TPU v4 OCS Reconfigurable Fabric](/concepts/tpu-v4-ocs-reconfigurable-fabric.md), [NVLink NVSwitch Scale-Up Fabric](/concepts/nvlink-nvswitch-scale-up-fabric.md), [Paper Deep-Dive Map](/summaries/paper-deepdive.md)；papers：`route-packets-not-wires`, `hoskote-5ghz-mesh-polaris`, `balfour-tiled-cmp-noc-tradeoffs`, `dally-virtual-channel-flow-control`, `kim-adaptive-routing-high-radix-clos`, `tpu-v4-optically-reconfigurable`, `nvidia-nvlink-hopper-blackwell`。
* **Update**: [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md), [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md), [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md), [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md), [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md), [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md), [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md), [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md), [Cerebras WSE](/entities/cerebras-wse.md), [Nvidia Vera Rubin NVL72](/entities/nvidia-vera-rubin-nvl72.md) — 精读链与 OCS/NVLink 对照交叉引用。

## 2026-07-21
* **Ingest**: Dally & Towles 互连网络 Day 19–21 → `raw/articles/interconn-study-21d-day-19.md` … `day-21.md`（源：`openclawdata/.../interconn-study-21d/day-19..21.md`；21 天计划完结）。
* **Creation**: [Network Interface and System-Level Design](/concepts/network-interface-and-system-design.md), [NoC Research Methodology and Case Studies](/concepts/noc-research-methodology-case-studies.md), [Interconn-Study 21d Knowledge Map](/summaries/interconn-study-21d-knowledge-map.md)。
* **Update**: [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md), [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md), [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md), [NoC Router Pipeline Optimizations](/concepts/noc-router-pipeline-optimizations.md), [Cerebras WSE](/entities/cerebras-wse.md), [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md) — NI/拥塞、论文案例、21 天地图交叉引用。

## 2026-07-17
* **Ingest**: Zotero 新下载 22 篇 PDF → `raw/papers/*.pdf`（上次批量 Find Available PDF / arXiv 直下）。
* **Creation** (papers + raw stubs): [MOCAP](/papers/mocap-wafer-scale-chunked-pipelining.md), [SuperInfer](/papers/superinfer-slo-aware-rotary-scheduling.md), [Heterogeneous Computing Agents](/papers/heterogeneous-computing-ai-agent-inference.md), [pHost](/papers/phost-coflow-aware-packet-scheduling.md), [Multi-Branch Self-Drafting](/papers/multi-branch-self-drafting-llm-inference.md), [M5 CXL](/papers/m5-cxl-tiered-memory-page-migration.md), [DynaX](/papers/dynax-sparse-attention-acceleration.md), [HyperMR](/papers/hypermr-hypergraph-matrix-storage-cim.md), [Comm/Comp Parallelism](/papers/optimizing-comm-comp-parallelism-training.md), [Silent Data Corruptions](/papers/silent-data-corruptions-production-cpu.md), [Cache-Resident LLC](/papers/cache-resident-llm-inference-llc.md), [PRESERVE](/papers/preserve-prefetch-weights-kv-cache.md), [FlexInfer](/papers/flexinfer-on-device-llm-offloading.md), [Code-Form Planning](/papers/code-form-planning-llm-reasoning.md), [Mixed Precision Training](/papers/mixed-precision-training.md), [HCache](/papers/hcache-fast-state-restoration.md), [Cloud-Scale RPC](/papers/cloud-scale-rpc-characterization.md), [CosMoS](/papers/cosmos-disaggregated-memory-data-movement.md), [PANDA](/papers/panda-adaptive-prefetch-dataflow.md), [Aurelia](/papers/aurelia-cxl-fabric-tentacle.md), [Alibaba HPN](/papers/alibaba-hpn-datacenter-network-llm.md), [Meta RDMA](/papers/rdma-over-ethernet-meta-training.md).
* **Creation** (concepts): [CXL Tiered Memory](/concepts/cxl-tiered-memory.md), [Mixed Precision Training](/concepts/mixed-precision-training.md).
* **Update**: [WaferLLM System](/concepts/waferllm-system.md), [Prefill-Decode Divergence](/concepts/prefill-decode-divergence.md), [Disaggregated Inference](/concepts/disaggregated-inference.md), [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md), [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md), [Heterogeneous Inference](/concepts/heterogeneous-inference.md), `SCHEMA.md`（补 speculative-decoding / dataflow / cxl / rdma）。
* **Indexes**: `generate_indexes.py` 重生成。

## 2026-07-14
* **Ingest**: Goossens et al. Æthereal NoC PDF → `raw/papers/Aethereal_Network_on_Chip_Concepts_Architectures_Implementations_2005.pdf`（Zotero: 4PFJG7KE, IEEE MDT 2005, DOI 10.1109/MDT.2005.99）。
* **Creation**: [Æthereal NoC](/concepts/aethereal-noc.md), [papers/aethereal-network-on-chip.md](/papers/aethereal-network-on-chip.md), `raw/papers/aethereal-network-on-chip.md`。
* **Update**: [Switching Principles](/concepts/switching-principles.md), [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md), [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Deterministic Execution](/concepts/deterministic-execution.md), [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — TDM GS / 确定性通信对照交叉引用。

## 2026-07-13
* **Ingest**: Dally & Towles 互连网络 Day 15–18 → `raw/articles/interconn-study-21d-day-15.md` … `day-18.md`（源：`openclawdata/.../interconn-study-21d/day-15..18.md`）。
* **Creation**: [Flow Control Fundamentals](/concepts/flow-control-fundamentals.md), [Virtual Channel Flow Control](/concepts/virtual-channel-flow-control.md), [NoC Router Pipeline and Allocators](/concepts/noc-router-pipeline-allocators.md), [NoC Router Pipeline Optimizations](/concepts/noc-router-pipeline-optimizations.md)。
* **Update**: [Switching Principles](/concepts/switching-principles.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md), [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md), [Topology Optimization Variants](/concepts/topology-optimization-variants.md), [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Cerebras WSE](/entities/cerebras-wse.md) — 流控/VC/流水线交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 27–30 → `raw/articles/arch-study-30d-day-27.md` … `day-30.md`（源：`openclawdata/.../arch-study-30d/day-27..30.md`）。
* **Creation**: [LLM Distributed Training Collectives](/concepts/llm-distributed-training-collectives.md), [Architecture Paper Reading Methodology](/concepts/architecture-paper-reading-methodology.md), [Post-Moore Architecture Frontiers](/concepts/post-moore-architecture-frontiers.md), [Arch-Study 30d Knowledge Map](/summaries/arch-study-30d-knowledge-map.md)。
* **Update**: [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md)（补 FRED/FREDR 笔记命名对照）, [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md), [Cerebras WSE](/entities/cerebras-wse.md), [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md), [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md), [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — Day 27–30 交叉引用。

## 2026-07-22
* **Ingest**: 4 篇 layout/NoC paper PDF → `raw/papers/MAERI_*`, `SIGMA_*`, `SmartMem_*`, `Venus_*`。
* **Creation**: [MAERI](/papers/maeri-flexible-dataflow-reconfigurable-interconnects.md), [SIGMA](/papers/sigma-sparse-gemm-flexible-interconnects.md), [SmartMem](/papers/smartmem-layout-transformation-elimination.md), [Venus](/papers/venus-versatile-reconfigurable-accelerator.md), [Layout-Aware NoC and Flexible Dataflow Accelerators](/concepts/layout-aware-noc-flexible-dataflow.md)。
* **Update**: [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — 新增 Gap 7 (layout-aware mesh GEMV) + 阶段 B 加 3 个新 pass。
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [FEATHER Accelerator](/concepts/feather-accelerator.md) — 反向链接到新概念页。
* **Validation**: `validate_bundle.py` 通过；11 个 index 自动重生成。

## 2026-07-09
* **Ingest**: Dally & Towles 互连网络 Day 13–14 → `raw/articles/interconn-study-21d-day-13.md`、`day-14.md`（源：`openclawdata/.../interconn-study-21d/day-13..14.md`）。
* **Creation**: [Deadlock-Free Routing CDG and Dally Theorem](/concepts/deadlock-free-routing-cdg-dally.md), [Duato Escape VC Deadlock-Free Routing](/concepts/duato-escape-vc-deadlock-free-routing.md).
* **Update**: [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md), [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Switching Principles](/concepts/switching-principles.md), [Cerebras WSE](/entities/cerebras-wse.md) — CDG/Dally、逃逸 VC、协议层死锁、Mesh vs Torus 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 25–26 → `raw/articles/arch-study-30d-day-25.md`、`day-26.md`（源：`openclawdata/.../arch-study-30d/day-25..26.md`）。
* **Creation**: [DNN Accelerator Systolic Dataflow](/concepts/dnn-accelerator-systolic-dataflow.md), [WSE Quantitative Architecture Analysis](/concepts/wse-quantitative-architecture-analysis.md).
* **Update**: [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md), [Plasticine Accelerator](/concepts/plasticine-accelerator.md), [Cerebras WSE](/entities/cerebras-wse.md), [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md), [WaferLLM System](/concepts/waferllm-system.md) — 脉动/WS·OS·RS、Amdahl/Roofline/Mesh 量化、SLA vs TPU 交叉引用。

## 2026-07-07
* **Creation**: [GEMM vs GEMV in LLM Inference](/concepts/gemm-vs-gemv.md) — 算子基础概念页：算术强度公式、Roofline、H100 decode <1% 峰值 FLOPS、prefill/decode 对应、编译器优化空间。
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [WaferLLM System](/concepts/waferllm-system.md), [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md) — 反向链接到新 GEMM vs GEMV 页。

* **Ingest**: 4 篇 paper PDF → `raw/papers/LoopLynx_*`, `SambaNova_SN40L_*`, `LLM_Inference_Acceleration_*`, `AI_Accelerators_LLM_*`（arXiv: 2504.09561, 2405.07518, 2410.04466, 2506.00008）。
* **Creation**: [LoopLynx](/papers/looplynx-scalable-dataflow-llm-inference.md), [SambaNova SN40L](/papers/sambanova-sn40l-dataflow-coe.md), [LLM Inference Hardware Survey](/papers/llm-inference-acceleration-comprehensive-hardware-survey.md), [AI Accelerators Cross-Architecture](/papers/ai-accelerators-llm-inference.md), [PagedAttention / vLLM](/concepts/pagedattention-vllm.md), [WaferLLM Compiler Research Gaps](/analyses/waferllm-compiler-research-gaps.md)。
* **Update**: [WaferLLM System](/concepts/waferllm-system.md) — 补 §7.5/§8 作者承认的 3 个未解瓶颈，[Cerebras WSE](/entities/cerebras-wse.md) — 新增 compiler research gaps 链接。
* **Validation**: `validate_bundle.py` 通过（4 个新 raw + 1 个新 analyses + 4 个新 paper 摘要 + 1 个新 concept）；11 个 index 自动重生成。

* **Ingest**: WaferLLM PDF → `raw/papers/WaferLLM_LLM_Inference_at_Wafer_Scale_2025.pdf`（Zotero: arXiv:2502.04563v3）。
* **Creation**: [WaferLLM System](/concepts/waferllm-system.md), [papers/waferllm-wafer-scale-llm-inference.md](/papers/waferllm-wafer-scale-llm-inference.md), `raw/papers/waferllm-wafer-scale-llm-inference.md`.
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [SpaDA Programming Language](/concepts/spada-programming-language.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — PLMR/MeshGEMM/V、KV shift、WSE LLM serving 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 24 → `raw/articles/arch-study-30d-day-24.md`（源：`openclawdata/.../arch-study-30d/day-24.md`）。
* **Creation**: [GPU SIMT Architecture](/concepts/gpu-simt-architecture.md).
* **Update**: [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md), [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md), [Branch Prediction](/concepts/branch-prediction.md), [DRAM and Memory System](/concepts/dram-memory-system.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — SIMT/Warp/Tensor Core、Roofline、WSE 对照交叉引用。
* **Ingest**: Dally & Towles 互连网络 Day 12 → `raw/articles/interconn-study-21d-day-12.md`（源：`openclawdata/.../interconn-study-21d/day-12.md`）。
* **Creation**: [Adaptive Routing for NoC](/concepts/adaptive-routing-noc.md).
* **Update**: [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Cerebras WSE](/entities/cerebras-wse.md) — 最小/VRR/VC、Duato 预告、DOR 选型交叉引用。

## 2026-07-06
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 9–11 → `raw/articles/interconn-study-21d-day-09.md`、`day-10.md`、`day-11.md`（源：`openclawdata/.../interconn-study-21d/day-09..11.md`）。
* **Creation**: [Topology Optimization Variants](/concepts/topology-optimization-variants.md), [Deterministic Routing and DOR](/concepts/deterministic-routing-dor.md).
* **Update**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md) — 六拓扑统一比较、选型决策树（Day 10）；[Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md), [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md), [Collective-Capable NoC](/concepts/collective-capable-noc.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Cerebras WSE](/entities/cerebras-wse.md) — Folding/CMesh/Express、Dally 1990、XY/e-cube 路由交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 21–23 → `raw/articles/arch-study-30d-day-21.md`、`day-22.md`、`day-23.md`（源：`openclawdata/.../arch-study-30d/day-21..23.md`）。
* **Creation**: [NoC Fundamentals (H&P Appendix F)](/concepts/noc-fundamentals-hp-appendix-f.md), [End-to-End Memory Data Path](/concepts/end-to-end-memory-data-path.md), [Multicore SMT and NUCA](/concepts/multicore-smt-nuca.md).
* **Update**: [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md), [DRAM and Memory System](/concepts/dram-memory-system.md), [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cache Coherence](/concepts/cache-coherence.md), [Memory Consistency Model](/concepts/memory-consistency-model.md), [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md), [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Cerebras WSE](/entities/cerebras-wse.md) — 存储篇综合、NoC 五问、SMT/NUCA/Amdahl 交叉引用。
* **Ingest**: TileLoom PDF → `raw/papers/TileLoom_Automatic_Dataflow_Planning_2026.pdf`（Zotero: arXiv:2512.22168v2）。
* **Creation**: [TileLoom Compiler](/concepts/tileloom-compiler.md), [papers/tileloom-automatic-dataflow-planning.md](/papers/tileloom-automatic-dataflow-planning.md), `raw/papers/tileloom-automatic-dataflow-planning.md`.
* **Update**: [SpaDA Programming Language](/concepts/spada-programming-language.md), [Plasticine Accelerator](/concepts/plasticine-accelerator.md), [Collective-Capable NoC](/concepts/collective-capable-noc.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md) — Triton/Helion dataflow planning vs WSE SpaDA 交叉引用。

## 2026-07-03
* **Ingest**: Constable 精读笔记 → `raw/reports/constable-deepdive.md`（源：`openclawdata/.../superscalar-cpu/constable-deepdive.md`）。
* **Creation**: [Constable Load Elimination](/concepts/constable-load-elimination.md), [papers/constable-load-elimination.md](/papers/constable-load-elimination.md).
* **Update**: [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — SLD/RMT/AMT、ISCA'24 Best Paper 交叉引用。
* **Ingest**: OpenClaw 超标量 CPU 研究综述 → `raw/reports/superscalar-cpu-final-report.md`、`raw/reports/superscalar-cpu-report.md`（源：`openclawdata/.../superscalar-cpu/FINAL-report.md`）。
* **Creation**: [Superscalar CPU Research (2023-2026)](/concepts/superscalar-cpu-research-2023-2026.md), [summaries/superscalar-cpu-research-2023-2026.md](/summaries/superscalar-cpu-research-2023-2026.md).
* **Update**: [Branch Prediction](/concepts/branch-prediction.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Cerebras WSE](/entities/cerebras-wse.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [Memory Consistency Model](/concepts/memory-consistency-model.md) — Constable/Bullseye/Prophet/CVA6S+ 与 WSE/LLM 交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 8 → `raw/articles/interconn-study-21d-day-08.md`（源：`openclawdata/.../interconn-study-21d/day-08.md`）。
* **Creation**: [Butterfly and MIN Topology](/concepts/butterfly-min-topology.md).
* **Update**: [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md), [Switching Networks](/concepts/switching-networks.md), [Flattened Butterfly Topology](/concepts/flattened-butterfly-topology.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md) — Butterfly/Omega/Banyan/Batcher-Banyan 与 Clos/Mesh 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 20 → `raw/articles/arch-study-30d-day-20.md`（源：`openclawdata/.../arch-study-30d/day-20.md`）。
* **Creation**: [SSD and NVMe Storage System](/concepts/ssd-nvme-storage-system.md).
* **Update**: [DRAM and Memory System](/concepts/dram-memory-system.md), [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md), [CMX & STX](/concepts/cmx-stx.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [Inference Capacity Trap](/concepts/inference-capacity-trap.md) — FTL/RAID/NVMe/io_uring、memoryX、KV tier 交叉引用。
* **Ingest**: 郑启航 知乎「分布式存储架构下的矩阵乘与编译器」→ `raw/articles/分布式存储架构下的矩阵乘与编译器.md`（已有 clippings；补 OKF frontmatter）。
* **Creation**: [Distributed GEMM Algorithms](/concepts/distributed-gemm-algorithms.md), [summaries/distributed-gemm-and-compiler.md](/summaries/distributed-gemm-and-compiler.md).
* **Update**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [Graphcore IPU](/entities/graphcore-ipu.md), [SpaDA Programming Language](/concepts/spada-programming-language.md) — Cannon/SUMMA/2.5D/3D GEMM 与 T10 rTensor 交叉引用。

## 2026-06-24
* **Ingest**: Rabenseifner 2004 MPI collective reduction ICCS PDF → `raw/papers/Rabenseifner_Collective_Reduction_Operations_2004.pdf`（Zotero: ICCS 2004, LNCS 3036）。
* **Creation**: [MPI Reduce/AllReduce Algorithms](/concepts/mpi-reduce-allreduce-algorithms.md), [papers/rabenseifner-collective-reduction-operations.md](/papers/rabenseifner-collective-reduction-operations.md), `raw/papers/rabenseifner-collective-reduction-operations.md`.
* **Update**: [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [Near-Optimal Wafer-Scale Reduce](/papers/near-optimal-wafer-scale-reduce.md) — MPI Ring/RHD 与 WSE collective 谱系交叉引用。
* **Ingest**: Aimuyo et al. 2025 FlashMoE NeurIPS PDF → `raw/papers/FlashMoE_Fast_Distributed_MoE_Single_Kernel_2025.pdf`（Zotero: arXiv:2506.04667）。
* **Creation**: [FlashMoE Kernel](/concepts/flashmoe-kernel.md), [papers/flashmoe-fast-distributed-moe-single-kernel.md](/papers/flashmoe-fast-distributed-moe-single-kernel.md), `raw/papers/flashmoe-fast-distributed-moe-single-kernel.md`.
* **Update**: [MegaMoE Kernel](/concepts/megamoe-kernel.md), [M2N Communication](/concepts/m2n-communication.md), [Disaggregated Inference](/concepts/disaggregated-inference.md), [Parallelism Transition Point](/concepts/parallelism-transition-point.md), [MegaScale-Infer](/papers/megascale-infer-2504.02263.md) — MoE EP kernel 栈交叉引用。
* **Ingest**: Shah et al. 2024 FlashAttention-3 PDF → `raw/papers/FlashAttention3_Asynchrony_Low_Precision_2024.pdf`（Zotero: arXiv:2407.08608）。
* **Creation**: [FlashAttention-3](/concepts/flashattention-3.md), [papers/flashattention-3-asynchrony-low-precision.md](/papers/flashattention-3-asynchrony-low-precision.md), `raw/papers/flashattention-3-asynchrony-low-precision.md`.
* **Update**: [FlashAttention](/concepts/flashattention.md), [FlashAttention-2](/concepts/flashattention-2.md), [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) — FA→FA2→FA3 谱系补全。
* **Ingest**: Dao et al. 2022 FlashAttention NeurIPS PDF → `raw/papers/FlashAttention_Fast_IO_Aware_Attention_2022.pdf`（Zotero: arXiv:2205.14135, NeurIPS 2022）。
* **Creation**: [FlashAttention](/concepts/flashattention.md), [papers/flashattention-io-aware-exact-attention.md](/papers/flashattention-io-aware-exact-attention.md), `raw/papers/flashattention-io-aware-exact-attention.md`.
* **Update**: [FlashAttention-2](/concepts/flashattention-2.md), [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md) — FA→FA2→FlashDecoding 谱系交叉引用。
* **Ingest**: Dao 2023 FlashAttention-2 PDF → `raw/papers/FlashAttention2_Faster_Attention_2023.pdf`（Zotero: arXiv:2307.08691）。
* **Creation**: [FlashAttention-2](/concepts/flashattention-2.md), [papers/flashattention-2-faster-attention.md](/papers/flashattention-2-faster-attention.md), `raw/papers/flashattention-2-faster-attention.md`.
* **Update**: [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md) — prefill attention vs decode kernel 栈交叉引用。
* **Ingest**: Hong et al. 2024 FlashDecoding++ PDF → `raw/papers/FlashDecoding_PlusPlus_LLM_Inference_GPUs_2024.pdf`（Zotero: arXiv:2311.01282）。
* **Creation**: [FlashDecoding++](/concepts/flashdecoding-plus-plus.md), [papers/flashdecoding-plus-plus-llm-gpu-inference.md](/papers/flashdecoding-plus-plus-llm-gpu-inference.md), `raw/papers/flashdecoding-plus-plus-llm-gpu-inference.md`.
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md), [Heterogeneous Inference](/concepts/heterogeneous-inference.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md) — decode kernel vs speculative/异构推理交叉引用。
* **Ingest**: Prabhakar et al. 2017 Plasticine ISCA PDF → `raw/papers/Plasticine_Reconfigurable_Parallel_Patterns_2017.pdf`（Zotero: ISCA 2017, DOI 10.1145/3079856.3080256）。
* **Creation**: [Plasticine Accelerator](/concepts/plasticine-accelerator.md), [papers/plasticine-reconfigurable-parallel-patterns.md](/papers/plasticine-reconfigurable-parallel-patterns.md), `raw/papers/plasticine-reconfigurable-parallel-patterns.md`.
* **Update**: [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md), [SpaDA Programming Language](/concepts/spada-programming-language.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [FEATHER Accelerator](/concepts/feather-accelerator.md), [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md) — parallel patterns CGRA、dataflow 谱系交叉引用。
* **Ingest**: Chen et al. 2017 Eyeriss JSSC PDF → `raw/papers/Eyeriss_Energy_Efficient_CNN_Accelerator_2017.pdf`（Zotero: JSSC 2017, DOI 10.1109/JSSC.2016.2616357）。
* **Creation**: [Eyeriss Accelerator](/concepts/eyeriss-accelerator.md), [papers/eyeriss-energy-efficient-cnn-accelerator.md](/papers/eyeriss-energy-efficient-cnn-accelerator.md), `raw/papers/eyeriss-energy-efficient-cnn-accelerator.md`.
* **Update**: [FEATHER Accelerator](/concepts/feather-accelerator.md), [papers/feather-reconfigurable-accelerator.md](/papers/feather-reconfigurable-accelerator.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Collective-Capable NoC](/concepts/collective-capable-noc.md), [NoC Router 微架构](/concepts/noc-router-microarchitecture.md) — RS dataflow、GIN 组播 NoC、FEATHER 固定基线交叉引用。
* **Ingest**: Dennis & Misunas 1975 basic data-flow processor PDF → `raw/papers/Dennis_Misunas_Basic_Data_Flow_Processor_1975.pdf`（Zotero: ISCA 1975, ACM 641675.642111）。
* **Creation**: [Basic Data-Flow Processor](/concepts/basic-data-flow-processor.md), [papers/dennis-misunas-basic-data-flow-processor.md](/papers/dennis-misunas-basic-data-flow-processor.md), `raw/papers/dennis-misunas-basic-data-flow-processor.md`.
* **Update**: [Deterministic Execution](/concepts/deterministic-execution.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md), [SpaDA Programming Language](/concepts/spada-programming-language.md), [Cerebras WSE](/entities/cerebras-wse.md) — 数据流架构历史交叉引用。
* **Update**: [Collective-Capable NoC](/concepts/collective-capable-noc.md), [papers/collective-capable-noc-ml-accelerators.md](/papers/collective-capable-noc-ml-accelerators.md) — 扩充 DCA 范式。
* **Ingest**: Colagrande et al. 2026 collective-capable NoC PDF → `raw/papers/Collective_Capable_NoC_ML_Accelerators_2026.pdf`（Zotero: MLSys 2026, arXiv:2603.26438）。
* **Creation**: [Collective-Capable NoC](/concepts/collective-capable-noc.md), [papers/collective-capable-noc-ml-accelerators.md](/papers/collective-capable-noc-ml-accelerators.md), `raw/papers/collective-capable-noc-ml-accelerators.md`.
* **Update**: [NoC Router 微架构](/concepts/noc-router-microarchitecture.md), [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Memory Consistency Model](/concepts/memory-consistency-model.md), [Cerebras WSE](/entities/cerebras-wse.md) — FlooNoC multicast/reduction/DCA/barrier 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 19 → `raw/articles/arch-study-30d-day-19.md`.
* **Creation**: [Memory Consistency Model](/concepts/memory-consistency-model.md).
* **Update**: [Cache Coherence](/concepts/cache-coherence.md), [Memory Fence and Barrier](/concepts/memory-fence-barrier.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Deterministic Execution](/concepts/deterministic-execution.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Cerebras WSE](/entities/cerebras-wse.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md) — SC/TSO/ARM、fence、CAS/MCS 锁、WSE barrier 交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 7 → `raw/articles/interconn-study-21d-day-07.md`.
* **Creation**: [Clos and Fat-Tree Topology](/concepts/clos-fat-tree-topology.md).
* **Update**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md), [Switching Networks](/concepts/switching-networks.md), [Multi-plane Clos Topology for AI Training](/concepts/multi-plane-clos-topology.md) — Clos 定理、Fat-Tree、间接网络交叉引用。
* **Ingest**: FEATHER 论文 PDF → `raw/papers/FEATHER_Reconfigurable_Accelerator_Dataflow_Switching_2024.pdf`（Zotero: Tong et al. 2024, arXiv:2405.13170）。
* **Creation**: [FEATHER Accelerator](/concepts/feather-accelerator.md), [papers/feather-reconfigurable-accelerator.md](/papers/feather-reconfigurable-accelerator.md), `raw/papers/feather-reconfigurable-accelerator.md`.
* **Update**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [SpaDA Programming Language](/concepts/spada-programming-language.md) — dataflow/layout 可重构交叉引用。
* **Ingest**: SpaDA 论文 PDF → `raw/papers/SpaDA_Spatial_Dataflow_Architecture_Programming_Language_2026.pdf`（Zotero: Gianinazzi et al. 2026, arXiv:2511.09447）。
* **Creation**: [SpaDA Programming Language](/concepts/spada-programming-language.md), [papers/spada-spatial-dataflow-architecture.md](/papers/spada-spatial-dataflow-architecture.md), `raw/papers/spada-spatial-dataflow-architecture.md`.
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md), [Cerebras Color Mechanism](/concepts/cerebras-color-mechanism.md), [WSE Reduce Algorithms](/concepts/wse-reduce-algorithms.md), [Cache Coherence](/concepts/cache-coherence.md) — SpaDA/CSL 编程模型交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 6 → `raw/articles/interconn-study-21d-day-06.md`.
* **Creation**: [Mesh and Torus Topology](/concepts/mesh-torus-topology.md).
* **Update**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Linear and Ring Topology](/concepts/linear-ring-topology.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md) — 2-D Mesh/Torus、k-ary n-cube、Dally d_opt 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 18 → `raw/articles/arch-study-30d-day-18.md`.
* **Creation**: [Cache Coherence](/concepts/cache-coherence.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [Memory Fence and Barrier](/concepts/memory-fence-barrier.md), [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [Cerebras WSE](/entities/cerebras-wse.md) — MESI/Snooping/Directory/False Sharing 交叉引用。
* **Ingest**: 体系结构 30 天学习笔记 Day 17 → `raw/articles/arch-study-30d-day-17.md`.
* **Creation**: [DRAM and Memory System](/concepts/dram-memory-system.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md) — DRAM/HBM/内存墙交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 5 → `raw/articles/interconn-study-21d-day-05.md`.
* **Creation**: [Linear and Ring Topology](/concepts/linear-ring-topology.md).
* **Update**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md) — 1-D 基线、TileLink Ring 交叉引用。
* **Ingest**: DSpark 论文 PDF → `raw/papers/DSpark_Confidence-Scheduled_Speculative_Decoding_2026.pdf`（Zotero: Cheng et al. 2026）。
* **Creation**: [DSpark Speculative Decoding](/concepts/dspark-speculative-decoding.md), [papers/dspark-speculative-decoding.md](/papers/dspark-speculative-decoding.md), `raw/papers/dspark-speculative-decoding.md`.
* **Update**: [DeepSeek-V4](/entities/deepseek-v4.md), [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md), [Heterogeneous Inference](/concepts/heterogeneous-inference.md) — speculative decode 交叉引用。
* **Ingest**: Memory Fence 深度研究报告 → `raw/articles/memory-fence-hardware-2026-06-28.md`（源：`openclawdata/.../notes/reports/`）。
* **Creation**: [Memory Fence and Barrier](/concepts/memory-fence-barrier.md).
* **Update**: [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Deterministic Execution](/concepts/deterministic-execution.md), [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md), [ISA Design Principles](/concepts/isa-design-principles.md), [Cerebras WSE](/entities/cerebras-wse.md) — fence/coherence 交叉引用。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 3–4 → `raw/articles/interconn-study-21d-day-03.md`, `interconn-study-21d-day-04.md`.
* **Creation**: [Interconnection Topology Metrics](/concepts/interconnection-topology-metrics.md), [Interconnection Network Cost Model](/concepts/interconnection-network-cost-model.md).
* **Update**: [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Cerebras WSE](/entities/cerebras-wse.md) — 拓扑度量、延迟/B_b 模型、Mesh vs Torus 权衡。
* **Ingest**: 体系结构 30 天学习笔记 Day 15–16 → `raw/articles/arch-study-30d-day-15.md`, `arch-study-30d-day-16.md`.
* **Creation**: [Virtual Memory and TLB](/concepts/virtual-memory-tlb.md), [DSA Processor Design Tradeoffs](/concepts/dsa-processor-design-tradeoffs.md).
* **Update**: [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md), [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md) — TLB/核心篇总结交叉引用。
* **Ingest**: Hennessy & Patterson 30 天体系结构学习笔记 Day 1–14 → `raw/articles/arch-study-30d-day-*.md`（14 文件）。
* **Creation**: [Quantitative Architecture Fundamentals](/concepts/quantitative-architecture-fundamentals.md), [ISA Design Principles](/concepts/isa-design-principles.md), [Numeric Formats for AI Hardware](/concepts/numeric-formats-ai-hardware.md), [Architecture Benchmark Methodology](/concepts/architecture-benchmark-methodology.md), [CPU Pipeline Fundamentals](/concepts/cpu-pipeline-fundamentals.md), [Instruction-Level Parallelism](/concepts/instruction-level-parallelism.md), [Out-of-Order Execution](/concepts/out-of-order-execution.md), [Branch Prediction](/concepts/branch-prediction.md), [Memory Hierarchy and Cache](/concepts/memory-hierarchy-cache.md).
* **Update**: [Cerebras WSE](/entities/cerebras-wse.md), [Deterministic Execution](/concepts/deterministic-execution.md), [FP4 Quantization-Aware Training](/concepts/fp4-qat.md) — 与 CPU 体系结构概念交叉引用。
* **Schema**: 标签 taxonomy 新增 `isa`, `pipeline`, `cache`, `power`。
* **Ingest**: Dally & Towles 互连网络 21 天学习笔记 Day 1–2 → `raw/articles/interconn-study-21d-day-01.md`, `interconn-study-21d-day-02.md`.
* **Creation**: [Interconnection Network Design Space](/concepts/interconnection-network-design-space.md), [Interconnection Network Protocol Stack](/concepts/interconnection-network-protocol-stack.md).
* **Update**: [Switching Principles](/concepts/switching-principles.md) — 报文/虫孔交换、历史里程碑；[Cerebras WSE](/entities/cerebras-wse.md) — Mesh 度量与虫孔选型。
* **Schema**: 标签 taxonomy 新增 `interconnect`。
* **Cleanup**: 删除重复的 `references/raw/`（OKF 转换副本）；唯一原始资料目录为 `raw/`。`megascale-infer-2504.02263.pdf`、`cassini-network-aware-scheduling-2308.00852.pdf` 本就位于 `raw/papers/`（与 `references/raw/papers/` 为同内容副本），无需迁移。
* **Docs**: README 与 OKF skill 统一为仅使用 `raw/`。
* **Creation**: [Graphcore IPU](/entities/graphcore-ipu.md), [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md).
* **Update**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md), [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 交叉引用拆分页。
* **Schema**: 标签 taxonomy 新增 `graphcore`。
* **Ingest**: [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) from `raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf` (arXiv:2604.26821).
* **Creation**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md).
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 3D chip prefill/decode 设计空间差异。
* **Creation**: Converted LLM wiki at `/home/luke/wiki` to OKF v0.1 bundle (54 work pages + raw sources).
* **Source**: Karpathy-style LLM wiki (entities, concepts, papers, summaries, analyses).
* **Update**: Generated interactive `viz.html` (74 concepts, 237 cross-links).
