from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from .base import COLORS, STANDARDS_EN, DISCLAIMER_EN

def build_pdf_en(violations, page_name, page_url, stats, path):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "Web Accessibility Report")

    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-70, f"Page: {page_name}")
    c.drawCentredString(w/2, h-85, f"URL: {page_url[:50]}...")
    c.drawCentredString(w/2, h-100, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(60, h-115, w-60, h-115)

    y = h - 140
    indent = 60

    c.setFont("Helvetica-Bold", 13)
    c.drawString(indent, y, "1. Summary")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(indent+10, y, f"Total: {stats['total']}")
    y -= 15
    c.drawString(indent+10, y, f"Critical: {stats['critical']}  Serious: {stats['serious']}")
    y -= 15
    c.drawString(indent+10, y, f"Moderate: {stats['moderate']}  Minor: {stats['minor']}")
    y -= 15
    c.setFillColor(COLORS["success"])
    c.drawString(indent+10, y, f"Compliance Rate: {stats['compliance_rate']}%")
    c.setFillColor(COLORS["text"])
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(indent, y, "2. Issues")
    y -= 20
    c.setFont("Helvetica", 10)

    for idx, v in enumerate(violations, 1):
        if y < 80:
            c.showPage()
            y = h - 60
        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']} [{v['impact']}]")
        y -= 14
        c.setFillColor(COLORS["text"])
        c.drawString(indent+10, y, f"Desc: {v['description'][:50]}")
        y -= 14
        c.drawString(indent+10, y, f"Fix: {v['help'][:50]}")
        y -= 18
        c.line(indent, y, w-indent, y)
        y -= 10

    if y < 150:
        c.showPage()
        y = h - 60
    c.setFont("Helvetica-Bold", 13)
    c.drawString(indent, y, "3. Disclaimer")
    y -= 20
    c.setFont("Helvetica", 9)
    for line in DISCLAIMER_EN.split("\n"):
        if line.strip():
            c.drawString(indent+10, y, line.strip())
            y -= 14

    c.save()