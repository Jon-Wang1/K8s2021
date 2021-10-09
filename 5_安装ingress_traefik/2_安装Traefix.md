### 配置DNS (DNSCA)
```shell script
cat > /var/named/qytang.com.zone <<'EOF'
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

EOF

systemctl restart named
```

### 应用资源配置清单
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/crd.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/traefik/dashboard.yaml

kubectl delete -f http://mgmtcentos.qytanghost.com/traefik/dashboard.yaml
kubectl delete -f http://mgmtcentos.qytanghost.com/traefik/dp.yaml
kubectl delete -f http://mgmtcentos.qytanghost.com/traefik/rbac.yaml
kubectl delete -f http://mgmtcentos.qytanghost.com/traefik/crd.yaml
```

### 参考文档
https://www.qikqiak.com/post/traefik-2.1-101/


### 应用资源配置清单
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/ingress-dp.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/ingress-ds.yaml
```