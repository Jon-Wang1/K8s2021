### 下载镜像并上传 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull kibana:7.14.2
docker tag kibana:7.14.2 harbor.qytanghost.com/efk/kibana:7.14.2
docker push harbor.qytanghost.com/efk/kibana:7.14.2

docker pull kibana:6.8.13
docker tag kibana:6.8.13 harbor.qytanghost.com/efk/kibana:6.8.13
docker push harbor.qytanghost.com/efk/kibana:6.8.13

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

### 查看PVC (任何Master)
[root@master01 ~]# kubectl get pvc -n efk
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
kibana-pvc          Bound    pvc-f9e4287f-dd5d-4ff6-bc50-c8d5d51e9e78   100Gi      RWO            rook-cephfs    34s

### 查看POD (任何一个Master)
[root@master01 ~]# kubectl get pod -l "app=kibana" -n efk -o wide
NAME                      READY   STATUS    RESTARTS   AGE    IP              NODE                    NOMINATED NODE   READINESS GATES
kibana-84ccdb896b-qdsmq   1/1     Running   0          2m3s   172.16.202.29   node02.qytanghost.com   <none>           <none>


----------------------------------注意此处切换设备--------------------------------------

###测试kibana首页 (mgmtwin7)
https://kibana.qytangk8s.com/


###激活Monitoring (mgmtwin7)
Management --- Stack Monitoring --- Or,set up with self monitoring -- Turn on monitoring

激活后可以看到Elasticsearch和Kibana都是Healthy(健康的)