# 项目决策记录

## 决策：LiteLLM 独立部署

- 选择：在 `/Users/mjhorse/ai-observability/litellm` 单独部署 LiteLLM。
- 原因：避免修改 Langfuse upstream clone，职责边界清晰，便于独立升级和回滚。

## 决策：初始阶段不修改全局 shell profile

- 选择：不改 `~/.zshrc` 或 `~/.zprofile`。
- 原因：避免影响 Claude Code 日常使用，先用临时环境变量验证兼容性。

## 决策：使用 main-stable 镜像

- 选择：使用 `ghcr.io/berriai/litellm:main-stable`。
- 原因：`main-latest` 在当前环境退出码为 132，稳定镜像可正常启动。
