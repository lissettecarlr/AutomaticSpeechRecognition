import requests
import json
import time


def test_aliyun_paraformer():
    test_data = [
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
    start_time = time.time()
    response = requests.post("http://localhost:23333/v1/asr/recognize", json=test_data)
    end_time = time.time()
    print(f"请求耗时: {end_time - start_time} 秒")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print("请求失败")
        print(response.text)


if __name__ == "__main__":
    test_aliyun_paraformer()
