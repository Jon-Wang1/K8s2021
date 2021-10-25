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
[root@localhost ~]# which cfssl
/usr/bin/cfssl

# cfssljson程序，从cfssl程序获取JSON输出，并将证书，密钥，CSR和bundle写入磁盘(dnsca)
[root@localhost ~]# which cfssl-json
/usr/bin/cfssl-json

# 输出给定证书的证书信息(dnsca)
[root@localhost ~]# which cfssl-certinfo
/usr/bin/cfssl-certinfo

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
        "expiry": "175200h"
    }
}
EOF

```

## 初始化CA(dnsca)
### cfssl gencert -initca ca-csr.json 输出文本(json)结果
### cfssl-json -bare ca 把输出文本信息(json), 产生文件

```shell script
cd /opt/certs/
cfssl gencert -initca ca-csr.json | cfssl-json -bare ca

```

### 下面是输出结果(dnsca)
2021/10/08 12:47:21 [INFO] generating a new CA key and certificate from CSR
2021/10/08 12:47:21 [INFO] generate received request
2021/10/08 12:47:21 [INFO] received CSR
2021/10/08 12:47:21 [INFO] generating key: rsa-4096
2021/10/08 12:47:27 [INFO] encoded CSR
2021/10/08 12:47:27 [INFO] signed certificate with serial number 367155466849847377434969243887200627215915796633

### 查看证书(dnsca)
[root@localhost certs]# ll
总用量 16
-rw-r--r-- 1 root root 1667 Oct  8 12:47 ca.csr      # 证书请求
-rw-r--r-- 1 root root  302 Oct  8 12:47 ca-csr.json
-rw------- 1 root root 3243 Oct  8 12:47 ca-key.pem  # 根的私钥
-rw-r--r-- 1 root root 2000 Oct  8 12:47 ca.pem      # 根证书

### 查看证书信息(dnsca)
cfssl-certinfo -cert ca.pem

## 配置证书模板(dnsca)
### 相当于微软的证书模板
### server 服务器证书
### client 客户证书
### peer   既扮演服务器, 也扮演客户, 例如:ETCD的节点

```shell script
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

----------------------------------注意此处切换设备--------------------------------------

### mgmtwin7 下载根证书ca.pem, 改名为ca.cer, 双击安装到“受信任的根颁发机构” （mgmtwin7）

----------------------------------注意此处切换设备--------------------------------------

### 确认dnsca秘钥（全部主机）
[root@dnsca certs]# ssh root@dnsca.qytanghost.com
The authenticity of host 'dnsca.qytanghost.com (10.1.1.219)' can't be established.
ECDSA key fingerprint is SHA256:jWlSzcu5QdgKgh19Haz/pXf4AfIwbt9cfzDERxuzwCs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'dnsca.qytanghost.com,10.1.1.219' (ECDSA) to the list of known hosts.
root@dnsca.qytanghost.com's password:
Last login: Mon Oct 25 09:54:48 2021 from 10.1.1.201

[root@dnsca ~]# exit  ### 注意注意注意！一定要退出
logout


### 下载根证书，更新受信任根证书颁发机构(全部主机)
```shell
yum install -y epel-release
yum install -y sshpass

mkdir -p /opt/certs
cd /opt/certs
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .

cat ca.pem >> qytanghost.com.crt
cp qytanghost.com.crt /etc/pki/ca-trust/source/anchors/qytanghost.com.crt
update-ca-trust

```
