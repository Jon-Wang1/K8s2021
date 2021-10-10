### 前期准备controller manager (不需要配置, 只是回顾)
```shell script
kube-controller-manager启动参数
  --allocate-node-cidrs=true \
  --cluster-cidr 172.16.0.0/16 \
```

### 前期的准备kubelet (不需要配置, 只是回顾)
```shell script
kubelet 启动参数
  --network-plugin=cni : 网络插件使用cni
```

----------------------------------注意此处切换设备--------------------------------------

### 下载并上传镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
# calico_only
docker pull quay.io/tigera/operator:v1.20.4
docker pull calico/ctl:v3.20.2
docker tag quay.io/tigera/operator:v1.20.4 harbor.qytanghost.com/public/calico_operator:v1.20.4
docker tag calico/ctl:v3.20.2 harbor.qytanghost.com/public/calico_ctl:v3.20.2
docker push harbor.qytanghost.com/public/calico_operator:v1.20.4
docker push harbor.qytanghost.com/public/calico_ctl:v3.20.2

```

----------------------------------注意此处切换设备--------------------------------------

### NGINX配置 (mgmtcentos)
```shell script
yum install -y nginx

systemctl start nginx
systemctl enable nginx

cat > /etc/nginx/conf.d/mgmtcentos.qytanghost.com.conf <<'EOF'

server {
        listen          80;
        server_name     mgmtcentos.qytanghost.com;

        location / {
                autoindex       on;
                default_type    text/plain;
                root            /K8S2021/yaml_dockerfile/k8s-yaml;
        }
}
EOF
nginx -s reload

```

----------------------------------注意此处切换设备--------------------------------------

### mgmtwin7上传整个项目到mgmtcentos

### mgmtwin7测试是否可以打开http://mgmtcentos.qytanghost.com/

----------------------------------注意此处切换设备--------------------------------------
### 应用资源配置清单,安装calico(任何一个Master)
### https://docs.projectcalico.org/getting-started/kubernetes/quickstart
```shell script
kubectl create -f http://mgmtcentos.qytanghost.com/calico/tigera-operator.yaml
kubectl create -f http://mgmtcentos.qytanghost.com/calico/custom-resources.yaml

```

### 应用资源配置清单,安装calicoctl(任何一个Master)
# https://docs.projectcalico.org/getting-started/clis/calicoctl/install
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/calico/calicoctl.yaml

```

### 等待3-5分钟，查看命名空间(任何一个Master)
[root@master01 ~]# kubectl get ns
NAME               STATUS   AGE
calico-apiserver   Active   7m36s
calico-system      Active   9m51s
default            Active   164m
kube-node-lease    Active   164m
kube-public        Active   164m
kube-system        Active   164m
tigera-operator    Active   10m


### 查看命名空间tigera-operator的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n tigera-operator
NAME                               READY   STATUS    RESTARTS   AGE
tigera-operator-59f4845b57-knzgz   1/1     Running   1          10m


### 查看命名空间calico-system的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n calico-system
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-5dc68f7985-tkxp6   1/1     Running   0          10m
calico-node-5dwzm                          1/1     Running   0          10m
calico-node-v9xxh                          1/1     Running   0          10m
calico-node-z5975                          1/1     Running   0          10m
calico-typha-658c5d57d-bxqkz               1/1     Running   0          10m
calico-typha-658c5d57d-fqbnh               1/1     Running   0          10m
calico-typha-658c5d57d-xvgkh               1/1     Running   0          10m

### 查看命名空间calico-apiserver的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n calico-apiserver
NAME                                READY   STATUS    RESTARTS   AGE
calico-apiserver-6bb8d7579f-dc8s7   1/1     Running   0          8m11s


### 查看位于kube-system中的calicoctl(任何一个Master)
[root@master01 ~]# kubectl get pod -n kube-system
NAME        READY   STATUS    RESTARTS   AGE
calicoctl   1/1     Running   0          4m34s


## 如果希望预留地址(推荐)(任何一个Master)

### 给node打标签(任何一个Master)
```shell
kubectl label nodes node01.qytanghost.com rack=1
kubectl label nodes node02.qytanghost.com rack=2
kubectl label nodes node03.qytanghost.com rack=3

```

# 授权etcd-client kubelet-api-admin （etcd-client这个证书，用来和apiserver通信写入apiserver数据库）(任何一个Master)
```shell
kubectl create clusterrolebinding kube-apiserver:kubelet-apis --clusterrole=system:kubelet-api-admin --user etcd-client

```

# 查看地址池(任何一个Master)
```shell
kubectl exec -it calicoctl -n kube-system -- calicoctl get ippool -o wide

```
# 删除默认的地址池(任何一个Master)
```shell
kubectl exec -it calicoctl -n kube-system -- calicoctl delete ippools default-ipv4-ippool

```

# 下载资源配置清单(任何一个Master)
```shell
wget http://mgmtcentos.qytanghost.com/calico/node01.yaml
wget http://mgmtcentos.qytanghost.com/calico/node02.yaml
wget http://mgmtcentos.qytanghost.com/calico/node03.yaml

```
# 应用资源配置清单(任何一个Master)
```shell
kubectl exec -it calicoctl -n kube-system -- calicoctl create -f - < node01.yaml
kubectl exec -it calicoctl -n kube-system -- calicoctl create -f - < node02.yaml
kubectl exec -it calicoctl -n kube-system -- calicoctl create -f - < node03.yaml

```

# 查看地址池(任何一个Master)
[root@master01 ~]# kubectl exec -it calicoctl -n kube-system -- calicoctl get ippool -o wide
NAME            CIDR              NAT    IPIPMODE   VXLANMODE   DISABLED   SELECTOR
rack-1-ippool   172.16.201.0/24   true   Never      Always      false      rack == "1"
rack-2-ippool   172.16.202.0/24   true   Never      Always      false      rack == "2"
rack-3-ippool   172.16.203.0/24   true   Never      Always      false      rack == "3"
