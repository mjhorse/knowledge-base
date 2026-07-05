---
type: adr
status: accepted
date: 2026-07-05
tags: [knowledge-base, markdown, local-first]
---

# ADR-0001：使用 Markdown 作为知识库源格式

## 状态

Accepted

## 背景

需要构建一个本地优先的知识库，用于沉淀日常工作要点、项目阶段成果、概念、排障经验和产出物索引，并支持后续 AI 查询和云端扩展。

## 决策

使用 Markdown 文件作为知识库的源格式，目录结构按 `daily/projects/concepts/decisions/playbooks/troubleshooting/assets/templates` 划分。

## 原因

- 本地可控，不依赖单一平台。
- 可用 Obsidian、VS Code、Claude Code 直接读写。
- Git 友好，便于版本追踪。
- 后续可平滑扩展到全文检索、向量检索和云端 Wiki。

## 替代方案

- Notion：协作体验好，但平台锁定明显。
- Confluence：适合团队，但个人本地优先场景较重。
- 直接数据库：查询强，但编辑和迁移不如 Markdown 简单。

## 影响

第一阶段优先保证知识资产稳定和可迁移，暂不引入复杂数据库或向量索引。
