from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def build_excel_en(violations, page_name, page_url, stats, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Accessibility Report"

    # 标题
    ws.merge_cells('A1:F1')
    ws['A1'] = "Website Accessibility Test Report"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # 基础信息
    ws['A2'] = "Page"
    ws['B2'] = page_name
    ws['A3'] = "URL"
    ws['B3'] = page_url
    ws['A4'] = "Total Issues"
    ws['B4'] = stats['total']
    ws['C4'] = "Critical"
    ws['D4'] = stats['critical']
    ws['E4'] = "Compliance Rate"
    ws['F4'] = f"{stats['compliance_rate']}%"

    # 表头
    headers = ["No.", "Issue ID", "Severity", "Description", "Fix Recommendation"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=6, column=col, value=h)
        cell.fill = PatternFill("solid", fgColor="2c3e50")
        cell.font = Font(color="FFFFFF", bold=True)

    # 缺陷明细
    for i, v in enumerate(violations, 1):
        row = 6 + i
        ws.cell(row=row, column=1, value=i)
        ws.cell(row=row, column=2, value=v['id'])
        ws.cell(row=row, column=3, value=v['impact'])
        ws.cell(row=row, column=4, value=v['description'])  # 修正原代码列号错位问题
        ws.cell(row=row, column=5, value=v['help'])         # 修正原代码列号错位问题

    wb.save(path)