# Bundle Update Log

## 2026-06-24
* **Cleanup**: 删除重复的 `references/raw/`（OKF 转换副本）；唯一原始资料目录为 `raw/`。
* **Migration**: `megascale-infer-2504.02263.pdf`、`cassini-network-aware-scheduling-2308.00852.pdf` 迁入 `raw/papers/`。
* **Docs**: README 与 OKF skill 统一为仅使用 `raw/`。

## 2026-06-24
* **Creation**: [Graphcore IPU](/entities/graphcore-ipu.md), [Core Group (DRAM Access Synchronization)](/concepts/core-group-dram-access.md).
* **Update**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md), [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) — 交叉引用拆分页。
* **Schema**: 标签 taxonomy 新增 `graphcore`。

## 2026-06-24
* **Ingest**: [Voxel 3D-Stacked AI Chip LLM Inference](/papers/voxel-3d-stacked-ai-chip-llm-inference.md) from `raw/papers/Exploring the efficiency of 3D-stacked AI chip architecture for LLM inference with voxel.pdf` (arXiv:2604.26821).
* **Creation**: [3D-Stacked AI Chip](/concepts/3d-stacked-ai-chip.md), [Voxel Simulator](/concepts/voxel-simulator.md).
* **Update**: [Prefill-Decode Resource Divergence](/concepts/prefill-decode-divergence.md) — 3D chip prefill/decode 设计空间差异。

## 2026-06-24
* **Creation**: Converted LLM wiki at `/home/luke/wiki` to OKF v0.1 bundle (54 work pages + raw sources).
* **Source**: Karpathy-style LLM wiki (entities, concepts, papers, summaries, analyses).
* **Update**: Generated interactive `viz.html` (74 concepts, 237 cross-links).
