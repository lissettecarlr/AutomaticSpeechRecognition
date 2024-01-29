# 使用本地推理的faster whisper
import langid
import os

import torch
# pip install faster-whisper
from faster_whisper import WhisperModel

class Whispers():
  
    def __init__(self,model_name="small",device='cuda') -> None:
            '''
            model_name: 模型名称，small,medium,large
            device: cuda 或者 cpu
            '''
            self.model = WhisperModel(model_name,device=device)
            torch.cuda.empty_cache()



    def infer(self,audio_path,audio_binary_io = None,
              language="zh",
              beam_size=5,
              is_vad_filter=True,
              min_silence_duration_ms=1000):
        '''
        audio_path: 语音文件路径
        audio_binary_io: 语音文件的二进制流，如果不为空，则优先使用二进制流
        '''
          
        # 如果没有传入音频的二进制，则认为是本地文件
        if audio_binary_io == None:
            if not os.path.exists(audio_path):
                raise Exception("File not found")
            audio = audio_path

        else:
            audio = audio_binary_io

        segments, info = self.model.transcribe(audio = audio,
                                        beam_size=beam_size,
                                        language=language,
                                        vad_filter=is_vad_filter,
                                        vad_parameters=dict(min_silence_duration_ms=min_silence_duration_ms))
        
        #print("识别语言 '%s' 识别概率 %f" % (info.language, info.language_probability))
        transcript = ""
        for segment in segments:
            #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            transcript += segment.text
            transcript += "\n"
        
        if(self.filter(transcript) ==False):
            raise ValueError("识别结果不符合要求，已经被过滤。{}".format(transcript))
           
        return transcript

    # 过滤 单个字符可能也会返回false
    def filter(self,text):
        lang, prob = langid.classify(text)
        if lang == 'zh' or lang == 'en':
            return True
        else:
            return False 
        
if __name__ == '__main__':
    audio_path = "../audio/asr_example.wav"
    service = Whispers()
    result = service.infer(audio_path) 
    print(result)        