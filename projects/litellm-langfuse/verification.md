# 验证记录

## 已验证成功

- `litellm-gateway` 容器运行中。
- LiteLLM `/v1/models` 可返回模型列表。
- Langfuse success/failure callbacks 初始化成功。
- Langfuse Traces 页面可见 `litellm-acompletion` 失败 trace。
- 上游 `https://ai.gsykj.com/v1/models` 可用。
- 上游 `gpt-5.5` 直连 chat 可返回结果。

## 未完全通过

- 通过 LiteLLM 调用上游时，上游返回 `403 Your request was blocked`。
- 上游 `claude-sonnet-4-6` 直连 chat 返回 `502`。

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
