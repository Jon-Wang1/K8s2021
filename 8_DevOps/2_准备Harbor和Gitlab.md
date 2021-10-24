###Harbor创建私有项目devops(详细截图看PPT) （Harbor图形界面）

----------------------------------注意此处切换设备--------------------------------------

###Gitlab创建私有项目Nameko_DevOps(详细截图看PPT) （Gitlab图形界面）

###复制项目Git地址(详细截图看PPT)（Gitlab图形界面）

----------------------------------注意此处切换设备--------------------------------------

###PyCharm定义Remote(详细截图看PPT) （mgmtwin7）

###PyCharm Push项目到Gitlab(详细截图看PPT) （mgmtwin7）

----------------------------------注意此处切换设备--------------------------------------

###Gitlab查看两个分支(详细截图看PPT) （Gitlab图形界面）

----------------------------------注意此处切换设备--------------------------------------

### 安装Runner (Gitlab)
```shell
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh" | sudo bash
yum install -y gitlab-ci-multi-runner

```

----------------------------------注意此处切换设备--------------------------------------

### 查看Runner注册URL与Token(详细截图看PPT) (Gitlab图形界面)

----------------------------------注意此处切换设备--------------------------------------

### 注册Gitlab Runner (Gitlab)
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

### 查看注册的Runner (详细截图看PPT) (Gitlab图形界面)

----------------------------------注意此处切换设备--------------------------------------

### 添加Runner到sudouser  (详细截图看PPT) (Gitlab)
[root@gitlab ~]# visudo
```shell
## Allow root to run any commands anywhere
root    ALL=(ALL)       ALL
gitlab-runner   ALL=(ALL:ALL) NOPASSWD:ALL  # 添加内容
```

----------------------------------注意此处切换设备--------------------------------------

### 创建登录harbor的secret (任何一个Master)
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/nameko_harbor_secret/harbor_secret.yaml

```

----------------------------------注意此处切换设备--------------------------------------

###拷贝kubeconfig到Gitlab
#### Gitlab创建目录 (Gitlab)
[root@gitlab ~]# mkdir /etc/deploy

----------------------------------注意此处切换设备--------------------------------------

#### Mastor01 拷贝kubeconfig到gitlab (Master01)
[root@master01 ~]# scp /root/.kube/config root@gitlab.qytanghost.com:/etc/deploy/config

----------------------------------注意此处切换设备--------------------------------------

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
----------------------------------注意此处切换设备--------------------------------------

### 设置Gitlab 环境变量 (详细截图看PPT)（Gitlab图形界面）
REGISTRY_PASSWORD	:	 Cisc0123 	
REGISTRY_USERNAME	:	 admin

### 启动 nameko_microservice分支的Pipeline,并且查看CICD pipeline （Gitlab图形界面）

----------------------------------注意此处切换设备--------------------------------------

### 查看nameko_microservice pod （任何一个Master）
[root@master01 ~]# kubectl get pod -l "app=nameko-microservice" -n devops
NAME                                   READY   STATUS    RESTARTS   AGE
nameko-microservice-7486c445fb-mwpgz   1/1     Running   0          2m32s

----------------------------------注意此处切换设备--------------------------------------

### 启动 nameko_flask分支的Pipeline,并且查看CICD pipeline（Gitlab图形界面）

----------------------------------注意此处切换设备--------------------------------------

### 查看nameko_flask pod （任何一个Master）
[root@master01 ~]# kubectl get pod -l "app=nameko-app" -n devops
NAME                          READY   STATUS    RESTARTS   AGE
nameko-app-75b56f5588-p69pq   1/1     Running   0          4m39s

