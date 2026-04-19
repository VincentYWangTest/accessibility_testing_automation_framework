import os

def scan_accessibility(page):
    # 从本地文件读取 axe（最稳定，商用标准）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    axe_path = os.path.join(current_dir, "axe.min.js")
    with open(axe_path, "r", encoding="utf-8") as f:
        axe_script = f.read()

    # 注入 axe 到页面
    page.evaluate(f"""() => {{
        {axe_script}
    }}""")

    results = page.evaluate("""() => axe.run({
        runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa', 'wcag21a','wcag21aa','section508','EN-301-549']
        }
    })""")
    # print(results)
    return results

def get_critical_issues(results):
    violations = results.get("violations", [])
    return [v for v in violations if v.get("impact") in ["critical", "serious"]]