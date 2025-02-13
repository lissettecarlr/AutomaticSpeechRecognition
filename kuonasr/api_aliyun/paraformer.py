"""
阿里云语音识别
paraformer-v2 模型
https://bailian.console.aliyun.com/#/model-market/detail/paraformer-v2
https://help.aliyun.com/zh/isi/developer-reference/api-details

使用示例:

audio_files = [
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
]
api_key = os.getenv('ALIYUN_API_KEY')
asr = AliyunParaformerASR(config={"api-key": api_key})
# 流式识别
for result in asr.recognize_stream(audio_files):
    logger.info(json.dumps(result, indent=2, ensure_ascii=False))
# 非流式识别
result = asr.recognize(audio_files)

"""

from ..core.base import ASRBase
from ..utils.logger import add_file_handler

import json
from urllib import request
import dashscope
import time
import logging

# 异步
import asyncio
from typing import List
import threading

VALID_MODELS = ['paraformer-v2', 'paraformer-8k-v2', 'paraformer-v1', 'paraformer-8k-v1','paraformer-mtl-v1']

class AliyunParaformerASR(ASRBase):
    """
    Paraformer识别类
    config:
        api-key: 阿里云api key
        max_audio_list_length: 音频列表最大长度/个，默认100
        max_audio_size_gb:     音频文件最大大小/G，默认2
        recognition_timeout:   识别超时时间/秒，默认600
    """
    def __init__(self, config: dict):
        super().__init__()
        self.model_name = "paraformer-v2"
        self.version = "1.0.0"

        self.config = config
        if 'api-key' not in config or config['api-key'] == '':
            raise ValueError("api-key is required")
        
        dashscope.api_key = config['api-key']
        self.max_audio_list_length = config.get('max_audio_list_length', 100)
        self.max_audio_size_gb = config.get('max_audio_size_gb', 2)
        self.recognition_timeout = config.get('recognition_timeout', 600)

        self.logger = logging.getLogger('kuonasr')
        add_file_handler(self.logger, 'paraformer.log')

        self.logger.info("Kuonasr Paraformer ASR initialized")

    def _parse_transcription(self, transcription_response:str):
        """
        解析阿里云返回的识别报告,根据情况提取出其中需要的字段,原始报告格式:
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
            "properties": {
            "audio_format": "pcm_s16le",
            "channels": [
                0
            ],
            "original_sampling_rate": 16000,
            "original_duration_in_milliseconds": 4726
        },
        "transcripts": [
            {
                "channel_id": 0,
                "content_duration_in_milliseconds": 4570,
                "text": "Hello world, 这里是阿里巴巴语音实验室。",
                "sentences": [
                    {
                        "begin_time": 140,
                        "end_time": 4710,
                        "text": "Hello world, 这里是阿里巴巴语音实验室。",
                        "words": [
                            {
                                "begin_time": 140,
                                "end_time": 597,
                                "text": "Hello ",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 597,
                                "end_time": 1054,
                                "text": "world",
                                "punctuation": ", "
                            },
                            {
                                "begin_time": 1054,
                                "end_time": 1663,
                                "text": "这里",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 1663,
                                "end_time": 2272,
                                "text": "是阿",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 2272,
                                "end_time": 2881,
                                "text": "里巴",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 2881,
                                "end_time": 3490,
                                "text": "巴语",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 3490,
                                "end_time": 4099,
                                "text": "音实",
                                "punctuation": ""
                            },
                            {
                                "begin_time": 4099,
                                "end_time": 4710,
                                "text": "验室",
                                "punctuation": "。"
                            }
                            ]
                        }
                    ]
                }
            ]
        }
        输入:json字符串
        输出:
        {
            "file_url": xxx,
            "transcripts": []
        }
        """
        try:
            transcription_response = json.loads(transcription_response)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON provided for transcription_response")

        # 只保留file_url和transcripts参数
        parse_transcription = {
            "file_url": transcription_response['file_url'],
            "transcripts": transcription_response['transcripts']
        }
        return parse_transcription

    def _check_audio_list(self, audio_list):
        """
        检查音频列表是否符合要求
        1. 去重
        2. 判断音频url是否有效
        3. 判断音频格式
        4. 判断音频大小
        """
        if not isinstance(audio_list, list):
            raise ValueError("audio_list must be a list")
        if len(audio_list) > self.max_audio_list_length:
            raise ValueError("audio_list length must be less than " + str(self.max_audio_list_length))

        audio_list_filter = list(set(audio_list))
        if len(audio_list_filter) != len(set(audio_list_filter)):
            self.logger.warning("audio_list contains duplicate audio: %s", audio_list)
        for audio in audio_list_filter:
            try:
                if not request.urlopen(audio).getcode() == 200:
                    raise ValueError("audio url is invalid ", audio)
            except Exception as e:
                raise ValueError("audio url is invalid ", audio)
            supported_formats = [
                '.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac', 
                '.amr', '.flv', '.mp4', '.mkv', '.mov', '.mpeg', 
                '.webm', '.wma', '.wmv'
            ]
            if not any(audio.endswith(ext) for ext in supported_formats):
                raise ValueError("Audio format must be one of the following: " + ", ".join(supported_formats))

            response = request.urlopen(audio)
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > self.max_audio_size_gb * 1024 * 1024 * 1024:
                raise ValueError("audio size must be less than " + str(self.max_audio_size_gb) + "G")
        return audio_list_filter
   
    def recognize(self, audio_list, language_hints=['zh', 'en']):
        """
        语音识别
        输入:
            audio_list: 音频列表
            language_hints: 语言提示列表,默认['zh', 'en']
        输出:[
            {
                "status": "SUCCEEDED", 
                "result": {
                    "file_url": xxx,
                    "transcripts": []
                }
            }
        ]
        """
        self.logger.info("Kuonasr Paraformer ASR recognize")
        self.logger.info("Kuonasr Paraformer ASR audio_list: %s", audio_list)
        try:
            audio_list = self._check_audio_list(audio_list)
        except Exception as e:
            self.logger.error("Kuonasr Paraformer ASR audio_list check failed: %s", e)
            raise ValueError(f"Audio list check failed: {e}")
       
        try:
            task_response = dashscope.audio.asr.Transcription.async_call(
                model='paraformer-v2',
                file_urls=audio_list,
                language_hints=language_hints
            )  
        except Exception as e:
            self.logger.error("Kuonasr Paraformer ASR task_response failed: %s", e)
            raise ValueError(f"Task response failed: {e}")
        
        transcription_response = dashscope.audio.asr.Transcription.wait(
            task=task_response.output.task_id)
        if transcription_response.output.task_status == 'FAILED':
            raise ValueError("Task failed")
        asr_result = []
        for result in transcription_response.output.results:
            if result['subtask_status'] == 'SUCCEEDED':
                transcription_text =  request.urlopen(result['transcription_url']).read().decode('utf8')
                parse_transcription = self._parse_transcription(transcription_text)
                asr_result.append({'status': 'SUCCEEDED', 'result': parse_transcription})
            else:
                asr_result.append({'status': 'FAILED', 'result': None})
        self.logger.info("Kuonasr Paraformer ASR asr_result: %s", asr_result)
        return asr_result

    def recognize_stream(self, audio_list, language_hints=['zh', 'en']):
        """
        流式识别
        输入:
            audio_list: 音频列表
            language_hints: 语言提示列表,默认['zh', 'en']
        输出:
            {
                "status": "SUCCEEDED",
                "result": {
                    "file_url": xxx,
                    "transcripts": []
                }
            }
        """
        self.logger.info("Kuonasr Paraformer ASR recognize_stream")
        self.logger.info("Kuonasr Paraformer ASR audio_list: %s", audio_list)
        try:
            audio_list = self._check_audio_list(audio_list)
        except Exception as e:
            self.logger.error("Kuonasr Paraformer ASR audio_list check failed: %s", e)
            raise ValueError(f"Audio list check failed: {e}")
        
        task_response = dashscope.audio.asr.Transcription.async_call(
            model='paraformer-v2',
            file_urls=audio_list,
            language_hints=language_hints
        )  
        completed_tasks = set()  
        start_time = time.time()

        while True:
            if time.time() - start_time > self.recognition_timeout:
                raise TimeoutError(f"Recognition timed out after {self.recognition_timeout} seconds")
  
            transcription_response = dashscope.audio.asr.Transcription.fetch(
                task=task_response.output.task_id
            )
            if transcription_response.output.task_status == 'FAILED':
                self.logger.error("Kuonasr Paraformer ASR recognize_stream task failed")
                raise ValueError("Task failed")
            
            # 没有结果的时候就继续等待
            if 'results' not in transcription_response.output:
                time.sleep(0.5)
                continue

            for result in transcription_response.output.results:
                if result['subtask_status'] in ['SUCCEEDED', 'FAILED'] and result['file_url'] not in completed_tasks:
                    completed_tasks.add(result['file_url'])
                    if result['subtask_status'] == 'SUCCEEDED':
                        transcription_url = result['transcription_url']
                        transcription_text = request.urlopen(transcription_url).read().decode('utf8')
                        parse_transcription = self._parse_transcription(transcription_text)
                        self.logger.info("Kuonasr Paraformer ASR recognize_stream parse_transcription: %s", parse_transcription)
                        yield {'status': 'SUCCEEDED', 'result': parse_transcription}
                    else:
                        self.logger.info("Kuonasr Paraformer ASR recognize_stream FAILED")
                        yield {'status': 'FAILED', 'result': None}

            # 如果所有任务都完成了，发送退出信号
            if len(completed_tasks) == len(transcription_response.output.results):
                self.logger.info("Kuonasr Paraformer ASR recognize_stream completed")
                return
            time.sleep(0.1)

    async def async_recognize(self, audio_list: List[str], language_hints=['zh', 'en']):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self.recognize,
            audio_list,
            language_hints
        )
    
    async def async_recognize_stream(self, audio_list: List[str], language_hints=['zh', 'en']):
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue()
        def run_recognize_stream():
            try:
                for result in self.recognize_stream(audio_list, language_hints):
                    # 将结果放入异步队列中
                    asyncio.run_coroutine_threadsafe(queue.put(result), loop)
            except Exception as e:
                # 如果发生异常，将异常对象放入队列
                asyncio.run_coroutine_threadsafe(queue.put(e), loop)
            finally:
                # 表示生成器结束，放入一个特殊的结束信号
                asyncio.run_coroutine_threadsafe(queue.put(None), loop)

        # 在单独的线程中运行同步的 recognize_stream
        threading.Thread(target=run_recognize_stream, daemon=True).start()

        while True:
            item = await queue.get()
            if item is None:
                # 生成器已经结束
                break
            elif isinstance(item, Exception):
                # 发生异常，抛出以供处理
                raise item
            else:
                yield item