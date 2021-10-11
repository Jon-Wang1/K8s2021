### 确认dnsca.qytanghost.com的ssh秘钥(mgmtcentos)[应该之前就处理过]
[root@mgmtcentos certs]# ssh root@dnsca.qytanghost.com
The authenticity of host 'dnsca.qytanghost.com (10.1.1.219)' can't be established.
ECDSA key fingerprint is SHA256:jWlSzcu5QdgKgh19Haz/pXf4AfIwbt9cfzDERxuzwCs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'dnsca.qytanghost.com,10.1.1.219' (ECDSA) to the list of known hosts.
root@dnsca.qytanghost.com's password:
Last login: Fri Oct  8 13:01:50 2021 from 10.1.1.50
[root@harbor ~]# exit [一定要退出]
logout


### 下载根证书(mgmtcentos)[应该之前就处理过]
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
# mgmtcentos docker login(mgmtcentos)[应该之前就处理过]
# 如果出现证书问题，建议重启尝试
[root@mgmtcentos ~]# docker login harbor.qytanghost.com
Username: admin
Password: Cisc0123
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded


# 自作nginx-curl镜像, 并推送到私有仓库 (mgmtcentos)
```shell script
cd /K8S2021/yaml_dockerfile/dockerfile/qyt_lb/

docker build -t harbor.qytanghost.com/public/qyt_lb .

docker push harbor.qytanghost.com/public/qyt_lb 

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/qyt-lb-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/qyt-lb-ds.yaml

```

### 查看状况 (任何一个Master)
[root@master01 ~]# kubectl get deploy
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
qyt-lb-dp   1/1     1            1           84s

[root@master01 ~]# kubectl get deploy -o wide
NAME        READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS           IMAGES                                SELECTOR
qyt-lb-dp   1/1     1            1           101s   container-1-qyt-lb   harbor.qytanghost.com/public/qyt_lb   app=qyt-lb-dp-label

[root@master01 ~]# kubectl get daemonset
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
qyt-lb-ds   3         3         3       3            3           <none>          118s

[root@master01 ~]# kubectl get daemonset -o wide
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE     CONTAINERS           IMAGES                                SELECTOR
qyt-lb-ds   3         3         3       3            3           <none>          2m13s   container-1-qyt-lb   harbor.qytanghost.com/public/qyt_lb   app=qyt-lb-ds-label

[root@master01 ~]# kubectl get replicaset
NAME                   DESIRED   CURRENT   READY   AGE
qyt-lb-dp-7f677cd4cf   1         1         1       2m29s

[root@master01 ~]# kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
qyt-lb-dp-7f677cd4cf-bq6gg   1/1     Running   0          2m43s
qyt-lb-ds-rlxq2              1/1     Running   0          2m42s
qyt-lb-ds-tz9pm              1/1     Running   0          2m42s
qyt-lb-ds-zmpls              1/1     Running   0          2m42s

[root@master01 ~]# kubectl get pod -o wide
NAME                         READY   STATUS    RESTARTS   AGE     IP             NODE                    NOMINATED NODE   READINESS GATES
qyt-lb-dp-7f677cd4cf-bq6gg   1/1     Running   0          2m56s   172.16.203.1   node03.qytanghost.com   <none>           <none>
qyt-lb-ds-rlxq2              1/1     Running   0          2m55s   172.16.203.2   node03.qytanghost.com   <none>           <none>
qyt-lb-ds-tz9pm              1/1     Running   0          2m55s   172.16.202.1   node02.qytanghost.com   <none>           <none>
qyt-lb-ds-zmpls              1/1     Running   0          2m55s   172.16.201.1   node01.qytanghost.com   <none>           <none>
