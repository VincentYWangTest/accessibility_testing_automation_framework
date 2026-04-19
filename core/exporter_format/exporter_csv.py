def build_csv(violations, page_name, page_url, stats, path):
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write("检测页面,URL,总缺陷,严重,较严重,一般,轻微,合规率\n")
        f.write(f"{page_name},{page_url},{stats['total']},{stats['critical']},{stats['serious']},{stats['moderate']},{stats['minor']},{stats['compliance_rate']}%\n\n")
        f.write("序号,缺陷ID,等级,WCAG,描述,建议,元素定位(CSS)\n")
        for i, v in enumerate(violations, 1):
            desc = v["description"].replace(',', ' ').replace('\n', ' ')
            fix  = v["help"].replace(',', ' ').replace('\n', ' ')
            
            selectors = []
            for node in v.get('nodes', []):
                selectors.extend(node.get('target', []))
            loc = ' | '.join(list(set(selectors))) if selectors else '无'
            
            # WCAG
            wcag_level = []
            for t in v.get('tags', []):
                if t in ["wcag2a","wcag21a"]: wcag_level.append("A")
                elif t in ["wcag2aa","wcag21aa"]: wcag_level.append("AA")
                elif t in ["wcag2aaa","wcag21aaa"]: wcag_level.append("AAA")
            wcag = "/".join(sorted(set(wcag_level))) if wcag_level else "Best Practice"
            
            f.write(f"{i},{v['id']},{v['impact']},{wcag},{desc},{fix},{loc}\n")