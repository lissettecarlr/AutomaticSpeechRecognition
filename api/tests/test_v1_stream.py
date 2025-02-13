import json
import logging
import requests

logging.basicConfig(level=logging.INFO)

def test_aliyun_paraformer_stream():
    # 测试数据
    audio_items = [
        {
            "index":1,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
        },
        {
            "index":2,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
        },
        {
            "index":3,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
        },
        {
            "index":4,
            "tts":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
        }
    ]

    # 发送流式请求
    response = requests.post(
        "http://localhost:23333/v1/asr/recognize_stream",
        json=audio_items,
        headers={'Accept': 'text/event-stream'},
        stream=True
    )
    
    assert response.status_code == 200

    # 读取SSE流
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line.replace('data: ', ''))
                logging.info(f"收到事件: {json.dumps(data, ensure_ascii=False)}")
                
                # 如果是识别结果，验证数据结构
                if 'data' in data and isinstance(data['data'], dict):
                    result = data['data']
                    assert 'index' in result
                    assert 'text' in result
                    assert 'tts' in result

if __name__ == "__main__":
    test_aliyun_paraformer_stream()
