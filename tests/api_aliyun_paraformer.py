"""
测试阿里云paraformer
先设置环境变量ALIYUN_API_KEY:
export ALIYUN_API_KEY=sk-
set ALIYUN_API_KEY=sk-

然后运行:
python tests/api_aliyun_paraformer.py
"""

import sys
import os
import json
import time  # 添加time模块导入

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kuonasr import AliyunParaformerASR
from kuonasr import setup_logger
import logging

# 为api模块创建独立的logger
logger = setup_logger('test', 
    log_file='test_api_aliyun_paraformer.log',
    log_dir=os.path.join(os.path.dirname(__file__), 'logs'),
    level=logging.DEBUG
)


audio_files = [
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav',
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav',
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
]

api_key = os.getenv('ALIYUN_API_KEY')
asr = AliyunParaformerASR(config={"api-key": api_key})

# 测试流式识别
logger.info("测试流式识别")
try:
    start_time = time.time()
    for result in asr.recognize_stream(audio_files):
        logger.info(json.dumps(result, indent=2, ensure_ascii=False))
    logger.info(f"流式识别总耗时: {time.time() - start_time:.2f}秒")
except Exception as e:
    logger.error(e)

logger.info("==============================")

# 测试非流式识别
logger.info("测试非流式识别")
try:
    start_time = time.time()
    result = asr.recognize(audio_files)
    for r in result:
        logger.info(json.dumps(r, indent=2, ensure_ascii=False))
    logger.info(f"非流式识别总耗时: {time.time() - start_time:.2f}秒")
except Exception as e:
    logger.error(e)

