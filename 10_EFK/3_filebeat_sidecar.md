### 构建NGINX并且上传镜像 (mgmtcentos)
```shell script
cd /K8S2021/yaml_dockerfile/dockerfile/nginx_log/
docker build -t harbor.qytanghost.com/efk/nginx-log .
docker push harbor.qytanghost.com/efk/nginx-log

```

### 下载并推送镜像
```shell script
docker pull elastic/filebeat:7.14.2
docker tag elastic/filebeat:7.14.2 harbor.qytanghost.com/efk/filebeat:7.14.2
docker push harbor.qytanghost.com/efk/filebeat:7.14.2

docker pull elastic/filebeat:6.8.13
docker tag elastic/filebeat:6.8.13 harbor.qytanghost.com/efk/filebeat:6.8.13
docker push harbor.qytanghost.com/efk/filebeat:6.8.13

```

### 构建filebeat并且上传镜像
```shell script
cd /K8S2021/yaml_dockerfile/dockerfile/filebeat/
docker build -t harbor.qytanghost.com/efk/qyt-filebeat:6.8.13 .
docker push harbor.qytanghost.com/efk/qyt-filebeat:6.8.13
#docker build -t harbor.qytanghost.com/efk/qyt-filebeat:7.14.2 .
#docker push harbor.qytanghost.com/efk/qyt-filebeat:7.14.2

```

### 删除deploy(任何一个Master)
```shell script
kubectl delete deploy nameko-nginx -n devops

```

###应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/filebeat-nginx.yaml

```

### 测试访问网页 （mgmtwin7）
https://nameko-app.qytangk8s.com
https://nameko-app.qytangk8s.com/error