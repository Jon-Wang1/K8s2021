# 二进制安装apiserver (Master01, Master02 and Master03)

### 查看版本
https://github.com/kubernetes/kubernetes/tags

https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md

### 下载二进制文件, 解压缩, 创建目录, 做软链接(Master01, Master02 and Master03)
```shell script
wget https://dl.k8s.io/v1.20.11/kubernetes-server-linux-amd64.tar.gz

tar xf kubernetes-server-linux-amd64.tar.gz -C /opt

cd /opt
mv /opt/kubernetes/ /opt/kubernetes-v1.20.11-linux-amd64
ln -s /opt/kubernetes-v1.20.11-linux-amd64/ /opt/kubernetes
mkdir /opt/kubernetes/server/cert
mkdir /opt/kubernetes/server/conf

```

### 查看目录(Master01, Master02 and Master03)
[root@master02 opt]# pwd
/opt

[root@localhost opt]# ll | grep kubernetes
lrwxrwxrwx  1 root root   24 Oct  8 16:37 kubernetes -> /opt/kubernetes-1.20.11/
drwxrwxr-x 20 root root 4096 Oct  8 16:38 kubernetes-1.20.11

----------------------------------注意此处切换设备--------------------------------------

### 申请并颁发etcd client证书 (dnsca)
```shell script
cd /opt/certs/
cat >/opt/certs/etcd-client-csr.json <<EOF
{
    "CN": "etcd-client",
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
            "O": "qytang",
            "OU": "qytangk8s"
        }
    ]
}
EOF

cd /opt/certs/
cfssl gencert -ca=ca.pem \
              -ca-key=ca-key.pem \
              -config=ca-config.json \
              -profile=client etcd-client-csr.json \
              |cfssl-json -bare etcd-client

cat >/opt/certs/apiserver-kubelet-client-csr.json <<EOF
{
    "CN": "apiserver-kubelet-client",
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
              -profile=client apiserver-kubelet-client-csr.json \
              |cfssl-json -bare apiserver-kubelet-client

```

### 查看etcd client证书
[root@localhost certs]# ll
-rw-r--r-- 1 root root 1009 Oct  9 08:33 etcd-client.csr
-rw-r--r-- 1 root root  293 Oct  9 08:33 etcd-client-csr.json
-rw------- 1 root root 1675 Oct  9 08:33 etcd-client-key.pem
-rw-r--r-- 1 root root 1708 Oct  9 08:33 etcd-client.pem
-rw-r--r-- 1 root root 1025 Oct 25 10:35 apiserver-kubelet-client.csr
-rw-r--r-- 1 root root  299 Oct 25 10:35 apiserver-kubelet-client-csr.json
-rw------- 1 root root 1675 Oct 25 10:35 apiserver-kubelet-client-key.pem
-rw-r--r-- 1 root root 1724 Oct 25 10:35 apiserver-kubelet-client.pem


### 申请并颁发apiserver证书 (dnsca)
```shell
cd /opt/certs/
cat >/opt/certs/kubernetes-csr.json <<EOF
{
    "CN": "kubernetes",
    "hosts": [
        "127.0.0.1",
        "192.168.0.1",
        "kubernetes.default",
        "kubernetes.default.svc",
        "kubernetes.default.svc.cluster",
        "kubernetes.default.svc.cluster.local",
        "kubernetes.qytanghost.com",
        "kubernetes.qytangk8s.com",
        "10.1.1.10",
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
            "O": "qytang",
            "OU": "qytangk8s"
        }
    ]
}
EOF

cfssl gencert -ca=ca.pem \
              -ca-key=ca-key.pem \
              -config=ca-config.json \
              -profile=server kubernetes-csr.json \
              |cfssl-json -bare kubernetes

```

### 查看apiserver证书 (dnsca)
[root@localhost certs]# ll
-rw-r--r-- 1 root root 1330 Oct  9 08:35 kubernetes.csr
-rw-r--r-- 1 root root  649 Oct  9 08:35 kubernetes-csr.json
-rw------- 1 root root 1679 Oct  9 08:35 kubernetes-key.pem
-rw-r--r-- 1 root root 2009 Oct  9 08:35 kubernetes.pem

### 申请并颁发metrics-server证书 (dnsca)[由于API server没有安装网络,无法和metric server通讯所以无需安装]
```shell
cat > /opt/certs/proxy-client-csr.json <<EOF
{
  "CN": "aggregator",
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
            "O": "qytang",
            "OU": "qytangk8s"
      }
  ]
}
EOF

cd /opt/certs

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=peer \
  proxy-client-csr.json |cfssl-json -bare proxy-client

```

### 查看metrics-server证书 (dnsca)[由于API server没有安装网络,无法和metric server通讯所以无需安装]
[root@localhost certs]# ll
-rw-r--r-- 1 root root 1009 Oct 10 19:57 proxy-client.csr
-rw-r--r-- 1 root root  263 Oct 10 19:57 proxy-client-csr.json
-rw------- 1 root root 1675 Oct 10 19:57 proxy-client-key.pem
-rw-r--r-- 1 root root 1720 Oct 10 19:57 proxy-client.pem


### 产生用于--service-account-key-file的公钥 (dnsca)
```shell script
# 产生秘钥对
cd /opt/certs
openssl genrsa -des3 -out rsapair.pem 2048

# 导出公钥
openssl rsa -in rsapair.pem -outform PEM -pubout -out public.pem

# 导出私钥
openssl rsa -in rsapair.pem -out private.pem -outform PEM

```

### 查看产生的秘钥(dnsca)
[root@dnsca certs]# ll
-rw------- 1 root root 1679 Oct  9 08:38 private.pem
-rw-r--r-- 1 root root  451 Oct  9 08:38 public.pem
-rw------- 1 root root 1751 Oct  9 08:38 rsapair.pem

----------------------------------注意此处切换设备--------------------------------------

### 下载证书与秘钥, 启动apiserver服务 (Master01, Master02 and Master03)
```shell script
cd /opt/kubernetes/server/cert

sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubernetes-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubernetes.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/etcd-client-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/etcd-client.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/apiserver-kubelet-client-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/apiserver-kubelet-client.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/public.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/private.pem  .

# [由于API server没有安装网络,无法和metric server通讯所以无需安装]
# sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/proxy-client.pem .
# sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/proxy-client-key.pem .

```

### 查看下载的证书与秘钥 (Master01, Master02 and Master03)
[root@master01 cert]# pwd
/opt/kubernetes/server/cert

[root@master01 cert]# ll
total 36
-rw------- 1 root root 1675 Oct 25 10:37 apiserver-kubelet-client-key.pem
-rw-r--r-- 1 root root 1724 Oct 25 10:37 apiserver-kubelet-client.pem
-rw-r--r-- 1 root root 2000 Oct 25 10:37 ca.pem
-rw------- 1 root root 1675 Oct 25 10:37 etcd-client-key.pem
-rw-r--r-- 1 root root 1708 Oct 25 10:37 etcd-client.pem
-rw------- 1 root root 1679 Oct 25 10:37 kubernetes-key.pem
-rw-r--r-- 1 root root 2009 Oct 25 10:37 kubernetes.pem
-rw------- 1 root root 1679 Oct 25 10:37 private.pem
-rw-r--r-- 1 root root  451 Oct 25 10:37 public.pem

### 官方实例
https://kubernetes.io/zh/docs/tasks/debug-application-cluster/audit/

### 创建审计策略文件 (Master01, Master02 and Master03)
```shell
cat >/opt/kubernetes/server/conf/audit.yaml <<'EOF'
apiVersion: audit.k8s.io/v1beta1
kind: Policy
rules:
  # The following requests were manually identified as high-volume and low-risk, so drop them.
  - level: None
    resources:
      - group: ""
        resources:
          - endpoints
          - services
          - services/status
    users:
      - 'system:kube-proxy'
    verbs:
      - watch
  - level: None
    resources:
      - group: ""
        resources:
          - nodes
          - nodes/status
    userGroups:
      - 'system:nodes'
    verbs:
      - get
  - level: None
    namespaces:
      - kube-system
    resources:
      - group: ""
        resources:
          - endpoints
    users:
      - 'system:kube-controller-manager'
      - 'system:kube-scheduler'
      - 'system:serviceaccount:kube-system:endpoint-controller'
    verbs:
      - get
      - update
  - level: None
    resources:
      - group: ""
        resources:
          - namespaces
          - namespaces/status
          - namespaces/finalize
    users:
      - 'system:apiserver'
    verbs:
      - get
  # Don't log HPA fetching metrics.
  - level: None
    resources:
      - group: metrics.k8s.io
    users:
      - 'system:kube-controller-manager'
    verbs:
      - get
      - list
  # Don't log these read-only URLs.
  - level: None
    nonResourceURLs:
      - '/healthz*'
      - /version
      - '/swagger*'
  # Don't log events requests.
  - level: None
    resources:
      - group: ""
        resources:
          - events
  # node and pod status calls from nodes are high-volume and can be large, don't log responses for expected updates from nodes
  - level: Request
    omitStages:
      - RequestReceived
    resources:
      - group: ""
        resources:
          - nodes/status
          - pods/status
    users:
      - kubelet
      - 'system:node-problem-detector'
      - 'system:serviceaccount:kube-system:node-problem-detector'
    verbs:
      - update
      - patch
  - level: Request
    omitStages:
      - RequestReceived
    resources:
      - group: ""
        resources:
          - nodes/status
          - pods/status
    userGroups:
      - 'system:nodes'
    verbs:
      - update
      - patch
  # deletecollection calls can be large, don't log responses for expected namespace deletions
  - level: Request
    omitStages:
      - RequestReceived
    users:
      - 'system:serviceaccount:kube-system:namespace-controller'
    verbs:
      - deletecollection
  # Secrets, ConfigMaps, and TokenReviews can contain sensitive & binary data,
  # so only log at the Metadata level.
  - level: Metadata
    omitStages:
      - RequestReceived
    resources:
      - group: ""
        resources:
          - secrets
          - configmaps
      - group: authentication.k8s.io
        resources:
          - tokenreviews
  # Get repsonses can be large; skip them.
  - level: Request
    omitStages:
      - RequestReceived
    resources:
      - group: ""
      - group: admissionregistration.k8s.io
      - group: apiextensions.k8s.io
      - group: apiregistration.k8s.io
      - group: apps
      - group: authentication.k8s.io
      - group: authorization.k8s.io
      - group: autoscaling
      - group: batch
      - group: certificates.k8s.io
      - group: extensions
      - group: metrics.k8s.io
      - group: networking.k8s.io
      - group: policy
      - group: rbac.authorization.k8s.io
      - group: scheduling.k8s.io
      - group: settings.k8s.io
      - group: storage.k8s.io
    verbs:
      - get
      - list
      - watch
  # Default level for known APIs
  - level: RequestResponse
    omitStages:
      - RequestReceived
    resources:
      - group: ""
      - group: admissionregistration.k8s.io
      - group: apiextensions.k8s.io
      - group: apiregistration.k8s.io
      - group: apps
      - group: authentication.k8s.io
      - group: authorization.k8s.io
      - group: autoscaling
      - group: batch
      - group: certificates.k8s.io
      - group: extensions
      - group: metrics.k8s.io
      - group: networking.k8s.io
      - group: policy
      - group: rbac.authorization.k8s.io
      - group: scheduling.k8s.io
      - group: settings.k8s.io
      - group: storage.k8s.io
  # Default level for all other requests.
  - level: Metadata
    omitStages:
      - RequestReceived
EOF

```


### apiserver命令选项
https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/

### –target-ram-mb
内存配置选项和node数量的关系，单位是MB：--target-ram-mb=node_nums * 60

### Kubelet authentication
https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet-authentication-authorization/
To enable X509 client certificate authentication to the kubelet's HTTPS endpoint:
start the kubelet with the --client-ca-file flag, providing a CA bundle to verify client certificates with
start the apiserver with --kubelet-client-certificate and --kubelet-client-key flags

### API的认证
https://kubernetes.io/zh/docs/reference/access-authn-authz/authentication/
通过给 API 服务器传递 --client-ca-file=SOMEFILE 选项，就可以启动客户端证书身份认证。 
所引用的文件必须包含一个或者多个证书机构，用来验证向 API 服务器提供的客户端证书。 
如果提供了客户端证书并且证书被验证通过，则 subject 中的公共名称（Common Name）就被 作为请求的用户名。

### 配置apiserver启动脚本 (Master01, Master02 and Master03)
```shell
cat >/opt/kubernetes/server/bin/kube-apiserver.sh <<'EOF'
#!/bin/bash
etcd_host_1=10.1.1.101
etcd_host_2=10.1.1.102
etcd_host_3=10.1.1.103
./kube-apiserver \
  --audit-log-path /data/logs/kubernetes/kube-apiserver/audit-log \
  --audit-policy-file /opt/kubernetes/server/conf/audit.yaml \
  --authorization-mode RBAC \
  --allow-privileged=true \
  --feature-gates=VolumeSnapshotDataSource=true \
  --requestheader-client-ca-file /opt/kubernetes/server/cert/ca.pem \
  --client-ca-file /opt/kubernetes/server/cert/ca.pem \
  --etcd-cafile /opt/kubernetes/server/cert/ca.pem \
  --etcd-certfile /opt/kubernetes/server/cert/etcd-client.pem \
  --etcd-keyfile /opt/kubernetes/server/cert/etcd-client-key.pem \
  --etcd-servers https://${etcd_host_1}:2379,https://${etcd_host_2}:2379,https://${etcd_host_3}:2379 \
  --service-account-key-file /opt/kubernetes/server/cert/public.pem \
  --service-account-signing-key-file /opt/kubernetes/server/cert/private.pem \
  --service-account-issuer=kubernetes.qytanghost.com \
  --service-cluster-ip-range 192.168.0.0/16 \
  --target-ram-mb=180 \
  --anonymous-auth=false \
  --kubelet-certificate-authority=/opt/kubernetes/server/cert/ca.pem \
  --kubelet-client-certificate /opt/kubernetes/server/cert/apiserver-kubelet-client.pem \
  --kubelet-client-key /opt/kubernetes/server/cert/apiserver-kubelet-client-key.pem \
  --kubelet-https=true \
  --kubelet-timeout=10s \
  --log-dir /data/logs/kubernetes/kube-apiserver \
  --secure-port=6443 \
  --insecure-port=0 \
  --tls-cert-file /opt/kubernetes/server/cert/kubernetes.pem \
  --tls-private-key-file /opt/kubernetes/server/cert/kubernetes-key.pem \
  --v 2
EOF

```

###[由于API server没有安装网络,无法和metric server通讯所以取消如下选项]
```shell
  --proxy-client-cert-file=/opt/kubernetes/server/cert/proxy-client.pem
  --proxy-client-key-file=/opt/kubernetes/server/cert/proxy-client-key.pem
  --requestheader-allowed-names=aggregator
  --requestheader-extra-headers-prefix=X-Remote-Extra-
  --requestheader-group-headers=X-Remote-Group
  --requestheader-username-headers=X-Remote-User
  --enable-aggregator-routing=true
```


### 授权可执行权限 (Master01, Master02 and Master03)
```shell
chmod +x /opt/kubernetes/server/bin/kube-apiserver.sh

```

### 创建目录 (Master01, Master02 and Master03)
```shell
mkdir -p /data/logs/kubernetes/kube-apiserver

```

### 创建supervisord的kube-apiserver.ini文件 (Master01, Master02 and Master03)
```shell
cat >/etc/supervisord.d/kube-apiserver.ini <<EOF
[program:kube-apiserver]      ; 显示的程序名,类似my.cnf,可以有多个
command=sh /opt/kubernetes/server/bin/kube-apiserver.sh
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
stdout_logfile=/data/logs/kubernetes/kube-apiserver/apiserver.stdout.log
stdout_logfile_maxbytes=64MB  ; 日志文件大小 (default 50MB)
stdout_logfile_backups=4      ; 日志文件滚动个数 (default 10)
stdout_capture_maxbytes=1MB   ; 设定capture管道的大小(default 0)
killasgroup=true
stopasgroup=true
EOF

```

### 更新配置并查看状态(master01, master02, master03)
```shell
supervisorctl update
supervisorctl status

```

### 查看状态 (Master01, Master02 and Master03)
[root@master0x cert]# supervisorctl status

etcd-server                      RUNNING   pid 1443, uptime 0:10:24
kube-apiserver                   RUNNING   pid 1750, uptime 0:00:38

### 查看开放端口 (Master01, Master02 and Master03)
[root@master0x cert]# netstat -tulnp | grep kube-api
#### https 6443 提供kubelet 连接
tcp6       0      0 :::6443                 :::*                    LISTEN      2027/./kube-apiserv
