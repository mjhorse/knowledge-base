---
type: playbook
tags: [obsidian, copilot, claude, anthropic, knowledge-base]
---

# 操作手册：配置 Obsidian Copilot 使用 Claude Code 同源模型

## 适用场景

适用于在 Obsidian Copilot 中使用本地 Claude Code 同一套上游模型服务，例如通过自定义 Anthropic-compatible relay 调用 `claude-sonnet-4-6`。

## 前置条件

- Obsidian 已打开 `/Users/mjhorse/knowledge-base` 作为 Vault。
- Copilot 插件已安装并启用。
- 本机 Claude Code 环境中已有可用的 `ANTHROPIC_BASE_URL` 与 `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`。
- Copilot 配置文件 `.obsidian/plugins/copilot/data.json` 已加入 `.gitignore`，避免同步 API key。

## 操作步骤

### 1. 先确认模型协议

不要只看模型名，要确认模型在哪种协议下可用。

本次验证结果：

- `claude-sonnet-4-6` 通过 Anthropic `/v1/messages` 可用。
- `claude-sonnet-4-6` 通过 OpenAI-compatible `/v1/chat/completions` 不可用。

因此 Copilot 应选择：

```text
claude-sonnet-4-6 | anthropic
```

不要选择：

```text
claude-sonnet-4-6 | openai
```

### 2. 配置 Copilot 模型

Copilot 的 Anthropic provider 支持模型级 `baseUrl`。最终配置要点：

```text
Provider: anthropic
Model: claude-sonnet-4-6
Base URL: https://ai.gsykj.com
API key: 使用 Claude Code 同源 key
Default model key: claude-sonnet-4-6|anthropic
```

### 3. 处理 keychainOnly

如果 Copilot 报：

```text
API key is not provided for the model
```

检查 Copilot 配置中的：

```json
"_keychainOnly": true
```

如果需要让 Copilot 读取 `data.json` 中的本地配置，可改为：

```json
"_keychainOnly": false
```

### 4. 重启 Obsidian

修改插件配置后，重启 Obsidian 或重新打开应用，确保 Copilot 重新加载配置。

## 检查清单

- Copilot 模型下拉框选择 `claude-sonnet-4-6 | anthropic`。
- `claude-sonnet-4-6 | openai` 不作为默认模型。
- Copilot 能成功返回简单测试问题。
- `.obsidian/plugins/copilot/data.json` 不进入 Git 提交。

## 常见问题

### Failed to fetch

如果 OpenAI-compatible 配置下出现 `Failed to fetch`，不要立刻判断为网络问题。先验证模型是否支持该协议。本次问题的根因是 Claude 模型应走 Anthropic protocol，而不是 OpenAI Chat Completions protocol。

### 同一个上游 relay 为什么有两种协议？

同一个 relay 可能同时提供 OpenAI-compatible 与 Anthropic-compatible API，但不同模型在不同协议下支持情况可能不同。Claude 模型优先使用 Anthropic provider。

## 示例

正确选择：

```text
claude-sonnet-4-6 | anthropic
```

错误选择：

```text
claude-sonnet-4-6 | openai
```
