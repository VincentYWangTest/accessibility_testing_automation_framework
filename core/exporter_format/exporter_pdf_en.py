from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from .base import COLORS, STANDARDS_EN, DISCLAIMER_EN

def build_pdf_en(violations, page_name, page_url, stats, path):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4

    # Title section - beautified
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "Web Accessibility Compliance Report")
    
    # Title underline
    c.setStrokeColor(COLORS["title"])
    c.setLineWidth(1.5)
    c.line(w/2 - 150, h-55, w/2 + 150, h-55)

    # Page info
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-75, f"Page: {page_name}")
    c.drawCentredString(w/2, h-90, f"URL: {page_url[:50]}{'...' if len(page_url) > 50 else ''}")
    c.drawCentredString(w/2, h-105, f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Separator line
    c.setStrokeColor(COLORS["border"])
    c.setLineWidth(1)
    c.line(60, h-120, w-60, h-120)

    y = h - 150
    indent = 60

    # 1. Summary
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "1. Summary")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 60, y-5)
    
    y -= 25
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS["text"])
    stats_lines = [
        f"Total Issues: {stats['total']}",
        f"Critical: {stats['critical']}  Serious: {stats['serious']}",
        f"Moderate: {stats['moderate']}  Minor: {stats['minor']}",
        f"Compliance Rate: {stats['compliance_rate']}%"
    ]
    for line in stats_lines[:-1]:
        c.drawString(indent+10, y, line)
        y -= 18
    # Highlight compliance rate
    c.setFillColor(COLORS["success"])
    c.drawString(indent+10, y, stats_lines[-1])
    c.setFillColor(COLORS["text"])
    y -= 35

    # 2. Testing Standards - new section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "2. Testing Standards")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 120, y-5)
    
    y -= 25
    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS["standard"])
    for line in STANDARDS_EN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 18
    c.setFillColor(COLORS["text"])
    y -= 35

    # 3. Issues Details
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "3. Issues Details")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 110, y-5)
    
    y -= 25
    c.setFont("Helvetica", 10)

    for idx, v in enumerate(violations, 1):
        if y < 80:
            c.showPage()
            y = h - 80
            # New page title
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(COLORS["title"])
            c.drawString(indent, y, "3. Issues Details (Continued)")
            c.setStrokeColor(COLORS["border"])
            c.line(indent, y-5, indent + 140, y-5)
            y -= 25
            c.setFont("Helvetica", 10)
        
        # Issue severity color
        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']} [{v['impact']}]")
        y -= 16
        
        # Issue description
        c.setFillColor(COLORS["text"])
        desc = v['description']
        c.drawString(indent+10, y, f"Description: {desc[:50]}")
        y -= 16
        if len(desc) > 50:
            remaining_desc = desc[50:]
            for i in range(0, len(remaining_desc), 50):
                c.drawString(indent+10, y, remaining_desc[i:i+50])
                y -= 16
        
        # Fix suggestion
        help_text = v['help']
        c.drawString(indent+10, y, f"Recommendation: {help_text[:50]}")
        y -= 16
        if len(help_text) > 50:
            c.drawString(indent+10, y, help_text[50:100])
            y -= 16
        
        # Separator line
        c.setStrokeColor(COLORS["border"])
        c.line(indent, y-5, w-indent, y-5)
        y -= 15

    # 4. Disclaimer
    if y < 180:
        c.showPage()
        y = h - 80
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(COLORS["title"])
    c.drawString(indent, y, "4. Disclaimer")
    c.setStrokeColor(COLORS["border"])
    c.line(indent, y-5, indent + 80, y-5)
    
    y -= 25
    c.setFont("Helvetica", 9)
    for line in DISCLAIMER_EN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 16

    c.save()