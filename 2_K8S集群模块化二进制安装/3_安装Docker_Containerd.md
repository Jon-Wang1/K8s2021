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
https://kubernetes.io/docs/setup/production-environment/container-runtimes/

### 安装docker的时候已经安装了containerd.io

### 系统准备 (node01, node02, node03)
```shell
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Setup required sysctl params, these persist across reboots.
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

# Apply sysctl params without reboot
sudo sysctl --system

```

### 产生配置文件  (node01, node02, node03)
```shell
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

```

### 修改配置文件“/etc/containerd/config.toml” (node01, node02, node03)
vim /etc/containerd/config.toml

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true # 添加此内容


### 加载并启动服务 (node01, node02, node03)
```shell
systemctl enable containerd
systemctl restart containerd
systemctl status containerd

```