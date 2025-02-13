## 批量识别接口

* 接口路径: /v1/asr/recognize
* 请求方法: POST
* 功能: 批量提交多个音频URL进行识别，进行异步识别，识别完成后返回结果
* 请求格式:
    ```json
    [
        {
            "index":1,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        },
        {
            "index":2,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
        }
    ]
    ```
* 返回格式:
    ```json
    {
        "code": 200,
        "msg": "ok",
        "data": [
            {
                "index": 1,
                "tts": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
                "text": "Hello world, 这里是阿里巴巴语音实验室。"
            },
            {
                "index": 2,
                "tts": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                "text": "Hello world, 这里是阿里巴巴语音实验室。"
            }
        ]
    }
    ```

## 流式识别接口

* 接口路径: /v1/asr/recognize_stream
* 请求方法: POST
* 功能: 批量提交音频URL，进行异步识别，通过SSE协议实时返回每个音频的识别结果
* 请求格式:
    ```json
    [
        {
            "index":1,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        },
        {
            "index":2,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
        }
    ]
    ```
* 响应格式: SSE格式，每条数据为：
    ```json
    connect：{"status": "connected"}
    recognition：{"code": 200, "msg": "ok", "data": {"index": 1, "tts": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav", "text": "Hello world, 这里是阿里巴巴语音实验室。"}}
    recognition：{"code": 200, "msg": "ok", "data": {"index": 3, "tts": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav", "text": "Hello world, 这里是阿里巴巴语音实验室。"}}
    complete：{"message": "All audio files processed"}
    ```