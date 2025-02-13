## kuonasr语音识别器

语音识别器，对接多种语音识别引擎，并提供多种使用方式。

### 支持引擎

* 阿里云Paraformer-v2

#### 使用

* 见`docs`中的文档

#### 开发docker

构建镜像

```bash
docker build -f Dockerfile.dev -t kuonasr-api .
```

运行容器（将本地代码目录挂载到容器中）
```bash
docker run -v $(pwd):/app -p 23333:23333 -e ALIYUN_API_KEY=your_aliyun_api_key kuonasr-api
```

#### 生产docker

构建
```bash
docker build -t kuonasr-api .
```

运行
```bash
docker run -p 23333:23333 -e ALIYUN_API_KEY=your_aliyun_api_key -v $(pwd)/logs:/app/api/logs kuonasr-api
```

### 目录结构

```text
project/
├── kuonasr/                 # 核心ASR包
│   ├── requirements         # kuonasr依赖包
│   ├── kuonasr/             # 实际的包代码
│   │   ├── core/            # ASR基类定义  
│   │   ├── api_aliyun/      # 阿里云实现
│   │   └── utils/           # 工具函数
│
├── api/                    # API服务
│   ├── requirements.txt    # API相关依赖
│   ├── app/
│   │   ├── V1/              # API版本
│   └── tests/               # API测试
│
└── examples/              # 使用示例
```

