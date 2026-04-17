# core/exporter.py 【最终完整版】
import os
from datetime import datetime
from .exporter_format.base import calc_stats
from .exporter_format.exporter_csv import build_csv
from .exporter_format.exporter_html import build_html
from .exporter_format.exporter_excel import build_excel
from .exporter_format.exporter_csv_en import build_csv_en
from .exporter_format.exporter_html_en import build_html_en
from .exporter_format.exporter_excel_en import build_excel_en
from .exporter_format.exporter_pdf_cn import build_pdf_cn
from .exporter_format.exporter_pdf_en import build_pdf_en

# ====================== 你原来的方法（保留）======================
def export_dashboard(violations, page_name, page_url):
    # 兼容你旧代码，不报错
    export_all(violations, page_name, page_url)

# ====================== 你现在的新方法（5种报告）======================
def export_all(violations, page_name, page_url):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"reports/{page_name}_{ts}"
    stats = calc_stats(violations)

    build_csv(violations, page_name, page_url, stats, f"{base}.csv")
    build_html(violations, page_name, page_url, stats, f"{base}.html")
    build_excel(violations, page_name, page_url, stats, f"{base}.xlsx")
    build_csv_en(violations, page_name, page_url, stats, f"{base}_en.csv")
    build_html_en(violations, page_name, page_url, stats, f"{base}_en.html")
    build_excel_en(violations, page_name, page_url, stats, f"{base}_en.xlsx")
    build_pdf_cn(violations, page_name, page_url, stats, f"{base}_cn.pdf")
    build_pdf_en(violations, page_name, page_url, stats, f"{base}_en.pdf")

    print(f"\n✅ 5 种报告已生成：{base}.*\n")