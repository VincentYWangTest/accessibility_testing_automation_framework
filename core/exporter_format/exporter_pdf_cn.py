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

    # 标题部分 - 美化
    c.setFont("STSong-Light", 20)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "网站无障碍合规检测报告")
    
    # 副标题下划线
    c.setStrokeColor(COLORS["title"])
    c.setLineWidth(1.5)
    c.line(w/2 - 120, h-55, w/2 + 120, h-55)

    # 页面信息 - 调整间距和格式
    c.setFont("STSong-Light", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-75, f"页面：{page_name}")
    c.drawCentredString(w/2, h-90, f"URL：{page_url[:50]}{'...' if len(page_url) > 50 else ''}")
    c.drawCentredString(w/2, h-105, f"检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 分隔线
    c.setStrokeColor(COLORS["border"])
    c.setLineWidth(1)
    c.line(60, h-120, w-60, h-120)

    y = h - 150
    indent = 60

    # 1. 检测统计 - 美化
    c.setFont("STSong-Light", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "一、检测统计")
    # 小标题下划线
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 80, y-5)
    
    y -= 25
    c.setFont("STSong-Light", 11)
    c.setFillColor(COLORS["text"])
    # 统计信息排版优化
    stats_lines = [
        f"总缺陷：{stats['total']}",
        f"严重：{stats['critical']}  较严重：{stats['serious']}",
        f"一般：{stats['moderate']}  轻微：{stats['minor']}",
        f"合规率：{stats['compliance_rate']}%"
    ]
    for line in stats_lines[:-1]:
        c.drawString(indent+10, y, line)
        y -= 18
    # 合规率突出显示
    c.setFillColor(COLORS["success"])
    c.drawString(indent+10, y, stats_lines[-1])
    c.setFillColor(COLORS["text"])
    y -= 35

    # 2. 检测标准 - 新增部分
    c.setFont("STSong-Light", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "二、检测标准")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 80, y-5)
    
    y -= 25
    c.setFont("STSong-Light", 11)
    c.setFillColor(COLORS["standard"])
    for line in STANDARDS_CN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 18
    c.setFillColor(COLORS["text"])
    y -= 35

    # 3. 缺陷详情
    c.setFont("STSong-Light", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "三、缺陷详情")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 80, y-5)
    
    y -= 25
    c.setFont("STSong-Light", 10)

    for idx, v in enumerate(violations, 1):
        # 页面不足时新建页面
        if y < 80:
            c.showPage()
            y = h - 80
            # 新页面标题
            c.setFont("STSong-Light", 14)
            c.setFillColor(COLORS["title"])
            c.drawString(indent, y, "三、缺陷详情（续）")
            c.setStrokeColor(COLORS["border"])
            c.line(indent, y-5, indent + 100, y-5)
            y -= 25
            c.setFont("STSong-Light", 10)
        
        # 缺陷级别标色
        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']} [{v['impact']}]")
        y -= 16
        
        # 缺陷描述
        c.setFillColor(COLORS["text"])
        desc = v['description']
        c.drawString(indent+10, y, f"描述：{desc[:50]}")
        y -= 16
        if len(desc) > 50:
            remaining_desc = desc[50:]
            # 分段显示长描述
            for i in range(0, len(remaining_desc), 50):
                c.drawString(indent+10, y, remaining_desc[i:i+50])
                y -= 16
        
        # 修复建议
        help_text = v['help']
        c.drawString(indent+10, y, f"建议：{help_text[:50]}")
        y -= 16
        if len(help_text) > 50:
            c.drawString(indent+10, y, help_text[50:100])
            y -= 16
        
        # 分隔线
        c.setStrokeColor(COLORS["border"])
        c.line(indent, y-5, w-indent, y-5)
        y -= 15

    # 4. 免责声明
    if y < 180:
        c.showPage()
        y = h - 80
    
    c.setFont("STSong-Light", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "四、免责声明")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 80, y-5)
    
    y -= 25
    c.setFont("STSong-Light", 9)
    for line in DISCLAIMER_CN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 16

    c.save()