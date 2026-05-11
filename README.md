# LLM Wiki

本仓库是一个基于 [**Hermes Agent 的 `llm-wiki` skill**](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md) 搭建的 **LLM Wiki**：用互相链接的 Markdown 页面持续沉淀知识，而不是把结论留在单次对话里。

入门思路与整体叙事可参考 [**Karpathy Wiki（中文导读）**](https://karpathy-wiki.lol/zh)，它与 Andrej Karpathy 提出的「LLM Wiki」工作方式一脉相承；原始gist见 [LLM Wiki by Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

---

## Karpathy 知识库的核心理念

传统 **RAG** 往往在每次提问时从切片语料里临时检索并拼装答案；**Karpathy Wiki 模式**则强调 **先把跨资料的综合写进可维护的产物**，让之后的问答站在上一次整理过的结果上继续演进。

可以概括为几点：

- **沉淀而非反复从零推导**：高质量摘要、对比与结论写入页面；新资料进入时在已有页面上修订，而不是每次都从头拼一遍。
- **人机分工**：人负责选题、筛选资料与判断优先级；模型负责摘要、交叉引用、归档与一致性维护（具体目录与约定见仓库内的 `SCHEMA.md`）。
- **资料层与工作层分离**：原始材料放在不可随意改写的资料区（如 `raw/`），Wiki 页作为工作层吸收、评议与链接；Schema（如 `SCHEMA.md`）约束结构与标签，避免笔记发散成噪声。
- **矛盾与演进可追溯**：冲突信息记在相关页面或 frontmatter 中，配合日志（`log.md`），便于复核而不是被静默覆盖。
- **答案可复用**：有价值的问答可以回填为 `queries/`、`comparisons/` 等页面，避免优质推理只存在于聊天记录里。

一句话：**RAG 偏重「检索时的召回」，Karpathy Wiki 偏重「长期编译后的知识状态」。**

---

## 本仓库的目的：团体知识协作与共享

本 Wiki 面向 **团队共同维护与使用**：

- **共享同一套结构与术语**（见 `SCHEMA.md`、`index.md`），减少各人笔记孤岛与重复劳动。
- **协作增量**：新成员可通过索引与图谱快速定位主题； ingest / 更新 / lint 式的维护可由人或 Agent 按约定执行，变更记录在 `log.md`。
- **知识归属清晰**：资料来源与页面引用可追溯，便于评审、对齐与后续迭代。

仓库内的领域范围与标签体系以 `SCHEMA.md` 为准；若你希望扩展领域或协作流程（分支策略、评审门槛），建议在 Schema 或团队约定中显式写明，以便人机协作一致。

---

## 仓库导航（简要）

| 路径 | 作用 |
|------|------|
| `SCHEMA.md` | 领域、命名、标签与更新策略 |
| `index.md` | 内容目录与一页摘要 |
| `log.md` | 按时间记录的操作日志 |
| `raw/` | 原始资料（摄取后原则上不改写正文） |
| `entities/`、`concepts/` 等 | Wiki 工作层页面 |

本地可与 Obsidian 等 Markdown 工具配合使用；环境与路径约定可参考 Hermes skill 中的 `WIKI_PATH` 说明。

---

## 许可证与致谢

- Wiki **工作方法**来自 Karpathy 的 LLM Wiki 理念及 Hermes **`llm-wiki`** skill 的实践整理。
- 本 README 仅描述仓库用途与哲学背景；具体页面的版权声明与引用请以各 `raw/` 文件及页面 `sources` 为准。
