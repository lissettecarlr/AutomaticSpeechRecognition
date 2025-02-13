# kuonasr使用

### 环境

如果想使用kuonasr的所有识别引擎，则直接安装：
```bash
pip install -r kuonasr/requirements.txt
```

如果只想要使用其中的几个，可单独在requirements目录找到对应文件进行安装。
```bash
pip install -r kuonasr/requirements/api_aliyun.txt
```

## 使用

### 阿里云在线Paraformer模型识别

```python
from kuonasr import AliyunParaformerASR
audio_files = [
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
       'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav',
]

api_key = os.getenv('ALIYUN_API_KEY')
asr = AliyunParaformerASR(config={"api-key": api_key})

# 测试流式识别
logger.info("测试流式识别")
for result in asr.recognize_stream(audio_files):
    logger.info(json.dumps(result, indent=2, ensure_ascii=False))

# 测试非流式识别
logger.info("测试非流式识别")
result = asr.recognize(audio_files)
for r in result:
    logger.info(json.dumps(r, indent=2, ensure_ascii=False))


```

