# 项目排障记录

## 已知问题

1. LiteLLM `main-latest` 在当前 Colima/Docker 环境中 `exit 132`。
   - 处理：切换到 `ghcr.io/berriai/litellm:main-stable`。

2. LiteLLM/OpenAI SDK 风格请求被上游 Relay 拦截。
   - 现象：返回 `403 Your request was blocked`。
   - 判断：直接 curl `gpt-5.5` 成功，但模拟 OpenAI SDK 请求头会被拦截。
   - 下一步：确认上游推荐接入方式，或在本地清洗/覆盖请求头。

3. Claude 路由待确认。
   - 现象：`claude-sonnet-4-6` 直连 chat 返回 `502`。
   - 下一步：确认上游实际协议和模型名。

4. Word 架构图曾出现显示不完整。
   - 原因：QuickLook 将 `1600x1000` 图生成了 `1600x1600` 缩略图。
   - 处理：使用 `sips -s format png input.svg --out output.png` 保持比例。
