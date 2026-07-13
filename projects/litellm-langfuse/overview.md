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

- LiteLLM Gateway 当前按需停用：`litellm-gateway` 与数据库容器已停止；无已验证客户端需求时不启动，以节省资源。
- 控制面已改为多 relay、按客户端显式分配：`gsykj` 是 Claude Code、OpenClaw、Codex 的当前已分配 relay；`yq66` 已登记为备用 Anthropic/OpenAI-compatible relay，Responses 支持待确认。
- 路由查询必须区分默认配置、运行会话与 LiteLLM 网关证据；网关状态不能单独证明某个客户端当前路由。
- 历史验证曾确认 `/v1/models`、Langfuse success/failure callbacks 和失败 trace；先前上游兼容性问题仍应在重新启用网关时复验。

### 当前路由与网关状态

- 已分配客户端：Claude Code、OpenClaw、Codex → `gsykj`。
- 候选 relay：`yq66`（Anthropic、OpenAI-compatible；Responses 未确认）。
- LiteLLM：禁用且容器停止；若有客户端明确需要，先进行内存预检、健康检查和路由验证。

## 关联页面

- [架构说明](architecture.md)
- [部署配置](deployment.md)
- [验证记录](verification.md)
- [项目排障](troubleshooting.md)
- [项目决策](decisions.md)
- [OpenClaw Agent Session 与 Langfuse Session 语义映射架构](openclaw-langfuse-semantic-sessions.md)
- [产出物](artifacts.md)
