import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "bangumi_list", log_dir: str = "logs", level: int = logging.INFO) -> logging.Logger:
    """
    配置并返回日志记录器

    :param name: 日志记录器名称
    :param log_dir: 日志目录
    :param level: 日志级别
    :return: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    logger.propagate = False
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    try:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        log_file = log_path / f"{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建文件日志处理器: {e}")
    
    return logger


def get_logger(name: str = "bangumi_list") -> logging.Logger:
    """
    获取已配置的日志记录器

    :param name: 日志记录器名称
    :return: 日志记录器
    """
    return logging.getLogger(name)
