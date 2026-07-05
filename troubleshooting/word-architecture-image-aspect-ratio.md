---
type: troubleshooting
project: litellm-langfuse
date: 2026-07-05
tags: [word, ppt, svg, image, architecture-doc]
severity: low
status: resolved
---

# 问题：Word 架构图显示不完整或比例异常

## 现象

生成 Word 架构设计文档后，嵌入的架构图显示不完整或比例不正确。

## 根因判断

原始 SVG 为 `1600x1000`，但 QuickLook 生成的 PNG 缩略图变成了 `1600x1600`，导致 Word 中按错误比例显示。

## 解决方案

使用 macOS `sips` 转换 SVG：

```bash
sips -s format png input.svg --out output.png
```

转换后检查尺寸：

```bash
sips -g pixelWidth -g pixelHeight output.png
```

## 预防措施

生成 Word 架构文档时保留 SVG/PPT 源文件，并在嵌入前检查图片比例。
