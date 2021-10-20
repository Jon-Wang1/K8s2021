FROM harbor.qytanghost.com/efk/filebeat:7.14.2
USER root
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone
COPY filebeat.yml /usr/share/filebeat/filebeat.yml
RUN rm /usr/share/filebeat/modules.d/nginx.yml.disabled
COPY nginx.yml /usr/share/filebeat/modules.d/nginx.yml