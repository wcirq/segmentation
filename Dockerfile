# Use the Python3.6 image
# 使用python 3.6作为基础镜像
FROM python:3.6

# Set the working directory to /app
# 设置工作目录，作用是启动容器后直接进入的目录名称
WORKDIR /app

# Copy the current directory contents into the container at /app
# . 表示和Dockerfile同级的目录
# 该句将当前目录下的文件复制到docker镜像的/app目录中
ADD . /app

# 加入pip源
ENV pypi https://pypi.douban.com/simple
#ENV pypi https://pypi.tuna.tsinghua.edu.cn/simple
# Install the dependencies
# 安装相关依赖
RUN pip install --no-cache-dir -r requirements.txt -i ${pypi}
RUN pip install --no-cache-dir uwsgi -i ${pypi}

#EXPOSE 5000

# run the command to start uWSGI
# 容器启动后要执行的命令 -> 启动uWSGI服务器
CMD ["sh", "app.sh"]