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
    indent = 60
    y = h - 150

    c.setFont("STSong-Light", 20)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "网站无障碍合规检测报告")
    c.setStrokeColor(COLORS["title"])
    c.line(w/2 - 120, h-55, w/2 + 120, h-55)

    c.setFont("STSong-Light", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-75, f"页面：{page_name}")
    c.drawCentredString(w/2, h-90, f"URL：{page_url[:50]}..." if len(page_url) > 50 else f"URL：{page_url}")
    c.drawCentredString(w/2, h-105, f"检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(60, h-120, w-60, h-120)

    y -= 30
    c.setFont("STSong-Light", 14)
    c.drawString(indent, y, "一、检测统计")
    c.line(indent, y-5, indent + 80, y-5)
    y -= 25
    stats_lines = [
        f"总缺陷：{stats['total']}",
        f"严重：{stats['critical']}    较严重：{stats['serious']}",
        f"一般：{stats['moderate']}    轻微：{stats['minor']}",
        f"合规率：{stats['compliance_rate']}%"
    ]
    for line in stats_lines[:-1]:
        c.drawString(indent + 10, y, line)
        y -= 18
    c.setFillColor(COLORS["success"])
    c.drawString(indent + 10, y, stats_lines[-1])
    c.setFillColor(COLORS["text"])
    y -= 40

    c.setFont("STSong-Light", 14)
    c.drawString(indent, y, "二、检测标准")
    c.line(indent, y-5, indent + 80, y-5)
    y -= 25
    for line in STANDARDS_CN.split("\n"):
        if line.strip():
            c.drawString(indent + 10, y, line.strip())
            y -= 16
    y -= 30

    c.setFont("STSong-Light", 14)
    c.drawString(indent, y, "三、缺陷详情")
    c.line(indent, y-5, indent + 80, y-5)
    y -= 25
    c.setFont("STSong-Light", 10)

    for idx, v in enumerate(violations, 1):
        if y < 120:
            c.showPage()
            y = h - 80
            c.setFont("STSong-Light", 14)
            c.drawString(indent, y, "三、缺陷详情（续）")
            c.line(indent, y-5, indent + 100, y-5)
            y -= 25
            c.setFont("STSong-Light", 10)

        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']}  [{v['impact']}]")
        y -= 18
        c.setFillColor(COLORS["text"])

        # WCAG
        wcag_level = []
        for t in v.get('tags', []):
            if t in ["wcag2a","wcag21a"]: wcag_level.append("A")
            elif t in ["wcag2aa","wcag21aa"]: wcag_level.append("AA")
            elif t in ["wcag2aaa","wcag21aaa"]: wcag_level.append("AAA")
        wcag = "/".join(sorted(set(wcag_level))) if wcag_level else "Best Practice"
        c.drawString(indent + 12, y, f"WCAG 等级：{wcag}")
        y -= 16

        c.drawString(indent + 12, y, f"描述：{v['description'][:50]}")
        y -= 16
        rem = v['description'][50:]
        while rem:
            c.drawString(indent + 12, y, rem[:50])
            rem = rem[50:]
            y -= 16

        c.drawString(indent + 12, y, f"建议：{v['help'][:50]}")
        y -= 16
        rem = v['help'][50:]
        while rem:
            c.drawString(indent + 12, y, rem[:50])
            rem = rem[50:]
            y -= 16

        selectors = []
        for node in v.get('nodes', []):
            selectors.extend(node.get('target', []))
        selectors = list(set(selectors))

        c.drawString(indent + 12, y, "元素定位：")
        y -= 16
        if not selectors:
            c.drawString(indent + 18, y, "无")
            y -= 16
        else:
            for sel in selectors:
                c.drawString(indent + 18, y, f"- {sel[:50]}")
                y -= 14
                rem_sel = sel[50:]
                while rem_sel:
                    c.drawString(indent + 18, y, rem_sel[:50])
                    rem_sel = rem_sel[50:]
                    y -= 14

        y -= 6
        c.line(indent, y, w - indent, y)
        y -= 12

    if y < 200:
        c.showPage()
        y = h - 80

    y -= 10
    c.setFont("STSong-Light", 14)
    c.drawString(indent, y, "四、免责声明")
    c.line(indent, y-5, indent + 80, y-5)
    y -= 25
    c.setFont("STSong-Light", 9)
    for line in DISCLAIMER_CN.split("\n"):
        if line.strip():
            c.drawString(indent + 10, y, line.strip())
            y -= 16

    c.save()