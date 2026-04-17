from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from .base import COLORS, STANDARDS_CN, DISCLAIMER_CN

def build_pdf_cn(violations, page_name, page_url, stats, path):
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4

    c.setFont("STSong-Light", 18)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "网站无障碍合规检测报告")

    c.setFont("STSong-Light", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-70, f"页面：{page_name}")
    c.drawCentredString(w/2, h-85, f"URL：{page_url[:50]}...")
    c.drawCentredString(w/2, h-100, f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(60, h-115, w-60, h-115)

    y = h - 140
    indent = 60

    c.setFont("STSong-Light", 13)
    c.drawString(indent, y, "一、检测统计")
    y -= 20
    c.setFont("STSong-Light", 11)
    c.drawString(indent+10, y, f"总缺陷：{stats['total']}")
    y -= 15
    c.drawString(indent+10, y, f"严重：{stats['critical']}  较严重：{stats['serious']}")
    y -= 15
    c.drawString(indent+10, y, f"一般：{stats['moderate']}  轻微：{stats['minor']}")
    y -= 15
    c.setFillColor(COLORS["success"])
    c.drawString(indent+10, y, f"合规率：{stats['compliance_rate']}%")
    c.setFillColor(COLORS["text"])
    y -= 30

    c.setFont("STSong-Light", 13)
    c.drawString(indent, y, "二、缺陷详情")
    y -= 20
    c.setFont("STSong-Light", 10)

    for idx, v in enumerate(violations, 1):
        if y < 80:
            c.showPage()
            y = h - 60
        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']} [{v['impact']}]")
        y -= 14
        c.setFillColor(COLORS["text"])
        c.drawString(indent+10, y, f"描述：{v['description'][:50]}")
        y -= 14
        if len(v['description'])>50:
            c.drawString(indent+10, y, v['description'][50:100])
            y -=14
        c.drawString(indent+10, y, f"建议：{v['help'][:50]}")
        y -= 18
        c.line(indent, y, w-indent, y)
        y -= 10

    if y < 150:
        c.showPage()
        y = h - 60
    c.setFont("STSong-Light", 13)
    c.drawString(indent, y, "三、免责声明")
    y -= 20
    c.setFont("STSong-Light", 9)
    for line in DISCLAIMER_CN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 14

    c.save()