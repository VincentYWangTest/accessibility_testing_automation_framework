def build_csv_en(violations, page_name, page_url, stats, path):
    with open(path, 'w', encoding='utf-8-sig') as f:
        # 统计行表头
        f.write("Test Page,URL,Total Issues,Critical,Serious,Moderate,Minor,Compliance Rate\n")
        f.write(f"{page_name},{page_url},{stats['total']},{stats['critical']},{stats['serious']},{stats['moderate']},{stats['minor']},{stats['compliance_rate']}%\n\n")
        # 缺陷明细表头
        f.write("No.,Issue ID,Severity,Description,Recommendation\n")
        # 缺陷数据
        for i, v in enumerate(violations, 1):
            desc = v["description"].replace(',', ' ').replace('\n', ' ')
            fix  = v["help"].replace(',', ' ').replace('\n', ' ')
            f.write(f"{i},{v['id']},{v['impact']},{desc},{fix}\n")