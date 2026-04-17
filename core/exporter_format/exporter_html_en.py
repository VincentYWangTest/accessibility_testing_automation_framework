from datetime import datetime
from .base import STANDARDS_EN, DISCLAIMER_EN  # 需提前定义英文标准/免责声明

def build_html_en(violations, page_name, page_url, stats, path):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Accessibility Test Report</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Arial, sans-serif;background:#f7f8fa;padding:30px 10px}}
.container{{max-width:1000px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}}
.header{{background:#2c3e50;color:#fff;padding:30px 20px;text-align:center}}
.info{{padding:20px;background:#f8f9fa}}
.section{{padding:20px;border-bottom:1px solid #eee}}
h2{{font-size:18px;color:#2c3e50;margin-bottom:15px}}
.stats{{display:flex;gap:12px;flex-wrap:wrap}}
.stat{{flex:1;min-width:120px;background:#fff;padding:15px;border-radius:8px;border:1px solid #eee;text-align:center}}
.val{{font-size:22px;font-weight:bold;margin-top:5px}}
.critical{{color:#dc3545}}.serious{{color:#fd7e14}}.moderate{{color:#ffc107}}.minor{{color:#6c757d}}
.compliance{{text-align:center;padding:20px;font-size:18px;color:#28a745;font-weight:bold}}
.issue{{background:#f9f9f9;padding:18px;border-radius:8px;margin-bottom:12px;border-left:4px solid #ccc}}
.issue.critical{{border-color:#dc3545}}.issue.serious{{border-color:#fd7e14}}
.issue.moderate{{border-color:#ffc107}}.issue.minor{{border-color:#6c757d}}
.disclaimer{{background:#fff8e6;padding:20px;border-radius:8px;margin-top:20px;white-space:pre-line}}
.footer{{text-align:center;padding:20px;color:#999}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>Website Accessibility Compliance Report</h1><p>Commercial Delivery Version</p></div>
<div class="info">
<p>Page: {page_name}</p>
<p>URL: {page_url}</p>
<p>Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
<div class="section"><h2>Test Standards</h2><pre>{STANDARDS_EN}</pre></div>
<div class="section"><h2>Test Statistics</h2>
<div class="stats">
<div class="stat"><div>Total</div><div class="val">{stats['total']}</div></div>
<div class="stat"><div>Critical</div><div class="val critical">{stats['critical']}</div></div>
<div class="stat"><div>Serious</div><div class="val serious">{stats['serious']}</div></div>
<div class="stat"><div>Moderate</div><div class="val moderate">{stats['moderate']}</div></div>
<div class="stat"><div>Minor</div><div class="val minor">{stats['minor']}</div></div>
</div>
<div class="compliance">Compliance Rate: {stats['compliance_rate']}%</div>
</div>
<div class="section"><h2>Issue Details</h2>
'''
    # 缺陷明细
    for idx, v in enumerate(violations, 1):
        html += f'''
<div class="issue {v['impact']}">
<h3>{idx}. {v['id']}【{v['impact'].upper()}】</h3>
<p><strong>Description:</strong> {v['description']}</p>
<p><strong>Recommendation:</strong> {v['help']}</p>
</div>
'''
    # 尾部
    html += f'''
</div>
<div class="disclaimer"><h3>Disclaimer</h3><p>{DISCLAIMER_EN}</p></div>
<div class="footer">Commercial Use Allowed | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
</div>
</body></html>
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)