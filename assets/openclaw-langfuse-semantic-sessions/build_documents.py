from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

root = Path('/Users/mjhorse/knowledge-base/assets/openclaw-langfuse-semantic-sessions')
png = root / 'openclaw-langfuse-semantic-session-flow.png'
docx = root / 'openclaw-langfuse-semantic-session-experience-summary.docx'
pptx = root / 'openclaw-langfuse-semantic-session-flow.pptx'

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def para(text='', style=None, bold=False, code=False):
    style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if code else '') + '</w:rPr>'
    return f'<w:p>{style_xml}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
def bullet(text):
    return f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t>{escape(text)}</w:t></w:r></w:p>'
def table(rows):
    cells = []
    for row_i, row in enumerate(rows):
        row_xml = ''.join(f'<w:tc><w:tcPr><w:tcW w:w="{9000 // len(row)}" w:type="dxa"/>{"<w:shd w:fill=\"D9EAF7\"/>" if row_i == 0 else ""}</w:tcPr>{para(value, bold=row_i == 0)}</w:tc>' for value in row)
        cells.append(f'<w:tr>{row_xml}</w:tr>')
    grid = ''.join('<w:gridCol w:w="3000"/>' for _ in rows[0])
    return f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="6"/><w:left w:val="single" w:sz="6"/><w:bottom w:val="single" w:sz="6"/><w:right w:val="single" w:sz="6"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(cells)}</w:tbl>'

def image_paragraph(rel_id):
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="9144000" cy="5143500"/><wp:docPr id="1" name="语义化会话映射流程图"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="openclaw-langfuse-semantic-session-flow.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rel_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="5143500"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''

body = [
    para('OpenClaw Langfuse 语义化会话标识实施经验总结', 'Title'),
    para('文档用途：将一次可复用的可观测性改造沉淀为工程经验，便于在 OpenClaw、Langfuse 和其他消息渠道接入中复用。'),
    para('一、执行结论', 'Heading1'),
    para('已将 OpenClaw 的 Langfuse session.id 从难以阅读的稳定哈希，改为同时具备“来源语义 + 隐私保护 + 稳定关联”的标识。新产生的 Trace 可在 Langfuse Sessions 视图中按 agent、渠道、会话类型快速理解；历史数据和 OpenClaw 运行时会话注册表均未改动。'),
    table([['会话来源', '语义化 session.id 示例', '隐私处理'], ['WebChat 主会话', 'openclaw/main/webchat/direct/main', '固定 main，不暴露内部会话 UUID'], ['飞书群聊', 'openclaw/main/feishu/group/<shortHash>', 'oc_ 群 ID 仅在本地参与哈希'], ['飞书私聊', 'openclaw/main/feishu/direct/<shortHash>', 'ou_ 用户 ID 仅在本地参与哈希']]),
    para('二、总体流程', 'Heading1'),
    image_paragraph('rId2'),
    para('图 1　OpenClaw 本地会话到 Langfuse 语义化会话的隐私安全映射。'),
    para('三、实施方法', 'Heading1'),
    bullet('保持既有 hashUsageFamilyKey() 不变：继续生成 openclaw_usage_family_key_hash，确保历史关联方式可用。'),
    bullet('从本地 sessions.json 定位运行时会话记录，解析 agent、channel 和 chatType；WebChat 主会话明确映射到 webchat/direct/main。'),
    bullet('对飞书等外部会话对象使用 SHA-256 截断短哈希，拼接为 openclaw/{agent}/{channel}/{chatType}/{conversation}。'),
    bullet('在 metadata 中同时保存 openclaw_semantic_session_id、openclaw_agent_id、openclaw_channel、openclaw_chat_type 和稳定关联哈希。'),
    bullet('将 langfuse.trace.name 改为来源感知形式，如 openclaw-feishu-group-anthropic。'),
    para('四、关键实现约束', 'Heading1'),
    table([['约束', '处理原则'], ['隐私', '不得写出 raw usageFamilyKey、origin.from、origin.to、origin.label、飞书 oc_… 或 ou_…。'], ['可读性', '渠道与会话类型使用受控、路径安全的小写语义段；主 WebChat 会话使用 main。'], ['稳定性', '外部对象标识使用确定性 SHA-256 短哈希；同一会话持续落入同一 Langfuse Session。'], ['兼容性', '保留原始 openclaw_session_id 及 usage-family 哈希；不迁移、不重写历史 Trace。'], ['健壮性', '未知或记录缺失时，使用运行时 sessionId 的短哈希，避免多个未知会话聚合到同一个 Session。']]),
    para('五、验证记录', 'Heading1'),
    bullet('通过 node --check 对插件 JavaScript 做语法检查。'),
    bullet('通过动态 import 校验默认导出存在且插件 ID 为 langfuse-session。'),
    bullet('使用三个真实会话类型的本地记录进行运行时 metadata 检查：WebChat 主会话、飞书群聊、飞书私聊。'),
    bullet('人工确认 session.id 和新增 metadata 不包含飞书原始 oc_/ou_ 标识；usage-family 哈希仍在 usageFamilyKey 存在时输出。'),
    para('六、运行与维护说明', 'Heading1'),
    para('目标插件：/Users/mjhorse/.openclaw/extensions/openclaw-langfuse-session/index.js', code=True),
    para('会话记录来源：/Users/mjhorse/.openclaw/agents/main/sessions/sessions.json', code=True),
    para('变更对运行中的 OpenClaw 会话无侵入：插件只在新请求产生 Trace 时读取本地记录并组装外发 OTLP 属性。若未来增加新渠道，应补充渠道/会话类型的结构化解析规则，继续遵循“语义段白名单 + 外部对象哈希”的模式。'),
    para('七、风险与后续动作', 'Heading1'),
    table([['项目', '结论 / 建议'], ['历史数据', '不回填；Langfuse 中已有历史 Session 仍保留原有命名。'], ['哈希碰撞', '12 位十六进制短哈希适用于当前规模；如会话规模显著增长，可评估增加长度。'], ['新渠道接入', '先验证 usageFamilyKey 的实际结构，再定义可读的 channel/chatType 与需哈希的 conversation 部分。'], ['观测检查', '在 Langfuse Sessions 按 openclaw_semantic_session_id 或 openclaw_channel 过滤，确认命名和聚合符合预期。']]),
    para('八、可复用经验', 'Heading1'),
    para('可观测性系统中的 session 标识不应只追求唯一性，也应为运营排障提供最小必要的上下文。推荐将“可解释的非敏感维度”直接结构化展示，将“外部主体或用户标识”替换为稳定哈希，并保留单独的关联哈希字段以支持跨版本核对。这样可在可读性、隐私和诊断能力之间取得平衡。'),
]

styles = '''<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Aptos" w:eastAsia="PingFang SC"/><w:sz w:val="22"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F4E79"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F4E79"/></w:rPr></w:style></w:styles>'''
num = '''<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{''.join(body)}<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/><w:pgMar w:top="900" w:right="900" w:bottom="900" w:left="900"/></w:sectPr></w:body></w:document>'''
with ZipFile(docx, 'w', ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>''')
    z.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>''')
    z.writestr('word/document.xml', doc)
    z.writestr('word/styles.xml', styles)
    z.writestr('word/numbering.xml', num)
    z.writestr('word/_rels/document.xml.rels', '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>''')
    z.write(png, 'word/media/image1.png')

slide = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:pic><p:nvPicPr><p:cNvPr id="2" name="语义化会话映射流程图"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''
with ZipFile(pptx, 'w', ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>''')
    z.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>''')
    z.writestr('ppt/presentation.xml', '''<?xml version="1.0" encoding="UTF-8"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst/><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''')
    z.writestr('ppt/_rels/presentation.xml.rels', '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>''')
    z.writestr('ppt/slides/slide1.xml', slide)
    z.writestr('ppt/slides/_rels/slide1.xml.rels', '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/></Relationships>''')
    z.write(png, 'ppt/media/image1.png')
print(docx)
print(pptx)
