# API 服务使用

## 1 环境

### 1.1 安装API相关环境
```bash
pip install -r api/requirements.txt
```

### 1.2 安装ASR识别器环境

```bash
pip install -r kuonasr/requirements.txt
```

## 2 配置

通过环境变量的方式配置
```
export ALIYUN_API_KEY="your_api_key"
```

## 3 启动
```bash
python api/app/run.py
```

## 4 接口说明

### V1-AliyunParaformerASR

[接口说明](./V1-AliyunParaformerASR-接口说明.md)

## 5 测试接口

```bash
python tests/test_v1.py
```

流式：
```bash
python tests/test_v1_stream.py
```
