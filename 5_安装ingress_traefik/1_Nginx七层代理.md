### 签发证书 (dnsca)
```shell script
cd /opt/certs/
cat >/opt/certs/nginx-csr.json <<EOF
{
    "CN": "*.qytangk8s.com",
    "hosts": [
    "*.qytanghost.com",
    "*.qytangk8s.com"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "beijing",
            "L": "beijing",
            "O": "qytang",
            "OU": "qytangk8s"
        }
    ]
}
EOF


cfssl gencert \
      -ca=ca.pem \
      -ca-key=ca-key.pem \
      -config=ca-config.json \
      -profile=server \
      nginx-csr.json | cfssl-json -bare nginx

```
----------------------------------注意此处切换设备--------------------------------------

### 安装sshpass,并确认秘钥 (Nginx01, Nginx02)
```shell
yum install -y epel-release
yum install -y sshpass
```

### 确认dnsca.qytanghost.com的秘钥 (Nginx01, Nginx02)
[root@nginx02 ~]# ssh root@dnsca.qytanghost.com
The authenticity of host 'dnsca.qytanghost.com (10.1.1.219)' can't be established.
ECDSA key fingerprint is SHA256:jWlSzcu5QdgKgh19Haz/pXf4AfIwbt9cfzDERxuzwCs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'dnsca.qytanghost.com,10.1.1.219' (ECDSA) to the list of known hosts.
root@dnsca.qytanghost.com's password:
Last login: Sun Oct 10 16:31:59 2021 from 10.1.1.60
[root@dnsca ~]# exit [一定要退出]
logout
Connection to dnsca.qytanghost.com closed.
[root@nginx02 ~]#



### Nginx下载证书(Nginx01, Nginx02)
```shell
mkdir /etc/nginx/certs
cd /etc/nginx/certs
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/ca.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/nginx.pem .
sshpass -p "Cisc0123" scp dnsca.qytanghost.com:/opt/certs/nginx-key.pem .

```

### 配置NGINX nginx.conf(Nginx01, Nginx02)
```shell script
cat > /etc/nginx/nginx.conf <<'EOF'
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
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

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers PROFILE=SYSTEM;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}


stream {
    upstream kube-apiserver {
        server 10.1.1.101:6443     max_fails=3 fail_timeout=30s;
        server 10.1.1.102:6443     max_fails=3 fail_timeout=30s;
        server 10.1.1.103:6443     max_fails=3 fail_timeout=30s;
    }
    server {
        listen 6443;
        proxy_connect_timeout 2s;
        proxy_timeout 900s;
        proxy_pass kube-apiserver;
    }
}
EOF

```

### 配置NGINX qytang.com.conf(Nginx01, Nginx02)
```shell script
cat > /etc/nginx/conf.d/qytang.com.conf <<'EOF'
upstream default_backend_traefik {
    server 10.1.1.201:6868    max_fails=3 fail_timeout=10s;
    server 10.1.1.202:6868    max_fails=3 fail_timeout=10s;
    server 10.1.1.203:6868    max_fails=3 fail_timeout=10s;
}
server {
    listen      80;
    server_name *.qytangk8s.com;

    location / {
        proxy_pass http://default_backend_traefik;
        proxy_set_header Host       $http_host;
        proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
    }
}
server {
    listen       443 ssl;
    server_name  *.qytangk8s.com;

    ssl_certificate     "certs/nginx.pem";
    ssl_certificate_key "certs/nginx-key.pem";
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  10m;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://default_backend_traefik;
        proxy_set_header Host       $http_host;
        proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
    }
}
EOF

```

### 重启nginx服务
```shell
nginx -s reload
systemctl restart nginx

```