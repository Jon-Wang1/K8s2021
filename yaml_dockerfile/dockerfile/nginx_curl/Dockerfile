FROM harbor.qytanghost.com/public/centos
#定义启动jenkins的用户
USER root

#修改时区为东八区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone

# 安装必要工具
RUN yum install -y nginx && yum install -y net-tools && yum install -y bind-utils && yum install -y lrzsz && yum install -y curl

# 启动Nginx
CMD nginx -g 'daemon off;'
