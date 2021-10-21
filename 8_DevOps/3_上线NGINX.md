### 准备镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull nginx
docker tag nginx harbor.qytanghost.com/public/nginx
docker push harbor.qytanghost.com/public/nginx

```

----------------------------------注意此处切换设备--------------------------------------

### 确认如下路径有乾颐堂的ico文件 (mgmtcentos)
/K8S2021/nfs-volume/nameko_nginx/static/images/favicon.ico

[root@mgmtcentos ~]# cd /K8S2021/nfs-volume/nameko_nginx/static/images/
[root@mgmtcentos images]# ll
total 4
-rw-r--r-- 1 root root 1150 Oct  9 12:15 favicon.ico

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单, 准备PVC (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/pv_nfs.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/pvc_nfs.yaml

```

### 查看pv和pvc (任何一个Master)
[root@master01 ~]# kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS                        REASON   AGE
nameko-nginx-static-pv                     10Gi       RWX            Retain           Bound    devops/nameko-nginx-static-pvc             nameko-nginx-static-storage-class            14s

[root@master01 ~]# kubectl get pvc -n devops
NAME                      STATUS   VOLUME                   CAPACITY   ACCESS MODES   STORAGECLASS                        AGE
nameko-nginx-static-pvc   Bound    nameko-nginx-static-pv   10Gi       RWX            nameko-nginx-static-storage-class   8h

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_nginx/ingress.yaml

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
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 测试访问 nameko-app.qytangk8s.com (mgmtwin7)
https://nameko-app.qytangk8s.com

### PyCharm修改分支nameko_microservice 的index.html，Push修改到Gitlab测试DevOps Pipeline （mgmt PyCharm）

### 测试访问 nameko-app.qytangk8s.com 查看修改 (mgmtwin7)
https://nameko-app.qytangk8s.com