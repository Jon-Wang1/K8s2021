FROM harbor.qytanghost.com/public/centos

USER root

#修改时区为东八区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone

# 安装必要工具
RUN yum install -y nginx && yum install -y net-tools && yum install -y bind-utils && yum install -y lrzsz && yum install -y curl && yum install -y python3 && yum install -y dos2unix

# 安装Python模块
RUN pip3 install -i https://pypi.douban.com/simple/ flask

# 工作目录
WORKDIR /qytang

# 拷贝APP
COPY app.py .

# 转码
RUN dos2unix app.py

# 添加执行权限
RUN chmod +x app.py

ENV startup_delay=10 readiness_time=50 liveliness_time=100

# 启动脚本
CMD ["/qytang/app.py"]