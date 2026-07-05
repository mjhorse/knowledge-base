---
type: playbook
tags: [obsidian, git, github, knowledge-base]
---

# 操作手册：配置 Obsidian + GitHub 知识库同步

## 适用场景

适用于将本地 Markdown 知识库作为 Obsidian Vault 使用，并通过 GitHub 远程仓库进行备份与同步。

## 前置条件

- 本地知识库目录已存在：`/Users/mjhorse/knowledge-base`
- 本地目录已初始化为 Git 仓库并至少有一次提交。
- GitHub 上已创建空仓库，例如：`git@github.com:mjhorse/knowledge-base.git`
- Obsidian 已安装。
- Obsidian Git 社区插件已安装并启用。

## 操作步骤

### 1. 关联 GitHub 远程仓库

在知识库目录中配置远程仓库：

```bash
cd /Users/mjhorse/knowledge-base
git remote add origin git@github.com:mjhorse/knowledge-base.git
git branch -M main
git push -u origin main
```

如果 `git remote -v` 没有输出，说明还未配置远程仓库。

### 2. 添加 Obsidian 适用的 `.gitignore`

建议忽略本机状态、缓存、临时文件和密钥：

```gitignore
.DS_Store
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache/
.trash/
*.tmp
*.temp
*.swp
*.swo
.env
*.env
```

可同步的内容主要是 Markdown、模板、项目文档、概念文档、排障文档、附件索引和必要的 Obsidian 插件配置。

### 3. 打开知识库作为 Obsidian Vault

在 Obsidian 中选择：

```text
Open folder as vault
```

选择目录：

```text
/Users/mjhorse/knowledge-base
```

也可以尝试使用 Obsidian URI：

```text
obsidian://open?path=/Users/mjhorse/knowledge-base
```

### 4. 配置 Obsidian Git 插件

进入：

```text
Obsidian → Preferences → Community plugins → Obsidian Git → Options
```

推荐配置：

```text
Auto commit interval: 10
Auto push interval: 60
Pull updates on startup: On
Auto pull interval: 0
```

说明：

- Auto commit interval：自动本地提交频率。
- Auto push interval：自动推送到 GitHub 的频率。
- Pull updates on startup：启动时先从远程拉取更新。
- Auto pull interval：单机使用时可设为 0，多设备编辑时可设为 30 或 60。

### 5. 手动同步

在 Obsidian 命令面板中按：

```text
⌘ + P
```

搜索：

```text
git
```

常用命令：

- `Obsidian Git: Sync`：推荐用于重要变更后的手动同步。
- `Obsidian Git: Push`：只上传本地已提交内容。
- `Obsidian Git: Pull`：只拉取远程更新。

## 检查清单

- `git remote -v` 能看到 `origin`。
- `git branch --show-current` 输出 `main`。
- `git push` 可以成功推送到 GitHub。
- Obsidian 能打开 `/Users/mjhorse/knowledge-base`。
- Obsidian 命令面板中能搜索到 `Obsidian Git: Sync` 或 `Push`。
- GitHub 仓库中能看到最新 Markdown 文件和 `.gitignore`。

## 常见问题

### Obsidian 里找不到 Settings

macOS 版可能显示为 `Preferences`：

```text
Obsidian → Preferences...
```

也可以用快捷键：

```text
⌘ + ,
```

### 命令面板里没有 Create backup

不同版本的 Obsidian Git 命令名称不同。优先搜索 `git`，使用：

```text
Obsidian Git: Sync
```

或分别使用：

```text
Obsidian Git: Push
Obsidian Git: Pull
```

### Push 失败显示 Repository not found

通常表示 GitHub 仓库还未创建，或当前机器 SSH key 没有访问权限。先确认远程仓库存在，再确认 SSH 权限。

## 示例

日常推荐流程：

1. 在 Obsidian 中写笔记。
2. 等待自动 commit 和 auto push。
3. 重要阶段成果完成后，手动执行 `Obsidian Git: Sync`。
4. 用 Claude Code 执行“录入知识库”时，确认文件写入 `/Users/mjhorse/knowledge-base` 后再同步。
