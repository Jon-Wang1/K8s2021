FROM harbor.qytanghost.com/public/centos
#定义启动jenkins的用户
USER root

#修改时区为东八区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone

# 安装必要工具
RUN yum install -y nginx && yum install -y net-tools && yum install -y bind-utils && yum install -y lrzsz && yum install -y curl && yum install -y python3 && yum install -y dos2unix

# 安装Python模块
RUN pip3 install -i https://pypi.douban.com/simple/ kubernetes

# 工作目录
WORKDIR /qytang

# 拷贝APP
COPY get_pods.py .
COPY get_pod_logs.py .
COPY watch_pods.py .
COPY get_pod_detail.py .
COPY create_deploy.py .
COPY create_deploy_yaml.py .
COPY delete_deploy.py .
COPY update_deploy.py .
COPY dp.yaml .


# 转码
RUN dos2unix get_pods.py
RUN dos2unix get_pod_logs.py
RUN dos2unix watch_pods.py
RUN dos2unix get_pod_detail.py
RUN dos2unix create_deploy.py .
RUN dos2unix create_deploy_yaml.py .
RUN dos2unix delete_deploy.py .
RUN dos2unix update_deploy.py .
RUN dos2unix dp.yaml .

# 添加执行权限
RUN chmod +x get_pods.py
RUN chmod +x get_pod_logs.py
RUN chmod +x watch_pods.py
RUN chmod +x get_pod_detail.py
RUN chmod +x create_deploy.py .
RUN chmod +x create_deploy_yaml.py .
RUN chmod +x delete_deploy.py .
RUN chmod +x update_deploy.py .

# 启动Nginx
CMD nginx -g 'daemon off;'
