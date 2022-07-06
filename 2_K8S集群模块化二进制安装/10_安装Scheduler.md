### 申请并颁发scheduler证书 (dnsca)
```shell
cd /opt/certs
cat >/opt/certs/scheduler-csr.json <<EOF
{
    "CN": "system:kube-scheduler",
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
            "O": "system:kube-scheduler",
            "OU": "qytangk8s"
        }
    ]
}
EOF

cfssl gencert -ca=ca.pem \
              -ca-key=ca-key.pem \
              -config=ca-config.json \
              -profile=peer scheduler-csr.json \
              |cfssl-json -bare scheduler

```

### 查看scheduler证书 (dnsca)
[root@localhost certs]# ll
-rw-r--r-- 1 root root 1115 Oct  8 21:39 scheduler.csr
-rw-r--r-- 1 root root  396 Oct  8 21:39 scheduler-csr.json
-rw------- 1 root root 1675 Oct  8 21:39 scheduler-key.pem
-rw-r--r-- 1 root root 1809 Oct  8 21:39 scheduler.pem

----------------------------------注意此处切换设备--------------------------------------

### 下载scheduler的证书与秘钥 (Master01, Master02 and Master03)
```shell script
cd /opt/kubernetes/server/cert

sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/scheduler-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/scheduler.pem .

```

### 创建scheduler的kubeconfig文件 (Master01, Master02 and Master03)
```shell
cd /opt/kubernetes/server/conf/
kubectl config set-cluster kubernetes \
  --certificate-authority=/opt/kubernetes/server/cert/ca.pem \
  --embed-certs=true \
  --server=https://kubernetes.qytanghost.com:6443 \
  --kubeconfig=kube-controller-manager.kubeconfig
  
kubectl config set-credentials system:kube-scheduler \
  --client-certificate=/opt/kubernetes/server/cert/scheduler.pem \
  --client-key=/opt/kubernetes/server/cert/scheduler-key.pem \
  --embed-certs=true \
  --kubeconfig=kube-scheduler.kubeconfig
  
kubectl config set-context system:kube-scheduler \
  --cluster=kubernetes \
  --user=system:kube-scheduler \
  --kubeconfig=kube-scheduler.kubeconfig
  
kubectl config use-context system:kube-scheduler --kubeconfig=kube-scheduler.kubeconfig

```

### 创建 kube-scheduler 配置文件(Master01, Master02 and Master03)
```shell
cat >/opt/kubernetes/server/conf/kube-scheduler.yaml <<EOF
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration
clientConnection:
  burst: 200
  kubeconfig: "/opt/kubernetes/server/conf/kube-scheduler.kubeconfig"
  qps: 100
enableContentionProfiling: false
enableProfiling: true
healthzBindAddress: 0.0.0.0:10251
leaderElection:
  leaderElect: true
metricsBindAddress: 0.0.0.0:10251
EOF

```

### scheduler启动脚本 (Master01, Master02 and Master03)
```shell script
cat >/opt/kubernetes/server/bin/kube-scheduler.sh <<'EOF'
#!/bin/sh
./kube-scheduler \
  --config=/opt/kubernetes/server/conf/kube-scheduler.yaml \
  --bind-address=0.0.0.0 \
  --tls-cert-file=/opt/kubernetes/server/cert/scheduler.pem \
  --tls-private-key-file=/opt/kubernetes/server/cert/scheduler-key.pem \
  --client-ca-file=/opt/kubernetes/server/cert/ca.pem \
  --leader-elect  \
  --log-dir /data/logs/kubernetes/kube-scheduler \
  --master https://kubernetes.qytanghost.com:6443 \
  --v 2
EOF

```

# kube-scheduler命令选项
https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/

# 授权可执行权限(Master01, Master02 and Master03)
```shell
chmod +x  /opt/kubernetes/server/bin/kube-scheduler.sh

```

### 创建目录(Master01, Master02 and Master03)
```shell
mkdir -p /data/logs/kubernetes/kube-scheduler

```

### 创建supervisord的kube-scheduler.ini文件(Master01, Master02 and Master03)
```shell
cat >/etc/supervisord.d/kube-scheduler.ini <<EOF
[program:kube-scheduler]
command=sh /opt/kubernetes/server/bin/kube-scheduler.sh
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
stdout_logfile=/data/logs/kubernetes/kube-scheduler/scheduler.stdout.log
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

etcd-server                      RUNNING   pid 1570, uptime 1:28:05
kube-apiserver                   RUNNING   pid 1995, uptime 0:47:08
kube-controller-manager          RUNNING   pid 2261, uptime 0:22:54
kube-scheduler                   RUNNING   pid 2442, uptime 0:05:03


### 使用kubectl查看集群状态
[root@localhost ~]# kubectl get cs

NAME                 STATUS    MESSAGE              ERROR
scheduler            Healthy   ok                   
controller-manager   Healthy   ok                   
etcd-0               Healthy   {"health": "true"}   
etcd-2               Healthy   {"health": "true"}   
etcd-1               Healthy   {"health": "true"}   
```