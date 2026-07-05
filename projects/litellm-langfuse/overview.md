---
type: project_overview
project: litellm-langfuse
tags: [litellm, langfuse, observability, local-gateway]
status: in_progress
---

# LiteLLM + Langfuse 本地观测接入

## 背景

本项目目标是在本地部署 LiteLLM Gateway，让 Claude Code、Codex 或 OpenAI-compatible 客户端请求经过本地网关，再由 LiteLLM 将 LLM 调用成功/失败 trace 写入本地 Langfuse，用于性能诊断、失败分析和调用链追踪。

## 当前目标

- 本地 LiteLLM Gateway 监听 `127.0.0.1:4000`。
- OpenAI-compatible 客户端使用 `http://127.0.0.1:4000/v1`。
- 上游模型 Relay 使用 `https://ai.gsykj.com/v1`。
- Langfuse 本地 UI 使用 `http://localhost:3000`。
- 不修改全局 shell profile，先使用临时环境变量验证。

## 当前结论

- LiteLLM Gateway 已运行，容器名为 `litellm-gateway`。
- `/v1/models` 已返回模型别名。
- Langfuse success/failure callbacks 已初始化。
- 失败 trace 已在 Langfuse 中可见。
- 当前阻塞：LiteLLM/OpenAI SDK 风格请求被上游 Relay 403 拦截；Claude 模型直连 chat 当前返回 502。

## 关联页面

- [架构说明](architecture.md)
- [部署配置](deployment.md)
- [验证记录](verification.md)
- [项目排障](troubleshooting.md)
- [项目决策](decisions.md)
- [产出物](artifacts.md)
