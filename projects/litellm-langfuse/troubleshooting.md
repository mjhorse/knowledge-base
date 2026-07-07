# 项目排障记录

## 已知问题

1. LiteLLM `main-latest` 在当前 Colima/Docker 环境中 `exit 132`。
   - 处理：切换到 `ghcr.io/berriai/litellm:main-stable`。

2. LiteLLM/OpenAI SDK 风格请求被上游 Relay 拦截。
   - 现象：返回 `403 / error code: 1010` 或 `Your request was blocked`。
   - 判断：普通 Python/OpenAI 风格请求会被上游 WAF/Cloudflare 风控拦截；加浏览器风格 `User-Agent: Mozilla/5.0` 与 `Accept: application/json` 后 `/v1/models` 可通过。
   - 处理：在 `/Users/mjhorse/ai-observability/litellm/config.yaml` 为 OpenAI-compatible 上游路由配置 `extra_headers`。

3. Claude 路由待确认。
   - 现象：`claude-sonnet-4-6` 通过上游返回模型权限限制。
   - 判断：当前上游账号/通道不支持该模型，不是 LiteLLM 本地网关问题。
   - 下一步：在 relay 侧开通 Claude 模型或更换支持 Claude 的上游 key/账号。

4. Codex CLI 经 LiteLLM Responses API 仍有 DB 依赖问题。
   - 现象：Codex CLI 能打到本地 LiteLLM `/v1/responses`，但返回 `No connected db`。
   - 判断：LiteLLM Responses API 本身可被 curl 调通；Codex CLI 还触发会话存储/embedding/auth 路径，需要 LiteLLM DB 支撑或调整接入方式。

4. Word 架构图曾出现显示不完整。
   - 原因：QuickLook 将 `1600x1000` 图生成了 `1600x1600` 缩略图。
   - 处理：使用 `sips -s format png input.svg --out output.png` 保持比例。
