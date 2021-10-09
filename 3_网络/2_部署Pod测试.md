# 自作nginx-curl镜像 (dnsca)
```shell script
cd /data/dockerfile/qyt_lb/

docker build -t harbor.qytang.com/public/qyt_lb .

docker login harbor.qytang.com
admin
Cisc0123

docker push harbor.qytang.com/public/qyt_lb 
```

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://k8s-yaml.qytang.com/qyt-lb/qyt-lb-dp.yaml
kubectl apply -f http://k8s-yaml.qytang.com/qyt-lb/qyt-lb-ds.yaml
```

### 查看状况 (任何一个Master)
```shell script
[root@master03 ~]# kubectl get deploy
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
qyt-lb-dp   1/1     1            1           6m24s

[root@master03 ~]# kubectl get deploy -o wide
NAME        READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS           IMAGES                            SELECTOR
qyt-lb-dp   1/1     1            1           6m38s   container-1-qyt-lb   harbor.qytang.com/public/qyt_lb   app=qyt-lb-dp-label

[root@master03 ~]# kubectl get daemonset
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
qyt-lb-ds   3         3         3       3            3           <none>          6m54s

[root@master03 ~]# kubectl get daemonset -o wide
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE    CONTAINERS           IMAGES                            SELECTOR
qyt-lb-ds   3         3         3       3            3           <none>          7m5s   container-1-qyt-lb   harbor.qytang.com/public/qyt_lb   app=qyt-lb-ds-label

[root@master03 ~]# kubectl get replicaset
NAME                   DESIRED   CURRENT   READY   AGE
qyt-lb-dp-7bd5c8fd74   1         1         1       7m22s

[root@master03 ~]# kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
qyt-lb-dp-7bd5c8fd74-xlvt6   1/1     Running   0          7m32s
qyt-lb-ds-jxkm8              1/1     Running   0          7m31s
qyt-lb-ds-kghhs              1/1     Running   0          7m31s
qyt-lb-ds-pds22              1/1     Running   0          7m31s

[root@master03 ~]# kubectl get pod -o wide
NAME                         READY   STATUS    RESTARTS   AGE     IP             NODE              NOMINATED NODE   READINESS GATES
qyt-lb-dp-7bd5c8fd74-xlvt6   1/1     Running   0          7m42s   172.16.203.4   node03.host.com   <none>           <none>
qyt-lb-ds-jxkm8              1/1     Running   0          7m41s   172.16.202.2   node02.host.com   <none>           <none>
qyt-lb-ds-kghhs              1/1     Running   0          7m41s   172.16.201.3   node01.host.com   <none>           <none>
qyt-lb-ds-pds22              1/1     Running   0          7m41s   172.16.203.5   node03.host.com   <none>           <none>
```