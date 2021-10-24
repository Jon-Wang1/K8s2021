### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull gcr.io/cadvisor/cadvisor:v0.42.0
docker tag gcr.io/cadvisor/cadvisor:v0.42.0 harbor.qytanghost.com/monitoring/cadvisor:v0.42.0
docker push harbor.qytanghost.com/monitoring/cadvisor:v0.42.0

```

----------------------------------注意此处切换设备--------------------------------------

###应用资源配置清单(任何一个Master) [由于kubelet内置所有可以不用部署]
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/cadvisor/cadvisor-ds.yaml

```

###查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -l "app.kubernetes.io/name=cadvisor" -n monitoring -o wide
NAME             READY   STATUS    RESTARTS   AGE   IP              NODE                    NOMINATED NODE   READINESS GATES
cadvisor-7kwnt   1/1     Running   0          45s   172.16.201.66   node01.qytanghost.com   <none>           <none>
cadvisor-nltwd   1/1     Running   0          45s   172.16.202.21   node02.qytanghost.com   <none>           <none>
cadvisor-vrjts   1/1     Running   0          45s   172.16.203.67   node03.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

###查看端口与测试(任何一个计算节点)

[root@node01 ~]# curl 172.16.203.67:4194/healthz
ok

[root@node01 ~]# curl 172.16.203.67:4194/metrics

---忽略大量输出---