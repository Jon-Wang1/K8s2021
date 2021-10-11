### 安装metric-server[由于API server没有安装网络,无法和metric server通讯所以无需安装]
https://github.com/kubernetes-sigs/metrics-server
# 官方资源配置文件
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.5.1/components.yaml

```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/dashboard_v2/metrics-server.yaml

```

### 下载并推送镜像到私有仓库 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull kubernetesui/dashboard:v2.3.1
docker tag kubernetesui/dashboard:v2.3.1 harbor.qytanghost.com/public/dashboard:v2.3.1
docker push harbor.qytanghost.com/public/dashboard:v2.3.1

# 由于没有安装metrics-server所以metrics-scraper就没有意义了
#docker pull kubernetesui/metrics-scraper:v1.0.6
#docker tag kubernetesui/metrics-scraper:v1.0.6 harbor.qytanghost.com/public/metrics-scraper:v1.0.6
#docker push harbor.qytanghost.com/public/metrics-scraper:v1.0.6

```

### 官方资源配置清单
https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/dashboard_v2/recommended.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/dashboard_v2/ingress.yaml

```

### 查看deployment和pod状态 (任何一个Master)
[root@master01 ~]# kubectl get deploy -n kubernetes-dashboard
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
dashboard-metrics-scraper   1/1     1            1           2m50s
kubernetes-dashboard        1/1     1            1           2m51s

[root@master01 ~]# kubectl get pod -n kubernetes-dashboard
NAME                                         READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-79c5968bdc-8xhxc   1/1     Running   0          3m26s
kubernetes-dashboard-658485d5c7-47d68        1/1     Running   0          3m27s

### 获取Dashboard Admin Token (任何一个Master)
[root@master01 ~]# kubectl get secret -n kubernetes-dashboard
NAME                               TYPE                                  DATA   AGE
dashboard-admin-token-f8txk        kubernetes.io/service-account-token   3      18s
default-token-tq8zt                kubernetes.io/service-account-token   3      12m
kubernetes-dashboard-certs         Opaque                                0      12m
kubernetes-dashboard-csrf          Opaque                                1      12m
kubernetes-dashboard-key-holder    Opaque                                2      12m
kubernetes-dashboard-token-9djr7   kubernetes.io/service-account-token   3      12m

[root@master01 ~]# kubectl describe secret dashboard-admin-token-f8txk -n kubernetes-dashboard
Name:         dashboard-admin-token-f8txk
Namespace:    kubernetes-dashboard
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-admin
              kubernetes.io/service-account.uid: 60e6b3eb-be49-4833-a3ec-9c236beb3a33

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     2000 bytes
namespace:  20 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IksyM0tpU1F1ZUZIMUQ2NU8wbzRGSEgxZk5xTzh6b2ZPQTJYNzhSNkh6SVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tZjh0eGsiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNjBlNmIzZWItYmU0OS00ODMzLWEzZWMtOWMyMzZiZWIzYTMzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmVybmV0ZXMtZGFzaGJvYXJkOmRhc2hib2FyZC1hZG1pbiJ9.Dz9WEtUN0Zj5iapz7cK9VZCj60QSy5wFltyrpgXsFfer3ljj0U7Lv-q3FGE6-D8UCjlTfX5ER9eenGEdt_5ftH-mZIZfvbCxoFfvRQI6cDxeCDHeCHASJRB66l2NyX2w89Av-63-QOf5S46Alhmwq6odfVFrbdvIFrceUWBmvHNwpOsyxNSPM-_EUYppkvnMxADfyeMjxBzNlPYuj0ZEr7HBikYM5trH3mHJL0GfPLNipVwc1ZlgPrxilgSKFyXsJtssXY9RLS3vpHxqPpiGEm5mA_9U8my97hk3TSAegHfena-KsGLUudPO-7lYwdFsUXHIn89zD85JDI_bLkzXPw

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
metricsserver                A   10.1.1.10
EOF

systemctl restart named

```
----------------------------------注意此处切换设备--------------------------------------

### 登录Dashboard测试 (mgmtwin7)
#### 推荐使用无痕模式
https://k8sdashboard.qytangk8s.com/