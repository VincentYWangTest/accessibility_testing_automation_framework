from datetime import datetime
from .base import STANDARDS_CN, DISCLAIMER_CN

def build_html(violations, page_name, page_url, stats, path):
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>无障碍检测报告</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Microsoft YaHei,sans-serif;background:#f7f8fa;padding:30px 10px}}
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
<div class="header"><h1>网站无障碍合规检测报告</h1><p>商用交付版</p></div>
<div class="info">
<p>页面：{page_name}</p>
<p>URL：{page_url}</p>
<p>时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
<div class="section"><h2>检测标准</h2><pre>{STANDARDS_CN}</pre></div>
<div class="section"><h2>检测统计</h2>
<div class="stats">
<div class="stat"><div>总数</div><div class="val">{stats['total']}</div></div>
<div class="stat"><div>严重</div><div class="val critical">{stats['critical']}</div></div>
<div class="stat"><div>较严重</div><div class="val serious">{stats['serious']}</div></div>
<div class="stat"><div>一般</div><div class="val moderate">{stats['moderate']}</div></div>
<div class="stat"><div>轻微</div><div class="val minor">{stats['minor']}</div></div>
</div>
<div class="compliance">合规率：{stats['compliance_rate']}%</div>
</div>
<div class="section"><h2>缺陷明细</h2>
'''
    for idx, v in enumerate(violations, 1):
        html += f'''
<div class="issue {v['impact']}">
<h3>{idx}. {v['id']}【{v['impact'].upper()}】</h3>
<p><strong>描述：</strong>{v['description']}</p>
<p><strong>建议：</strong>{v['help']}</p>
</div>
'''
    html += f'''
</div>
<div class="disclaimer"><h3>免责声明</h3><p>{DISCLAIMER_CN}</p></div>
<div class="footer">报告可商用 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
</div>
</body></html>
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)