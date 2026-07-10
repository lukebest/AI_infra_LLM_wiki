# LLM Wiki

本仓库是一个 **Open Knowledge Format (OKF)** 知识库：在 Karpathy LLM Wiki 的沉淀理念之上，用带 YAML frontmatter 的 Markdown 概念页持续编译 AI 基础设施领域知识。日常 **摄取、更新与查询** 通过仓库自带的 [`.cursor/skills/okf-knowledge-base`](.cursor/skills/okf-knowledge-base/SKILL.md) skill 在 Cursor 等 Agent 中执行。

理念来源：[Karpathy Wiki（中文导读）](https://karpathy-wiki.lol/zh) / [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)；格式参考 [Google Knowledge Catalog OKF](https://github.com/google/knowledge-catalog)。上游 Hermes [`llm-wiki` skill](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md) 仍是相近工作流的参考实现。

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
- **协作增量**：新成员可通过索引与图谱快速定位主题；ingest / 更新 / 校验可由 Cursor Agent 按 OKF skill 执行，变更记录在 `log.md`。
- **知识归属清晰**：资料来源与页面引用可追溯，便于评审、对齐与后续迭代。

仓库内的领域范围与标签体系以 `SCHEMA.md` 为准；若你希望扩展领域或协作流程（分支策略、评审门槛），建议在 Schema 或团队约定中显式写明，以便人机协作一致。

---

## 快速开始：克隆仓库并用 OKF skill 增量维护

下面是一条完整路径：**克隆本仓库 → 用 Cursor 打开 → 让 Agent 加载 `.cursor/skills/okf-knowledge-base` → 在已有 OKF bundle 上 ingest 新资料**。

Skill 定义见 [`.cursor/skills/okf-knowledge-base/SKILL.md`](.cursor/skills/okf-knowledge-base/SKILL.md)；本仓库本身即是一个 OKF bundle（`entities/`、`concepts/`、`papers/` 等目录 + 各目录 `index.md` + 根目录 `log.md`）。

### 1. 克隆本仓库

在你希望存放知识库的目录执行（将 URL 换成你 fork 后的地址亦可）。在 **`git clone` 末尾写上目录名 `wiki`**：

```bash
git clone https://github.com/lukebest/AI_infra_LLM_wiki.git wiki
cd wiki
```

若使用 SSH：

```bash
git clone git@github.com:lukebest/AI_infra_LLM_wiki.git wiki
cd wiki
```

确认根目录下已有 `SCHEMA.md`、`index.md`、`log.md` 以及 `entities/`、`concepts/`、`raw/` 等——说明这是**已有内容**的知识库，后续只做增量 enrich。

### 2. 用 Cursor 打开并启用 OKF skill

1. 在 Cursor 中 **Open Folder**，选择刚克隆的 `wiki` 目录。
2. Skill 已随仓库位于 **`.cursor/skills/okf-knowledge-base/`**，Cursor 会在本项目中自动发现；无需单独安装 Hermes Hub 或配置 `WIKI_PATH`。
3. 新开 Agent 对话时，可直接说明：「按 OKF knowledge base skill 操作本仓库。」

可选：将 [`SKILL.md`](.cursor/skills/okf-knowledge-base/SKILL.md) 中的「Enrich Existing OKF Bundle」要点写入项目 `.cursor/rules`，减少每次重复说明。

### 3. 增量维护的典型流程（每次有新资料）

对应 skill 中的 **Workflow 3: Enrich Existing OKF Bundle**：

1. **同步团队最新内容（可选但推荐）**
   ```bash
   cd wiki
   git pull
   ```

2. **定向（Orient）**  
   让 Agent 先读 `SCHEMA.md`、各目录 `index.md`（或根 `index.md`）、`log.md` 近期条目，并搜索是否已有相关 concept，避免重复建页。

3. **摄取（Ingest）**  
   向 Agent 提供 URL、PDF、文件路径或粘贴正文，示例话术：
   - 「采用 OKF skill，把 `raw/papers/xxx.pdf` 加入本知识库」
   - 「按 OKF skill ingest 这篇资料，更新相关 entities/concepts」

   Agent 应按 skill 执行：
   - 原文保留在 `raw/`（`articles/`、`papers/` 等子目录；摄取后原则上不改写正文）
   - 按 `SCHEMA.md` 阈值 **新建或更新** concept 页（frontmatter 含 `type`、`title`、`description`、`tags`、`timestamp`）
   - 页面内至少 **2 条** bundle 相对路径交叉链接，并写 `# Citations`
   - 更新对应目录的 `index.md` 与根 `log.md`

4. **校验（Validate，可选）**
   ```bash
   python .cursor/skills/okf-knowledge-base/scripts/validate_bundle.py .
   python .cursor/skills/okf-knowledge-base/scripts/generate_indexes.py .
   ```
   修复缺失 `type`、frontmatter 解析错误等问题后再提交。

5. **提交并推送（团体协作）**
   ```bash
   git status
   git add -A
   git commit -m "wiki: ingest <简短说明>"
   git push
   ```

**增量**体现在：新资料进入 `raw/`，concept 页与索引在原有基础上追加与修订，并通过 Git 与他人合并。

---

## 使用 OKF knowledge base skill 维护知识库

**前提：** 请先完成上一节 **「快速开始」**（克隆仓库并在 Cursor 中打开）。

Skill 路径：[`.cursor/skills/okf-knowledge-base/SKILL.md`](.cursor/skills/okf-knowledge-base/SKILL.md)。以下聚焦本仓库上的 **摄取、enrich 与校验**；OKF 规范摘要见 skill 内 [`references/okf-spec-summary.md`](.cursor/skills/okf-knowledge-base/references/okf-spec-summary.md)。

### 1. Skill 何时激活

在 Cursor 对话中提到以下意图时，Agent 应读取并遵循该 skill：

- ingest / 加入 / 更新知识库、处理 `raw/` 下新资料
- OKF、Knowledge Bundle、concept 页创建或 enrich
- 校验 bundle、生成 index、知识库健康检查

### 2. 核心操作（由你在对话里发起）

| 操作 | 示例话术 | Agent 按 skill 做的事 |
|------|----------|------------------------|
| **摄取 ingest** | 「用 OKF skill 把这篇 PDF 加入 wiki」 | 读 `SCHEMA.md` + index → 写/更新 `entities/`、`concepts/`、`papers/` 等 → 更新 `index.md`、`log.md` |
| **Enrich 已有页** | 「把新来源合并进 [[某 concept]]」 | 更新 frontmatter `timestamp`、正文与 `# Citations`，补交叉链接 |
| **校验 validate** | 「对 bundle 做 OKF 校验」 | 运行 `validate_bundle.py`，报告缺失 `type` 等问题 |
| **查询 query** | 「根据 wiki 回答…并引用页面」 | 读 index → 定位 concept → 综合回答；高价值结论可新建 `papers/` 或 `analyses/` 页并记 log |

**注意：** `raw/` 摄取后视为不可原地改写；修订结论写在 concept 工作层。

### 3. Concept 页约定（OKF + 本仓库 SCHEMA）

- **必填 frontmatter（OKF）：** `type`（如 `Entity`、`Concept`、`Summary`）
- **推荐：** `title`、`description`、`tags`、`timestamp`（ISO 8601）；扩展字段 `sources`、`created` 可保留
- **交叉链接：** 使用 bundle 相对路径，如 `[Cerebras WSE](/entities/cerebras-wse.md)`
- **标签：** 须出现在 `SCHEMA.md` 的 taxonomy 中；新标签先写入 SCHEMA 再使用

### 4. 实用脚本（skill 自带）

在仓库根目录执行：

```bash
# 校验 frontmatter / type
python .cursor/skills/okf-knowledge-base/scripts/validate_bundle.py .

# 重新生成各目录 index.md
python .cursor/skills/okf-knowledge-base/scripts/generate_indexes.py .

# 生成交互式概念关系图 viz.html（可选）
python .cursor/skills/okf-knowledge-base/scripts/generate_viz.py .

# 生成可部署的静态站（默认输出 site/，面向 https://lukebest.github.io/）
python .cursor/skills/okf-knowledge-base/scripts/generate_site.py . --out site --base-path ""
```

公开站点：<https://lukebest.github.io/>（由 `generate_site.py` 生成后推送到 [`lukebest/lukebest.github.io`](https://github.com/lukebest/lukebest.github.io) 仓库根目录，覆盖原博客）。

---

## 使用 Agent 查询知识库

查询的本质：**先从已编译的 OKF concept 页作答**，必要时再补充外部检索；高价值回答可回填为 `papers/`、`analyses/` 等页面并记入 `log.md`。

### Cursor（推荐）

- **打开本仓库为工作区**，对话中说明：「先读 SCHEMA、index、近期 log，再按 OKF skill 查询。」
- 示例：「根据 wiki 总结 [某概念] 与 [另一实体] 的关系，引用 `/concepts/` 与 `/entities/` 页面。」
- Agent 流程：**读 `index.md` → 搜索关键词 → 读相关 concept → 回答并标注路径链接**。

### OpenClaw、Hermes 与其它 Agent

将 **本仓库挂载为可读工作区**，在系统提示中固定：

1. 先读 `SCHEMA.md`、各目录 `index.md`、近期 `log.md`。
2. 只读/写工作层（`entities/`、`concepts/`、`papers/` 等），**勿改写 `raw/` 原文**。
3. 回答须引用实际读到的 concept；持久结论写入 bundle 并更新 `index.md` / `log.md`。

若使用 Hermes，也可额外加载上游 [`llm-wiki` skill](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md) 并将 `WIKI_PATH` 指向克隆目录；Cursor 用户**无需**此步骤。

### 人工快速查阅

用编辑器或 Obsidian 打开本目录，从各目录 `index.md` 跳转；复杂主题可全文搜索 `*.md`。

---

## 仓库导航（简要）

| 路径 | 作用 |
|------|------|
| `.cursor/skills/okf-knowledge-base/` | OKF 维护 skill（`SKILL.md` + 校验/索引脚本） |
| `SCHEMA.md` | 领域、命名、标签与更新策略 |
| `index.md` | 根目录与子目录内容索引 |
| `log.md` | 按时间记录的操作日志 |
| `raw/` | 原始资料（摄取后原则上不改写正文） |
| `entities/`、`concepts/`、`papers/` 等 | OKF concept 工作层页面 |

本地可与 Obsidian 等 Markdown 工具配合使用；维护与查询流程见上文 **「快速开始」** 与 **「使用 OKF knowledge base skill」**。

---

## 许可证与致谢

- 知识沉淀理念来自 Karpathy LLM Wiki；**OKF 格式与维护流程**见 [`.cursor/skills/okf-knowledge-base`](.cursor/skills/okf-knowledge-base/SKILL.md) 与 [Google Knowledge Catalog](https://github.com/google/knowledge-catalog)。
- 本 README 仅描述仓库用途与哲学背景；具体页面的版权声明与引用请以各 `raw/` 文件及页面 `sources` 为准。
