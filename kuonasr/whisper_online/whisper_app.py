# 使用whisper的方式进行语音转文字
# 官方文档：https://platform.openai.com/docs/guides/speech-to-text
# Whisper API仅支持小于25 MB的文件
import langid
from openai import OpenAI
import os

class Whispers():
    def __init__(self,api_key,base_url):
        self.client = OpenAI(api_key=api_key,base_url=base_url)

    def infer(self,audio_path,language="zh"):
        # 查看文件是否大于25M
        if(os.path.getsize(audio_path) > 25*1024*1024):
            raise ValueError("语音文件大于25M，需要分割")
        # from pydub import AudioSegment
        # song = AudioSegment.from_mp3("good_morning.mp3")
        # # PyDub handles time in milliseconds
        # ten_minutes = 10 * 60 * 1000
        # first_10_minutes = song[:ten_minutes]
        # first_10_minutes.export("good_morning_10.mp3", format="mp3")
        else:
            try:
                with open(audio_path, 'rb') as audio_file:
                    #response = openai.Audio.transcribe('whisper-1', audio_file,language="zh")
                    transcript = self.client.audio.transcriptions.create(
                                model="whisper-1", 
                                file=audio_file, 
                                response_format="text",
                                language=language
                    )
            except Exception as e:
                raise ValueError("语音转换失败，错误信息：{}".format(e))
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
    key = ""
    url = ""
    audio_path = "../audio/asr_example.wav"
    service = Whispers(key,url)
    result = service.infer(audio_path) 
    print(result)        