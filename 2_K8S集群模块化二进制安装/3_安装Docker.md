### 切换国内镜像源 (harbor, gitlab, master01, master02, master03, node01, node02, node03)
```shell script
yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager \
                  --add-repo \
                  http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y docker-ce docker-ce-cli containerd.io
```

### 安装Docker (harbor, gitlab, master01, master02, master03, node01, node02, node03)
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

###安装docker-compose (harbor, gitlab, master01, master02, master03, node01, node02, node03)
```shell
下载docker-compose:
curl -L "https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 查看版本
docker-compose --version
```