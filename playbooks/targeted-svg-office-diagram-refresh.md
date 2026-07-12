---
type: playbook
tags: [svg, diagram, docx, pptx, office, verification, litellm]
status: verified
project: litellm-langfuse
---

# 操作手册：定向刷新 SVG 架构图与 Word/PPT 内嵌媒体

## 适用场景

用于修复既有 SVG 架构图、时序图或部署图的箭头端点、箭头头部等渲染问题，并且仅把已修复 PNG 定向刷新到现有 DOCX/PPTX。尤其适用于 Office 中出现箭头未接触目标生命线/组件边缘的情况。

本流程避免重跑会重写全部图、文档或演示文件的生成脚本，从而控制变更范围。

## 已验证原则

- SVG 是图形源文件；对应的生成脚本也必须同步修改，防止未来重生成回退。
- 手写 `<polygon>` 箭头中，path 终点与 polygon 第一个点（箭头尖端）必须完全相同，且均落在目标生命线或组件外边缘。
- 目标媒体映射必须通过 OpenXML relationship/XML 确认，不能仅按图片编号猜测。
- 定向更新时，只替换准确的 ZIP 成员，例如 DOCX 的 `word/media/image2.png` 与 PPTX 的 `ppt/media/image2.png`；其余 ZIP 内容保持原样。
- 写入临时文件、使用 `ZipFile.testzip()` 校验、校验替换字节后才原子替换原件。

## 前置条件

- 已知需要修改的 SVG、PNG、DOCX、PPTX 和生成脚本路径。
- 已确认目标箭头的源/目标坐标以及 Office 内对应的媒体成员。
- macOS 环境可使用 `sips`。
- Python 标准库可使用 `zipfile`。

## 操作步骤

1. **先读后改**：读取 SVG 中的 path、polygon、生命线/卡片坐标；读取生成脚本中相同图的生成逻辑；读取 DOCX/PPTX 的媒体列表和关系文件。
2. **精确修复几何**：只修改受影响 path 的终点和 polygon 尖端；右向箭头使用 `b,y b-20,y-10 b-20,y+10`，左向箭头使用 `b,y b+20,y-10 b+20,y+10`。保持标签、颜色、标题、泳道、其他图不变。
3. **同步生成逻辑**：生成脚本保留生命线到生命线坐标，依据 `b > a` 生成右向或左向 polygon；不要再用会产生内缩的 marker-end 逻辑。
4. **仅渲染目标 PNG**：
   ```bash
   sips -s format png "<diagram>.svg" --out "<diagram>.png"
   ```
5. **安全替换内嵌媒体**：在目标文件同目录创建临时 ZIP，复制所有原成员，仅以新 PNG 替换映射成员。对临时文件执行 `testzip()`，并确认嵌入 PNG 与独立 PNG 字节一致后再原子替换。
6. **打开成品检查**：打开 PNG、DOCX、PPTX，按照最终 Office 展示尺寸检查连接点。

## 检查清单

- [ ] PNG 为有效格式，尺寸与 SVG 预期一致。
- [ ] 所有被改 arrow path 终点都等于指定目标坐标。
- [ ] 每个 polygon 的第一个 point 等于相应 path 终点。
- [ ] SVG 中箭头尖端列表与预期坐标逐项匹配。
- [ ] DOCX、PPTX 都满足 `ZipFile.testzip() is None`。
- [ ] DOCX/PPTX 的目标嵌入媒体与独立 PNG 的 SHA-256 一致。
- [ ] DOCX relationship 仍指向预期 `word/media/...`，图片引用数量不变且每张预期图仅引用一次。
- [ ] PPTX 对应媒体路径正确，其他媒体和 XML 未改动。
- [ ] 生成脚本通过 Python 语法编译。
- [ ] 视觉检查无箭头空隙、无箭头过度进入组件/生命线、无箭头尖端裁剪。

## LiteLLM 架构图实例（2026-07-12）

在 `/Users/mjhorse/ai-observability/litellm/litellm-client-routing-design/` 中，修复了 `02-request-sequence.svg` 的 7 条时序消息箭头，使尖端精确接触目标生命线；仅重渲染 `02-request-sequence.png`，并定向更新：

- `litellm-client-routing-architecture-design.docx` → `word/media/image2.png`
- `litellm-client-routing-architecture-diagram.pptx` → `ppt/media/image2.png`

验证结果：PNG 为 `1800 × 1020`；两份 Office 包完整性通过；内嵌媒体 SHA-256 与独立 PNG 一致；DOCX 保留三张图的各一次引用；生成脚本通过语法检查；已打开 PNG、Word 和 PPT 进行视觉复核。

## 常见问题

- **箭头看似接近但 Office 仍有缝隙**：检查的是 polygon base 或 marker 参考点而非 polygon tip；使 path 终点和 polygon 的第一个坐标完全一致。
- **完整生成后问题复发**：只改了输出 SVG，未改生成脚本。必须同时修改对应 sequence loop。
- **替换后打开文档异常**：通常是 ZIP 重写过程遗漏成员或替换前未校验。改用逐成员复制、临时文件、`testzip()` 和原子替换。
- **替换了错误图片**：不要依赖编号猜测；从 relationship/XML 确认源图与媒体成员的语义映射。
