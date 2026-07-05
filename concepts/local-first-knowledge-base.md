---
type: concept
tags: [knowledge-base, markdown, local-first]
---

# 概念：本地优先知识库

## 一句话解释

本地优先知识库以本地 Markdown 文件作为知识源，优先保证数据可控、可迁移、可搜索，再逐步叠加全文索引、向量检索和云端扩展。

## 核心原则

- Markdown 是源格式。
- 本地文件系统和 Git 是基础。
- Obsidian、VS Code、Claude Code 都可直接读写。
- 后续可扩展 SQLite FTS、Chroma/Qdrant、S3/R2、Docusaurus 等能力。
