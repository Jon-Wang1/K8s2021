### 下载镜像并上传 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull kibana:7.14.2
docker tag kibana:7.14.2 harbor.qytanghost.com/efk/kibana:7.14.2
docker push harbor.qytanghost.com/efk/kibana:7.14.2

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
kibana                       A   10.1.1.10
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/kibana-pvc.yaml

kubectl apply -f http://mgmtcentos.qytanghost.com/efk/kibana-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/kibana-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/efk/kibana-ingress.yaml

```

----------------------------------注意此处切换设备--------------------------------------

###测试kibana首页 (mgmtwin7)
https://kibana.qytangk8s.com/


###激活Monitoring (mgmtwin7)
Management --- Stack Monitoring --- Or,set up with self monitoring -- Turn on monitoring

激活后可以看到Elasticsearch和Kibana都是Healthy(健康的)