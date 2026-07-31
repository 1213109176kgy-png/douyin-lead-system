import os
import sys
import traceback
from datetime import datetime
from loguru import logger
from functools import wraps

try:
    from application.config import BaseConfig
except ImportError:
    class BaseConfig:
        ENABLE_LOGGING = True
        LOG_LEVEL = "INFO"
        LOG_TO_FILE = True
        DEBUG = True
        LOG_RETENTION_DAYS = 30
        LOG_FILE_SIZE_LIMIT = 2  # MB

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
if not os.path.exists(LOGS_DIR) and BaseConfig.LOG_TO_FILE and BaseConfig.ENABLE_LOGGING:
    os.makedirs(LOGS_DIR)

today = datetime.now().strftime("%Y-%m-%d")
today_log_dir = os.path.join(LOGS_DIR, today)
if not os.path.exists(today_log_dir) and BaseConfig.LOG_TO_FILE and BaseConfig.ENABLE_LOGGING:
    os.makedirs(today_log_dir)

logger.remove()

log_level = BaseConfig.LOG_LEVEL.upper()
if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    log_level = "INFO"

if BaseConfig.ENABLE_LOGGING:
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>" if BaseConfig.DEBUG else "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=log_level
    )

if BaseConfig.LOG_TO_FILE and BaseConfig.ENABLE_LOGGING:
    file_size_limit = f"{BaseConfig.LOG_FILE_SIZE_LIMIT} MB"
    retention_days = f"{BaseConfig.LOG_RETENTION_DAYS} days"

    logger.add(
        os.path.join(today_log_dir, "{time:YYYY-MM-DD_HH-mm-ss}.log"),
        rotation=file_size_limit,
        compression="zip",
        retention=retention_days,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        encoding="utf-8"
    )


def handle_exception(exc_type, exc_value, exc_traceback):
    """处理未捕获的异常"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    if BaseConfig.ENABLE_LOGGING:
        logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical("未捕获的异常")


if BaseConfig.ENABLE_LOGGING:
    sys.excepthook = handle_exception


def log_exception(func):
    """装饰器：捕获函数异常并记录"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if BaseConfig.ENABLE_LOGGING:
                logger.exception(f"函数 {func.__name__} 执行出错: {str(e)}")
            raise

    return wrapper


def get_logger(name="app"):
    return logger.bind(name=name)
