from main import app
import logging
import os
from uvicorn import Config, Server
import signal
from logging.handlers import RotatingFileHandler

# 修改日志路径的计算方式
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'api.log')
try:
    with open(log_file, 'a') as f:
        pass
except Exception as e:
    raise e



logging_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 30,      # 备份文件
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "kuonasr": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    },
}

def api_run():
    config = Config(
        app=app,
        host="0.0.0.0",
        port=23333,
        log_config=logging_config,
        reload=False,
        workers=1
    )
    server = Server(config=config)
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    server.run()

def handle_shutdown(signum, frame):
    print("Shutdown initiated")

if __name__ == "__main__":
    api_run()

