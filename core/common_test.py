import allure
from core.axe_engine import scan_accessibility
from core.exporter import export_all, export_dashboard
from core.logger import get_logger
from core.utils import Utils

logger = get_logger()

# 新增：全局统计（用于生成总览报告）
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
    warn_only=False  # 新增：warn only，只报警告，不阻断用例
):
    global global_stats
    global_stats["total_pages"] += 1
    logger.info(f"=== Start accessibility check for: {page_name} ===")

    try:
        # 执行无障碍扫描
        results = scan_accessibility(page)
        all_violations = results.get("violations", [])

        # 1. 过滤忽略规则
        ignored = test_config.get("ignore_rules", [])
        filtered_violations = [v for v in all_violations if v["id"] not in ignored]

        # 2. 过滤缺陷级别
        if only_critical:
            final_violations = [v for v in filtered_violations if v["impact"] == "critical"]
        else:
            final_violations = filtered_violations

        # 3. 统计更新
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

        # 4. 导出所有报告
        export_all(final_violations, page_name, page)
        logger.info(f"Check finished: {page_name} | Issues: {len(final_violations)}")

        # 5. Allure报告展示
        with allure.step(f"Accessibility Check: {page_name}"):
            mode_text = "CRITICAL ONLY" if only_critical else "ALL ISSUES"
            summary = (
                f"Mode: {mode_text}\n"
                f"Total Issues: {len(final_violations)}\n"
                f"Critical: {critical_cnt} | Serious: {serious_cnt} | Moderate: {moderate_cnt} | Minor: {minor_cnt}"
            )
            allure.attach(summary, name="Summary", attachment_type=allure.attachment_type.TEXT)

            # 详细缺陷
            detail_text = ""
            for idx, v in enumerate(final_violations, 1):
                detail_text += f"[{idx}] ID: {v['id']}\n"
                detail_text += f"Impact: {v['impact'].upper()}\n"
                detail_text += f"Description: {v['description']}\n"
                detail_text += f"Fix Suggestion: {v['help']}\n\n"
            if detail_text:
                allure.attach(detail_text, name="Issue Details", attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("No accessibility issues found", name="Issue Details", attachment_type=allure.attachment_type.TEXT)

            # 页面截图（无论成败都截图）
            screenshot_path = Utils.take_screenshot(page, page_name, suffix="check")
            allure.attach.file(screenshot_path, name=f"{page_name} Screenshot", attachment_type=allure.attachment_type.PNG)

        # 6. 控制：warn only 不阻断用例
        if final_violations and not warn_only:
            from pytest import fail
            fail(f"{page_name} has {len(final_violations)} accessibility issues", pytrace=False)

    except Exception as e:
        # 全局异常捕获，不崩框架，记录日志+截图
        error_msg = f"Accessibility check failed for {page_name}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        # 异常截图
        screenshot_path = Utils.take_screenshot(page, page_name, suffix="error")
        allure.attach.file(screenshot_path, name=f"{page_name} Error Screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(error_msg, name="Error Details", attachment_type=allure.attachment_type.TEXT)
        if not warn_only:
            from pytest import fail
            fail(error_msg, pytrace=False)

# 新增：生成总览统计大盘
def generate_summary_dashboard():
    export_dashboard(global_stats)
    logger.info("Summary dashboard generated: reports/dashboard.html")