FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r api/requirements.txt && \
    pip install --no-cache-dir -r kuonasr/requirements.txt

# 设置环境变量
ENV ALIYUN_API_KEY=""

EXPOSE 23333

# 启动命令
CMD ["python", "api/app/run.py"]