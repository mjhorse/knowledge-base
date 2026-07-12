---
type: architecture_design
project: litellm-langfuse
tags: [openclaw, langfuse, agent-session, session-mapping, observability, privacy]
status: implemented
created: 2026-07-12
---

# OpenClaw Agent Session 与 Langfuse Session 语义映射架构

## 设计问题

OpenClaw 的 Agent Session 与 Langfuse Session 服务于不同目标：

- **OpenClaw Agent Session**：用于运行时路由、上下文续接和 session 生命周期管理。运行时 `sessionId` 可轮换，不适合直接作为长期观测聚合键。
- **Langfuse Session**：用于在 Sessions 视图将多个 Trace 按一个业务会话聚合，需要稳定、可读且可筛选的 `session.id`。

因此，不能简单把 OpenClaw UUID 复制到 Langfuse；应从 OpenClaw 的稳定 `usageFamilyKey` 中抽取会话语义，并在外发前完成脱敏。

## 目标模型

```text
OpenClaw usageFamilyKey
  → { agentId, channel, chatType, conversation }
  → openclaw/{agent}/{channel}/{chatType}/{conversationKey}
  → Langfuse session.id
```

其中：

- `agentId`、`channel`、`chatType`：可读、低敏感的会话分类维度。
- `conversation`：可能是渠道侧用户或群标识，必须转换为稳定短哈希。
- `conversationKey`：WebChat 主会话使用固定值 `main`；渠道会话使用 `shortHash(conversation)`；本地记录未命中时使用 `shortHash(runtime sessionId)`。

## 具体映射方案

| OpenClaw `usageFamilyKey` | 解析后的语义域 | Langfuse `session.id` |
| --- | --- | --- |
| `agent:main:main` | `main / webchat / direct / main` | `openclaw/main/webchat/direct/main` |
| `agent:main:feishu:group:oc_<groupId>` | `main / feishu / group / shortHash(groupId)` | `openclaw/main/feishu/group/<shortHash>` |
| `agent:main:feishu:direct:ou_<userId>` | `main / feishu / direct / shortHash(userId)` | `openclaw/main/feishu/direct/<shortHash>` |
| `agent:{agent}:{channel}:{account}:direct:{peer}` | 定位 `direct`/`group` 段，再取后续 peer | `openclaw/{agent}/{channel}/{type}/<shortHash>` |

格式定义：

```text
openclaw/{agent}/{channel}/{chatType}/{conversationKey}
```

## 解析与降级规则

1. `usageFamilyKey` 是首选输入，用于恢复稳定的 Agent Session 家族语义。
2. `agent:…:main` 是 WebChat 主会话特殊规则，映射为 `webchat/direct/main`，不需要哈希。
3. 对渠道会话，解析时定位 `direct` 或 `group` 标记，不依赖固定数组索引，以兼容含 `accountId` 的 session key。
4. 对渠道对象采用 `SHA-256` 截断 12 位十六进制短哈希，保证同一对象稳定聚合且不暴露原值。
5. 本地 `sessions.json` 未命中或 `usageFamilyKey` 不可用时，使用运行时 `sessionId` 短哈希，避免所有未知请求错误合并到一个 `unknown` Session。

## 外发字段与隐私边界

| 字段 | 是否外发 | 说明 |
| --- | --- | --- |
| `session.id` | 是 | 语义化 Langfuse 聚合主键。 |
| `openclaw_semantic_session_id` | 是 | 等同 `session.id`，用于 metadata 筛选。 |
| `openclaw_usage_family_key_hash` | 是 | 稳定关联哈希，保留既有追溯能力。 |
| `openclaw_session_id` | 是 | 运行时诊断关联，不作为聚合主键。 |
| `openclaw_agent_id` / `channel` / `chat_type` | 是 | 可读、低敏感筛选字段。 |
| 原始 `usageFamilyKey` | 否 | 可能包含渠道对象。 |
| `origin.from` / `origin.to` / `origin.label` | 否 | 可能包含通信对象或内容标识。 |
| 飞书 `oc_…` / `ou_…` | 否 | 仅在本地参与哈希计算。 |

## Trace 命名

Trace 名称按来源生成：

```text
openclaw-{channel}-{chatType}-anthropic
```

示例：`openclaw-feishu-group-anthropic`。该名称用于区分调用来源；`session.id` 继续承担跨 Trace 的会话聚合职责。

## 兼容性与验证

- 不修改 OpenClaw 的 `sessions.json`、运行时注册表或已存在的 Langfuse Session。
- 仅后续新产生的 Trace 使用语义化名称。
- 已完成 JavaScript 语法检查、模块导入检查，以及 WebChat 主会话、飞书群聊、飞书私聊的实际 metadata 输出检查。
- 核验结果：语义 ID 符合预期，飞书原始 `oc_…` / `ou_…` 未外发，`openclaw_usage_family_key_hash` 仍被保留。

## 产出物

- [架构设计 Word 文档](../../assets/openclaw-langfuse-semantic-sessions/openclaw-agent-to-langfuse-session-mapping-architecture-design.docx)
- [可编辑架构图 PPT](../../assets/openclaw-langfuse-semantic-sessions/openclaw-agent-to-langfuse-session-mapping-architecture.pptx)
- [架构图 SVG](../../assets/openclaw-langfuse-semantic-sessions/openclaw-agent-to-langfuse-session-mapping.svg)
- [架构图 PNG](../../assets/openclaw-langfuse-semantic-sessions/openclaw-agent-to-langfuse-session-mapping.png)
