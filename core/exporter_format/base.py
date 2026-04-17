from datetime import datetime
from reportlab.lib.colors import HexColor

def calc_stats(violations):
    total = len(violations)
    critical = len([v for v in violations if v["impact"] == "critical"])
    serious  = len([v for v in violations if v["impact"] == "serious"])
    moderate = len([v for v in violations if v["impact"] == "moderate"])
    minor    = len([v for v in violations if v["impact"] == "minor"])

    compliance = 100.0
    if total > 0:
        compliance = round((1 - (critical + serious) / (total + 100)) * 100, 2)
    return {
        "total": total,
        "critical": critical,
        "serious": serious,
        "moderate": moderate,
        "minor": minor,
        "compliance_rate": compliance
    }

STANDARDS_CN = """
1. WCAG 2.1 AA 国际Web无障碍标准
2. GB/T 38604-2020 信息无障碍国家标准
3. axe-core 行业权威检测引擎
"""

STANDARDS_EN = """
1. WCAG 2.1 AA International Standard
2. GB/T 38604-2020 National Standard
3. axe-core Engine
"""

DISCLAIMER_CN = """
1. 本报告由自动化检测工具生成，仅供网站无障碍优化参考，不具备法定认证效力。
2. 报告为检测时刻页面快照结果，页面内容更新后需重新检测。
3. 因使用本报告所产生的任何直接或间接损失，检测方不承担责任。
4. 本报告可用于企事业单位内部整改、合规自查、工作汇报等场景。
"""

DISCLAIMER_EN = """
1. This report is generated automatically and for reference only.
2. It reflects the page status at the time of testing.
3. We are not responsible for any loss caused by using this report.
4. This report can be used for internal compliance and reporting.
"""

COLORS = {
    "critical": HexColor("#dc3545"),
    "serious": HexColor("#fd7e14"),
    "moderate": HexColor("#ffc107"),
    "minor": HexColor("#6c757d"),
    "title": HexColor("#2c3e50"),
    "text": HexColor("#333333"),
    "success": HexColor("#28a745"),
}