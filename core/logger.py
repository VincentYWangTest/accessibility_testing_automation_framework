import logging
import os
from datetime import datetime

def get_logger(name="accessibility"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 关键：避免重复添加 handler（彻底解决占用）
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s")

    # 控制台输出
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 重点：每次运行生成唯一日志文件，永不占用
    os.makedirs("logs", exist_ok=True)
    unique_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/accessibility_{unique_ts}.log"

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger