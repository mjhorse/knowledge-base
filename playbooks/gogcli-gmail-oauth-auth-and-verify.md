---
type: playbook
tags: [google, oauth, gmail, gogcli, cli, keychain]
status: captured
date: 2026-07-05
---

# 操作手册：gogcli Gmail OAuth 授权与验证

## 适用场景

用于在本机通过 `gog` / `gogcli` 授权 Gmail API，并验证授权 token 是否属于目标账号、目标 OAuth Client，以及是否包含预期 Gmail scopes。

适用于：

- 本地 CLI 发送/读取/修改 Gmail。
- 排查 “OAuth Client 页面没有 API 权限清单，但 token 能访问 Gmail API” 的疑问。
- 验证 `gogcli` token 存储位置和实际授权范围。

## 前置条件

1. Google Cloud Project 已启用 Gmail API。
2. OAuth consent screen 已配置。
3. Testing 状态下，目标 Google 账号已加入 Test users。
4. 本机存在 OAuth client 凭据：

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
```

5. 本机可访问 Google OAuth 端点。若直连超时，可使用本地代理，例如：

```text
http://127.0.0.1:7892
```

## 常用命令

### 固定 keyring 后端为 macOS Keychain

为避免后台/飞书远程触发时出现 `gogcli` passphrase 输入提示，先将 keyring backend 固定为 macOS Keychain：

```bash
gog auth keyring keychain
```

验证：

```bash
gog auth status
```

期望看到：

```text
keyring_backend	keychain
keyring_backend_source	config
```

### M78 代理环境

当前本机 M78 加速器代理端口为：

```text
127.0.0.1:7892
```

调用 Google/Gmail API 时建议显式加代理，尤其是 OpenClaw/飞书后台触发场景：

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog auth list --no-input
```


### 查看 gog 命令帮助

```bash
gog --help
gog auth --help
gog auth add --help
```

### 发起 Gmail 授权

```bash
gog auth add mjhorse1984@gmail.com --services gmail --force-consent
```

等价简写：

```bash
gog login mjhorse1984@gmail.com
```

说明：

- `--services gmail`：只请求 Gmail 相关服务能力。
- `--force-consent`：强制重新显示授权页，确保可重新获得 refresh token。

### 手动/远程授权

无浏览器或远程环境可使用：

```bash
gog auth add mjhorse1984@gmail.com --services gmail --manual
```

或按帮助使用 remote 两步模式：

```bash
gog auth add mjhorse1984@gmail.com --services gmail --remote --step 1
# 浏览器完成授权后，复制 redirect URL

gog auth add mjhorse1984@gmail.com --services gmail --remote --step 2 --auth-url '<redirect-url>'
```

### 查看授权状态

```bash
gog auth status
gog auth list
```

### 查看支持服务与 scopes

```bash
gog auth services
```

## token 存储位置

### OAuth client 凭据

```text
/Users/mjhorse/Library/Application Support/gogcli/credentials.json
```

这里保存的是 OAuth client 信息，不是用户 token。

### 用户 refresh token

`gogcli` 使用 macOS Keychain 存储用户 refresh token：

```text
Service: gogcli
Account: token:default:mjhorse1984@gmail.com
Keychain: /Users/mjhorse/Library/Keychains/login.keychain-db
```

查看 Keychain 条目元数据：

```bash
security find-generic-password \
  -s gogcli \
  -a "token:default:mjhorse1984@gmail.com"
```

查看 secret 明文会输出敏感 token，不建议复制或保存：

```bash
security find-generic-password \
  -s gogcli \
  -a "token:default:mjhorse1984@gmail.com" \
  -w
```

## access token 获取与验证

`gogcli` 通常长期保存 refresh token，而不是 access token。access token 是运行时用 refresh token 临时换取的短期凭证。

### 用 refresh token 换 access token

需要从 `credentials.json` 获取 `client_id` 和 `client_secret`，从 Keychain 获取 `refresh_token`。

不要把这些值写入历史记录、文档或聊天。建议使用临时变量或安全脚本处理。

基本请求：

```bash
curl -x http://127.0.0.1:7892 \
  -X POST https://oauth2.googleapis.com/token \
  -d client_id="<client_id>" \
  -d client_secret="<client_secret>" \
  -d refresh_token="<refresh_token>" \
  -d grant_type="refresh_token"
```

返回中会包含：

```json
{
  "access_token": "<redacted>",
  "expires_in": 3599,
  "scope": "...",
  "token_type": "Bearer"
}
```

### 验证 access token

```bash
curl -x http://127.0.0.1:7892 \
  "https://oauth2.googleapis.com/tokeninfo?access_token=<access_token>"
```

关键字段：

| 字段 | 含义 |
|---|---|
| `email` | token 绑定的 Google 账号 |
| `azp` | 被授权的 OAuth client |
| `aud` | token 受众，通常也是 OAuth client |
| `scope` | token 实际拥有的权限范围 |
| `expires_in` | 剩余有效秒数 |
| `access_type` | 是否 offline，可由 refresh token 刷新 |

## 本次验证结论示例

本次验证到的 scope 包括：

```text
email
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.settings.basic
https://www.googleapis.com/auth/gmail.settings.sharing
```

这说明该授权不是只允许发送邮件，而是包含 Gmail 修改和设置相关权限。

## 检查清单

- [ ] Google Cloud Project 已启用 Gmail API。
- [ ] OAuth consent screen 处于 Testing 时，账号已加入 Test users。
- [ ] `credentials.json` 存在且包含 OAuth client 信息。
- [ ] `gog auth add <email> --services gmail --force-consent` 能完成授权。
- [ ] macOS Keychain 中存在 `service=gogcli`、`account=token:default:<email>` 的 token 条目。
- [ ] 可用 refresh token 换取 access token。
- [ ] `tokeninfo` 返回的 `email`、`azp`、`scope` 符合预期。
- [ ] 没有将 token、client secret、API key 写入文档或 Git。

## 常见问题

### OAuth Client 页面为什么没有 Gmail API 权限清单？

OAuth Client 只定义应用身份和 redirect URI。Gmail 权限由授权请求中的 `scope` 决定，并在用户 consent 后写入 token。

### Test users 是否等于授权 Gmail API？

不是。Test users 只决定 Testing 状态下哪些 Google 账号可以完成授权流程，不决定 API 权限。

### 为什么 tokeninfo 不能用 refresh token？

`tokeninfo?access_token=` 需要 access token。refresh token 必须先通过 token endpoint 换成 access token。

### curl 访问 Google 超时怎么办？

如果本地网络无法直连 Google，可指定代理：

```bash
curl -x http://127.0.0.1:7892 <url>
```

### refresh token 泄露怎么办？

立即撤销授权或删除 Keychain token 后重新授权：

```bash
gog logout mjhorse1984@gmail.com
```

或：

```bash
security delete-generic-password \
  -s gogcli \
  -a "token:default:mjhorse1984@gmail.com"
```

然后重新授权：

```bash
gog auth add mjhorse1984@gmail.com --services gmail --force-consent
```

## 示例

### 发送 Gmail

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail send \
  --account "mjhorse1984@gmail.com" \
  --to "recipient@example.com" \
  --subject "邮件标题" \
  --body "邮件正文" \
  --no-input
```

带附件：

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail send \
  --account "mjhorse1984@gmail.com" \
  --to "recipient@example.com" \
  --subject "邮件标题" \
  --body "请查收附件。" \
  --attach "/absolute/path/to/file" \
  --no-input
```

### OpenClaw/飞书远程发信注意

- OpenClaw 必须运行在已完成 `gog` 授权的同一 macOS 用户下。
- 命令必须带 M78 代理环境变量。
- 命令必须带 `--no-input`，避免后台等待密码输入直到系统超时。
- 外发邮件前应确认收件人、标题、正文和附件。

完整安全验证思路：

```text
1. 确认 OAuth client 凭据文件存在。
2. 执行 gog auth add 重新授权。
3. 用 security find-generic-password 确认 Keychain token 条目存在。
4. 用 refresh token 换 access token。
5. 用 tokeninfo 验证 email / client / scope。
6. 不保存 token 明文，只记录 scope 和结论。
```

## 相关文件

- 概念说明：[Google OAuth、Gmail API 与 gogcli 本地授权](../concepts/google-oauth-gmail-gogcli.md)
- 排障记录：[gogcli Gmail OAuth token 定位与验证](../troubleshooting/gogcli-gmail-oauth-token-location-and-verification.md)
