### 下载并推送镜像到私有仓库 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull kubernetesui/dashboard:v2.3.1
docker tag kubernetesui/dashboard:v2.3.1 harbor.qytanghost.com/public/dashboard:v2.3.1
docker push harbor.qytanghost.com/public/dashboard:v2.3.1

```

### 官方资源配置清单
https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/dashboard_v2/recommended.yaml
```

### 查看deployment和pod状态 (任何一个Master)
[root@master01 ~]# kubectl get deploy -n kubernetes-dashboard
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-dashboard   1/1     1            1           33m

[root@master01 ~]# kubectl get pod -n kubernetes-dashboard
NAME                                    READY   STATUS    RESTARTS   AGE
kubernetes-dashboard-7774587476-2ljmr   1/1     Running   0          5m7s

### 获取Dashboard Admin Token (任何一个Master)
[root@master01 ~]# kubectl get secret -n kubernetes-dashboard
NAME                               TYPE                                  DATA   AGE
dashboard-admin-token-sb5hs        kubernetes.io/service-account-token   3      34m
default-token-rfdrp                kubernetes.io/service-account-token   3      34m
kubernetes-dashboard-certs         Opaque                                0      34m
kubernetes-dashboard-csrf          Opaque                                1      34m
kubernetes-dashboard-key-holder    Opaque                                2      34m
kubernetes-dashboard-token-wr4q4   kubernetes.io/service-account-token   3      34m

[root@master01 ~]# kubectl describe secret dashboard-admin-token-sb5hs -n kubernetes-dashboard
Name:         dashboard-admin-token-sb5hs
Namespace:    kubernetes-dashboard
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-admin
              kubernetes.io/service-account.uid: 134df2b1-c54f-4737-9c5d-19bf353b6110

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     2000 bytes
namespace:  20 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IksyM0tpU1F1ZUZIMUQ2NU8wbzRGSEgxZk5xTzh6b2ZPQTJYNzhSNkh6SVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tc2I1aHMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMTM0ZGYyYjEtYzU0Zi00NzM3LTljNWQtMTliZjM1M2I2MTEwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.fObEXVsNDCQlEyCt98Zv10mPDY_N64slTJgS6Fwn5IxZxgjY-Dp0PMB4qXxMfFKf5MbIM648_yWGQ0S17QFPRUx6Wf9HF2euaAp-STYaZvj0sAvdnZcjNpgcLsDzDKd3V0CY9lGUNo9iCZBc82EhD-lFw0QyUX7_v-4AHSeLbPhxH_IckmECqP-j1r4fQTEiR2DPspdRNPeUKXEs-cR0lCURZ6nSrgXIEtH5gUZJ29Ygi3aIZVuyPC7xuwUT5D-AH-x087n9lGorhL_sAoip-78AanU1aS_c3vwtNrNPEWRtvgZ2NXnIv7wGCmrvEXlcwOIH4bwk1gELisjDE6_TDA

----------------------------------注意此处切换设备--------------------------------------

### 配置DNS (DNSCA)
```shell script
cat > /var/named/qytangk8s.com.zone <<'EOF'
$ORIGIN qytangk8s.com.
$TTL 600    ;   10 minutes
@       IN SOA  dnsca.qytangk8s.com. dnsadmin.qytangk8s.com. (
                                        2020090901      ; serial
                                        10800           ; refresh (3 hours)
                                        900             ; retry (15 minutes)
                                        604800          ; expire (1 week)
                                        86400           ; minimum (1 day)
                                        )
        NS      dnsca.qytangk8s.com.
$TTL 60    ;   1 minute
dnsca                        A   10.1.1.219
traefik                      A   10.1.1.10
qyt-lb-ds                    A   10.1.1.10
qyt-lb-dp                    A   10.1.1.10
k8sdashboard                 A   10.1.1.10
EOF

systemctl restart named

```
----------------------------------注意此处切换设备--------------------------------------

### 登录Dashboard测试 (mgmtwin7)
#### 推荐使用无痕模式
https://k8sdashboard.qytangk8s.com/