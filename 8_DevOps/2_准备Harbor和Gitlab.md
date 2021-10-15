###Harbor创建私有项目devops(详细截图看PPT)

###Gitlab创建私有项目Nameko_DevOps(详细截图看PPT)

###复制项目Git地址(详细截图看PPT)

###PyCharm定义Remote(详细截图看PPT)

###PyCharm Push项目到Gitlab(详细截图看PPT)

###Gitlab查看两个分支(详细截图看PPT)

### 安装Runner (gitlab)
```shell
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh" | sudo bash
yum install -y gitlab-ci-multi-runner

```

### 查看Runner注册URL与Token(详细截图看PPT)

### 注册Gitlab Runner (gitlab)
[root@gitlab deploy]# gitlab-ci-multi-runner register
Runtime platform                                    arch=amd64 os=linux pid=733460 revision=e0218c92 version=14.3.2
Running in system-mode.

Enter the GitLab instance URL (for example, https://gitlab.com/):
http://gitlab.qytanghost.com/
Enter the registration token:
S7ebdyvFKBFyk3udYcbb
Enter a description for the runner:
[gitlab.qytanghost.com]: k8s
Enter tags for the runner (comma-separated):
k8s
Registering runner... succeeded                     runner=S7ebdyvF
Enter an executor: kubernetes, docker, docker-ssh, parallels, shell, virtualbox, docker+machine, docker-ssh+machine, custom, ssh:
shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!

### 查看注册的Runner (详细截图看PPT)

### 添加Runner到sudouser  (详细截图看PPT)

### 创建登录harbor的secret (任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_harbor_secret/harbor_secret.yaml
```

###拷贝kubeconfig到Gitlab
#### Gitlab创建目录 (Gitlab)
[root@gitlab ~]# mkdir /etc/deploy

#### Mastor01 拷贝kubeconfig到gitlab (Master01)
[root@master01 ~]# scp /root/.kube/config root@gitlab.qytanghost.com:/etc/deploy/config

#### 让gitlab-runner成为config文件的拥有者 (Gitlab)
[root@gitlab ~]# chown gitlab-runner /etc/deploy/config


### 二进制安装kubectl (Gitlab)
#### 查看版本
https://github.com/kubernetes/kubernetes/tags

https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md

#### 下载二进制文件, 解压缩, 创建目录, 做软链接 (Gitlab)
```shell script
yum install -y wget
wget https://dl.k8s.io/v1.20.11/kubernetes-client-linux-amd64.tar.gz

tar xf kubernetes-client-linux-amd64.tar.gz -C /opt

cd /opt
mv /opt/kubernetes/ /opt/kubernetes-v1.20.11-linux-amd64
ln -s /opt/kubernetes-v1.20.11-linux-amd64/ /opt/kubernetes
ln -s /opt/kubernetes/client/bin/kubectl /usr/bin/kubectl

```

### 设置Gitlab 环境变量 (详细截图看PPT)

### push nameko_microservice分支,并且查看CICD pipeline

### push nameko_flask分支,并且查看CICD pipeline


