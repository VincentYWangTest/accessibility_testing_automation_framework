import os
import json
from datetime import datetime
from fpdf import FPDF
from core.logger import get_logger

logger = get_logger()

def export_all(violations, page_name, page):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = f"reports/{page_name}_{ts}"

    export_csv(violations, f"{base_path}.csv")
    export_json(violations, f"{base_path}.json")
    export_html(violations, page_name, f"{base_path}.html")
    export_pdf(violations, page_name, f"{base_path}.pdf")

def export_csv(violations, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("No.,ID,Impact,Description,Fix Suggestion,Page\n")
        for idx, v in enumerate(violations, 1):
            desc = v["description"].replace(",", "，").replace("\n", " ")
            help = v["help"].replace(",", "，").replace("\n", " ")
            f.write(f"{idx},{v['id']},{v['impact']},{desc},{help},{os.path.basename(path).split('_')[0]}\n")

def export_json(violations, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "page": os.path.basename(path).split('_')[0],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "violations": violations
        }, f, indent=2, ensure_ascii=False)

def export_html(violations, page_name, path):
    total = len(violations)
    critical = len([v for v in violations if v["impact"] == "critical"])
    serious = len([v for v in violations if v["impact"] == "serious"])
    moderate = len([v for v in violations if v["impact"] == "moderate"])
    minor = len([v for v in violations if v["impact"] == "minor"])

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Accessibility Report | {page_name}</title>
        <style>
            body {{font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;}}
            .header {{text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px;}}
            .summary {{margin: 30px 0; padding: 20px; background: #f5f5f5; border-radius: 8px;}}
            .critical {{color: #dc3545; font-weight: bold;}}
            .serious {{color: #fd7e14;}}
            .moderate {{color: #ffc107;}}
            .minor {{color: #6c757d;}}
            .issue {{margin: 20px 0; padding: 15px; border-left: 4px solid #333; background: #f9f9f9;}}
        </style>
    </head>
    <body>
        <div class="header"><h1>Accessibility Report - {page_name}</h1></div>
        <div class="summary">
            <p>Total: {total} | Critical: {critical} | Serious: {serious} | Moderate: {moderate} | Minor: {minor}</p>
        </div>
    """
    for idx, v in enumerate(violations, 1):
        html += f"<div class='issue {v['impact']}'><h3>{idx}. {v['id']} ({v['impact'].upper()})</h3><p>{v['description']}</p><p><b>Fix:</b> {v['help']}</p></div>"
    html += "</body></html>"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

# ====================== ✅ 新增：PDF 报告 ======================
def export_pdf(violations, page_name, path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Accessibility Test Report: {page_name}", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    total = len(violations)
    critical = len([v for v in violations if v["impact"] == "critical"])
    serious = len([v for v in violations if v["impact"] == "serious"])
    moderate = len([v for v in violations if v["impact"] == "moderate"])
    minor = len([v for v in violations if v["impact"] == "minor"])

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 8, f"Total Issues: {total}", ln=True)
    pdf.cell(200, 8, f"Critical: {critical}", ln=True)
    pdf.cell(200, 8, f"Serious: {serious}", ln=True)
    pdf.cell(200, 8, f"Moderate: {moderate}", ln=True)
    pdf.cell(200, 8, f"Minor: {minor}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Issue Details", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    for idx, v in enumerate(violations, 1):
        pdf.set_font("Arial", "B", 11)
        pdf.cell(200, 8, f"{idx}. {v['id']} | {v['impact'].upper()}", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(200, 6, f"Description: {v['description']}")
        pdf.multi_cell(200, 6, f"Fix Suggestion: {v['help']}")
        pdf.ln(3)

    pdf.output(path)
    logger.info(f"✅ PDF report generated: {path}")

def export_dashboard(stats):
    path = "reports/dashboard.html"
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Accessibility Summary Dashboard</title>
        <style>
            body {{font-family: Arial, sans-serif; margin: 40px;}}
            table {{width:100%; border-collapse:collapse;}}
            th,td{{border:1px solid #ddd; padding:10px;}}
            th{{background:#333; color:white;}}
        </style>
    </head>
    <body>
        <h1>Accessibility Test Dashboard</h1>
        <p>Total Pages: {stats['total_pages']}</p>
        <p>Total Issues: {stats['total_issues']}</p>
        <table>
            <tr><th>Page</th><th>Total</th><th>Critical</th><th>Serious</th><th>Moderate</th><th>Minor</th></tr>
    """
    for p in stats["pages"]:
        html += f"<tr><td>{p['page_name']}</td><td>{p['total']}</td><td>{p['critical']}</td><td>{p['serious']}</td><td>{p['moderate']}</td><td>{p['minor']}</td></tr>"
    html += "</table></body></html>"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)