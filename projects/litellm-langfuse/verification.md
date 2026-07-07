# 验证记录

## 已验证成功

- `litellm-gateway` 容器运行中。
- LiteLLM `/v1/models` 可返回模型列表。
- Langfuse success/failure callbacks 初始化成功。
- Langfuse Traces 页面可见 `litellm-acompletion` 失败 trace。
- 上游 `https://ai.gsykj.com/v1/models` 可用。
- 上游 `gpt-5.5` 直连 chat 可返回结果。
- 2026-07-06：本地 `LITELLM_MASTER_KEY` 已轮换，`litellm-gateway` 重启后 readiness healthy。
- 2026-07-06：LiteLLM `codex-default` 已映射到可用的 `openai/gpt-5.5`，curl 请求 HTTP 200。
- 2026-07-06：Langfuse/ClickHouse 中可查到成功 trace/observation，包含 token、cost，latency 可由 observation start/end 计算。

## 未完全通过

- 上游 `403 / error code: 1010` 已定位为 relay / Cloudflare 按请求特征拦截；LiteLLM 侧已通过 `extra_headers` 增加浏览器风格 `User-Agent` 与 `Accept` 缓解。
- `claude-sonnet-4-6` 当前失败原因是上游账号/通道模型权限限制，需要 relay 侧开通或更换支持 Claude 的上游 key/账号。
- Codex CLI 能打到本地 LiteLLM `/v1/responses`，但会话存储/embedding/auth 路径返回 `No connected db`，需要后续接入 LiteLLM DB 或调整 Codex 接入方式。
- Langfuse public API 查询曾返回 502，但 ClickHouse 侧可验证 trace 写入。

## Trace 查看入口

```text
http://localhost:3000/project/cmr023lrx0006mn07dde0uuc9/traces
```

## 临时客户端配置

```bash
export OPENAI_BASE_URL=http://127.0.0.1:4000/v1
export OPENAI_API_KEY=<LITELLM_MASTER_KEY>
export OPENAI_MODEL=codex-default
```
