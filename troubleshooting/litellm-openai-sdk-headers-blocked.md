---
type: troubleshooting
project: litellm-langfuse
date: 2026-07-05
tags: [litellm, openai-sdk, upstream, 403]
severity: medium
status: open
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

- 直接 curl 上游 `/v1/models` 成功。
- 直接 curl 上游 `gpt-5.5` chat 成功。
- 通过 LiteLLM 调用返回 403。
- 模拟 OpenAI SDK 风格请求头后，上游也返回 blocked。

## 根因判断

上游 Relay 可能对 OpenAI SDK 风格请求头或请求特征有拦截策略。

## 后续方案

- 确认上游推荐接入方式。
- 尝试配置 LiteLLM 覆盖或清洗请求头。
- 必要时增加本地轻量转发层。
