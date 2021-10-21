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

EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------
### 参考文档
https://www.qikqiak.com/post/traefik-2.1-101/

### 下载镜像，改标签并推送到私有仓库 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell
docker pull traefik:2.3
docker tag traefik:2.3 harbor.qytanghost.com/public/traefik:v2.3
docker push harbor.qytanghost.com/public/traefik:v2.3

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单(任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/crd.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/ds.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/dashboard.yaml

```

### 查看traefix的pod(任何一个Master)
[root@master01 ~]# kubectl get pod -n kube-system
NAME                     READY   STATUS    RESTARTS   AGE
calicoctl                1/1     Running   0          76m
coredns-9dbbd976-f6kxp   1/1     Running   0          27m
traefik-6m4zm            1/1     Running   0          4m11s
traefik-c8jws            1/1     Running   0          40s
traefik-dl5jt            1/1     Running   0          4m11s

----------------------------------注意此处切换设备--------------------------------------

### 测试访问traefix管理页面（mgmtwin7)
https://traefik.qytangk8s.com/

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单(任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/ingress-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/ingress-ds.yaml

```

### 测试访问qyt-lb-dp的页面（mgmtwin7)
https://qyt-lb-dp.qytangk8s.com/

### 测试访问qyt-lb-ds的页面（尝试多次访问，测试负载均衡效果）（mgmtwin7)
https://qyt-lb-ds.qytangk8s.com/