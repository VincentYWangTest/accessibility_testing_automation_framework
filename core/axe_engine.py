def scan_accessibility(page):
    page.add_script_tag(
        url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js"
    )

    results = page.evaluate("""() => axe.run({
        runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa', 'section508']
        }
    })""")
    # print(results)
    return results

def get_critical_issues(results):
    violations = results.get("violations", [])
    return [v for v in violations if v.get("impact") in ["critical", "serious"]]