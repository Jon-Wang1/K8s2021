### 下载并创建configmap (任何一个Master)
```shell script
wget http://mgmtcentos.qytanghost.com/configmap/nginx.conf
kubectl create configmap qytang-configmap-nginx-conf --from-file=nginx.conf
wget http://mgmtcentos.qytanghost.com/configmap/index.html
kubectl create configmap qytang-configmap-nginx-html --from-file=index.html
```

### 查看cm (任何一个Master)
[root@master01 ~]# kubectl describe cm qytang-configmap-nginx-conf
Name:         qytang-configmap-nginx-conf
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
nginx.conf:
----
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /qytang_nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            # try_files $uri $uri/index.html index.html;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
}
Events:  <none>

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/configmap/nginx-curl-configmap-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/configmap/svc-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/configmap/ingress-dp.yaml
```

### 查看pod (任何一个Master)
[root@master01 ~]# kubectl get pod -o wide
NAME                                         READY   STATUS    RESTARTS   AGE     IP              NODE                    NOMINATED NODE   READINESS GATES
nginx-curl-configmap-5dcfb6dd5d-qdtx6        1/1     Running   0          2m3s

### http测试 注意:查看具体的Node (mgmtwin7)
```shell script
http://node01.qytanghost.com:6888/

https://nginx-configmap.qytangk8s.com/
```

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
nginx-configmap              A   10.1.1.10
EOF

systemctl restart named

```

### 修改ConfigMap
#### 方案一
kubectl delete configmap qytang-configmap-nginx-html
wget http://mgmtcentos.qytanghost.com/configmap/index.html
kubectl create configmap qytang-configmap-nginx-html --from-file=index.html

#### 方案二
kubectl edit cm qytang-configmap-nginx-html

#### 方案三
kubectl create configmap qytang-configmap-nginx-html --from-file index.html -o yaml --dry-run=client | kubectl apply -f -

#### 方案四
使用Dashboard修改
