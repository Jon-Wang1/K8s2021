### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull gcr.io/cadvisor/cadvisor:v0.42.0
docker tag gcr.io/cadvisor/cadvisor:v0.42.0 harbor.qytanghost.com/monitoring/cadvisor:v0.42.0
docker push harbor.qytanghost.com/monitoring/cadvisor:v0.42.0

```

----------------------------------注意此处切换设备--------------------------------------

###应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/cadvisor/cadvisor-ds.yaml

```

###查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -n monitoring -o wide
NAME                                 READY   STATUS    RESTARTS   AGE   IP               NODE                    NOMINATED NODE   READINESS GATES
cadvisor-ncvp9                       1/1     Running   0          19s   172.16.201.148   node01.qytanghost.com   <none>           <none>
cadvisor-vzfp4                       0/1     Running   0          19s   172.16.203.143   node03.qytanghost.com   <none>           <none>
cadvisor-zzsfn                       0/1     Running   0          19s   172.16.202.98    node02.qytanghost.com   <none>           <none>
kube-state-metrics-598c57868-qbp87   1/1     Running   0          21m   172.16.201.144   node01.qytanghost.com   <none>           <none>
node-exporter-84ccs                  1/1     Running   0          12m   172.16.201.145   node01.qytanghost.com   <none>           <none>
node-exporter-pgvfq                  1/1     Running   0          12m   172.16.202.97    node02.qytanghost.com   <none>           <none>
node-exporter-ww8pd                  1/1     Running   0          12m   172.16.203.142   node03.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

###查看端口与测试(任何一个计算节点)

[root@node01 ~]# curl 172.16.201.148:4194/healthz
ok

[root@node01 ~]# curl 172.16.201.148:4194/metrics

---忽略大量输出---