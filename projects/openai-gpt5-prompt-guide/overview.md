---
type: project_overview
project: openai-gpt5-prompt-guide
tags: [openai, gpt-5, prompting, agents, presentation]
status: completed
---

# OpenAI GPT-5 Prompting Guide｜新版叙事结构

## 目标

将 OpenAI 官方 GPT-5 Prompting Guide 的关键实践重构为面向 Agent 工程落地的中文演示材料，而非泛化的提示词技巧清单。

## 交付结果

- **推荐交付（V4 演讲版）**：`/Users/mjhorse/.openclaw/workspace/artifacts/openai-gpt5-prompt-guide/v4/OpenAI_GPT5_Prompting_Guide_V4_规范重制版.pptx`
- V4 PDF 渲染稿与逐页 PNG：`/Users/mjhorse/.openclaw/workspace/artifacts/openai-gpt5-prompt-guide/v4/qa/`
- V4 页面设计表：`/Users/mjhorse/.openclaw/workspace/artifacts/openai-gpt5-prompt-guide/v4/design.md`
- V4 QA：`/Users/mjhorse/.openclaw/workspace/artifacts/openai-gpt5-prompt-guide/v4/qa/QA.md`
- V3 是此前结构版本，保留在 `artifacts/openai-gpt5-prompt-guide/v3/` 供追溯。

## 核心结论

- Prompt 的角色从“提问技巧”升级为 Agent 的行为控制面。
- 可预测性来自边界、主动性、检索停止条件和风险阈值的显式定义。
- 多步任务应利用连续上下文、工具过程预告及可验证的 Rubric，而不是仅增加文字指令。
- 上线前需通过边界、风险、评测与工程保障四类决策门。

## 质量验证

- LibreOffice 成功真实渲染 V4 为 PDF，并生成 13 张页面 PNG。
- 结构检查：13 页、16:9、原生可编辑文本和形状，未发现对象越界；已移除 V3 连续 9pt 长说明带。
- 可读性检查：未发现低于 8pt 的文字；正文通常 11–13pt，关键结论 15pt 以上。
- 证据检查：13 个可点击来源链接，依据 OpenAI Cookbook、Responses API 与官方 Prompt Engineering Best Practices。
- 限制：视觉模型服务因访问拦截/超时不可用，未完成独立视觉模型复核。

## 后续

- 如用于正式分享，建议先由受众/业务场景审阅术语与案例，再做定向改版。
