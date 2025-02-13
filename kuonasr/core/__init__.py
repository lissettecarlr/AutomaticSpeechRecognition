
# 从当前包中导入 base.py 中的 ASRBase 类
from .base import ASRBase

# 定义 __all__ 列表
__all__ = ['ASRBase']

# # 异常类
# class ASRError(Exception):
#     """Base exception for all ASR related errors"""
#     pass

# class ModelNotFoundError(ASRError):
#     """Raised when ASR model is not found"""
#     pass

# # 基础常量
# DEFAULT_SAMPLE_RATE = 16000
# SUPPORTED_FORMATS = ['.wav', '.mp3', '.flac']

# # 工具函数
# def validate_audio(audio_path: str) -> bool:
#     """验证音频文件是否可用"""
#     pass

# __all__ = [
#     "BaseRecognizer",
#     "ASRError",
#     "ModelNotFoundError",
#     "DEFAULT_SAMPLE_RATE",
#     "SUPPORTED_FORMATS",
#     "validate_audio"
# ]