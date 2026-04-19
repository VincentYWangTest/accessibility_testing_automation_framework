import allure
from core.axe_engine import scan_accessibility
from core.exporter import export_all, export_dashboard
from core.logger import get_logger
from core.utils import Utils

logger = get_logger()

global_stats = {
    "total_pages": 0,
    "total_issues": 0,
    "critical": 0,
    "serious": 0,
    "moderate": 0,
    "minor": 0,
    "pages": []
}

def run_accessibility_check(
    page, 
    page_name, 
    test_config, 
    only_critical,
    warn_only=False
):
    global global_stats
    global_stats["total_pages"] += 1
    logger.info(f"=== Start accessibility check for: {page_name} ===")

    try:
        results = scan_accessibility(page)
        all_violations = results.get("violations", [])

        # 过滤忽略规则和级别
        ignored = test_config.get("ignore_rules", [])
        filtered_violations = [v for v in all_violations if v["id"] not in ignored]
        final_violations = [v for v in filtered_violations if v["impact"] == "critical"] if only_critical else filtered_violations

        # 统计更新
        critical_cnt = len([v for v in final_violations if v["impact"] == "critical"])
        serious_cnt = len([v for v in final_violations if v["impact"] == "serious"])
        moderate_cnt = len([v for v in final_violations if v["impact"] == "moderate"])
        minor_cnt = len([v for v in final_violations if v["impact"] == "minor"])

        global_stats["total_issues"] += len(final_violations)
        global_stats["critical"] += critical_cnt
        global_stats["serious"] += serious_cnt
        global_stats["moderate"] += moderate_cnt
        global_stats["minor"] += minor_cnt
        global_stats["pages"].append({
            "page_name": page_name,
            "total": len(final_violations),
            "critical": critical_cnt,
            "serious": serious_cnt,
            "moderate": moderate_cnt,
            "minor": minor_cnt
        })

        export_all(final_violations, page_name, page.url)
        logger.info(f"Check finished: {page_name} | Issues: {len(final_violations)}")

        # Allure报告：重点补充CSS Selector
        with allure.step(f"Accessibility Check: {page_name}"):
            mode_text = "CRITICAL ONLY" if only_critical else "ALL ISSUES"
            summary = (
                f"Mode: {mode_text}\n"
                f"Total Issues: {len(final_violations)}\n"
                f"Critical: {critical_cnt} | Serious: {serious_cnt} | Moderate: {moderate_cnt} | Minor: {minor_cnt}"
            )
            allure.attach(summary, name="Summary", attachment_type=allure.attachment_type.TEXT)

            # 详细缺陷：仅保留CSS Selector（满足debug定位）
            detail_text = ""
            for idx, v in enumerate(final_violations, 1):
                detail_text += f"[{idx}] ID: {v['id']}\n"
                detail_text += f"Impact: {v['impact'].upper()}\n"
                detail_text += f"Description: {v['description']}\n"
                detail_text += f"Fix Suggestion: {v['help']}\n"
                
                # 核心：提取axe原生的CSS选择器（debug直接用）
                if "nodes" in v and len(v["nodes"]) > 0:
                    detail_text += "Debug CSS Selectors:\n"
                    for node_idx, node in enumerate(v["nodes"], 1):
                        # axe的target字段是数组，第一个元素就是核心CSS选择器
                        css_selector = node.get("target", ["N/A"])[0] if node.get("target") else "N/A"
                        # 补充失败摘要（辅助定位，比如元素文本）
                        failure_summary = node.get("failureSummary", "N/A")
                        detail_text += f"  [{node_idx}] CSS: {css_selector}\n"
                        detail_text += f"     Failure Info: {failure_summary}\n"
                
                # WCAG level
                wcag_level = []
                for t in v.get('tags', []):
                    if t in ["wcag2a","wcag21a"]: wcag_level.append("A")
                    elif t in ["wcag2aa","wcag21aa"]: wcag_level.append("AA")
                    elif t in ["wcag2aaa","wcag21aaa"]: wcag_level.append("AAA")
                wcag = "/".join(sorted(set(wcag_level))) if wcag_level else "Best Practice"
                detail_text += f"WCAG Level: {wcag}\n"
                
                detail_text += "\n"  # 分隔不同违规项
                
            if detail_text:
                allure.attach(detail_text, name="Issue Details (with CSS)", attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("No accessibility issues found", name="Issue Details", attachment_type=allure.attachment_type.TEXT)

            # 页面截图（配合CSS定位更直观）
            screenshot_path = Utils.take_screenshot(page, page_name, suffix="check")
            allure.attach.file(screenshot_path, name=f"{page_name} Screenshot", attachment_type=allure.attachment_type.PNG)

        if final_violations and not warn_only:
            from pytest import fail
            fail(f"{page_name} has {len(final_violations)} accessibility issues", pytrace=False)

    except Exception as e:
        error_msg = f"Accessibility check failed for {page_name}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        screenshot_path = Utils.take_screenshot(page, page_name, suffix="error")
        allure.attach.file(screenshot_path, name=f"{page_name} Error Screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(error_msg, name="Error Details", attachment_type=allure.attachment_type.TEXT)
        if not warn_only:
            from pytest import fail
            fail(error_msg, pytrace=False)

def generate_summary_dashboard():
    export_dashboard(global_stats)
    logger.info("Summary dashboard generated: reports/dashboard.html")