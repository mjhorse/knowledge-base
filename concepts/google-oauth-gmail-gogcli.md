---
type: concept
tags: [google, oauth, gmail, gogcli, api-auth]
status: captured
date: 2026-07-05
---

# 概念：Google OAuth、Gmail API 与 gogcli 本地授权

## 一句话解释

Google OAuth 的核心是：本地应用用 OAuth Client 表明“我是谁”，用户通过 Google 授权页同意特定 scopes，Google 再签发带权限范围的 token；Gmail API 在调用时检查 token 的 scope，而不是读取 OAuth Client 页面里的固定 API 权限清单。

## 背景

本次排查围绕本地 `gog` / `gogcli` 使用 Gmail API 时的授权来源、token 存储位置、access token 验证方式，以及 Google Cloud Console 中 OAuth Client、测试用户、API 启用、scope 之间的关系。

## 解决什么问题

- 解释为什么本地发送 Gmail 需要 OAuth，而不能只用 API Key。
- 解释 OAuth Client 是否代表用户身份。
- 解释为什么 OAuth Client 页面没有 API 权限清单，但 token 仍可访问 Gmail API。
- 找到 `gogcli` 本地 token 存储位置。
- 验证 access token 中实际携带的 Gmail scopes。

## 核心机制

### 角色拆分

| 角色/配置 | 作用 |
|---|---|
| Resource Owner | 用户，例如 `mjhorse1984@gmail.com` |
| OAuth Client | 应用身份，例如 `gogcli` 使用的 `client_id` / `client_secret` |
| Authorization Server | Google OAuth 服务，例如 `accounts.google.com`、`oauth2.googleapis.com/token` |
| Resource Server | Gmail API，例如 `gmail.googleapis.com` |
| OAuth consent screen | 展示应用名称、请求的 scopes、测试用户限制等 |
| Test users | Testing 状态下允许完成授权流程的 Google 账号 |
| Scopes | 本次授权请求想获得的权限，例如 Gmail 读写/设置权限 |
| Access token | 短期访问凭证，通常约 1 小时有效 |
| Refresh token | 长期刷新凭证，用于换取新的 access token |

### OAuth Client 不等于用户身份

OAuth Client 表示“哪个应用在请求授权”，不是“哪个用户”。用户身份来自 Google 登录账号。用户授权后，Google 签发的 token 同时绑定：

- 用户：例如 `mjhorse1984@gmail.com`；
- Client：例如某个 `*.apps.googleusercontent.com`；
- Scopes：例如 Gmail 相关权限；
- 有效期和访问类型。

### Test users 的真实作用

在 OAuth App 处于 Testing 状态时，只有被加入 Test users 的 Google 账号可以通过授权流程。

Test users 解决的是：

```text
谁可以授权这个 testing app？
```

它不解决：

```text
这个 app 可以访问哪些 API？
```

### Gmail API 权限来自 scopes

OAuth Client 页面通常没有“API 权限清单”。Gmail API 权限来自 OAuth 授权请求中的 `scope` 参数，以及用户在 consent screen 上的同意。

典型授权请求会包含类似：

```text
scope=https://www.googleapis.com/auth/gmail.modify
```

用户同意后，access token / refresh token 就会携带这些 scopes。Gmail API 调用时检查 token 是否包含所需 scope。

### Google Cloud Project 还需要启用 Gmail API

完整条件是：

1. Google Cloud Project 启用了 Gmail API；
2. OAuth 授权请求包含 Gmail scopes；
3. 用户账号被允许授权该 OAuth App（Testing 状态下需是 Test user）；
4. 用户同意授权；
5. Gmail API 调用时 access token 有效且 scope 足够。

## 本次验证到的 gogcli 配置

### OAuth client 凭据文件

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
```

用途：保存 OAuth client 凭据，例如 `client_id`、`client_secret`、redirect URIs。

注意：该文件是 client secret，不是用户 token。不要公开。

### gogcli 配置文件

```text
/Users/mjhorse/Library/Application Support/gogcli/config.json
```

### 用户 token 存储位置

`gogcli` 使用 macOS Keychain 存储 refresh token：

```text
Keychain: /Users/mjhorse/Library/Keychains/login.keychain-db
Service: gogcli
Account: token:default:mjhorse1984@gmail.com
```

本次查到 Keychain 条目的元数据，但知识库中不保存任何 token 明文。

### token 中验证到的 scopes

通过 `tokeninfo` 验证到 access token 携带以下 scope（仅记录 scope，不记录 token）：

```text
email
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.settings.basic
https://www.googleapis.com/auth/gmail.settings.sharing
```

这些权限比单纯发送邮件更大：

| Scope | 含义 |
|---|---|
| `gmail.modify` | 读取、修改 Gmail 邮件和标签，不能永久删除 |
| `gmail.settings.basic` | 读取/修改 Gmail 基础设置 |
| `gmail.settings.sharing` | 管理 Gmail 共享/委托等设置 |
| `userinfo.email` / `email` / `openid` | 身份与邮箱信息 |

若只需要发送邮件，原则上更小权限是：

```text
https://www.googleapis.com/auth/gmail.send
```

但实际 `gogcli --services gmail` 默认请求哪些 Gmail scope 取决于该工具版本设计。

## 认证流程

```text
1. gogcli 读取 credentials.json
   获取 OAuth client_id / client_secret / redirect URI

2. 执行授权命令
   gog auth add <email> --services gmail --force-consent

3. gogcli 打开 Google 授权页
   授权 URL 包含 client_id、redirect_uri、scope 等参数

4. 用户用 Google 账号登录并同意 scopes

5. Google 返回 authorization code

6. gogcli 用 authorization code + client_id + client_secret 换 token

7. gogcli 将 refresh token 存入 macOS Keychain

8. 后续调用 Gmail API 时
   gogcli 用 refresh token 换短期 access token
   再用 access token 调用 Gmail API
```

## 使用场景

- 本地 CLI 工具访问 Gmail、Drive、Calendar 等用户私有资源。
- 需要离线访问能力，即用户不在场时也能通过 refresh token 换取 access token。
- 需要为 AI Agent 或自动化工具配置 Google Workspace 能力。

## 与相关概念的区别

| 概念 | 说明 |
|---|---|
| API Key | 适合访问非用户私有资源或项目级 API；不适合代表用户访问 Gmail 私有邮箱 |
| OAuth Client | 应用身份，不是用户身份 |
| Test users | Testing 状态下谁能授权，不是 API 权限配置 |
| Scopes | token 能访问哪些资源的关键依据 |
| Access token | 短期访问凭证，用于实际 API 调用 |
| Refresh token | 长期刷新凭证，用于获取新的 access token |
| Service Account | 服务器到服务器身份；普通个人 Gmail 通常不用它。Workspace 域级委托场景才可能用 |

## 当前环境中的应用

- 本机工具：`gog` / `gogcli`。
- OAuth client 凭据位置：`/Users/mjhorse/Library/Application Support/gogcli/credentials.json`。
- token 存储：macOS Keychain，`service=gogcli`。
- 网络：访问 Google OAuth/Gmail 端点需要走本地 M78 加速器代理，当前端点为 `http://127.0.0.1:7892`。
- `gog` keyring backend 已固定为 `keychain`，避免后台/飞书触发时落到需要 passphrase 的 file keyring。
- OpenClaw 远程发信链路为：飞书指令 → 本机 OpenClaw → `gog` → macOS Keychain refresh token → Gmail API。

## 安全注意事项

- 不要在聊天、文档、Git 仓库中保存 `refresh_token`、`access_token`、`client_secret`、API Key。
- `refresh_token` 是长期凭证，泄露后应立即撤销并重新授权。
- 若只是发送邮件，应优先使用最小权限 scope，例如 `gmail.send`，避免过度授权。
- `tokeninfo` 适合验证 access token 的 scopes，但不要把 token 明文写进知识库。

## 相关链接

- 本地操作手册：[gogcli Gmail OAuth 授权与验证](../playbooks/gogcli-gmail-oauth-auth-and-verify.md)
- 排障记录：[gogcli Gmail OAuth token 定位与验证](../troubleshooting/gogcli-gmail-oauth-token-location-and-verification.md)
