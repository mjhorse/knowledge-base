---
type: troubleshooting
project: litellm-langfuse
date: 2026-07-05
tags: [litellm, openai-sdk, upstream, 403]
severity: medium
status: mitigated
---

# 问题：LiteLLM/OpenAI SDK 风格请求被上游拦截

## 现象

通过 LiteLLM 调用上游模型时，上游返回：

```text
403 Your request was blocked
```

## 环境

- LiteLLM Gateway：`127.0.0.1:4000`
- 上游 Relay：`https://ai.gsykj.com/v1`
- 当前 codex-default：`openai/gpt-5.5`

## 排查过程

- 直接 curl 上游 `/v1/models` 曾经成功，但 2026-07-06 复测时普通 Python/OpenAI 风格请求返回 `403 / error code: 1010`。
- 同一上游、同一 key，加浏览器风格请求头后 `/v1/models` 成功：
  - `User-Agent: Mozilla/5.0`
  - `Accept: application/json`
- 通过 LiteLLM 调用上游时，若未覆盖请求头，会触发同类 403/1010。
- 加请求头后，`gpt-5.5` 与映射到 `gpt-5.5` 的 `codex-default` 可通过 LiteLLM 成功返回。
- `claude-sonnet-4-6` 仍失败，但错误已变为上游账号/通道模型权限限制。

## 根因判断

上游 Relay / Cloudflare 对请求特征敏感，会拦截普通 SDK/Python 风格请求；这不是 LiteLLM master key、容器启动、本地网络或 Langfuse callback 问题。

## 处理方案

在 `/Users/mjhorse/ai-observability/litellm/config.yaml` 的 OpenAI-compatible 上游路由中增加：

```yaml
extra_headers:
  User-Agent: Mozilla/5.0
  Accept: application/json
```

同时将 `codex-default` 临时映射到当前上游可用模型：

```yaml
model: openai/gpt-5.5
```

## 后续方案

- 在 relay 侧生成新的上游 key，替换本机相关配置后重启验证。
- 如果要继续使用 `claude-sonnet-4-6`，需要 relay 侧开通模型权限或更换支持 Claude 的上游账号/key。
- 如果 Codex CLI 必须走本地 LiteLLM，需要继续处理 Responses API 的 DB 依赖问题。
