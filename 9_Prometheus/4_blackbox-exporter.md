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

###查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -n monitoring
NAME                                 READY   STATUS    RESTARTS   AGE
blackbox-exporter-7fd7d9997d-w54vl   1/1     Running   0          33s
cadvisor-ncvp9                       1/1     Running   0          13m
cadvisor-vzfp4                       1/1     Running   0          13m
cadvisor-zzsfn                       1/1     Running   0          13m
kube-state-metrics-598c57868-qbp87   1/1     Running   0          35m
node-exporter-84ccs                  1/1     Running   0          25m
node-exporter-pgvfq                  1/1     Running   0          25m
node-exporter-ww8pd                  1/1     Running   0          25m

----------------------------------注意此处切换设备--------------------------------------

### 游览器访问 (mgmtwin7)
https://blackbox.qytanghost.com/