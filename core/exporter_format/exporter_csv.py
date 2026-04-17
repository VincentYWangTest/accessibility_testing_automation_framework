def build_csv(violations, page_name, page_url, stats, path):
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write("检测页面,URL,总缺陷,严重,较严重,一般,轻微,合规率\n")
        f.write(f"{page_name},{page_url},{stats['total']},{stats['critical']},{stats['serious']},{stats['moderate']},{stats['minor']},{stats['compliance_rate']}%\n\n")
        f.write("序号,缺陷ID,等级,描述,建议\n")
        for i, v in enumerate(violations, 1):
            desc = v["description"].replace(',', ' ').replace('\n', ' ')
            fix  = v["help"].replace(',', ' ').replace('\n', ' ')
            f.write(f"{i},{v['id']},{v['impact']},{desc},{fix}\n")