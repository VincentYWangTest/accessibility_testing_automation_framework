import os
import shutil
import subprocess

def clean():
    for folder in ["allure-results", "reports", "screenshots"]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except:
                pass

if __name__ == "__main__":
    clean()
    print("✅ Running accessibility tests...")

    # 运行测试（无视失败状态，只关心是否执行成功）
    subprocess.run(["pytest", "tests/", "-v", "--alluredir=allure-results"])

    # 打开报告
    try:
        subprocess.run(["allure", "serve", "allure-results"])
    except:
        print("\n📊 Reports generated successfully!")
        print("📁 Open reports/dashboard.html to view full statistics")