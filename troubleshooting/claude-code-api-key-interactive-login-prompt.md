---
type: troubleshooting
project: Claude Code 本地开发环境
date: 2026-07-12
tags: [claude-code, api-key, authentication, zsh]
severity: medium
status: resolved
---

# 问题：Claude Code 交互界面提示 `/login`，但 API Key 非交互调用正常

## 现象

- 新启动的 Claude Code 交互式会话状态栏显示 `Not logged in · Run /login`；发送消息后提示 `Not logged in · Please run /login`。
- 同一交互式 zsh 环境中，`claude auth status` 显示 API Key 认证正常，且 `claude -p` 能得到正常模型响应。

## 环境

- macOS，交互式 zsh。
- Claude Code 使用 `ANTHROPIC_API_KEY` 与自定义 `ANTHROPIC_BASE_URL`。
- Claude Code 旧版与 Homebrew 安装版均复现该交互式提示，因此不是 CLI 版本差异本身造成。

## 影响范围

- 新开的交互式 Claude Code 会话无法发送任务。
- 已在运行的会话、API Key、路由、Langfuse、本地项目与会话记录不受影响。

## 排查过程

1. 验证环境变量已由交互式 zsh 加载。
2. 验证 `claude auth status` 与非交互式模型请求成功。
3. 用 API 调试日志复现交互式失败；日志显示请求未解析到认证方法。
4. 检查 `~/.claude.json` 的本地 API Key 选择状态。

## 根因判断

Claude Code 在检测到自定义 `ANTHROPIC_API_KEY` 时会询问是否使用该 Key。此前该 Key 的末 20 位被记录在 `~/.claude.json` 的 `customApiKeyResponses.rejected` 中。交互式 TUI 尊重该拒绝记录并不携带 Key；非交互式调用仍可从环境变量使用 Key，因此两种模式表现不一致。

## 解决方案

1. 先备份 `~/.claude.json`。
2. 从 `customApiKeyResponses.rejected` 移除当前 Key 对应的本地指纹记录。
3. 在 `~/.zshrc` 增加 `claude()` 包装器：每次启动 Claude Code 前，仅清除当前 Key 的本地允许/拒绝记录，使 TUI 每次重新询问是否使用该 Key。
4. 在确认页使用方向键选择 `Yes` 后再按 Enter；默认高亮为 `No (recommended)`，直接 Enter 会再次拒绝。

## 验证结果

- 新启动的 Claude Code 已重新出现 “Detected a custom API key in your environment” 确认页。
- `claude auth status` 仍显示 API Key 认证；非交互式请求保持成功。

## 预防措施

- 不要直接在默认高亮为 `No (recommended)` 的确认页按 Enter。
- 如需恢复默认行为，可删除 `~/.zshrc` 中的 `claude()` 包装器；这不会影响 API Key、路由或历史会话。

## 相关文件

- `~/.zshrc`
- `~/.claude.json`
- `~/.claude/backups/.claude.json.pre-key-prompt-20260712-183352`
