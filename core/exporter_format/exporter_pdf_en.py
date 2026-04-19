from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from .base import COLORS, STANDARDS_EN, DISCLAIMER_EN

def build_pdf_en(violations, page_name, page_url, stats, path):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    indent = 60
    y = h - 150

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(COLORS["title"])
    c.drawCentredString(w/2, h-50, "Web Accessibility Compliance Report")
    c.setStrokeColor(COLORS["title"])
    c.line(w/2 - 150, h-55, w/2 + 150, h-55)

    c.setFont("Helvetica", 11)
    c.setFillColor(COLORS["text"])
    c.drawCentredString(w/2, h-75, f"Page: {page_name}")
    c.drawCentredString(w/2, h-90, f"URL: {page_url[:50]}..." if len(page_url) > 50 else f"URL: {page_url}")
    c.drawCentredString(w/2, h-105, f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(60, h-120, w-60, h-120)

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(indent, y, "1. Summary")
    c.line(indent, y-5, indent + 60, y-5)
    y -= 25
    stats_lines = [
        f"Total Issues: {stats['total']}",
        f"Critical: {stats['critical']}    Serious: {stats['serious']}",
        f"Moderate: {stats['moderate']}    Minor: {stats['minor']}",
        f"Compliance Rate: {stats['compliance_rate']}%"
    ]
    for line in stats_lines[:-1]:
        c.drawString(indent + 10, y, line)
        y -= 18
    c.setFillColor(COLORS["success"])
    c.drawString(indent + 10, y, stats_lines[-1])
    c.setFillColor(COLORS["text"])
    y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(indent, y, "2. Testing Standards")
    c.line(indent, y-5, indent + 120, y-5)
    y -= 25
    c.setFont("Helvetica", 11)
    for line in STANDARDS_EN.split("\n"):
        if line.strip():
            c.drawString(indent + 10, y, line.strip())
            y -= 16
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(indent, y, "3. Issues Details")
    c.line(indent, y-5, indent + 110, y-5)
    y -= 25
    c.setFont("Helvetica", 10)

    for idx, v in enumerate(violations, 1):
        if y < 120:
            c.showPage()
            y = h - 80
            c.setFont("Helvetica-Bold", 14)
            c.drawString(indent, y, "3. Issues Details (Continued)")
            c.line(indent, y-5, indent + 140, y-5)
            y -= 25
            c.setFont("Helvetica", 10)

        c.setFillColor(COLORS[v["impact"]])
        c.drawString(indent, y, f"{idx}. {v['id']}  [{v['impact'].upper()}]")
        y -= 18
        c.setFillColor(COLORS["text"])

        # WCAG
        wcag_level = []
        for t in v.get('tags', []):
            if t in ["wcag2a","wcag21a"]: wcag_level.append("A")
            elif t in ["wcag2aa","wcag21aa"]: wcag_level.append("AA")
            elif t in ["wcag2aaa","wcag21aaa"]: wcag_level.append("AAA")
        wcag = "/".join(sorted(set(wcag_level))) if wcag_level else "Best Practice"
        c.drawString(indent + 12, y, f"WCAG Level: {wcag}")
        y -= 16

        c.drawString(indent + 12, y, f"Description: {v['description'][:60]}")
        y -= 16
        rem = v['description'][60:]
        while rem:
            c.drawString(indent + 12, y, rem[:60])
            rem = rem[60:]
            y -= 16

        c.drawString(indent + 12, y, f"Recommendation: {v['help'][:60]}")
        y -= 16
        rem = v['help'][60:]
        while rem:
            c.drawString(indent + 12, y, rem[:60])
            rem = rem[60:]
            y -= 16

        selectors = []
        for node in v.get('nodes', []):
            selectors.extend(node.get('target', []))
        selectors = list(set(selectors))

        c.drawString(indent + 12, y, "Element Locators:")
        y -= 16
        if not selectors:
            c.drawString(indent + 18, y, "N/A")
            y -= 16
        else:
            for sel in selectors:
                c.drawString(indent + 18, y, f"- {sel[:60]}")
                y -= 14
                rem_sel = sel[60:]
                while rem_sel:
                    c.drawString(indent + 18, y, rem_sel[:60])
                    rem_sel = rem_sel[60:]
                    y -= 14

        y -= 6
        c.line(indent, y, w - indent, y)
        y -= 12

    if y < 200:
        c.showPage()
        y = h - 80

    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(indent, y, "4. Disclaimer")
    c.line(indent, y-5, indent + 80, y-5)
    y -= 25
    c.setFont("Helvetica", 9)
    for line in DISCLAIMER_EN.split("\n"):
        if line.strip():
            c.drawString(indent + 10, y, line.strip())
            y -= 16

    c.save()