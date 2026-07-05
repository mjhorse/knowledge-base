---
type: troubleshooting
project: local-google-cli
date: 2026-07-05
tags: [google, oauth, gmail, gogcli, keychain, token, proxy]
severity: medium
status: resolved
---

# 问题：gogcli Gmail OAuth token 定位与验证

## 现象

在排查本地 Gmail 发送授权时，最初以为 token 存在：

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
```

但实际打开后发现该文件是 OAuth client secret，而不是用户授权 token。

随后通过 `security find-generic-password` 查到 `gogcli` 在 macOS Keychain 中保存了用户 refresh token。

另一个现象是：直接用 refresh token 调用：

```text
https://oauth2.googleapis.com/tokeninfo?access_token=<token>
```

不正确，因为 `tokeninfo?access_token=` 需要 access token，不接受 refresh token。并且本地直连 Google OAuth 端点曾出现超时。

## 环境

- OS: macOS
- 工具：`gog` / `gogcli` v0.11.0
- OAuth client 凭据：

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
```

- token 存储后端：macOS Keychain
- Keychain 条目：

```text
Service: gogcli
Account: token:default:mjhorse1984@gmail.com
Keychain: /Users/mjhorse/Library/Keychains/login.keychain-db
```

- Google OAuth 端点：

```text
https://oauth2.googleapis.com/token
https://oauth2.googleapis.com/tokeninfo
```

- 可能需要代理：

```text
http://127.0.0.1:7892
```

## 影响范围

- 无法理解本地 Gmail API 授权来源。
- 无法区分 OAuth client secret、refresh token、access token。
- 可能误把 refresh token 当作 access token 验证。
- 可能因为网络直连 Google 超时误判为 token 或 OAuth 配置错误。
- OpenClaw/飞书远程触发 `gog` 时，若未带代理或发生交互式 keyring 密码提示，会表现为命令长期无返回，约 90 秒后被系统超时终止。
- 若 token 明文被复制到聊天或文档，存在凭证泄露风险。

## 排查过程

### 1. 查找常见 token 文件

查找常见路径和文件名：

```text
token.json
*token*.json
*credentials*.json
application_default_credentials.json
.credentials/
```

结果：未发现普通 `token.json`；发现：

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
/Users/mjhorse/Library/Application Support/gogcli/config.json
```

### 2. 判断 credentials.json 类型

用户确认 `credentials.json` 内容是 client secret，不是 token。

结论：该文件是 OAuth client 凭据，只代表应用身份，不是用户授权凭据。

### 3. 搜索明文 token 字段

在常见配置目录中按字段搜索：

```text
"access_token" | "refresh_token"
```

未在 `gogcli` Application Support 目录中发现明文 token。

### 4. 检查 macOS Keychain

执行 Keychain 查询：

```bash
security find-generic-password -s gogcli
```

发现条目：

```text
Service: gogcli
Account: token:default:mjhorse1984@gmail.com
```

结论：`gogcli` 将用户 token 存入 macOS Keychain。

### 5. 确认 token 类型

Keychain secret 中包含：

```json
{
  "refresh_token": "<redacted>",
  "services": ["gmail"],
  "scopes": ["..."]
}
```

结论：长期保存的是 refresh token，不是 access token。

### 6. 纠正 tokeninfo 用法

错误用法：

```bash
curl "https://oauth2.googleapis.com/tokeninfo?access_token=<refresh_token>"
```

正确流程：

```text
refresh_token + client_id + client_secret
→ POST https://oauth2.googleapis.com/token
→ 得到短期 access_token
→ GET https://oauth2.googleapis.com/tokeninfo?access_token=<access_token>
```

### 7. 处理网络超时

直连 OAuth endpoint 出现：

```text
Failed to connect to oauth2.googleapis.com port 443
```

判断为网络连通性问题，不是 token 语义问题。使用本地代理可验证：

```bash
curl -x http://127.0.0.1:7892 <google-oauth-url>
```

### 8. 验证 access token

用 refresh token 换取 access token 后，`tokeninfo` 返回包含：

```text
email: mjhorse1984@gmail.com
azp/aud: <OAuth client id>
scope: email openid userinfo.email gmail.modify gmail.settings.basic gmail.settings.sharing
expires_in: 约 1 小时
access_type: offline
```

说明 OAuth 授权链路有效。

## 根因判断

1. `gogcli` 不把用户 token 存在 `credentials.json`，而是保存在 macOS Keychain。
2. `credentials.json` 是 OAuth client 凭据，不是用户 token。
3. Keychain 中长期保存的是 refresh token；access token 是运行时临时换取。
4. `tokeninfo?access_token=` 只能验证 access token，不能直接验证 refresh token。
5. 访问 Google OAuth 端点超时属于网络连通性问题，可通过代理区分。
6. 飞书远程发邮件卡住的主要原因通常不是邮件内容，而是后台执行 `gog` 时缺少 M78 代理，或 keyring 后端触发交互式密码输入。

## 解决方案

### 重新授权

```bash
gog auth add mjhorse1984@gmail.com --services gmail --force-consent
```

### 查看授权状态

```bash
gog auth status
gog auth list
```

### 固定 keyring backend

```bash
gog auth keyring keychain
```

验证：

```bash
gog auth status
```

期望：

```text
keyring_backend	keychain
keyring_backend_source	config
```

### 后台/远程调用统一加代理和 no-input

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail send \
  --account "mjhorse1984@gmail.com" \
  --to "recipient@example.com" \
  --subject "邮件标题" \
  --body "邮件正文" \
  --no-input
```

### 定位 Keychain token 条目

```bash
security find-generic-password \
  -s gogcli \
  -a "token:default:mjhorse1984@gmail.com"
```

### 获取 access token

使用 `client_id`、`client_secret`、`refresh_token` 调 Google token endpoint：

```bash
curl -x http://127.0.0.1:7892 \
  -X POST https://oauth2.googleapis.com/token \
  -d client_id="<client_id>" \
  -d client_secret="<client_secret>" \
  -d refresh_token="<refresh_token>" \
  -d grant_type="refresh_token"
```

### 验证 access token

```bash
curl -x http://127.0.0.1:7892 \
  "https://oauth2.googleapis.com/tokeninfo?access_token=<access_token>"
```

### token 泄露后的处理

如果 refresh token 被公开，应撤销授权并重新授权：

```bash
gog logout mjhorse1984@gmail.com
```

或删除 Keychain 条目：

```bash
security delete-generic-password \
  -s gogcli \
  -a "token:default:mjhorse1984@gmail.com"
```

然后：

```bash
gog auth add mjhorse1984@gmail.com --services gmail --force-consent
```

## 验证结果

最终 `tokeninfo` 验证结果显示：

- token 绑定用户：`mjhorse1984@gmail.com`；
- token 受众/授权方为 gogcli 使用的 OAuth client；
- token 具有 offline access；
- access token 有约 1 小时有效期；
- scopes 包含 Gmail 修改和设置相关权限。

本次归档不保存任何 token、client secret、API key 明文。

## 预防措施

- 永远不要把 refresh token、access token、client secret、API key 粘贴到聊天或文档。
- 验证权限时只记录 scope、client id、账号、结论，不记录 token。
- 使用最小权限原则。若只需发邮件，优先使用 `gmail.send`；避免不必要的 `gmail.modify`、`gmail.settings.*`。
- 遇到 Google endpoint 超时，先区分网络问题和认证问题：
  - 网络问题：连接超时、无法建立 TCP/TLS；
  - 认证问题：HTTP 400/401/403，返回 OAuth 错误 JSON。
- 确认 OAuth App Testing 状态下目标账号在 Test users 中。
- 确认 Google Cloud Project 已启用 Gmail API。

## 相关文件

- `/Users/mjhorse/Library/Application Support/gogcli/credentials.json`：OAuth client 凭据，敏感。
- `/Users/mjhorse/Library/Application Support/gogcli/config.json`：gogcli 配置。
- `/Users/mjhorse/Library/Keychains/login.keychain-db`：Keychain token 存储数据库。
- [Google OAuth、Gmail API 与 gogcli 本地授权](../concepts/google-oauth-gmail-gogcli.md)
- [gogcli Gmail OAuth 授权与验证](../playbooks/gogcli-gmail-oauth-auth-and-verify.md)
