from __future__ import annotations

import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


def _col(index):
    out = ""
    while index: index, rem = divmod(index - 1, 26); out = chr(65 + rem) + out
    return out


def _cell(ref, value, style=0):
    if isinstance(value, (int, float)) and not isinstance(value, bool): return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{escape(str(value or ""))}</t></is></c>'


def _sheet(rows, widths, freeze=True, filter_row=None):
    body = []
    for r, row in enumerate(rows, 1): body.append(f'<row r="{r}">'+"".join(_cell(f'{_col(c)}{r}', v, 1 if r == 1 else 0) for c, v in enumerate(row, 1))+"</row>")
    cols = "".join(f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths, 1))
    views = '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>' if freeze else '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
    filt = f'<autoFilter ref="A{filter_row}:{_col(len(widths))}{max(len(rows),filter_row)}"/>' if filter_row else ""
    return f'<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">{views}<cols>{cols}</cols><sheetData>{"".join(body)}</sheetData>{filt}</worksheet>'


def export_leads(db, output: Path, keyword="", level="", task_id=None, status="") -> Path:
    leads = db.list_leads(keyword, level, task_id=task_id, status=status)
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter(row["level"] for row in leads)
    overview = [["抖音获客系统导出", "结果"], ["任务ID", task_id or "全部"], ["关键词", keyword or "全部"], ["导出客户", len(leads)], ["高意向", counts["高"]], ["中意向", counts["中"]], ["低意向", counts["低"]], ["导出时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")], ["说明", "仅包含公开资料，敏感联系方式已脱敏，不得用于骚扰或未经授权的商业用途。"]]
    headers = ["排名","任务ID","意向等级","意向分","公开昵称","公开用户ID","公开主页","关键词","原评论","来源视频","原视频地址","命中规则","跟进状态","标签","备注","证据数","首次发现","最后发现"]
    data=[headers]
    for i,r in enumerate(leads,1):
        evidence=db.lead_evidence(r["id"]); first_evidence=evidence[0] if evidence else {}
        data.append([i,r["task_id"],r["level"],r["score"],r["nickname"],r["user_id"],r["profile_url"],r["keyword"],first_evidence["comment_text"] if evidence else "",first_evidence["video_title"] if evidence else "",first_evidence["video_url"] if evidence else "",first_evidence["matched"] if evidence else "",r["status"],r["tags"],r["note"],r["evidence_count"],r["first_seen"],r["last_seen"]])
    with db.connect() as connection:
        logs = connection.execute("SELECT stage,target,status,found,message,created_at FROM operation_logs ORDER BY id DESC LIMIT 2000").fetchall()
    log_rows = [["阶段","对象","状态","发现数量","消息","时间"]] + [list(x) for x in logs]
    content_types = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    workbook = '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="概览" sheetId="1" r:id="rId1"/><sheet name="意向客户" sheetId="2" r:id="rId2"/><sheet name="运行记录" sheetId="3" r:id="rId3"/></sheets></workbook>'
    wb_rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
    styles = '<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Microsoft YaHei"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Microsoft YaHei"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1677FF"/></patternFill></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf/><xf fontId="1" fillId="2" applyFont="1" applyFill="1"/></cellXfs></styleSheet>'
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types); z.writestr("_rels/.rels", rels); z.writestr("xl/workbook.xml", workbook); z.writestr("xl/_rels/workbook.xml.rels", wb_rels); z.writestr("xl/styles.xml", styles)
        z.writestr("xl/worksheets/sheet1.xml", _sheet(overview,[24,88],False)); z.writestr("xl/worksheets/sheet2.xml", _sheet(data,[8,9,10,9,18,25,42,18,45,35,42,35,12,18,30,9,20,20],True,1)); z.writestr("xl/worksheets/sheet3.xml", _sheet(log_rows,[14,28,12,12,55,20],True,1))
    return output
