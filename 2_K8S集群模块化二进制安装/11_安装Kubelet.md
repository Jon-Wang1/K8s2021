### 签发证书 (dnsca)
```shell script
cd /opt/certs/
cat >/opt/certs/kubelet-csr.json <<EOF
{
    "CN": "qytang-k8s-kubelet",
    "hosts": [
    "127.0.0.1",
    "10.1.1.201",
    "10.1.1.202",
    "10.1.1.203",
    "node01.qytanghost.com",
    "node02.qytanghost.com",
    "node03.qytanghost.com"
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

cat >/opt/certs/kubelet-client-csr.json <<EOF
{
    "CN": "qytang-k8s-node",
    "hosts": [
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

cfssl gencert \
      -ca=ca.pem \
      -ca-key=ca-key.pem \
      -config=ca-config.json \
      -profile=server \
      kubelet-csr.json | cfssl-json -bare kubelet

cfssl gencert \
      -ca=ca.pem \
      -ca-key=ca-key.pem \
      -config=ca-config.json \
      -profile=client \
      kubelet-client-csr.json | cfssl-json -bare kubelet-client
      
[root@localhost certs]# ll
# kubelet-client 用于与APIServer进行通信
# 关注CN, 他会在RBAC中进行绑定
-rw-r--r-- 1 root root 1017 10月 25 04:36 kubelet-client.csr
-rw-r--r-- 1 root root  297 10月 25 04:36 kubelet-client-csr.json
-rw------- 1 root root 1679 10月 25 04:36 kubelet-client-key.pem
-rw-r--r-- 1 root root 1740 10月 25 04:36 kubelet-client.pem

# kubelet 作为服务器证书使用, 集群内访问K8S, 就是访问的Node的HTTPS 6443
-rw-r--r-- 1 root root 1090 10月 25 04:36 kubelet.csr
-rw-r--r-- 1 root root  370 10月 25 04:36 kubelet-csr.json
-rw------- 1 root root 1675 10月 25 04:36 kubelet-key.pem
-rw-r--r-- 1 root root 1797 10月 25 04:36 kubelet.pem
```

----------------------------------注意此处切换设备--------------------------------------

### 安装kubelet(Node01, Node02和Node03)
```shell script
yum install -y wget
wget https://dl.k8s.io/v1.20.11/kubernetes-node-linux-amd64.tar.gz

tar xf kubernetes-node-linux-amd64.tar.gz -C /opt

cd /opt
mv /opt/kubernetes/ /opt/kubernetes-v1.20.11-linux-amd64
ln -s /opt/kubernetes-v1.20.11-linux-amd64/ /opt/kubernetes

mkdir -p /opt/kubernetes/node/cert
cd /opt/kubernetes/node/cert
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubelet.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubelet-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubelet-client.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/kubelet-client-key.pem .
```

### 配置kubelet与apiserver通讯(Node01, Node02和Node03)
```shell script
# embed-certs为true表示将--certificate-authority证书写入到kubeconfig中

mkdir -p /opt/kubernetes/node/conf
cd /opt/kubernetes/node/conf/

ln -s /opt/kubernetes/node/bin/kubectl /usr/bin/kubectl

kubectl config set-cluster qytang-k8s-cluster \
    --certificate-authority=/opt/kubernetes/node/cert/ca.pem \
    --embed-certs=true \
    --server=https://kubernetes.qytanghost.com:7443 \
    --kubeconfig=kubelet.kubeconfig

kubectl config set-credentials qytang-k8s-credentials \
    --client-certificate=/opt/kubernetes/node/cert/kubelet-client.pem \
    --client-key=/opt/kubernetes/node/cert/kubelet-client-key.pem \
    --embed-certs=true \
    --kubeconfig=kubelet.kubeconfig

kubectl config set-context myk8s-context \
    --cluster=qytang-k8s-cluster \
    --user=qytang-k8s-credentials \
    --kubeconfig=kubelet.kubeconfig

kubectl config use-context myk8s-context --kubeconfig=kubelet.kubeconfig
```

# 查看产生的配置文件
```shell script
[root@node03 conf]# pwd
/opt/kubernetes/node/conf
[root@node03 conf]# cat kubelet.kubeconfig 
~~~忽略输出~~~
```

### RBAC配置 (任何一个Master)
```shell script
cat >/opt/kubernetes/server/conf/k8s-node.yaml <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: qytang-k8s-node
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:node
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: qytang-k8s-node
EOF

kubectl create -f /opt/kubernetes/server/conf/k8s-node.yaml
```

### 查看系统默认的ROLES
```shell script
[root@master01 cert]# kubectl get clusterroles
~~~忽略大量内容~~~
system:node                                            ClusterRole/system:node                                            45m
```

### 查看clusterrolebinding
```shell script
[root@master01 cert]# kubectl get clusterrolebinding
~~~忽略大量内容~~~
qytang-k8s-node                                        ClusterRole/system:node                                            69s
```

### kubelet启动脚本 (Node01)
```shell script
cat >/opt/kubernetes/node/bin/kubelet.sh <<'EOF'
#!/bin/sh
./kubelet \
  --hostname-override node01.qytanghost.com \
  --anonymous-auth=false \
  --cgroup-driver systemd \
  --cluster-dns 192.168.0.2 \
  --authentication-token-webhook=true \
  --authorization-mode=Webhook \
  --cluster-domain cluster.local \
  --runtime-cgroups=/systemd/system.slice \
  --kubelet-cgroups=/systemd/system.slice \
  --fail-swap-on="false" \
  --network-plugin=cni \
  --client-ca-file /opt/kubernetes/node/cert/ca.pem \
  --tls-cert-file /opt/kubernetes/node/cert/kubelet.pem \
  --tls-private-key-file /opt/kubernetes/node/cert/kubelet-key.pem \
  --image-gc-high-threshold 20 \
  --image-gc-low-threshold 10 \
  --kubeconfig /opt/kubernetes/node/conf/kubelet.kubeconfig \
  --log-dir /data/logs/kubernetes/kube-kubelet \
  --pod-infra-container-image harbor.qytanghost.com/public/pause:latest \
  --root-dir /data/kubelet
EOF
```

### kubelet启动脚本 (Node02)
```shell script
cat >/opt/kubernetes/node/bin/kubelet.sh <<'EOF'
#!/bin/sh
./kubelet \
  --hostname-override node02.qytanghost.com \
  --anonymous-auth=false \
  --cgroup-driver systemd \
  --cluster-dns 192.168.0.2 \
  --authentication-token-webhook=true \
  --authorization-mode=Webhook \
  --cluster-domain cluster.local \
  --runtime-cgroups=/systemd/system.slice \
  --kubelet-cgroups=/systemd/system.slice \
  --fail-swap-on="false" \
  --network-plugin=cni \
  --client-ca-file /opt/kubernetes/node/cert/ca.pem \
  --tls-cert-file /opt/kubernetes/node/cert/kubelet.pem \
  --tls-private-key-file /opt/kubernetes/node/cert/kubelet-key.pem \
  --image-gc-high-threshold 20 \
  --image-gc-low-threshold 10 \
  --kubeconfig /opt/kubernetes/node/conf/kubelet.kubeconfig \
  --log-dir /data/logs/kubernetes/kube-kubelet \
  --pod-infra-container-image harbor.qytanghost.com/public/pause:latest \
  --root-dir /data/kubelet
EOF
```

### kubelet启动脚本 (Node03)
```shell script
cat >/opt/kubernetes/node/bin/kubelet.sh <<'EOF'
#!/bin/sh
./kubelet \
  --hostname-override node03.qytanghost.com \
  --anonymous-auth=false \
  --cgroup-driver systemd \
  --cluster-dns 192.168.0.2 \
  --authentication-token-webhook=true \
  --authorization-mode=Webhook \
  --cluster-domain cluster.local \
  --runtime-cgroups=/systemd/system.slice \
  --kubelet-cgroups=/systemd/system.slice \
  --fail-swap-on="false" \
  --network-plugin=cni \
  --client-ca-file /opt/kubernetes/node/cert/ca.pem \
  --tls-cert-file /opt/kubernetes/node/cert/kubelet.pem \
  --tls-private-key-file /opt/kubernetes/node/cert/kubelet-key.pem \
  --image-gc-high-threshold 20 \
  --image-gc-low-threshold 10 \
  --kubeconfig /opt/kubernetes/node/conf/kubelet.kubeconfig \
  --log-dir /data/logs/kubernetes/kube-kubelet \
  --pod-infra-container-image harbor.qytanghost.com/public/pause:latest \
  --root-dir /data/kubelet
EOF
```

### 下载pause镜像 (Harbor)
```shell script
docker pull kubernetes/pause
docker tag kubernetes/pause harbor.qytanghost.com/public/pause
docker push harbor.qytanghost.com/public/pause
```

### 启动kubelet服务 (Node01, Node02和Node03)
```shell script
chmod +x /opt/kubernetes/node/bin/kubelet.sh
mkdir -p /data/logs/kubernetes/kube-kubelet
mkdir -p /data/kubelet
yum install supervisor -y
systemctl start supervisord
systemctl enable supervisord

cat >/etc/supervisord.d/kube-kubelet.ini  <<EOF
[program:kube-kubelet]
command=sh /opt/kubernetes/node/bin/kubelet.sh
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
stdout_logfile=/data/logs/kubernetes/kube-kubelet/kubelet.stdout.log
stdout_logfile_maxbytes=64MB  ; 日志文件大小 (default 50MB)
stdout_logfile_backups=4      ; 日志文件滚动个数 (default 10)
stdout_capture_maxbytes=1MB   ; 设定capture管道的大小(default 0)
;子进程还有子进程,需要添加这个参数,避免产生孤儿进程
killasgroup=true
stopasgroup=true
EOF

supervisorctl update
supervisorctl status
```

### 查看node状态, 并打标签 (任何一个Master)
```shell script
kubectl label node node01.qytanghost.com node-role.kubernetes.io/node=
kubectl label node node02.qytanghost.com node-role.kubernetes.io/node=
kubectl label node node03.qytanghost.com node-role.kubernetes.io/node=

# 如果即是计算节点也是Master, 可以再打上master的label
kubectl label node node01.host.com node-role.kubernetes.io/master=

# 删除标签
kubectl label node node01.host.com node-role.kubernetes.io/master-

# 查看节点, 由于CNI还未安装的原因, 所以状态为未就绪
[root@master03 ~]# kubectl get nodes
NAME              STATUS     ROLES   AGE   VERSION
node01.host.com   NotReady   node    46s   v1.18.9
node02.host.com   NotReady   node    45s   v1.18.9
node03.host.com   NotReady   node    46s   v1.18.9
```
