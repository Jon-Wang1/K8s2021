### 创建私有仓库monitoring(公开)(Harbor)

----------------------------------注意此处切换设备--------------------------------------

### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull k8s.gcr.io/kube-state-metrics/kube-state-metrics:v2.2.1
docker tag k8s.gcr.io/kube-state-metrics/kube-state-metrics:v2.2.1 harbor.qytanghost.com/monitoring/kube-state-metrics:v2.2.1
docker push harbor.qytanghost.com/monitoring/kube-state-metrics:v2.2.1

```

----------------------------------注意此处切换设备--------------------------------------

### 创建ns(任何一个Master)
```shell script
kubectl create ns monitoring

```

### 应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/kube-state-metrics/kube-state-metrics-cluster-role.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/kube-state-metrics/kube-state-metrics-service-account.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/kube-state-metrics/kube-state-metrics-cluster-role-binding.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/kube-state-metrics/kube-state-metrics-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/kube-state-metrics/kube-state-metrics-service.yaml

```

### 查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -n monitoring
NAME                                 READY   STATUS    RESTARTS   AGE
kube-state-metrics-598c57868-qbp87   1/1     Running   0          19s

[root@master01 ~]# kubectl get pod -n monitoring -o wide
NAME                                 READY   STATUS    RESTARTS   AGE   IP               NODE                    NOMINATED NODE   READINESS GATES
kube-state-metrics-598c57868-qbp87   1/1     Running   0          31s   172.16.201.144   node01.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

### 测试(任何一个计算节点)
[root@node01 ~]# curl 172.16.201.144:8080/healthz
OK

[root@node01 ~]# curl 172.16.201.144:8080/metrics

---忽略大量输出---

