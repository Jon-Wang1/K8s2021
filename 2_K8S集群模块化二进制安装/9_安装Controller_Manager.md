### 申请并颁发admin证书(dnsca)
```shell
cd /opt/certs/
cat >/opt/certs/admin-csr.json <<EOF
{
    "CN": "admin",
    "hosts": [],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "system:masters",
            "OU": "qytangk8s"
        }
    ]
}
EOF

cfssl gencert -ca=ca.pem \
              -ca-key=ca-key.pem \
              -config=ca-config.json \
              -profile=peer admin-csr.json \
              |cfssl-json -bare admin

```

### host域 zone配置文件(dnsca)
```shell script
cat > /var/named/qytanghost.com.zone <<'EOF'
$ORIGIN qytanghost.com.
$TTL 600    ;   10 minutes
@       IN SOA  dnsca.qytanghost.com. dnsadmin.qytanghost.com. (
                                        2020090901      ; serial
                                        10800           ; refresh (3 hours)
                                        900             ; retry (15 minutes)
                                        604800          ; expire (1 week)
                                        86400           ; minimum (1 day)
                                        )
        NS      dnsca.qytanghost.com.
$TTL 60    ;   1 minute
dnsca                       A   10.1.1.219
master01                    A   10.1.1.101
master02                    A   10.1.1.102
master03                    A   10.1.1.103
node01                      A   10.1.1.201
node02                      A   10.1.1.202
node03                      A   10.1.1.203
harbor                      A   10.1.1.220
nginx01                     A   10.1.1.11
nginx02                     A   10.1.1.12
gitlab                      A   10.1.1.230
kubernetes                  A   10.1.1.10
mgmtwin7                    A   10.1.1.50
mgmtcentos                  A   10.1.1.60
EOF

systemctl restart named
```

----------------------------------注意此处切换设备--------------------------------------

### 下载证书与秘钥 (Master01, Master02, Master03)
```shell script
cd /opt/kubernetes/server/cert

sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/admin-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/admin.pem .

```

### 配置集群参数 (Master01, Master02, Master03)
```shell
ln -s /opt/kubernetes/server/bin/kubectl /usr/bin/kubectl

mkdir -p ~/.kube
cd ~/.kube/

kubectl config set-cluster kubernetes \
  --certificate-authority=/opt/kubernetes/server/cert/ca.pem \
  --embed-certs=true \
  --server=https://kubernetes.qytanghost.com:6443\
  --kubeconfig=kubectl.kubeconfig

```

###设置客户端认证参数 (Master01, Master02, Master03)
```shell
kubectl config set-credentials admin \
  --client-certificate=/opt/kubernetes/server/cert/admin.pem \
  --client-key=/opt/kubernetes/server/cert/admin-key.pem \
  --embed-certs=true \
  --kubeconfig=kubectl.kubeconfig

```
###设置上下文参数 (Master01, Master02, Master03)
```shell
kubectl config set-context kubernetes \
  --cluster=kubernetes \
  --user=admin \
  --kubeconfig=kubectl.kubeconfig

```

###设置默认上下文 (Master01, Master02, Master03)
```shell

kubectl config use-context kubernetes --kubeconfig=kubectl.kubeconfig
cp kubectl.kubeconfig ~/.kube/config
```

### 测试kubectl
[root@master01 .kube]# kubectl get cs
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS      MESSAGE                                                                                       ERROR
scheduler            Unhealthy   Get "http://127.0.0.1:10251/healthz": dial tcp 127.0.0.1:10251: connect: connection refused
controller-manager   Unhealthy   Get "http://127.0.0.1:10252/healthz": dial tcp 127.0.0.1:10252: connect: connection refused
etcd-1               Healthy     {"health":"true"}
etcd-0               Healthy     {"health":"true"}
etcd-2               Healthy     {"health":"true"}


----------------------------------注意此处切换设备--------------------------------------

### 申请并颁发controller-manager证书 (dnsca)
```shell
cd /opt/certs
cat >/opt/certs/controller-manager-csr.json <<EOF
{
    "CN": "system:kube-controller-manager",
    "hosts": [
      "127.0.0.1",
      "10.1.1.101",
      "10.1.1.102",
      "10.1.1.103"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "system:kube-controller-manager",
            "OU": "qytangk8s"
        }
    ]
}
EOF

cfssl gencert -ca=ca.pem \
              -ca-key=ca-key.pem \
              -config=ca-config.json \
              -profile=peer controller-manager-csr.json \
              |cfssl-json -bare controller-manager

```

### 查看controller-manager证书 (dnsca)
[root@dnsca certs]# pwd
/opt/certs

[root@localhost certs]# ll
-rw-r--r-- 1 root root 1021 Oct  8 19:15 controller-manager.csr
-rw-r--r-- 1 root root  300 Oct  8 19:15 controller-manager-csr.json
-rw------- 1 root root 1679 Oct  8 19:15 controller-manager-key.pem
-rw-r--r-- 1 root root 1720 Oct  8 19:15 controller-manager.pem


----------------------------------注意此处切换设备--------------------------------------

### 下载controller-manager的证书与秘钥 (Master01, Master02 and Master03)
```shell script
cd /opt/kubernetes/server/cert

sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/controller-manager-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/controller-manager.pem .

```

### 创建controller-manager的kubeconfig文件 (Master01, Master02 and Master03)
```shell
cd /opt/kubernetes/server/conf/

kubectl config set-cluster kubernetes \
  --certificate-authority=/opt/kubernetes/server/cert/ca.pem \
  --embed-certs=true \
  --server=https://kubernetes.qytanghost.com:6443 \
  --kubeconfig=kube-controller-manager.kubeconfig
  
kubectl config set-credentials system:kube-controller-manager \
  --client-certificate=/opt/kubernetes/server/cert/controller-manager.pem \
  --client-key=/opt/kubernetes/server/cert/controller-manager-key.pem \
  --embed-certs=true \
  --kubeconfig=kube-controller-manager.kubeconfig
  
kubectl config set-context system:kube-controller-manager \
  --cluster=kubernetes \
  --user=system:kube-controller-manager \
  --kubeconfig=kube-controller-manager.kubeconfig
  
kubectl config use-context system:kube-controller-manager --kubeconfig=kube-controller-manager.kubeconfig

```


### 安装controller manager, --service-account-private-key-file 需要是 apiserver --service-account-key-file对应的私钥 (Master01, Master02 and Master03)
```shell script
cat >/opt/kubernetes/server/bin/kube-controller-manager.sh <<'EOF'
#!/bin/sh
./kube-controller-manager \
  --cluster-name=kubernetes \
  --profiling \
  --allocate-node-cidrs=true \
  --cluster-cidr 172.16.0.0/16 \
  --service-cluster-ip-range 192.168.0.0/16 \
  --master https://kubernetes.qytanghost.com:6443 \
  --leader-elect \
  --bind-address=0.0.0.0 \
  --use-service-account-credentials=true \
  --log-dir /data/logs/kubernetes/kube-controller-manager \
  --root-ca-file /opt/kubernetes/server/cert/ca.pem \
  --tls-cert-file=/opt/kubernetes/server/cert/controller-manager.pem \
  --tls-private-key-file=/opt/kubernetes/server/cert/controller-manager-key.pem \
  --authentication-kubeconfig=/opt/kubernetes/server/conf/kube-controller-manager.kubeconfig \
  --authorization-kubeconfig=/opt/kubernetes/server/conf/kube-controller-manager.kubeconfig \
  --kubeconfig=/opt/kubernetes/server/conf/kube-controller-manager.kubeconfig \
  --master https://kubernetes.qytanghost.com:6443 \
  --service-account-private-key-file /opt/kubernetes/server/cert/private.pem \
  --v 2
EOF

```
### kube-controller-manager命令选项
https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/

--root-ca-file：放置到容器 ServiceAccount 中的 CA 证书，用来对 kube-apiserver 的证书进行校验

### 授权可执行权限(Master01, Master02 and Master03)
```shell
chmod +x /opt/kubernetes/server/bin/kube-controller-manager.sh

```

### 创建目录(Master01, Master02 and Master03)
```shell
mkdir -p /data/logs/kubernetes/kube-controller-manager

```

### 创建supervisord的kube-apiserver.ini文件(Master01, Master02 and Master03)
```shell
cat >/etc/supervisord.d/kube-conntroller-manager.ini <<EOF
[program:kube-controller-manager] ; 显示的程序名
command=sh /opt/kubernetes/server/bin/kube-controller-manager.sh
numprocs=1                    ; 启动进程数 (def 1)
directory=/opt/kubernetes/server/bin
autostart=true                ; 是否自启 (default: true)
autorestart=true              ; 是否自动重启 (default: true)
startsecs=30                  ; 服务运行多久判断为成功(def. 1)
startretries=3                ; 启动重试次数 (default 3)
exitcodes=0,2                 ; 退出状态码 (default 0,2)
stopsignal=QUIT               ; 退出信号 (default TERM)
stopwaitsecs=10               ; 退出延迟时间 (default 10)
user=root                     ; 运行用户
redirect_stderr=true          ; 重定向错误输出到标准输出(def false)
stdout_logfile=/data/logs/kubernetes/kube-controller-manager/controller.stdout.log
stdout_logfile_maxbytes=64MB  ; 日志文件大小 (default 50MB)
stdout_logfile_backups=4      ; 日志文件滚动个数 (default 10)
stdout_capture_maxbytes=1MB   ; 设定capture管道的大小(default 0)
;子进程还有子进程,需要添加这个参数,避免产生孤儿进程
killasgroup=true
stopasgroup=true
EOF

```

### 更新配置并查看状态(Master01, Master02 and Master03)
```shell
supervisorctl update
supervisorctl status

```

### 查看状态(Master01, Master02 and Master03)
[root@master01 ~]# supervisorctl status

etcd-server                      RUNNING   pid 1394, uptime 0:01:30
kube-apiserver                   RUNNING   pid 1396, uptime 0:01:30
kube-controller-manager          RUNNING   pid 1766, uptime 0:00:35
```