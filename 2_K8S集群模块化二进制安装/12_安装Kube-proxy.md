### 签发证书 (DNSCA)
```shell script
cd /opt/certs/
cat >/opt/certs/kube-proxy-csr.json <<EOF
{
    "CN": "qytang-kube-proxy",
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

cfssl gencert \
      -ca=ca.pem \
      -ca-key=ca-key.pem \
      -config=ca-config.json \
      -profile=client \
      kube-proxy-csr.json |cfssl-json -bare kube-proxy-client

```

----------------------------------注意此处切换设备--------------------------------------

### 下载证书与秘钥 (Node01, Node02和Node03)
```shell script
cd /opt/kubernetes/node/cert
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kube-proxy-client.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kube-proxy-client-key.pem .

```

### 配置并且创建kubeconfig文件(Node01, Node02和Node03)
```shell
cd /opt/kubernetes/node/conf/

kubectl config set-cluster qytang-k8s-cluster \
    --certificate-authority=/opt/kubernetes/node/cert/ca.pem \
    --embed-certs=true \
    --server=https://kubernetes.qytanghost.com:6443 \
    --kubeconfig=kube-proxy.kubeconfig

kubectl config set-credentials qytang-kube-proxy \
    --client-certificate=/opt/kubernetes/node/cert/kube-proxy-client.pem \
    --client-key=/opt/kubernetes/node/cert/kube-proxy-client-key.pem \
    --embed-certs=true \
    --kubeconfig=kube-proxy.kubeconfig

kubectl config set-context qytang-myk8s-context \
    --cluster=qytang-k8s-cluster \
    --user=qytang-kube-proxy \
    --kubeconfig=kube-proxy.kubeconfig

kubectl config use-context qytang-myk8s-context --kubeconfig=kube-proxy.kubeconfig

```

----------------------------------注意此处切换设备--------------------------------------

### RBAC配置 (任何Master)
```shell script
cat >/opt/kubernetes/server/conf/k8s-proxy.yaml <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: qytang-kube-proxy
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:node-proxier
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: qytang-kube-proxy
EOF

kubectl apply -f /opt/kubernetes/server/conf/k8s-proxy.yaml

```

----------------------------------注意此处切换设备--------------------------------------

# 创建开机ipvs脚本 (Node01, Node02和Node03)
```shell script
cat >/etc/ipvs.sh <<'EOF'

#!/bin/bash
ipvs_mods_dir="/usr/lib/modules/$(uname -r)/kernel/net/netfilter/ipvs"
for i in $(ls $ipvs_mods_dir|grep -o "^[^.]*")
do
  /sbin/modinfo -F filename $i &>/dev/null
  if [ $? -eq 0 ];then
    /sbin/modprobe $i
  fi
done
EOF

sh /etc/ipvs.sh 

lsmod |grep ip_vs

```

### kube-proxy启动脚本 (Node01)
```shell script
cat >/opt/kubernetes/node/bin/kube-proxy.sh <<'EOF'
#!/bin/sh
./kube-proxy \
  --hostname-override node01.qytanghost.com \
  --cluster-cidr 172.16.0.0/16 \
  --proxy-mode=ipvs \
  --ipvs-scheduler=rr \
  --kubeconfig /opt/kubernetes/node/conf/kube-proxy.kubeconfig
EOF

```

### kube-proxy启动脚本 (Node02)
```shell script
cat >/opt/kubernetes/node/bin/kube-proxy.sh <<'EOF'
#!/bin/sh
./kube-proxy \
  --hostname-override node02.qytanghost.com \
  --cluster-cidr 172.16.0.0/16 \
  --proxy-mode=ipvs \
  --ipvs-scheduler=rr \
  --kubeconfig /opt/kubernetes/node/conf/kube-proxy.kubeconfig
EOF

```

### kube-proxy启动脚本 (Node03)
```shell script
cat >/opt/kubernetes/node/bin/kube-proxy.sh <<'EOF'
#!/bin/sh
./kube-proxy \
  --hostname-override node03.qytanghost.com \
  --cluster-cidr 172.16.0.0/16 \
  --proxy-mode=ipvs \
  --ipvs-scheduler=rr \
  --kubeconfig /opt/kubernetes/node/conf/kube-proxy.kubeconfig
EOF

```

### 启动kube-proxy服务 (Node01, Node02和Node03)
```shell script
cat >/etc/supervisord.d/kube-proxy.ini <<'EOF'
[program:kube-proxy]
command=sh /opt/kubernetes/node/bin/kube-proxy.sh
numprocs=1                    ; 启动进程数 (def 1)
directory=/opt/kubernetes/node/bin
autostart=true                ; 是否自启 (default: true)
autorestart=true              ; 是否自动重启 (default: true)
startsecs=30                  ; 服务运行多久判断为成功(def. 1)
startretries=3                ; 启动重试次数 (default 3)
exitcodes=0,2                 ; 退出状态码 (default 0,2)
stopsignal=QUIT               ; 退出信号 (default TERM)
stopwaitsecs=10               ; 退出延迟时间 (default 10)
user=root                     ; 运行用户
redirect_stderr=true          ; 重定向错误输出到标准输出(def false)
stdout_logfile=/data/logs/kubernetes/kube-proxy/proxy.stdout.log
stdout_logfile_maxbytes=64MB  ; 日志文件大小 (default 50MB)
stdout_logfile_backups=4      ; 日志文件滚动个数 (default 10)
stdout_capture_maxbytes=1MB   ; 设定capture管道的大小(default 0)
;子进程还有子进程,需要添加这个参数,避免产生孤儿进程
killasgroup=true
stopasgroup=true
EOF

mkdir -p /data/logs/kubernetes/kube-proxy
supervisorctl update
supervisorctl status

```

### anzhuang ipvs管理工具(Node01, Node02和Node03)
```shell
yum install ipvsadm -y

```

### 查看ipvs（IP Virtual Server）状态(Node01, Node02和Node03)
[root@node01 conf]# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  192.168.0.1:443 nq
  -> 10.1.1.101:6443              Masq    1      0          0         
  -> 10.1.1.102:6443              Masq    1      0          0         
  -> 10.1.1.103:6443              Masq    1      0          0   

----------------------------------注意此处切换设备--------------------------------------

###查看svc (任何Master)
root@localhost ~]# kubectl get svc
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   192.168.0.1   <none>        443/TCP   13h
