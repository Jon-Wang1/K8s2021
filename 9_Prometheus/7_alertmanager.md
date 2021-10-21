### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull prom/alertmanager:v0.23.0
docker tag prom/alertmanager:v0.23.0 harbor.qytanghost.com/monitoring/alertmanager:v0.23.0
docker push harbor.qytanghost.com/monitoring/alertmanager:v0.23.0

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/alertmanager/alertmanager-cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/alertmanager/alertmanager-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/alertmanager/alertmanager-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/alertmanager/alertmanager-ingress.yaml

```

### 查看pod信息
[root@master01 ~]# kubectl get pod -l "app=alertmanager" -n monitoring -o wide
NAME                            READY   STATUS    RESTARTS   AGE   IP              NODE                    NOMINATED NODE   READINESS GATES
alertmanager-695f8cb5f4-j429v   1/1     Running   0          71s   172.16.202.26   node02.qytanghost.com   <none>           <none>

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
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 制造故障 (任何一个Master)
```shell script
kubectl scale deploy nameko-app -n devops --replicas=0

```

### 访问alertmanager的首页，查看告警
https://alertmanager.qytangk8s.com