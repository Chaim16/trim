# 构建后端
FROM python:3.11-slim

# 设置中国时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置工作目录
WORKDIR /app

# 复制后端文件
COPY backend/ ./

# 安装依赖并初始化数据库
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && python init_db.py

# 复制已经构建好的前端文件
COPY frontend/dist ./frontend

# 暴露端口
EXPOSE 8001

# 启动命令
CMD ["python", "main.py"]
