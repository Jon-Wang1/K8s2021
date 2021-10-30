### 修改 ceph operator.yaml (Pycharm修改) (已经修改过了!无需操作)
```shell script
- name: ROOK_HOSTPATH_REQUIRES_PRIVILEGED
          value: "true"
```

### 重新应用ceph的资源配置清单 (任何一个Master)  (已经部署过了!无需操作)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/rook/operator.yaml

```

----------------------------------注意此处切换设备--------------------------------------

### 创建镜像仓库efk(公有) (mgmtwin7)

----------------------------------注意此处切换设备--------------------------------------

### 下载镜像并上传 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull elasticsearch:7.14.2
docker tag elasticsearch:7.14.2 harbor.qytanghost.com/efk/elasticsearch:7.14.2
docker push harbor.qytanghost.com/efk/elasticsearch:7.14.2

docker pull elasticsearch:6.8.13
docker tag elasticsearch:6.8.13 harbor.qytanghost.com/efk/elasticsearch:6.8.13
docker push harbor.qytanghost.com/efk/elasticsearch:6.8.13

```

----------------------------------注意此处切换设备--------------------------------------

### 创建命名空间efk(任何一个Master)
```shell script
kubectl create ns efk

```

----------------------------------注意此处切换设备--------------------------------------

### 配置DNS (DNSCA)
```shell script
cat > /var/named/qytangk8s.com.zone <<'EOF'
$ORIGIN qytangk8s.com.
$TTL 600    ;   10 minutes
@       IN SOA  dnsca.qytangk8s.com. dnsadmin.qytangk8s.com. (
                                        2020090901      ; serial
                                        10800           ; refresh (3 hours)
                                        900             ; retry (15 minutes)
                                        604800          ; expire (1 week)
                                        86400           ; minimum (1 day)
                                        )
        NS      dnsca.qytangk8s.com.
$TTL 60    ;   1 minute
dnsca                        A   10.1.1.219
traefik                      A   10.1.1.10
qyt-lb-ds                    A   10.1.1.10
qyt-lb-dp                    A   10.1.1.10
k8sdashboard                 A   10.1.1.10
metricsserver                A   10.1.1.10
nginx-configmap              A   10.1.1.10
ceph-mgr-dashboard           A   10.1.1.10
nginx-nfspvc                 A   10.1.1.10
nameko-app                   A   10.1.1.10
blackbox                     A   10.1.1.10
prometheus                   A   10.1.1.10
alertmanager                 A   10.1.1.10
grafana                      A   10.1.1.10
elasticsearch                A   10.1.1.10
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/elasticsearch-pvc.yaml

kubectl apply -f http://mgmtcentos.qytanghost.com/efk/elasticsearch-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/elasticsearch-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/elasticsearch-ingress.yaml

```

### 查看PVC （任何一个Master）
[root@master02 ~]# kubectl get pvc -n efk
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
elasticsearch-pvc   Bound    pvc-1a7f978b-cd77-4070-a3b7-d5f6ad79bde6   100Gi      RWO            rook-cephfs    27s

### 查看容器(任何一个Master)
[root@master02 ~]# kubectl get pod -l "app=elasticsearch" -n efk -o wide
NAME                             READY   STATUS    RESTARTS   AGE    IP              NODE                    NOMINATED NODE   READINESS GATES
elasticsearch-5d96668d69-n4xnp   1/1     Running   0          2m7s   172.16.201.70   node01.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

### 测试打开elasticsearch首页 (mgmtwin7)
https://elasticsearch.qytangk8s.com/
