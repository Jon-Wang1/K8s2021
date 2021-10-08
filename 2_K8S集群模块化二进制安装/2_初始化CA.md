### CFSSL介绍
https://blog.51cto.com/liuzhengwei521/2120535

### 下载安装cfssl(dnsca)
```shell script
yum install -y wget
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64 -O /usr/bin/cfssl
wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64 -O /usr/bin/cfssl-json
wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64 -O /usr/bin/cfssl-certinfo
chmod +x /usr/bin/cfssl*
```

### 确认安装(dnsca)
```shell script
# CFSSL的命令行工具
[root@localhost ~]# which cfssl
/usr/bin/cfssl

# cfssljson程序，从cfssl程序获取JSON输出，并将证书，密钥，CSR和bundle写入磁盘
[root@localhost ~]# which cfssl-json
/usr/bin/cfssl-json

# 输出给定证书的证书信息
[root@localhost ~]# which cfssl-certinfo
/usr/bin/cfssl-certinfo
```

### 自签名根证书(20年有效期)(dnsca)
```shell script
mkdir -p /opt/certs

cat >/opt/certs/ca-csr.json <<EOF
{
    "CN": "qytca",
    "hosts": [
    ],
    "key": {
        "algo": "rsa",
        "size": 4096
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "qytang"
        }
    ],
    "ca": {
        "expiry": "17520h"
    }
}
EOF
```

### 初始化CA(dnsca)
```shell script
# cfssl gencert -initca ca-csr.json 输出文本(json)结果
# cfssl-json -bare ca 把输出文本信息(json), 产生文件

cd /opt/certs/
cfssl gencert -initca ca-csr.json | cfssl-json -bare ca
~~~ 下面是输出 ~~~
2020/09/09 03:09:38 [INFO] generating a new CA key and certificate from CSR
2020/09/09 03:09:38 [INFO] generate received request
2020/09/09 03:09:38 [INFO] received CSR
2020/09/09 03:09:38 [INFO] generating key: rsa-2048
2020/09/09 03:09:39 [INFO] encoded CSR
2020/09/09 03:09:39 [INFO] signed certificate with serial number 305773733204133988374871170151725823517100191358

[root@localhost certs]# ll
总用量 16
-rw-r--r-- 1 root root 1009 9月   9 03:09 ca.csr      # 证书请求
-rw-r--r-- 1 root root  338 9月   9 03:07 ca-csr.json
-rw------- 1 root root 1675 9月   9 03:09 ca-key.pem  # 根的私钥
-rw-r--r-- 1 root root 1371 9月   9 03:09 ca.pem      # 根证书
```

### 查看证书信息(dnsca)
```shell script
cfssl-certinfo -cert ca.pem
```

### 配置证书模板
```shell script
# 相当于微软的证书模板
# server 服务器证书
# client 客户证书
# peer   既扮演服务器, 也扮演客户, 例如:ETCD的节点

cat >/opt/certs/ca-config.json <<EOF
{
    "signing": {
        "default": {
            "expiry": "87600h"
        },
        "profiles": {
            "server": {
                "expiry": "175200h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            },
            "peer": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            }
        }
    }
} 
EOF
```