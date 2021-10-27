### 下载并推送镜像到私有仓库 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull docker.io/coredns/coredns:1.8.6
docker tag coredns/coredns:1.8.6 harbor.qytanghost.com/public/coredns:v1.8.6
docker push harbor.qytanghost.com/public/coredns:v1.8.6

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)

### 资源配置清单参考
### https://raw.githubusercontent.com/kubernetes/kubernetes/master/cluster/addons/dns/coredns/coredns.yaml.base
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/coredns/svc.yaml

```

### 查看dp.yaml中使用sa(coredns)的部分
---忽略其他---
spec:
  replicas: 1
  selector:
    matchLabels:
      k8s-app: coredns
  template:
    metadata:
      labels:
        k8s-app: coredns
    spec:
      priorityClassName: system-cluster-critical
      serviceAccountName: coredns # 这个位置
      containers:
      - name: coredns
        image: harbor.qytanghost.com/public/coredns:v1.8.6
---忽略其他---

## 查看状态 (任何一个Master)
### 查看deployment(任何Master)
[root@master01 ~]# kubectl get deploy -n kube-system -o wide
NAME      READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                                        SELECTOR
coredns   1/1     1            1           74s   coredns      harbor.qytanghost.com/public/coredns:v1.8.6   k8s-app=coredns

### 查看pod(任何Master)
[root@master01 ~]# kubectl get pod -n kube-system -o wide
NAME                     READY   STATUS    RESTARTS   AGE    IP             NODE                    NOMINATED NODE   READINESS GATES
calicoctl                1/1     Running   0          50m    10.1.1.201     node01.qytanghost.com   <none>           <none>
coredns-9dbbd976-f6kxp   1/1     Running   0          118s   172.16.201.2   node01.qytanghost.com   <none>           <none>

### 查看service(任何Master)
[root@master01 ~]# kubectl get svc -n kube-system -o wide
NAME      TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE     SELECTOR
coredns   ClusterIP   192.168.0.2   <none>        53/UDP,53/TCP,9153/TCP   2m52s   k8s-app=coredns

### 查看configmap(任何Master)
[root@master01 ~]# kubectl get cm -n kube-system -o wide
NAME                                 DATA   AGE
coredns                              1      3m11s
extension-apiserver-authentication   6      128m
kube-root-ca.crt                     1      107m


### 查看configmap详情(任何Master)
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

### 查看ServiceAccount(任何Master)
[root@master01 ~]# kubectl get sa -n kube-system
NAME                                 SECRETS   AGE
coredns                              1         28m

### 查看rbac.yaml中创建SA(coredns)的部分
apiVersion: v1
kind: ServiceAccount
metadata:
  name: coredns
  namespace: kube-system
  labels:
      kubernetes.io/cluster-service: "true"
      addonmanager.kubernetes.io/mode: Reconcile

### 查看ClusterRoles(任何Master)
[root@master01 ~]# kubectl get clusterroles system:coredns
NAME             CREATED AT
system:coredns   2021-10-09T08:05:30Z

### 查看rbac.yaml中创建ClusterRole(system:coredns)的部分
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
    addonmanager.kubernetes.io/mode: Reconcile
  name: system:coredns
rules:
- apiGroups:
  - ""
  resources:
  - endpoints
  - services
  - pods
  - namespaces
  verbs:
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
- apiGroups:
  - discovery.k8s.io
  resources:
  - endpointslices
  verbs:
  - list
  - watch

### 查看ClusterRolebinding(任何Master)
[root@master01 ~]# kubectl get clusterrolebinding system:coredns
NAME             ROLE                         AGE
system:coredns   ClusterRole/system:coredns   29m

### 查看ClusterRolebinding详情(任何Master)
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

### 查看rbac.yaml中创建ClusterRoleBinding(system:coredns)的部分
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
    addonmanager.kubernetes.io/mode: EnsureExists
  name: system:coredns
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:coredns
subjects:
- kind: ServiceAccount
  name: coredns
  namespace: kube-system
  
### 应用nginx-curl-dp和nginx-curl-ds的service资源配置清单 (任何Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/svc-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/svc-ds.yaml

```

### 查看service (任何Master)
[root@master01 ~]# kubectl get svc
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes          ClusterIP   192.168.0.1      <none>        443/TCP    7h34m
qyt-lb-dp-service   ClusterIP   192.168.74.140   <none>        5000/TCP   10s
qyt-lb-ds-service   ClusterIP   192.168.59.17    <none>        5000/TCP   9s

----------------------------------注意此处切换设备--------------------------------------

### 查看ipvs (任何一个节点)
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
# calico-node的服务
TCP  192.168.56.9:5473 rr
  -> 10.1.1.201:5473              Masq    1      0          0
  -> 10.1.1.202:5473              Masq    1      0          0
  -> 10.1.1.203:5473              Masq    1      0          0
# calico-kube-controllers
TCP  192.168.10.57:9094 rr
  -> 172.16.202.2:9094            Masq    1      0          0
  
----------------------------------注意此处切换设备--------------------------------------

### 查看service (任何Master)
[root@master01 ~]# kubectl get svc
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes          ClusterIP   192.168.0.1      <none>        443/TCP    136m
qyt-lb-dp-service   ClusterIP   192.168.53.32    <none>        5000/TCP   6m27s
qyt-lb-ds-service   ClusterIP   192.168.197.39   <none>        5000/TCP   6m26s

### 容器内测试CoreDNS解析 (任何一个Master)
[root@master01 ~]# kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
qyt-lb-dp-7f677cd4cf-bq6gg   1/1     Running   0          33m
qyt-lb-ds-rlxq2              1/1     Running   0          33m
qyt-lb-ds-tz9pm              1/1     Running   0          33m
qyt-lb-ds-zmpls              1/1     Running   0          33m

[root@master01 ~]# kubectl exec -it $(kubectl get pod -l "app=qyt-lb-dp-label" -o jsonpath='{.items[0].metadata.name}') -- /bin/bash

[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# nslookup
> qyt-lb-ds-service
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   qyt-lb-ds-service.default.svc.cluster.local
Address: 192.168.197.39 （这是DNS解析的地址）
> qyt-lb-dp-service
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   qyt-lb-dp-service.default.svc.cluster.local
Address: 192.168.53.32 （这是DNS解析的地址）
>


# ping测试 (任何一个Master)
[root@qyt-lb-dp-7f677cd4cf-phdj4 qytang]# ping qyt-lb-ds-service
 PING qyt-lb-ds-service.default.svc.cluster.local (192.168.197.39) 56(84) bytes of data.
64 bytes from qyt-lb-ds-service.default.svc.cluster.local (192.168.197.39): icmp_seq=1 ttl=64 time=0.099 ms
64 bytes from qyt-lb-ds-service.default.svc.cluster.local (192.168.197.39): icmp_seq=2 ttl=64 time=0.129 ms

# curl测试 (任何一个Master)
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-rlxq2, My IP is 172.16.203.2
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-tz9pm, My IP is 172.16.202.1
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-zmpls, My IP is 172.16.201.1
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-rlxq2, My IP is 172.16.203.2
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-tz9pm, My IP is 172.16.202.1
[root@qyt-lb-dp-7f677cd4cf-bq6gg qytang]# curl qyt-lb-ds-service:5000
This is qyt-lb-ds-zmpls, My IP is 172.16.201.1
