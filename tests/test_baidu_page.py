import allure
import pytest
from core.common_test import run_accessibility_check

@allure.epic("Accessibility Testing")
@allure.feature("Baidu Homepage")
@pytest.mark.baidu
class TestBaiduHomepage:
    def test_baidu_homepage_accessibility(self, page, test_config, only_critical, warn_only):
        page.goto("https://www.baidu.com")
        run_accessibility_check(page, "Baidu Homepage", test_config, only_critical, warn_only)