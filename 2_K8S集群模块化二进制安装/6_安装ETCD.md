### CA服务器上签发ETCD的账户(dnsca)
```shell script
cat >/opt/certs/etcd-peer-csr.json <<EOF
{
    "CN": "etcd.qytanghost.com",
    "hosts": [
        "10.1.1.101",
        "10.1.1.102",
        "10.1.1.103",
        "master01.qytanghost.com",
        "master02.qytanghost.com",
        "master03.qytanghost.com"
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
```

# 进入目录签发证书(dnsca)
```shell script
cd /opt/certs

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=peer \
  etcd-peer-csr.json |cfssl-json -bare etcd-peer

[root@localhost certs]# ll
~~~忽略其它~~~
-rw-r--r-- 1 root root 1094 9月   9 20:21 etcd-peer.csr
-rw-r--r-- 1 root root  419 9月   9 20:19 etcd-peer-csr.json
-rw------- 1 root root 1675 9月   9 20:21 etcd-peer-key.pem
-rw-r--r-- 1 root root 1472 9月   9 20:21 etcd-peer.pem
```

----------------------------------注意此处切换设备--------------------------------------

#二进制安装etcd(Master01, Master02, Master03)

### 创建用户(Master01, Master02, Master03)
```shell script
useradd -s /sbin/nologin -M etcd
```

### etcd标签
https://github.com/etcd-io/etcd/releases/tag/v3.4.17

### 下载, 解压，软链接, 创建相关目录(Master01, Master02, Master03)
```shell
yum install -y wget
wget https://github.com/etcd-io/etcd/releases/download/v3.4.17/etcd-v3.4.17-linux-amd64.tar.gz

tar xf etcd-v3.4.17-linux-amd64.tar.gz -C /opt/
cd /opt/
mv etcd-v3.4.17-linux-amd64/ etcd-v3.4.17
ln -s /opt/etcd-v3.4.17/ /opt/etcd

mkdir -p /opt/etcd/certs /data/etcd /data/logs/etcd-server /data/etcd/etcd-server
```

### 下载证书文件(Master01, Master02, Master03)
```shell
cd /opt/etcd/certs/

sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/etcd-peer-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/etcd-peer.pem .
```

### 查看证书(Master01, Master02, Master03)
[root@localhost certs]# pwd
/opt/etcd/certs

[root@master02 certs]# ll
total 12
-rw-r--r-- 1 etcd etcd 2000 Oct  8 13:55 ca.pem
-rw------- 1 etcd etcd 1675 Oct  8 13:55 etcd-peer-key.pem
-rw-r--r-- 1 etcd etcd 1879 Oct  8 13:55 etcd-peer.pem

### 给与etcd账户,etcd相关目录的权限(Master01, Master02, Master03)
```shell
chown -R etcd.etcd /data/etcd/
chown -R etcd.etcd /data/logs/etcd-server/
chown -R etcd.etcd /opt/etcd-v3.4.17/
```

### etcd参数介绍
英文:
https://etcd.io/docs/v3.4/op-guide/configuration/

中文:
https://www.cnblogs.com/lowezheng/p/10307592.html

--quota-backend-bytes 参数介绍:
https://www.cnblogs.com/davygeek/p/8951999.html

### etcd启动脚本(master01)
```shell script
cat >/opt/etcd/etcd-server-startup.sh <<'EOF'
#!/bin/sh
etcd_host_1=10.1.1.101
etcd_host_2=10.1.1.102
etcd_host_3=10.1.1.103
etcd_name_host1=master01.qytanghost.com
etcd_name_host2=master02.qytanghost.com
etcd_name_host3=master03.qytanghost.com
./etcd \
    --name ${etcd_name_host1} \
    --data-dir /data/etcd/etcd-server \
    --listen-peer-urls https://${etcd_host_1}:2380 \
    --listen-client-urls https://${etcd_host_1}:2379,http://127.0.0.1:2379 \
    --quota-backend-bytes 8000000000 \
    --initial-advertise-peer-urls https://${etcd_host_1}:2380 \
    --advertise-client-urls https://${etcd_host_1}:2379,http://127.0.0.1:2379 \
    --initial-cluster  ${etcd_name_host1}=https://${etcd_host_1}:2380,${etcd_name_host2}=https://${etcd_host_2}:2380,${etcd_name_host3}=https://${etcd_host_3}:2380 \
    --client-cert-auth  \
    --cert-file ./certs/etcd-peer.pem \
    --key-file ./certs/etcd-peer-key.pem \
    --trusted-ca-file ./certs/ca.pem \
    --peer-client-cert-auth \
    --peer-cert-file ./certs/etcd-peer.pem \
    --peer-key-file ./certs/etcd-peer-key.pem \
    --peer-trusted-ca-file ./certs/ca.pem \
    --log-output stdout
EOF
```

### etcd启动脚本(master02)
```shell script
cat >/opt/etcd/etcd-server-startup.sh <<'EOF'
#!/bin/sh
etcd_host_1=10.1.1.101
etcd_host_2=10.1.1.102
etcd_host_3=10.1.1.103
etcd_name_host1=master01.qytanghost.com
etcd_name_host2=master02.qytanghost.com
etcd_name_host3=master03.qytanghost.com
./etcd \
    --name ${etcd_name_host2} \
    --data-dir /data/etcd/etcd-server \
    --listen-peer-urls https://${etcd_host_2}:2380 \
    --listen-client-urls https://${etcd_host_2}:2379,http://127.0.0.1:2379 \
    --quota-backend-bytes 8000000000 \
    --initial-advertise-peer-urls https://${etcd_host_2}:2380 \
    --advertise-client-urls https://${etcd_host_2}:2379,http://127.0.0.1:2379 \
    --initial-cluster  ${etcd_name_host1}=https://${etcd_host_1}:2380,${etcd_name_host2}=https://${etcd_host_2}:2380,${etcd_name_host3}=https://${etcd_host_3}:2380 \
    --client-cert-auth  \
    --cert-file ./certs/etcd-peer.pem \
    --key-file ./certs/etcd-peer-key.pem \
    --trusted-ca-file ./certs/ca.pem \
    --peer-client-cert-auth \
    --peer-cert-file ./certs/etcd-peer.pem \
    --peer-key-file ./certs/etcd-peer-key.pem \
    --peer-trusted-ca-file ./certs/ca.pem \
    --log-output stdout
EOF
```

### etcd启动脚本(master03)
```shell script
cat >/opt/etcd/etcd-server-startup.sh <<'EOF'
#!/bin/sh
etcd_host_1=10.1.1.101
etcd_host_2=10.1.1.102
etcd_host_3=10.1.1.103
etcd_name_host1=master01.qytanghost.com
etcd_name_host2=master02.qytanghost.com
etcd_name_host3=master03.qytanghost.com
./etcd \
    --name ${etcd_name_host3} \
    --data-dir /data/etcd/etcd-server \
    --listen-peer-urls https://${etcd_host_3}:2380 \
    --listen-client-urls https://${etcd_host_3}:2379,http://127.0.0.1:2379 \
    --quota-backend-bytes 8000000000 \
    --initial-advertise-peer-urls https://${etcd_host_3}:2380 \
    --advertise-client-urls https://${etcd_host_3}:2379,http://127.0.0.1:2379 \
    --initial-cluster  ${etcd_name_host1}=https://${etcd_host_1}:2380,${etcd_name_host2}=https://${etcd_host_2}:2380,${etcd_name_host3}=https://${etcd_host_3}:2380 \
    --client-cert-auth  \
    --cert-file ./certs/etcd-peer.pem \
    --key-file ./certs/etcd-peer-key.pem \
    --trusted-ca-file ./certs/ca.pem \
    --peer-client-cert-auth \
    --peer-cert-file ./certs/etcd-peer.pem \
    --peer-key-file ./certs/etcd-peer-key.pem \
    --peer-trusted-ca-file ./certs/ca.pem \
    --log-output stdout
EOF
```

### 使用supervisor启动etc脚本(master01, master02, master03)
```shell script
chmod +x /opt/etcd/etcd-server-startup.sh

yum install supervisor -y
systemctl start supervisord
systemctl enable supervisord

cat >/etc/supervisord.d/etcd-server.ini <<EOF
[program:etcd-server]  ; 显示的程序名,类型my.cnf,可以有多个
command=sh /opt/etcd/etcd-server-startup.sh
numprocs=1             ; 启动进程数 (def 1)
directory=/opt/etcd    ; 启动命令前切换的目录 (def no cwd)
autostart=true         ; 是否自启 (default: true)
autorestart=true       ; 是否自动重启 (default: true)
startsecs=30           ; 服务运行多久判断为成功(def. 1)
startretries=3         ; 启动重试次数 (default 3)
exitcodes=0,2          ; 退出状态码 (default 0,2)
stopsignal=QUIT        ; 退出信号 (default TERM)
stopwaitsecs=10        ; 退出延迟时间 (default 10)
user=etcd              ; 运行用户
redirect_stderr=true   ; 是否重定向错误输出到标准输出(def false)
stdout_logfile=/data/logs/etcd-server/etcd.stdout.log
stdout_logfile_maxbytes=64MB  ; 日志文件大小 (default 50MB)
stdout_logfile_backups=4      ; 日志文件滚动个数 (default 10)
stdout_capture_maxbytes=1MB   ; 设定capture管道的大小(default 0)
;子进程还有子进程,需要添加这个参数,避免产生孤儿进程
killasgroup=true
stopasgroup=true
EOF
```

### 更新并查看状态(master01, master02, master03)
```shell
supervisorctl update

supervisorctl status
etcd-server                      RUNNING   pid 2850, uptime 0:19:58
```

### 出现问题可以尝试查看日志(master01, master02, master03)
```shell
cat /data/logs/etcd-server/etcd.stdout.log
```

### 出现问题可以尝试重新启动服务(master01, master02, master03)
```shell
supervisorctl restart etcd-server
```

### 查看开放端口(master01, master02, master03)
```shell
netstat -lntup|grep etcd
# 2379 为客户提供服务
tcp        0      0 10.1.1.101:2379         0.0.0.0:*               LISTEN      2164/./etcd         
tcp        0      0 127.0.0.1:2379          0.0.0.0:*               LISTEN      2164/./etcd    
# 2380 ETCD内部通信     
tcp        0      0 10.1.1.101:2380         0.0.0.0:*               LISTEN      2164/./etcd  
```
 
# 查看成员状态(master01, master02, master03)
```shell
/opt/etcd/etcdctl member list -w table
+------------------+---------+-------------------------+-------------------------+-----------------------------------------------+------------+
|        ID        | STATUS  |          NAME           |       PEER ADDRS        |                 CLIENT ADDRS                  | IS LEARNER |
+------------------+---------+-------------------------+-------------------------+-----------------------------------------------+------------+
| 6561a639310282a3 | started | master02.qytanghost.com | https://10.1.1.102:2380 | http://127.0.0.1:2379,https://10.1.1.102:2379 |      false |
| 79ec7a671ffe12e8 | started | master01.qytanghost.com | https://10.1.1.101:2380 | http://127.0.0.1:2379,https://10.1.1.101:2379 |      false |
| b80844a3f01be1f2 | started | master03.qytanghost.com | https://10.1.1.103:2380 | http://127.0.0.1:2379,https://10.1.1.103:2379 |      false |
+------------------+---------+-------------------------+-------------------------+-----------------------------------------------+------------+

```

# 三个设备都执行以下命令，找到leader(master01, master02, master03)
```shell
/opt/etcd/etcdctl endpoint status -w table
+----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT    |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
| 127.0.0.1:2379 | 6561a639310282a3 |  3.4.17 |   20 kB |      true |      false |        11 |         13 |                 13 |        |
+----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
```

