---
type: concept
tags: [litellm, llm-gateway, proxy]
---

# 概念：LiteLLM Gateway

## 一句话解释

LiteLLM Gateway 是一个本地或服务端 LLM API 网关，用于统一承接 OpenAI-compatible 请求、映射模型别名、转发到不同上游模型服务，并可接入日志、鉴权和观测回调。

## 当前项目中的应用

在 LiteLLM + Langfuse 项目中，LiteLLM 监听 `127.0.0.1:4000`，为 Codex/OpenAI-compatible 客户端提供 `/v1` 入口，并将调用成功/失败写入 Langfuse。
