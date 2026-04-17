import pytest
from config import get_config

# 新增：自定义注解 - 只报警告，不阻断用例
def pytest_addoption(parser):
    parser.addoption("--env", default="saucedemo")
    parser.addoption("--only-critical", action="store_true")

# 新增：warn_only 注解
@pytest.fixture(scope="function")
def warn_only(request):
    return request.node.get_closest_marker("warn_only") is not None

# 原有fixture不变
@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def only_critical(request):
    return request.config.getoption("--only-critical")

@pytest.fixture(scope="session")
def test_config(env):
    return get_config(env)

# 新增：跳过无障碍检查注解
def pytest_collection_modifyitems(items):
    for item in items:
        if item.get_closest_marker("skip_accessibility"):
            item.add_marker(pytest.mark.skip(reason="Skip accessibility check"))