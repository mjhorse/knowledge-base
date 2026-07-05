# 架构说明：LiteLLM Gateway + Langfuse Trace

## 架构摘要

```text
Client / Codex / Claude Code
  -> Local LiteLLM Gateway 127.0.0.1:4000
  -> Existing Model Relay https://ai.gsykj.com/v1
  -> response/error
  -> LiteLLM success/failure callback
  -> Local Langfuse http://localhost:3000
```

## 关键组件

| 组件 | 作用 |
|---|---|
| Codex / OpenAI SDK | OpenAI-compatible 客户端入口 |
| Claude Code | 仅建议临时 shell 中验证兼容性 |
| LiteLLM Gateway | 本地鉴权、模型别名、上游转发、Langfuse callback |
| Existing Model Relay | 实际上游模型 API |
| Langfuse | Trace 记录与分析 |
| `.env` | 本地密钥与运行时配置 |

## 模型别名

| LiteLLM alias | 当前上游模型 |
|---|---|
| `codex-default` | `openai/gpt-5.5` |
| `claude-sonnet-4-6` | `openai/claude-sonnet-4-6`，待调试 |

## 设计原则

- LiteLLM 独立部署，不修改 Langfuse upstream clone。
- 网关仅绑定本机地址，不暴露到局域网。
- 密钥仅保存在 `.env`，不写入 YAML 或文档正文。
- 初始验证不修改 `~/.zshrc` 或 `~/.zprofile`。
