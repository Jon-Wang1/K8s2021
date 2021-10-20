# 参考文档备份
https://opensource.actionsky.com/20200622-prometheus/
https://songjiayang.gitbooks.io/prometheus/content/promql/summary.html
https://yunlzheng.gitbook.io/prometheus-book/parti-prometheus-ji-chu/promql/prometheus-promql-functions
https://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_liunx_65_prometheus_alertmanager_rule.html
https://yunlzheng.gitbook.io/prometheus-book/parti-prometheus-ji-chu/quickstart/prometheus-quick-start/use-node-exporter

# 其他alert
https://github.com/rook/rook/blob/master/cluster/examples/kubernetes/ceph/monitoring/prometheus-ceph-v14-rules.yaml
https://github.com/intuit/foremast/blob/master/deploy/prometheus-operator/prometheus-rules.yaml


### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull prom/prometheus:v2.30.3
docker tag prom/prometheus:v2.30.3 harbor.qytanghost.com/monitoring/prometheus:v2.30.3
docker push harbor.qytanghost.com/monitoring/prometheus:v2.30.3

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
EOF

systemctl restart named

```

----------------------------------注意此处切换设备--------------------------------------

### 产生configmap (任何一个Master)
```shell script
wget http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus.yml
kubectl create configmap prometheus-config --from-file=prometheus.yml -n monitoring
wget http://mgmtcentos.qytanghost.com/prometheus/prometheus/rules.yml
kubectl create configmap prometheus-rules --from-file=rules.yml -n monitoring
kubectl create secret generic ca-cert --from-file=/opt/kubernetes/server/cert/ca.pem -n monitoring
kubectl create secret generic etcd-client-cert --from-file=/opt/kubernetes/server/cert/etcd-client.pem -n monitoring
kubectl create secret generic etcd-client-key --from-file=/opt/kubernetes/server/cert/etcd-client-key.pem -n monitoring

```

###应用资源配置清单创建pvc (任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-pvc.yaml

```

### 查看pvc (任何一个Master)
[root@master01 cert]# kubectl get pvc -n monitoring
NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
prometheus-pvc   Bound    pvc-4e4bc041-30d2-4283-859c-a97451c471d7   100Gi      RWO            rook-cephfs    69s

###应用资源配置清单 (任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-ingress.yaml

```

### 快速更新Prometheus配置 (任何一个Master)
```shell
kubectl delete configmap prometheus-config -n monitoring
rm -f prometheus.yml
wget http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus.yml
kubectl create configmap prometheus-config --from-file=prometheus.yml -n monitoring
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/prometheus/prometheus-dp.yaml

kubectl delete pod $(kubectl get pod -l "app=prometheus" -n monitoring -o jsonpath='{.items[0].metadata.name}') -n monitoring

```
### 重新加载配置  (任何一个Master)
```
curl -X POST http://prometheus.qytangk8s.com/-/reload

```

----------------------------------注意此处切换设备--------------------------------------

### 测试访问prometheus (mgmtwin7)
https://prometheus.qytangk8s.com
