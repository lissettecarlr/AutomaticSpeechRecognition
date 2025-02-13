# 版本号
__version__ = "0.1.0"

# 从子模块中导入必要的类或函数
from .core import ASRBase
from .api_aliyun import AliyunParaformerASR
from .utils import setup_logger
import logging

__all__ = ['ASRBase', 'AliyunParaformerASR', 'setup_logger']

logger = setup_logger('kuonasr', log_file='kuonasr.log', log_dir='../logs', level=logging.DEBUG)