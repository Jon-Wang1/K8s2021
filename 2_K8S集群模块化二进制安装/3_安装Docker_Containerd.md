### 切换国内镜像源 (harbor, gitlab, mgmtcentos, master01, master02, master03, node01, node02, node03)
```shell script
yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager \
                  --add-repo \
                  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y docker-ce docker-ce-cli containerd.io

```

### 安装Docker (harbor, gitlab, mgmtcentos, master01, master02, master03, node01, node02, node03)
```shell script
# "live-restore": true  在 dockerd 停止时保证已启动的 Running 容器持续运行，并在 daemon 进程启动后重新接管
# "exec-opts": ["native.cgroupdriver=systemd"], 是为了匹配kubelet的 --cgroup-driver systemd 
# "storage-driver": "overlay2", 一种较新的存储方案
# "graph": "/data/docker",  修改镜像存储位置

mkdir -p /etc/docker /data/docker
cat >/etc/docker/daemon.json <<EOF
{
  "graph": "/data/docker", 
  "storage-driver": "overlay2",
  "registry-mirrors": ["https://0a041wc3.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "live-restore": true
}
EOF

systemctl start docker
systemctl enable docker

```

###安装docker-compose (harbor, mgmtcentos, gitlab, master01, master02, master03, node01, node02, node03)
```shell
下载docker-compose:
curl -L "https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 查看版本
docker-compose --version

```


=============================================安装Containerd========================================
### 参考文章
https://blog.csdn.net/tongzidane/article/details/114285188

### Github
https://github.com/containerd/containerd/

### 下载二进制文件 (所有计算节点)
```shell
yum install -y wget
wget https://github.com/containerd/containerd/releases/download/v1.5.7/containerd-1.5.7-linux-amd64.tar.gz

```

### 解压缩  (所有计算节点)
```shell
tar -xvf containerd-1.5.7-linux-amd64.tar.gz -C /usr/local/

```

### 创建目录并生成默认文件 (所有计算节点)
```shell
mkdir /etc/containerd
containerd config default> /etc/containerd/config.toml

```

### 配置containerd.service服务文件 (所有计算节点)
```shell
cat >/usr/lib/systemd/system/containerd.service <<EOF
[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target
 
[Service]
ExecStartPre=/sbin/modprobe overlay
ExecStart=/usr/local/bin/containerd
Delegate=yes
KillMode=process
LimitNOFILE=1048576
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNPROC=infinity
LimitCORE=infinity
 
[Install]
WantedBy=multi-user.target
EOF

```

### 加载并启动服务 
```shell
systemctl daemon-reload 
systemctl enable containerd
systemctl start containerd
systemctl status containerd

```