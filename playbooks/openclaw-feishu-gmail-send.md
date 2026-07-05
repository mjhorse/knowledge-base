---
type: playbook
tags: [openclaw, feishu, gmail, gogcli, m78, proxy, keychain]
status: captured
date: 2026-07-05
---

# 操作手册：OpenClaw/飞书远程触发本地 Gmail 发信

## 适用场景

通过飞书向本地 OpenClaw 下发指令，让本机使用 `gog` / Gmail API 发送邮件。

适用于：

- 手机端飞书远程指示 OpenClaw 发邮件。
- 本机 OpenClaw 调用 Gmail API。
- 排查远程发信命令卡住、超时、需要输入 `gogcli` 密码等问题。

## 前置条件

1. OpenClaw 在本机运行，且运行用户为已完成 `gog` 授权的 macOS 用户。
2. `gog auth list` 能看到：

```text
mjhorse1984@gmail.com    default    gmail    ...    oauth
```

3. `gog` keyring backend 固定为 macOS Keychain：

```bash
gog auth keyring keychain
gog auth status
```

期望：

```text
keyring_backend	keychain
keyring_backend_source	config
```

4. M78 加速器运行，当前本地代理端口为：

```text
127.0.0.1:7892
```

5. OpenClaw workspace 已写入相关规则：

```text
/Users/mjhorse/.openclaw/workspace/TOOLS.md
/Users/mjhorse/.openclaw/workspace/AGENTS.md
```

## 操作步骤

### 1. 验证授权与网络

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog auth list --no-input
```

成功时能看到 `mjhorse1984@gmail.com`。

### 2. 查询已发送邮件验证 Gmail API 可用

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail messages search "in:sent newer_than:1d" \
  --account "mjhorse1984@gmail.com" \
  --max 3 \
  --plain \
  --no-input
```

### 3. 发送邮件

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail send \
  --account "mjhorse1984@gmail.com" \
  --to "recipient@example.com" \
  --subject "邮件标题" \
  --body "邮件正文" \
  --no-input
```

### 4. 带附件发送

```bash
HTTPS_PROXY=http://127.0.0.1:7892 HTTP_PROXY=http://127.0.0.1:7892 gog gmail send \
  --account "mjhorse1984@gmail.com" \
  --to "recipient@example.com" \
  --subject "邮件标题" \
  --body "请查收附件。" \
  --attach "/absolute/path/to/file" \
  --no-input
```

## 检查清单

- [ ] 外发邮件前确认收件人、标题、正文、附件。
- [ ] 命令带 `HTTPS_PROXY` 与 `HTTP_PROXY`，端口为 `7892`。
- [ ] 命令带 `--no-input`，避免后台等待密码。
- [ ] `gog auth list` 显示目标账号。
- [ ] `gog auth status` 显示 `keyring_backend=keychain`。
- [ ] M78 的 `mqibaCore` 正在监听 `127.0.0.1:7892`。

## 常见问题

### 为什么飞书发信会卡住 90 秒？

常见原因：

1. OpenClaw 调用 `gog` 时未带 M78 代理，访问 Google API 超时。
2. `gog` keyring backend 使用 `auto` 或 `file`，后台触发 passphrase 输入，但飞书环境无法交互。
3. 命令未带 `--no-input`，导致等待交互直到系统超时。

### 为什么手机端不应输入 gogcli 密码？

手机端飞书不适合处理本地 keyring 密码输入。应在本机将 `gog` 固定为 macOS Keychain 后端，并让后台命令无交互执行。

### 如何确认 M78 端口？

```bash
lsof -nP -iTCP:7892 -sTCP:LISTEN
```

期望看到 `mqibaCore` 监听 `127.0.0.1:7892`。

## 示例

飞书里可以描述为：

```text
用本地 Gmail mjhorse1984@gmail.com 发邮件到 xxx@example.com，标题是“...”，正文是“...”。执行 gog 时必须使用 M78 代理 127.0.0.1:7892，并加 --no-input。
```

## 相关文件

- `/Users/mjhorse/.openclaw/workspace/TOOLS.md`
- `/Users/mjhorse/.openclaw/workspace/AGENTS.md`
- `/Users/mjhorse/.zshrc`
- [gogcli Gmail OAuth 授权与验证](gogcli-gmail-oauth-auth-and-verify.md)
- [gogcli Gmail OAuth token 定位与验证](../troubleshooting/gogcli-gmail-oauth-token-location-and-verification.md)
