import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(name, log_file=None, log_dir=None, level=logging.INFO):
    """
    设置日志系统
    :param name: 日志器名称
    :param log_file: 日志文件名,如果不指定则使用name.log
    :param log_dir: 日志保存目录,如果不指定则使用默认logs目录
    :param level: 日志级别,默认INFO
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 如果logger已经有handler,就不重复添加了
    if logger.handlers:
        return logger
        
    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件handler
    if log_file:
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(os.path.join(log_dir, log_file), encoding='utf-8')
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def add_file_handler(logger, log_file, log_dir=None, level=logging.INFO):
    """
    给已存在的logger添加新的文件handler
    """
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = logging.FileHandler(os.path.join(log_dir, log_file), encoding='utf-8')
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler) 