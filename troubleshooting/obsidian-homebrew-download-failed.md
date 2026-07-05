---
type: troubleshooting
project: knowledge-base
date: 2026-07-05
tags: [obsidian, homebrew, github, download]
severity: low
status: resolved
---

# 问题：Homebrew 安装 Obsidian 下载失败

## 现象

执行 Homebrew cask 安装 Obsidian 时，下载官方 DMG 失败或长时间卡住：

```text
brew install --cask obsidian
```

错误信息包括：

```text
Download failed: https://github.com/obsidianmd/obsidian-releases/releases/download/v1.12.7/Obsidian-1.12.7.dmg
curl: (92) HTTP/2 stream 1 was not closed cleanly: PROTOCOL_ERROR
```

重试时也可能一直停留在：

```text
Fetching downloads for: obsidian
```

## 环境

- macOS
- Homebrew cask
- Obsidian 版本：`1.12.7`
- 官方下载文件：`Obsidian-1.12.7.dmg`

## 影响范围

- 影响通过 Homebrew 自动下载和安装 Obsidian。
- 不影响手动从 Obsidian 官网下载 DMG。
- 不影响已下载 DMG 的本地安装。

## 排查过程

- 确认 Homebrew 可用。
- 确认 `/Applications/Obsidian.app` 最初不存在。
- Homebrew 自动更新成功，但下载 Obsidian DMG 时失败。
- 官网下载速度正常，且本机 `~/Downloads` 已存在 `Obsidian-1.12.7.dmg`。
- 改用本地 DMG 安装。

## 根因判断

问题出在 Homebrew 经 GitHub release 下载 DMG 时的网络连接中断或 HTTP/2 协议异常，不是 Obsidian 应用本身或本地知识库配置问题。

## 解决方案

使用已下载的官方 DMG 手动安装：

```bash
hdiutil attach "$HOME/Downloads/Obsidian-1.12.7.dmg" -nobrowse
cp -R "/Volumes/Obsidian 1.12.7-universal/Obsidian.app" "/Applications/Obsidian.app"
hdiutil detach "/Volumes/Obsidian 1.12.7-universal"
open -a Obsidian
```

## 验证结果

- `/Applications/Obsidian.app` 已存在。
- Obsidian 已成功打开。
- `/Users/mjhorse/knowledge-base` 已作为 Vault 使用。
- Obsidian Git 插件已安装并启用。

## 预防措施

- 如果 Homebrew cask 下载 GitHub release 失败，可优先使用官网 DMG 手动安装。
- 如果必须使用 Homebrew，可在网络稳定或代理可用时重试。
- 对于 GUI 应用，保留下载好的 DMG 可作为备用安装来源。

## 相关文件

- 本地 DMG：`~/Downloads/Obsidian-1.12.7.dmg`
- 应用路径：`/Applications/Obsidian.app`
- Vault 路径：`/Users/mjhorse/knowledge-base`
