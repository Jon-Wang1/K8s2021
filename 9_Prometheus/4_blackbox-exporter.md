### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull prom/blackbox-exporter:v0.19.0
docker tag  prom/blackbox-exporter:v0.19.0 harbor.qytanghost.com/monitoring/blackbox-exporter:v0.19.0
docker push harbor.qytanghost.com/monitoring/blackbox-exporter:v0.19.0

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
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/blackbox-exporter/blackbox-exporter-cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/blackbox-exporter/blackbox-exporter-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/blackbox-exporter/blackbox-exporter-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/blackbox-exporter/blackbox-exporter-ingress.yaml

```

### 查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -l "app=blackbox-exporter" -n monitoring -o wide
NAME                                 READY   STATUS    RESTARTS   AGE   IP              NODE                    NOMINATED NODE   READINESS GATES
blackbox-exporter-7fd7d9997d-plpx6   1/1     Running   0          57s   172.16.201.67   node01.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

### 游览器访问 (mgmtwin7)
https://blackbox.qytangk8s.com/

### 使用blackbox测试百度 (mgmtwin7)
https://blackbox.qytangk8s.com/probe?target=baidu.com&module=http_2xx