### 下载镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull prom/node-exporter:v1.2.2
docker tag prom/node-exporter:v1.2.2 harbor.qytanghost.com/monitoring/node-exporter:v1.2.2
docker push harbor.qytanghost.com/monitoring/node-exporter:v1.2.2

```

----------------------------------注意此处切换设备--------------------------------------

###应用资源配置清单(任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/prometheus/node-exporter/node-exporter-ds.yaml

```

### 查看pod状况(任何一个Master)
[root@master01 ~]# kubectl get pod -n monitoring
NAME                                 READY   STATUS    RESTARTS   AGE
kube-state-metrics-598c57868-qbp87   1/1     Running   0          9m51s
node-exporter-84ccs                  1/1     Running   0          24s
node-exporter-pgvfq                  1/1     Running   0          24s
node-exporter-ww8pd                  1/1     Running   0          24s

[root@master01 ~]# kubectl get pod -n monitoring -o wide
NAME                                 READY   STATUS    RESTARTS   AGE   IP               NODE                    NOMINATED NODE   READINESS GATES
kube-state-metrics-598c57868-qbp87   1/1     Running   0          10m   172.16.201.144   node01.qytanghost.com   <none>           <none>
node-exporter-84ccs                  1/1     Running   0          33s   172.16.201.145   node01.qytanghost.com   <none>           <none>
node-exporter-pgvfq                  1/1     Running   0          33s   172.16.202.97    node02.qytanghost.com   <none>           <none>
node-exporter-ww8pd                  1/1     Running   0          33s   172.16.203.142   node03.qytanghost.com   <none>           <none>

----------------------------------注意此处切换设备--------------------------------------

###查看端口与测试(任何一个计算节点)
[root@node01 ~]# curl 172.16.201.145:9100
<html>
                        <head><title>Node Exporter</title></head>
                        <body>
                        <h1>Node Exporter</h1>
                        <p><a href="/metrics">Metrics</a></p>
                        </body>
                        </html>


[root@node01 ~]# curl 172.16.201.145:9100/metrics

---忽略大量输出---