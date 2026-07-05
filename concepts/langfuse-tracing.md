---
type: concept
tags: [langfuse, tracing, observability]
---

# 概念：Langfuse Trace

## 一句话解释

Langfuse Trace 是对一次 LLM 应用调用过程的结构化记录，通常包含输入、输出、模型、延迟、token、错误、metadata、session 和用户信息。

## 当前项目中的应用

LiteLLM 通过 `success_callback` 和 `failure_callback` 将调用记录写入本地 Langfuse。当前已验证失败 trace 可见，名称为 `litellm-acompletion`。
