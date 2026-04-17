from config.config_saucedemo import SAUCE_DEMO_CONFIG
from config.config_baidu import BAIDU_CONFIG

CONFIG_MAP = {
    "saucedemo": SAUCE_DEMO_CONFIG,
    "baidu": BAIDU_CONFIG
}

def get_config(env):
    return CONFIG_MAP.get(env, SAUCE_DEMO_CONFIG)