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