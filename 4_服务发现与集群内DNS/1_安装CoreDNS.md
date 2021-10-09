### 下载并推送镜像到私有仓库 (Harbor)
```shell script
docker pull docker.io/coredns/coredns:1.8.6
docker tag coredns/coredns:1.8.6 harbor.qytanghost.com/public/coredns:v1.8.6
docker push harbor.qytanghost.com/public/coredns:v1.8.6
```

### 应用资源配置清单 (任何一个Master)
```shell script
# 资源配置清单参考
# https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/dns/coredns/coredns.yaml.base

kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/svc.yaml
```

### 查看状态 (任何一个Master)
```shell script
# 查看deployment
[root@master01 ~]# kubectl get deploy -n kube-system -o wide
NAME      READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                                        SELECTOR
coredns   1/1     1            1           47s   coredns      harbor.qytanghost.com/public/coredns:v1.8.6   k8s-app=coredns

# 查看pod
[root@master01 ~]# kubectl get pod -n kube-system -o wide
NAME                     READY   STATUS    RESTARTS   AGE     IP             NODE                    NOMINATED NODE   READINESS GATES
calicoctl                1/1     Running   0          4h49m   10.1.1.201     node01.qytanghost.com   <none>           <none>
coredns-9dbbd976-kxf85   1/1     Running   0          62s     172.16.202.3   node02.qytanghost.com   <none>           <none>

# 查看service
[root@master01 ~]# kubectl get svc -n kube-system -o wide
NAME      TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE   SELECTOR
coredns   ClusterIP   192.168.0.2   <none>        53/UDP,53/TCP,9153/TCP   25m   k8s-app=coredns

# 查看configmap
[root@master01 ~]# kubectl get cm -n kube-system -o wide
NAME                                 DATA   AGE
coredns                              1      26m
extension-apiserver-authentication   6      7h30m
kube-root-ca.crt                     1      7h5m


# 查看configmap详情
[root@master01 ~]# kubectl describe cm coredns -n kube-system
Name:         coredns
Namespace:    kube-system
Labels:       addonmanager.kubernetes.io/mode=EnsureExists
Annotations:  <none>

Data
====
Corefile:
----
.:53 {
    errors
    log
    health
    ready
    kubernetes cluster.local 192.168.0.0/16
    forward . 10.1.1.219
    cache 30
    loop
    reload
    loadbalance
   }

Events:  <none>


# 查看ServiceAccount
[root@master01 ~]# kubectl get sa -n kube-system
NAME                                 SECRETS   AGE
coredns                              1         28m

# 查看ClusterRoles
[root@master01 ~]# kubectl get clusterroles system:coredns
NAME             CREATED AT
system:coredns   2021-10-09T08:05:30Z

# 查看ClusterRolebinding
[root@master01 ~]# kubectl get clusterrolebinding system:coredns
NAME             ROLE                         AGE
system:coredns   ClusterRole/system:coredns   29m

# 查看ClusterRolebinding详情
[root@master01 ~]# kubectl describe clusterrolebinding system:coredns
Name:         system:coredns
Labels:       addonmanager.kubernetes.io/mode=EnsureExists
              kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
Role:
  Kind:  ClusterRole
  Name:  system:coredns
Subjects:
  Kind            Name     Namespace
  ----            ----     ---------
  ServiceAccount  coredns  kube-system

```

### 应用nginx-curl-dp和nginx-curl-ds的service资源配置清单 (任何Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/svc-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/svc-ds.yaml
```

### 查看service (任何Master)
```shell script
[root@master01 ~]# kubectl get svc
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes          ClusterIP   192.168.0.1      <none>        443/TCP    7h34m
qyt-lb-dp-service   ClusterIP   192.168.74.140   <none>        5000/TCP   10s
qyt-lb-ds-service   ClusterIP   192.168.59.17    <none>        5000/TCP   9s

```

### 查看ipvs (任何一个节点)
```shell script
[root@node01 ~]# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
# k8s的service
TCP  192.168.0.1:443 rr
  -> 10.1.1.101:6443              Masq    1      0          0         
  -> 10.1.1.102:6443              Masq    1      0          0         
  -> 10.1.1.103:6443              Masq    1      1          0   
# codedns的service      
TCP  192.168.0.2:53 rr
  -> 172.16.202.3:53              Masq    1      0          0  
# codedns的service      
TCP  192.168.0.2:9153 rr
  -> 172.16.202.3:9153            Masq    1      0          0  
# qyt-lb-ds的service      
TCP  192.168.59.17:5000 rr
  -> 172.16.201.1:5000            Masq    1      0          0
  -> 172.16.202.1:5000            Masq    1      0          0
  -> 172.16.203.2:5000            Masq    1      0          0 
# qyt-lb-dp的service     
TCP  192.168.74.140:5000 rr
  -> 172.16.203.1:5000            Masq    1      0          0
# codedns的service     
UDP  192.168.0.2:53 rr
  -> 172.16.202.3:53              Masq    1      0          0
# calico的服务
TCP  192.168.56.9:5473 rr
  -> 10.1.1.201:5473              Masq    1      0          0
  -> 10.1.1.202:5473              Masq    1      0          0
  -> 10.1.1.203:5473              Masq    1      0          0
```

### 容器内测试CoreDNS解析 (任何一个Master)
```shell script

[root@master01 ~]# kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
qyt-lb-dp-7f677cd4cf-phdj4   1/1     Running   0          3h32m
qyt-lb-ds-9kdfc              1/1     Running   0          3h32m
qyt-lb-ds-n75kn              1/1     Running   0          3h32m
qyt-lb-ds-qdnk6              1/1     Running   0          3h32m

[root@master01 ~]# kubectl exec -it qyt-lb-dp-7f677cd4cf-phdj4 -- /bin/bash

[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# nslookup
> qyt-lb-ds-service
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   qyt-lb-ds-service.default.svc.cluster.local
Address: 192.168.59.17
> qyt-lb-dp-service
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   qyt-lb-dp-service.default.svc.cluster.local
Address: 192.168.74.140

# ping测试
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# ping qyt-lb-ds-service
 
# curl测试
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-qdnk6, My IP is 172.16.203.2
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-n75kn, My IP is 172.16.202.1
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-9kdfc, My IP is 172.16.201.1
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-qdnk6, My IP is 172.16.203.2
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-n75kn, My IP is 172.16.202.1
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-9kdfc, My IP is 172.16.201.1
```