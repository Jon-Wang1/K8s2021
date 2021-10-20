### 应用添加注释的rabbitmq与nginx (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/nameko/k8s2021-nginx-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/nameko/k8s2021-rabbitmq-dp.yaml

```

### K8S2021_nameko_devops的nameko_flask分支, 已经做好的注释 (Gitlab)

### 修改kubelet.sh (每一个计算节点)
```shell script
vim /opt/kubernetes/node/bin/kubelet.sh 

添加
 --authentication-token-webhook=true \
 --authorization-mode=AlwaysAllow \

supervisorctl update
supervisorctl restart kube-kubelet

```

### 配置coredns (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/coredns/k8s2021-coredns-cm.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/coredns/k8s2021-coredns-dp.yaml

```

### 配置traefik (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/traefik/k8s2021-traefik-dp.yaml

```