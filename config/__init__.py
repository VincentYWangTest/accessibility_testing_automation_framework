from config.config_saucedemo import SAUCE_DEMO_CONFIG
from config.config_opensource import OPEN_SOURCE_CONFIG

CONFIG_MAP = {
    "saucedemo": SAUCE_DEMO_CONFIG,
    "opensource": OPEN_SOURCE_CONFIG
}

def get_config(env):
    return CONFIG_MAP.get(env, OPEN_SOURCE_CONFIG)