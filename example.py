from kuonasr import ASR

asr = ASR()
try:
    result = asr.convert("./kuonasr/audio/asr_example.wav")
    print(result)
except Exception as e:
    print(e)
