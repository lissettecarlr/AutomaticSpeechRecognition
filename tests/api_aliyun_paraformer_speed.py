"""
完全使用官方示例代码，排除个人开发原因，对识别应用进行速度测试

先设置环境变量ALIYUN_API_KEY:
export ALIYUN_API_KEY=sk-
set ALIYUN_API_KEY=sk-

"""
import sys
import os
import json
import time  
import dashscope
import json
from urllib import request
from http import HTTPStatus

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kuonasr import setup_logger
import logging

dashscope.api_key = os.getenv('ALIYUN_API_KEY')

# 为api模块创建独立的logger
logger = setup_logger('test', 
    log_file='test_api_aliyun_paraformer.log',
    log_dir=os.path.join(os.path.dirname(__file__), 'logs'),
    level=logging.DEBUG
)

start_time = time.time()
task_response = dashscope.audio.asr.Transcription.async_call(
    model='paraformer-v2',
    file_urls=[
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'
    ],
    language_hints=['zh', 'en'])

transcription_response = dashscope.audio.asr.Transcription.wait(
    task=task_response.output.task_id)

end_time = time.time()

logger.info(f"识别耗时: {end_time - start_time:.2f}秒")

# if transcription_response.status_code == HTTPStatus.OK:
#     for transcription in transcription_response.output['results']:
#         url = transcription['transcription_url']
#         result = json.loads(request.urlopen(url).read().decode('utf8'))
#         #print(json.dumps(result, indent=4, ensure_ascii=False))
#     print('transcription done!')
# else:    
#     print('Error: ', transcription_response.output.message)