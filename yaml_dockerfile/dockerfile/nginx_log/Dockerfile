FROM harbor.qytanghost.com/public/nginx
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone
RUN rm /var/log/nginx/*