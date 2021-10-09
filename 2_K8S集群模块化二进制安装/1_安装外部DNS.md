### 安装DNS (dnsca)
```shell script
yum install -y bind
```

### named配置文件(dnsca)
```shell script
cat >/etc/named.conf <<'EOF'
options {
        listen-on port 53 { 10.1.1.219; }; # 修改
        # listen-on-v6 port 53 { ::1; }; # 注释掉
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { any; }; # 修改
        forwarders      { 114.114.114.114; }; # 修改

        /*
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable
           recursion.
         - If your recursive DNS server has a public IP address, you MUST enable access
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface
        */
        recursion yes;

        dnssec-enable no; # 修改
        dnssec-validation no; # 修改
        managed-keys-directory "/var/named/dynamic";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
EOF
```

### 检查配置(dnsca)
```shell script
named-checkconf
```

### 配置zone文件(定义两个解析域)(dnsca)
```shell script
cat >/etc/named.rfc1912.zones <<'EOF'
zone "qytanghost.com" IN {
        type    master;
        file    "qytanghost.com.zone";
        allow-update    { 10.1.1.219; };
};

zone "qytangk8s.com" IN {
        type    master;
        file    "qytangk8s.com.zone";
        allow-update    { 10.1.1.219; };
};
EOF
```

### host域 zone配置文件(dnsca)
```shell script
cat > /var/named/qytanghost.com.zone <<'EOF'
$ORIGIN qytanghost.com.
$TTL 600    ;   10 minutes
@       IN SOA  dnsca.qytanghost.com. dnsadmin.qytanghost.com. (
                                        2020090901      ; serial
                                        10800           ; refresh (3 hours)
                                        900             ; retry (15 minutes)
                                        604800          ; expire (1 week)
                                        86400           ; minimum (1 day)
                                        )
        NS      dnsca.qytanghost.com.
$TTL 60    ;   1 minute
dnsca                       A   10.1.1.219
master01                    A   10.1.1.101
master02                    A   10.1.1.102
master03                    A   10.1.1.103
node01                      A   10.1.1.201
node02                      A   10.1.1.202
node03                      A   10.1.1.203
harbor                      A   10.1.1.220
nginx01                     A   10.1.1.11
nginx02                     A   10.1.1.12
gitlab                      A   10.1.1.230
kubernetes                  A   10.1.1.10
EOF
```

### qytang域 zone配置文件(dnsca)
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
EOF
```

### 再次check配置(dnsca)
```shell script
named-checkconf
```

### 启动服务(dnsca)
```shell script
systemctl start named
systemctl enable named
```

### 查看服务(dnsca)
```shell script
netstat -luntp | grep 53
```

### 修改网卡， 指向DNS (所有主机)
```shell script
vim /etc/sysconfig/network-scripts/ifcfg-ens192

DNS1=10.1.1.219
DOMAIN=qytanghost.com
```

###设置主机名
```shell
hostnamectl set-hostname xxx.qytanghost.com
```