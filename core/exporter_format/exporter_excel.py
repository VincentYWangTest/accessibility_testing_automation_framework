from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def build_excel(violations, page_name, page_url, stats, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "检测报告"

    ws.merge_cells('A1:F1')
    ws['A1'] = "网站无障碍检测报告"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    ws['A2'] = "页面"
    ws['B2'] = page_name
    ws['A3'] = "URL"
    ws['B3'] = page_url
    ws['A4'] = "总缺陷"
    ws['B4'] = stats['total']
    ws['C4'] = "严重"
    ws['D4'] = stats['critical']
    ws['E4'] = "合规率"
    ws['F4'] = f"{stats['compliance_rate']}%"

    headers = ["序号", "缺陷ID", "等级", "问题描述", "修复建议"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=6, column=col, value=h)
        cell.fill = PatternFill("solid", fgColor="2c3e50")
        cell.font = Font(color="FFFFFF", bold=True)

    for i, v in enumerate(violations, 1):
        row = 6 + i
        ws.cell(row=row, column=1, value=i)
        ws.cell(row=row, column=2, value=v['id'])
        ws.cell(row=row, column=3, value=v['impact'])
        ws.cell(row=row, column=5, value=v['description'])
        ws.cell(row=row, column=6, value=v['help'])

    wb.save(path)