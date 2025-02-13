FROM python:3.10-slim

WORKDIR /app

ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r api/requirements.txt && \
    pip install --no-cache-dir -r kuonasr/requirements.txt

ENV ALIYUN_API_KEY=""


# 创建日志目录
RUN mkdir -p /app/api/logs && \
    chmod 777 /app/api/logs

EXPOSE 23333

CMD ["python", "api/app/run.py"]