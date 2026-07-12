from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

root = Path('/Users/mjhorse/knowledge-base/assets/openclaw-langfuse-semantic-sessions')
png = root / 'openclaw-agent-to-langfuse-session-mapping.png'
docx = root / 'openclaw-agent-to-langfuse-session-mapping-architecture-design.docx'
pptx = root / 'openclaw-agent-to-langfuse-session-mapping-architecture.pptx'

def p(text='', style=None, bold=False, code=False):
    pr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    rp = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if code else '') + '</w:rPr>'
    return f'<w:p>{pr}<w:r>{rp}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
def bullet(text):
    return f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr><w:r><w:t>{escape(text)}</w:t></w:r></w:p>'
def tbl(rows, widths=None):
    cols = len(rows[0]); widths = widths or [9000//cols]*cols
    out=[]
    for i,row in enumerate(rows):
        cells=''.join(f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{"<w:shd w:fill=\"D9EAF7\"/>" if i==0 else ""}</w:tcPr>{p(v,bold=i==0)}</w:tc>' for j,v in enumerate(row))
        out.append(f'<w:tr>{cells}</w:tr>')
    grid=''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders><w:top w:val="single" w:sz="6"/><w:left w:val="single" w:sz="6"/><w:bottom w:val="single" w:sz="6"/><w:right w:val="single" w:sz="6"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(out)}</w:tbl>'
PAGE_WIDTH = 16838
PAGE_HEIGHT = 11906
MARGIN = 900
SAFETY_MARGIN = 800
MAX_IMAGE_WIDTH_TWIPS = PAGE_WIDTH - (2 * MARGIN) - SAFETY_MARGIN
IMAGE_RATIO = 1800 / 1080
IMAGE_WIDTH_EMU = int(MAX_IMAGE_WIDTH_TWIPS * 635)
IMAGE_HEIGHT_EMU = int(IMAGE_WIDTH_EMU / IMAGE_RATIO)


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def img():
    return f'''<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="{IMAGE_WIDTH_EMU}" cy="{IMAGE_HEIGHT_EMU}"/><wp:docPr id="1" name="Agent Session 到 Langfuse Session 映射架构"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="0" name="openclaw-agent-to-langfuse-session-mapping.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId2" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{IMAGE_WIDTH_EMU}" cy="{IMAGE_HEIGHT_EMU}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
body=[
 p('OpenClaw Agent Session 与 Langfuse Session 语义映射架构设计','Title'),
 p('文档定位：定义 OpenClaw Agent 运行时会话如何映射为 Langfuse 的可读、稳定且隐私安全的 Session 聚合标识。'),
 p('1. 设计目标与结论','Heading1'),
 p('OpenClaw 与 Langfuse 的 Session 不是同一层级的对象。OpenClaw Agent Session 用于运行时路由、上下文续接与会话生命周期管理；Langfuse Session 用于将多次模型调用按业务会话聚合展示。设计的核心不是复制 OpenClaw 的内部 UUID，而是从稳定的 usageFamilyKey 提炼会话语义后，生成适合 Langfuse 聚合与检索的 ID。'),
 tbl([['设计目标','对应方案'],['语义可读','ID 显式包含 agent、channel、chatType；WebChat 主会话直接使用 main。'],['聚合稳定','同一 usageFamilyKey 派生同一语义 Session；保留 usage-family 哈希作稳定关联。'],['隐私安全','渠道的原始 peer/group/user 标识仅本地哈希，不进入外发 ID 或 metadata。'],['兼容运行时','保留 OpenClaw 原始 sessionId 为 metadata；不修改 sessions.json 或历史 Langfuse 数据。']]),
 p('2. 领域模型与职责边界','Heading1'),
 tbl([['对象','职责','稳定性 / 可见性'],['OpenClaw sessionId','单次运行时会话实例标识；可能随 compaction/续接轮换。','不作为 Langfuse 聚合主键；保留为 openclaw_session_id。'],['usageFamilyKey','OpenClaw 会话家族/业务归属键；关联同一逻辑会话的多个 sessionId。','作为语义映射的主要输入；原值不外发。'],['Langfuse session.id','Langfuse Sessions 页面中的 Trace 聚合主键。','由语义映射层生成，供外部观测使用。'],['辅助 metadata','用于筛选、关联和故障诊断。','保留脱敏语义字段与 usageFamilyKey 哈希。']]),
 page_break(),p('3. 总体映射架构','Heading1'),img(),p('图 1　Agent Session 域、语义映射层与 Langfuse Session 域之间的责任分离和数据流。'),page_break(),
 p('4. Session Key 解析与语义分层','Heading1'),
 p('输入为本地会话记录中的 usageFamilyKey。解析目标不是把每一段原样透传，而是提取四个领域维度：agentId、channel、chatType 与 conversation。agentId、channel 和 chatType 是可读的低敏感维度；conversation 可能携带渠道侧的用户或群组对象，因此默认被视为敏感标识。'),
 tbl([['usageFamilyKey 形态','解析结果','说明'],['agent:main:main','agent=main；channel=webchat；chatType=direct；conversation=main','“main” 是 OpenClaw 主会话的特殊语义，不哈希。'],['agent:main:feishu:group:oc_<groupId>','agent=main；channel=feishu；chatType=group；conversation=oc_<groupId>','conversation 仅参与短哈希。'],['agent:main:feishu:direct:ou_<userId>','agent=main；channel=feishu；chatType=direct；conversation=ou_<userId>','conversation 仅参与短哈希。'],['agent:{agent}:{channel}:{account}:direct:{peer}','从 key 中定位 direct/group 段，再取其后的 peer','兼容带 account 范围的渠道会话键。']]),
 p('5. 具体映射规则','Heading1'),
 p('目标格式：',code=True),p('openclaw/{agent}/{channel}/{chatType}/{conversationKey}',code=True),
 tbl([['规则','conversationKey','最终 session.id 示例'],['WebChat 主会话','main','openclaw/main/webchat/direct/main'],['飞书群聊','shortHash(oc_<groupId>)','openclaw/main/feishu/group/05d9f3879d6e'],['飞书私聊','shortHash(ou_<userId>)','openclaw/main/feishu/direct/ac69e038e2bb'],['未知/本地记录未命中','shortHash(runtime sessionId)','openclaw/unknown/unknown/unknown/<shortHash>']]),
 bullet('shortHash 使用 SHA-256 后截取 12 位十六进制字符：确定性、不可直接反推原始对象，且适合 Langfuse 页面展示。'),
 bullet('semanticSegment 仅用于可读维度，转为小写路径安全片段并限制长度；不对渠道对象做语义清洗后再哈希，避免破坏其稳定性。'),
 bullet('解析时定位 direct/group 段而非依赖固定索引，以兼容带 accountId 的会话键。'),
 p('6. 外发字段与隐私边界','Heading1'),
 tbl([['字段','是否外发','用途 / 约束'],['session.id','是','语义化 Langfuse Session 聚合 ID。'],['openclaw_semantic_session_id','是','与 session.id 相同，便于 metadata 查询。'],['openclaw_usage_family_key_hash','是','usageFamilyKey 的稳定 SHA-256 截断哈希，用于关联。'],['openclaw_session_id','是','运行时诊断关联；不是 Langfuse 聚合主键。'],['openclaw_agent_id / channel / chat_type','是','低敏感、可读的筛选维度。'],['原始 usageFamilyKey','否','可能含渠道对象标识。'],['origin.from / origin.to / origin.label','否','可能含通信对象或内容相关标识。'],['飞书 oc_… / ou_…','否','只能在本地参与 shortHash 计算。']]),
 p('7. Trace 命名与数据流','Heading1'),
 p('每次 Anthropic 流式调用先通过 sessionId 查找本地 Session Record，然后构造 semantic session metadata。OTLP 导出时：session.id 使用语义化 ID；langfuse.trace.name 使用 openclaw-{channel}-{chatType}-anthropic，例如 openclaw-feishu-group-anthropic。这样 Langfuse 可同时按 Session 聚合，也可通过 Trace 名称区分调用来源。'),
 p('数据流：请求携带运行时 sessionId → 本地查找会话记录 → 解析 usageFamilyKey → 生成脱敏语义 Session ID 与 metadata → 写入 OTLP Trace → Langfuse 按 session.id 聚合。'),
 p('8. 兼容性、降级与验证','Heading1'),
 bullet('不修改 OpenClaw sessions.json、运行时会话注册或 Langfuse 已存历史数据；仅影响后续新 Trace。'),
 bullet('usageFamilyKey 不存在或本地会话记录未命中时，使用 runtime sessionId 短哈希作为 conversationKey，确保不同未知会话不会错误合并。'),
 bullet('已验证语法检查、插件动态导入、WebChat 主会话、飞书群聊与飞书私聊的实际 metadata 输出。'),
 bullet('验证要点：session.id 符合 openclaw/… 结构；飞书原始 ID 未出现；usage-family 哈希仍在 record 含 usageFamilyKey 时输出。'),
 p('9. 后续扩展规则','Heading1'),
 p('接入新渠道前，应先记录 usageFamilyKey 的真实形态，再明确哪些段是低敏感语义分类、哪些段是外部主体标识。低敏感分类可以进入路径；外部主体、群组、用户、电话号码或第三方资源 ID 必须只以稳定短哈希形式进入 conversationKey。')]
styles='''<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Aptos" w:eastAsia="PingFang SC"/><w:sz w:val="22"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F4E79"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1F4E79"/></w:rPr></w:style></w:styles>'''
numbering='''<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
document=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{''.join(body)}<w:sectPr><w:pgSz w:w="{PAGE_WIDTH}" w:h="{PAGE_HEIGHT}" w:orient="landscape"/><w:pgMar w:top="{MARGIN}" w:right="{MARGIN}" w:bottom="{MARGIN}" w:left="{MARGIN}"/></w:sectPr></w:body></w:document>'''
with ZipFile(docx,'w',ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','''<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>''')
 z.writestr('_rels/.rels','''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>''')
 z.writestr('word/document.xml',document); z.writestr('word/styles.xml',styles); z.writestr('word/numbering.xml',numbering)
 z.writestr('word/_rels/document.xml.rels','''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>''')
 z.write(png,'word/media/image1.png')
slide='''<?xml version="1.0"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:pic><p:nvPicPr><p:cNvPr id="2" name="Agent Session 映射架构"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''
with ZipFile(pptx,'w',ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','''<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>''')
 z.writestr('_rels/.rels','''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>''')
 z.writestr('ppt/presentation.xml','''<?xml version="1.0"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst/><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''')
 z.writestr('ppt/_rels/presentation.xml.rels','''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>''')
 z.writestr('ppt/slides/slide1.xml',slide); z.writestr('ppt/slides/_rels/slide1.xml.rels','''<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/></Relationships>'''); z.write(png,'ppt/media/image1.png')
print(docx); print(pptx)
