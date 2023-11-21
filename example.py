from kuonasr import ASR

asr = ASR()
# 循环3次
for i in range(3):
    try:
        result = asr.convert("./kuonasr/audio/test2.wav")
        #print(result)
    except Exception as e:
        print(e)
