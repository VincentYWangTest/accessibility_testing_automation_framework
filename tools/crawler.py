from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse
import re
import logging

# 配置日志，方便排查问题
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class UniversalCrawler:
    def __init__(self, start_url, max_depth=3):
        self.start_url = self.normalize_url(start_url)
        parsed = urlparse(self.start_url)
        self.base = f"{parsed.scheme}://{parsed.netloc}"
        self.domain = parsed.netloc

        self.visited = set()
        self.to_visit = [(self.start_url, 0)]
        self.max_depth = max_depth

    def normalize_url(self, url):
        """标准化URL：去除锚点、统一参数顺序、去除空参数"""
        if not url:
            return ""
        # 去除锚点
        url = url.split('#')[0].strip()
        parsed = urlparse(url)
        # 处理参数
        query_params = parse_qs(parsed.query)
        # 过滤空值参数，按key排序
        filtered_params = {k: v for k, v in query_params.items() if v}
        sorted_params = sorted(filtered_params.items())
        new_query = urlencode(sorted_params, doseq=True)
        # 重新拼接URL
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            ''
        ))
        return normalized

    def is_valid_page(self, url):
        if not url:
            return False

        # 只爬同域名
        parsed_url = urlparse(url)
        if parsed_url.netloc != self.domain:
            return False

        # 排除无效协议
        if re.match(r'^(mailto|tel|javascript|sms|ftp|file|about:)', url.lower()):
            return False

        # 排除静态文件
        static_file_pattern = re.compile(
            r'\.(pdf|jpg|jpeg|png|gif|svg|ico|css|js|woff|woff2|ttf|eot|mp4|mp3|zip|rar|7z|exe|doc|docx|xls|xlsx|ppt|pptx)$',
            re.IGNORECASE
        )
        if static_file_pattern.search(parsed_url.path):
            return False

        return True

    def run(self, login_info=None):
        with sync_playwright() as p:
            # 关闭无头模式（方便调试），添加防检测配置
            browser = p.chromium.launch(
                headless=True,  # 先改为False，能看到浏览器操作，调试完再改回True
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ]
            )
            context = browser.new_context(
                viewport={"width": 1600, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                # 绕过自动化检测
                java_script_enabled=True,
                locale="zh-CN"
            )
            # 移除webdriver标识
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            page = context.new_page()

            # ------------------- 登录（优化版） -------------------
            if login_info is not None:
                try:
                    logger.info(f"开始登录：{login_info['login_url']}")
                    page.goto(login_info["login_url"], timeout=30000)
                    # 动态等待用户名输入框出现（替代固定等待）
                    page.wait_for_selector(login_info["username_selector"], state="visible", timeout=10000)
                    # 清空输入框再填写
                    page.fill(login_info["username_selector"], "")
                    page.fill(login_info["username_selector"], login_info["username"])
                    
                    page.wait_for_selector(login_info["password_selector"], state="visible", timeout=10000)
                    page.fill(login_info["password_selector"], "")
                    page.fill(login_info["password_selector"], login_info["password"])
                    
                    # 点击登录按钮并等待页面跳转
                    page.click(login_info["button_selector"])
                    # 等待登录成功（可根据目标网站调整，比如等待某个登录后的元素）
                    page.wait_for_load_state("networkidle", timeout=20000)
                    logger.info("登录成功")
                except Exception as e:
                    logger.error(f"登录失败：{str(e)}")
                    browser.close()
                    return []

            # ------------------- 核心爬取（优化版） -------------------
            while self.to_visit:
                url, depth = self.to_visit.pop(0)
                normalized_url = self.normalize_url(url)

                if normalized_url in self.visited:
                    continue
                if depth > self.max_depth:
                    logger.info(f"超出最大深度 {self.max_depth}，跳过：{url}")
                    continue

                try:
                    logger.info(f"爬取：{url}（深度：{depth}）")
                    # 等待页面加载完成（networkidle更高效）
                    page.goto(url, timeout=30000, wait_until="networkidle")
                    
                    # 标记为已访问（标准化后的URL）
                    self.visited.add(normalized_url)

                    # ------------------- 提取所有链接 -------------------
                    # 用playwright的locator更稳定
                    links = page.locator('a[href]').all()
                    for link in links:
                        try:
                            href = link.get_attribute('href')
                            if not href:
                                continue
                            # 拼接绝对URL
                            clean_url = urljoin(self.base, href)
                            normalized_clean_url = self.normalize_url(clean_url)
                            
                            # 验证URL有效性
                            if self.is_valid_page(normalized_clean_url):
                                # 检查是否已访问/待访问
                                to_visit_urls = [self.normalize_url(x[0]) for x in self.to_visit]
                                if normalized_clean_url not in self.visited and normalized_clean_url not in to_visit_urls:
                                    self.to_visit.append((clean_url, depth + 1))
                                    logger.debug(f"加入待爬取：{clean_url}（深度：{depth+1}）")
                        except Exception as e:
                            logger.warning(f"提取链接失败：{str(e)}")
                            continue

                except Exception as e:
                    logger.error(f"爬取 {url} 失败：{str(e)}")
                    self.visited.add(normalized_url)
                    continue

            browser.close()
            logger.info(f"爬取完成，共抓取 {len(self.visited)} 个页面")
        return sorted(list(self.visited))


if __name__ == "__main__":
    # ===================== 客户信息 ======================
    START_URL  = "https://opensource-demo.orangehrmlive.com"

    login_info = {
        "login_url": "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
        "username": "Admin",
        "password": "admin123",
        "username_selector": "#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > form > div:nth-child(2) > div > div:nth-child(2) > input",    # 你改这里
        "password_selector": "#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > form > div:nth-child(3) > div > div:nth-child(2) > input", # 你改这里
        "button_selector": "#app > div.orangehrm-login-layout > div > div.orangehrm-login-container > div > div.orangehrm-login-slot > div.orangehrm-login-form > form > div.oxd-form-actions.orangehrm-login-action > button"      # 你改这里
    }
    # login_info = None  # 不需要登录时取消注释
    # ====================================================

    # 初始化爬虫（max_depth按需调整）
    crawler = UniversalCrawler(START_URL, max_depth=3)
    urls = crawler.run(login_info=login_info)

    # 保存结果
    with open("urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(urls))

    print(f"\n✅ 完成！共抓取 {len(urls)} 个页面")

    
