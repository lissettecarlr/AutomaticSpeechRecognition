import yaml
with open('./kuonasr/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
from loguru import logger
import time
class ASR:
    def __init__(self) -> None:
        start_time = time.time()
        if config['channel'] == "parafomer":
            from kuonasr.Paraformer import paraformer 
            self.service = paraformer()  
        elif config['channel'] == "whisper_online":
            from kuonasr.whisper_online.whisper_app import Whispers
            key = config['OPENAI']['key']
            base_url = config['OPENAI']['url']
            self.service = Whispers(key,base_url)
        elif config['channel'] == 'funasr':
            from kuonasr.funasr.client import FunASRClient
            self.service = FunASRClient(config['funasr']['url'])
        elif config['channel'] == 'whisper_offline':
            from kuonasr.whisper_offline.faster_whisper_app import Whispers
            model_name = config['whispers']['model_name']
            device = config['whispers']['device']
            self.service = Whispers(model_name,device)

        logger.info("asr init : {} ， 耗时：{}".format(config['channel'],round(time.time()-start_time,2)))
   
    def test(self):
        logger.debug("asr test")
        audio_path = "./kuonasr/audio/asr_example.wav"
        result = self.convert(audio_path) 
        logger.debug("asr test result:{}".format(result))
     

    def convert(self,audio_path):
        if config['channel'] == "parafomer" :
            start_time = time.time()
            try:
                result = self.service.infer(audio_path) 
            except Exception as e:
                raise ValueError("语音转换失败，错误信息：{}".format(e))
            logger.info("asr over. 文件 {} ,转换耗时:{}，结果：{}".format(audio_path,round(time.time()-start_time,2),result))
            return result
        
        elif config['channel'] == 'funasr':
            import asyncio
            start_time = time.time()
            try:
                result = asyncio.run(self.service.filter(audio_path))
            except Exception as e:
                raise ValueError("语音转换失败，错误信息：{}".format(e))
            logger.info("asr over. 文件 {} ,转换耗时:{}，结果：{}".format(audio_path,round(time.time()-start_time,2),result))
            return result
        
        elif config['channel'] == 'whisper_online':
            start_time = time.time()
            try:
                result = self.service.infer(audio_path) 
            except Exception as e:
                raise ValueError("语音转换失败，错误信息：{}".format(e))
            logger.info("asr over. 文件 {} ,转换耗时:{}，结果：{}".format(audio_path,round(time.time()-start_time,2),result))
            return result

        elif config['channel'] == 'whisper_offline':
            start_time = time.time()

            language = config['whispers']['language']
            beam_size = config['whispers']['beam_size']
            min_silence_duration_ms = config['whispers']['min_silence_duration_ms']
            if min_silence_duration_ms == 0:
                is_vad_filter = False
            else:
                is_vad_filter = True

            try:
                result = self.service.infer(audio_path,
                                            language=language,
                                            beam_size=beam_size,
                                            is_vad_filter=is_vad_filter,
                                            min_silence_duration_ms=min_silence_duration_ms) 
            except Exception as e:
                raise ValueError("语音转换失败，错误信息：{}".format(e))
            logger.info("asr over. 文件 {} ,转换耗时:{}，结果：{}".format(audio_path,round(time.time()-start_time,2),result))
            return result

        else:
            raise ValueError("不支持的asr服务,请检查配置文件channel字段")