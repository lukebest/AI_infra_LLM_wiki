---
type: Raw Source
title: Understanding Silent Data Corruptions in a Large Production CPU Population
source_path: /home/luke/wiki/raw/papers/Silent_Data_Corruptions_Production_CPU_2023.pdf
doi: '10.1145/3600006.3613149'
zotero: 89UG7I3S
ingested: 2026-07-17
sha256: 4303d2b4b90e09db3104473480faa094a1085b89ae79c16ed7c07bf221b292c0
---

# Understanding Silent Data Corruptions in a Large Production CPU Population

Authors: Shaobu Wang, Guangyan Zhang, Junyu Wei (Tsinghua); Yang Wang (Ohio State); Jiesheng Wu, Qingchao Luo (Alibaba Cloud)
Venue: SOSP 2023 | DOI: 10.1145/3600006.3613149

Structured notes / key excerpts:

- **Scope**: **>1M CPUs**, 28 DCs, 14 countries, 32 months testing (Alibaba Cloud); 633 vendor testcases.
- **SDC rate**: Overall **3.61‱** faulty; pre-production **3.262‱** (90.36% of all faults); regular in-production **0.348‱**.
- **Vulnerable features**: Cache coherence, FP, vector ops; FP SDCs often bitflip in fraction (small accuracy loss → hard to detect).
- **Reproducibility**: Some highly reproducible; others temperature/workload dependent.
- **Production cases**: Checksum mismatch (faulty instruction), cache coherence inconsistency, hash map assertion failures.
- **Farron mitigation**: Prioritized testing for reproducible SDCs + temperature control for sporadic ones; better coverage/lower overhead vs Alibaba baseline.
- **Comparison**: Consistent with Google/Meta order-of-magnitude reports but more precise rates.
