### 创建secret(kubectl) (任何一个Master)
kubectl create secret generic qytang-secret-kubectl --from-literal='username=admin' \
                                                    --from-literal='password=Cisc0123'
kubectl create secret docker-registry harbor-kubectl --docker-server=harbor.qytanghost.com \
                                                     --docker-username=admin \
                                                     --docker-password=Cisc0123

### 创建secret(yaml) (任何一个Master)
kubectl apply -f http://mgmtcentos.qytanghost.com/secret/create_normal_secret.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/secret/create_registrypullsecret.yaml

### 查看secret (任何一个Master)
[root@master01 ~]# kubectl get secrets
NAME                    TYPE                                  DATA   AGE
default-token-ftl5f     kubernetes.io/service-account-token   3      2d15h
harbor-kubectl          kubernetes.io/dockerconfigjson        1      4m44s
harbor-yaml             kubernetes.io/dockerconfigjson        1      21s
qytang-secret-kubectl   Opaque                                2      4m44s
qytang-secret-yaml      Opaque                                2      24s


### harbor上创建名字叫做"private"的私有仓库 (Harbor)

### 修改nginx_curl的tag,并上传到private仓库  (mgmtcentos)
```shell script
docker tag harbor.qytanghost.com/public/nginx_curl harbor.qytanghost.com/private/nginx_curl
docker push harbor.qytanghost.com/private/nginx_curl
```

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/secret/secret-kubectl-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/secret/secret-yaml-dp.yaml
```

### 查看pod (任何一个Master)
[root@master01 ~]# kubectl get pod
NAME                                         READY   STATUS    RESTARTS   AGE
secret-kubectl-7cb774ddc6-9nfzq              1/1     Running   0          8s
secret-yaml-6555bd96f4-9645d                 1/1     Running   0          7s

### 进入容器查看secret (任何一个Master)
[root@master01 ~]# kubectl exec -it secret-kubectl-7cb774ddc6-9nfzq -- /bin/bash
[root@secret-kubectl-7cb774ddc6-9nfzq /]# cat /etc/secret-volume/username
admin
[root@secret-kubectl-7cb774ddc6-9nfzq /]# cat /etc/secret-volume/password
Cisc0123