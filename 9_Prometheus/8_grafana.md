### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull grafana/grafana:8.2.1
docker tag grafana/grafana:8.2.1 harbor.qytanghost.com/monitoring/grafana:8.2.1
docker push harbor.qytanghost.com/monitoring/grafana:8.2.1

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/grafana/grafana-pvc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/grafana/grafana-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/grafana/grafana-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/grafana/grafana-ingress.yaml

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
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

###网页登录 (mgmtwin7)
https://grafana.qytangk8s.com
默认用户密码 admin/admin
密码改为: Cisc0123


### configuration --- preferences (mgmtwin7)
1. Org: qytang [Update organization name]
2. TimeZone: local browser time

### 安装插件 (任何一个Master)
[root@master01 ~]# kubectl get pod -n monitoring
NAME                                 READY   STATUS    RESTARTS   AGE
alertmanager-695f8cb5f4-kv8w7        1/1     Running   0          28m
blackbox-exporter-7fd7d9997d-frp7n   1/1     Running   0          7h25m
cadvisor-2jmtp                       1/1     Running   0          8h
cadvisor-9vqvt                       1/1     Running   0          8h
cadvisor-vbnb8                       1/1     Running   0          8h
grafana-655945f7d-hnmjs              1/1     Running   0          8m38s
kube-state-metrics-598c57868-cl5ck   1/1     Running   0          8h
node-exporter-fz826                  1/1     Running   0          8h
node-exporter-qfkmk                  1/1     Running   0          8h
node-exporter-qszz2                  1/1     Running   0          8h
prometheus-5f75b6865c-84wzh          1/1     Running   0          7h

### 进入grafana安装插件 (任何一个Master)
```shell
kubectl exec -it $(kubectl get pod -l "app=grafana" -n monitoring -o jsonpath='{.items[0].metadata.name}') -n monitoring -- /bin/bash

grafana-cli plugins install grafana-clock-panel
grafana-cli plugins install grafana-piechart-panel
grafana-cli plugins install briangann-gauge-panel
grafana-cli plugins install natel-discrete-panel

reboot
```

### 添加数据源 configuration --- Data Source --- Add Data Source
1. 选择prometheus
2. URL : http://prometheus.qytangk8s.com
   
### 添加dashboard


