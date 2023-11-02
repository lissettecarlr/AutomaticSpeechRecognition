## kunasr
该仓库用于语音识别，目前有三种实现方式，分别是paraformer、whisper_online、funasr。主要用于服务[kuon](https://github.com/lissettecarlr/kuon)仓库。

## 依赖

可以直接`pip install -r requirements.txt`安装所有环境，也可以根据选择方式安装

### paraformer

* onnxruntime-gpu 或者 onnxruntime
* numpy
* librosa 用于音频分析和处理
* pyyaml
* typeguard==2.13.3
* scipy

### whisper_online

* openai
* langid

### funasr_client

* websockets

## 配置
```bash
cp config.yaml.example config.yaml
```
* channel 从paraformer、whisper_online、funasr中选择一种
* 如果选择whisper_online，则需要配置openai的key
* 如果选择funasr，则需要配置funasr的服务端地址

## 使用

*如果使用funasr，则需要部署服务端*

```python
from kuonasr import ASR
test = ASR()
test.test()
```

```python
from kuonasr import ASR
asr = ASR()
try:
    result = asr.convert("./kuonasr/audio/asr_example.wav")
    print(result)
except Exception as e:
    print(e)
```


## 关于转换方式

### paraformer

源码来自rapid的[RapidASR仓库](https://github.com/RapidAI/RapidASR/blob/main/README.md)

[模型百度云](https://pan.baidu.com/s/1sY6ENdKcxM-X7bqK07RThg?pwd=kuon)，在paraformer文件夹下的名为asr_paraformerv2的文件，将其放置到kuonasr/paraformer/models文件中。或者去原项目下载。

### whisper_online

openai的whisper在线语音识别，请求方式来自[这里](https://platform.openai.com/docs/api-reference/audio)

### funasr

[github仓库](https://github.com/alibaba-damo-academy/FunASR)，需要先部署服务端，这里代码只是客户端进行接口的调用。部署方式可以看官方仓库，也可以参考[笔迹](https://blog.kala.love/posts/cbe699d7/)


## 报错：

### 1
```bash
ValueError: An error occurred: unknown format: 3
```
输入音频的格式不支持，可以使用sox进行转换，例如
```bash
sox test.wav -b 16 -e signed-integer test2.wav
```
* [sox的github](https://github.com/chirlu/sox)
