### 准备镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull rabbitmq
docker tag rabbitmq harbor.qytanghost.com/public/rabbitmq
docker push harbor.qytanghost.com/public/rabbitmq

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl create ns devops
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_rabbitmq/dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_rabbitmq/svc.yaml

```

### 查看pod状态 (任何一个Master)
[root@master01 ~]# kubectl get pods -n devops
NAME                        READY   STATUS    RESTARTS   AGE
rabbitmq-7fc568b68d-w7xpb   1/1     Running   0          37s
