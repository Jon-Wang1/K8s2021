### 安装NGINX （nginx01, nginx02)
```shell script
yum install -y nginx
```

### 配置文件 （nginx01, nginx02)
```shell script
cat >> /etc/nginx/nginx.conf <<'EOF'

stream {
    upstream kube-apiserver {
        server 10.1.1.101:6443     max_fails=3 fail_timeout=30s;
        server 10.1.1.102:6443     max_fails=3 fail_timeout=30s;
        server 10.1.1.103:6443     max_fails=3 fail_timeout=30s;
    }
    server {
        listen 7443;
        proxy_connect_timeout 2s;
        proxy_timeout 900s;
        proxy_pass kube-apiserver;
    }
}
EOF

systemctl start nginx
systemctl enable nginx
```

### 配置KEEPALIVE （nginx01, nginx02)
```shell script
yum install -y keepalived

cat >/etc/keepalived/check_port.sh <<'EOF'
#!/bin/bash
#keepalived 监控端口脚本
#使用方法：等待keepalived传入端口参数,检查改端口是否存在并返回结果
CHK_PORT=$1
if [ -n "$CHK_PORT" ];then
        PORT_PROCESS=`ss -lnt|grep $CHK_PORT|wc -l`
        if [ $PORT_PROCESS -eq 0 ];then
                echo "Port $CHK_PORT Is Not Used,End."
                exit 1
        fi
else
        echo "Check Port Cant Be Empty!"
fi
EOF

chmod +x /etc/keepalived/check_port.sh
```

### KEEPALIVE主 （nginx01)
```shell script
cat >/etc/keepalived/keepalived.conf <<'EOF'
! Configuration File for keepalived
global_defs {
   router_id 10.1.1.11
}
vrrp_script chk_nginx {
    script "/etc/keepalived/check_port.sh 7443"
    interval 2
    weight -20
}
vrrp_instance VI_1 {
    state MASTER
    interface ens192
    virtual_router_id 251
    priority 100
    advert_int 1
    mcast_src_ip 10.1.1.11
    nopreempt

    authentication {
        auth_type PASS
        auth_pass 11111111
    }
    track_script {
         chk_nginx
    }
    virtual_ipaddress {
        10.1.1.10
    }
}
EOF
```

### KEEPALIVE从 （nginx02)
```shell script
cat >/etc/keepalived/keepalived.conf <<'EOF'
! Configuration File for keepalived
global_defs {
   router_id 10.1.1.12
}
vrrp_script chk_nginx {
    script "/etc/keepalived/check_port.sh 7443"
    interval 2
    weight -20
}
vrrp_instance VI_1 {
    state BACKUP
    interface ens192
    virtual_router_id 251
    priority 100
    advert_int 1
    mcast_src_ip 10.1.1.12
    nopreempt

    authentication {
        auth_type PASS
        auth_pass 11111111
    }
    track_script {
         chk_nginx
    }
    virtual_ipaddress {
        10.1.1.10
    }
}
EOF

### 启动服务
```
systemctl start keepalived
systemctl enable keepalived
systemctl status keepalived
```