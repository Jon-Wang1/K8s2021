###Harbor证书申请文件(dnsca)
```shell script
cat >/opt/certs/harbor-csr.json <<EOF
{
    "CN": "harbor.qytanghost.com",
    "hosts": [
        "10.1.1.220",
        "harbor.qytanghost.com",
        "harbor.qytangk8s.com"
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

### 进入目录签发Harbor证书(dnsca)
```shell script
cd /opt/certs

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=server \
  harbor-csr.json |cfssl-json -bare harbor

```

### 查看签发的证书(dnsca)
[root@dnsca certs]# ll
-rw-r--r-- 1 root root 1115 Oct  8 09:22 harbor.csr
-rw-r--r-- 1 root root  376 Oct  8 09:21 harbor-csr.json
-rw------- 1 root root 1675 Oct  8 09:22 harbor-key.pem
-rw-r--r-- 1 root root 1793 Oct  8 09:22 harbor.pem

----------------------------------注意此处切换设备--------------------------------------

### 下载Harbor（harbor)
```shell
mkdir /opt/src
cd /opt/src/

yum install -y wget
wget https://github.com/goharbor/harbor/releases/download/v2.3.3/harbor-offline-installer-v2.3.3.tgz

tar xf harbor-offline-installer-v2.3.3.tgz  -C /opt/

cd /opt

```

### 查看解压目录（harbor)
[root@harbor opt]# ll
total 0
drwx--x--x 4 root root  28 Oct  8 12:55 containerd
drwxr-xr-x 2 root root 122 Oct  8 12:58 harbor
drwxr-xr-x 2 root root  49 Oct  8 12:57 src



### 移动harbor目录到有版本号的目录（harbor)
```shell
mv harbor/ harbor-v2.3.3

```

### 软链接回/opt/harbor,这个操作便于后续升级（harbor)
```shell
ln -s /opt/harbor-v2.3.3/ /opt/harbor

```

### 查看目录与软链接（harbor)
[root@harbor opt]# ll
total 0
drwx--x--x 4 root root  28 Oct  8 12:55 containerd
lrwxrwxrwx 1 root root  19 Oct  8 12:59 harbor -> /opt/harbor-v2.3.3/
drwxr-xr-x 2 root root 122 Oct  8 12:58 harbor-v2.3.3
drwxr-xr-x 2 root root  49 Oct  8 12:57 src

### 修改harbor配置文件(harbor)
[root@localhost opt]# cd /opt/harbor
[root@harbor harbor]# ll
total 610344
-rw-r--r-- 1 root root      3361 Sep 24 14:57 common.sh
-rw-r--r-- 1 root root 624956679 Sep 24 14:58 harbor.v2.3.3.tar.gz
-rw-r--r-- 1 root root      7840 Sep 24 14:57 harbor.yml.tmpl
-rwxr-xr-x 1 root root      2500 Sep 24 14:57 install.sh
-rw-r--r-- 1 root root     11347 Sep 24 14:57 LICENSE
-rwxr-xr-x 1 root root      1881 Sep 24 14:57 prepare

### 修改prepare文件(harbor)
```shell
cd /opt/harbor
vim prepare

```

### 具体修改内容
docker run --rm -v $input_dir:/input \
                    -v $data_path:/data \
                    -v $harbor_prepare_path:/compose_location \
                    -v $config_dir:/config \
                    -v /opt/harbor/certs:/hostfs \ # 修改部分
                    --privileged \
                    goharbor/prepare:v2.3.3 prepare $@


### 映射关系:
/opt/harbor/certs/harbor.pem
/hostfs/harbor.pem

# harbor容器内的路径
/harbor.pem

### 修改harbor.yml(harbor)
```shell
cd /opt/harbor
cp harbor.yml.tmpl harbor.yml
vim harbor.yml

```

### 具体修改内容
hostname: harbor.qytanghost.com

https:
  #https port for harbor, default is 443
  port: 443
  # The path of cert and key files for nginx
  certificate: /harbor.pem
  private_key: /harbor-key.pem

harbor_admin_password: Cisc0123
database:
  password: Cisc0123
data_volume: /data/harbor
log:
  local:
    location: /data/harbor/logs

### 创建harbor日志目录(harbor)
```shell
mkdir -p /data/harbor/logs

```

### 下载根证书与个人证书（harbor）
```shell
yum install -y epel-release
yum install -y sshpass
mkdir -p /opt/harbor/certs
cd /opt/harbor/certs
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/harbor-key.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/harbor.pem .

```

### 安装Harbor(harbor)
```shell
cd /opt/harbor
./install.sh 

```

----------------------------------注意此处切换设备--------------------------------------

### 从dnsca下载根证书ca.pem到管理WIN7(管理Win7）[详细操作参考PPT]
### 改名ca.pem到ca.cer(管理Win7）[详细操作参考PPT]
### 加载到受信任根证书颁发机构(管理Win7）[详细操作参考PPT]
### 游览器访问https://harbor.qytanghost.com测试(管理Win7） [详细操作参考PPT]
### 新建项目public(公开)(管理Win7）[详细操作参考PPT]

----------------------------------注意此处切换设备--------------------------------------

### docker login harbor.qytanghost.com测试(gitlab, harbor, mgmtcentos, master01, master02, master03, node01, node02, node03)
[root@master01 certs]# docker login harbor.qytanghost.com
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

----------------------------------注意此处切换设备--------------------------------------

### 拉取镜像(任何一个安装了Docker，并且docker login的设备)
```shell
docker pull centos
docker pull nginx

```

### 修改镜像标签(任何一个安装了Docker，并且docker login的设备)
```shell
docker tag centos harbor.qytanghost.com/public/centos
docker tag nginx harbor.qytanghost.com/public/nginx

```

### 推送镜像到私有仓库(任何一个安装了Docker，并且docker login的设备)
```shell
docker push harbor.qytanghost.com/public/centos
docker push harbor.qytanghost.com/public/nginx

```

----------------------------------注意此处切换设备--------------------------------------

### 测试从私有仓库拉取镜像(任何一个安装了Docker，并且docker login的设备)
```shell
docker pull harbor.qytanghost.com/public/centos
docker pull harbor.qytanghost.com/public/nginx

```