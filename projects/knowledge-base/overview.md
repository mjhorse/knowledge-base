---
type: project_summary
project: knowledge-base
date: 2026-07-05
tags:
  - knowledge-base
  - obsidian
  - github
  - git
status: active
---

# 本地知识库建设与同步配置

## 背景

本地知识库用于沉淀日常工作要点、项目阶段成果、概念知识、排障经验、决策记录和可复用操作手册。第一阶段采用 Markdown + Git + Obsidian 的本地优先方案，后续可扩展到云端仓库、全文索引或语义检索。

## 本阶段目标

- 将 `/Users/mjhorse/knowledge-base` 作为 Obsidian Vault 使用。
- 将知识库关联到 GitHub 远程仓库。
- 配置 Obsidian Git 插件，实现自动本地提交和远程同步。
- 配置 Obsidian Copilot 使用 Claude Code 同源 Claude 模型。
- 增加适合 Obsidian 的 `.gitignore`，避免提交本机状态、缓存和密钥文件。
- 增加 daily note 日记链接锚点，让阶段成果可以按日期回顾并形成 Obsidian 双链。

## 已完成事项

- 安装并打开 Obsidian。
- 使用 Obsidian 打开 `/Users/mjhorse/knowledge-base` 作为 Vault。
- 在 GitHub 创建并关联远程仓库：`git@github.com:mjhorse/knowledge-base.git`。
- 将本地知识库 `main` 分支推送到 `origin/main`。
- 安装并启用 Obsidian Git 插件。
- 配置 Obsidian Git 自动提交与推送策略。
- 新增 `.gitignore` 并推送到远程仓库。
- 安装 Copilot 插件，并确认 `claude-sonnet-4-6 | anthropic` 可用。
- 更新知识库 capture/query skills：录入时维护 daily note 双锚点链接，查询时将这些链接作为时间线索引。

## 当前建议配置

- Auto commit interval：`10` 分钟。
- Auto push interval：`60` 分钟。
- Pull on startup：开启。
- Auto pull interval：单机使用可设为 `0`。
- 重要变更后优先使用 `Obsidian Git: Sync` 手动同步。

## 关键结论

- Obsidian Git 插件不负责配置远程仓库；远程仓库需要在 Git 仓库层面配置。
- `Auto commit interval` 是本地提交频率，不会直接上传到 GitHub。
- `Auto push interval` 是远程推送频率，会把本地已提交内容上传到 GitHub。
- `Sync` 比单独 `Push` 更适合作为手动同步命令，因为它通常会同时处理拉取、提交和推送。
- Copilot 接入 Claude Code 同源模型时，`claude-sonnet-4-6` 应使用 Anthropic provider；OpenAI-compatible provider 对该模型不可用。
- 日记链接使用 `<!-- notehelper-links -->` 双锚点，知识库录入时在锚点之间插入去重后的 Obsidian wikilinks。

## 产出物

- 知识库目录：`/Users/mjhorse/knowledge-base`
- GitHub 远程仓库：`git@github.com:mjhorse/knowledge-base.git`
- Git 忽略规则：`/Users/mjhorse/knowledge-base/.gitignore`
- 操作手册：`playbooks/setup-obsidian-git-sync.md`
- 排障记录：`troubleshooting/obsidian-homebrew-download-failed.md`
- Copilot 配置手册：`playbooks/configure-obsidian-copilot-claude.md`
- Daily note 模板：`templates/daily-note-template.md`
- Knowledge wiki skills：`/Users/mjhorse/.claude/skills/knowledge-wiki-capture/SKILL.md`、`/Users/mjhorse/.claude/skills/knowledge-wiki-query/SKILL.md`

## 下一步

- 持续使用 `knowledge-wiki-capture` 将阶段成果、概念和排障经验录入知识库。
- 定期确认 Obsidian Git 自动同步是否成功。
- 后续如果多设备编辑，再打开更频繁的自动 pull 或处理冲突流程。
