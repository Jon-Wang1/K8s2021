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
[root@master01 ~]# kubectl get pod -l "app.kubernetes.io/name=node-exporter" -n monitoring -o wide
NAME                  READY   STATUS    RESTARTS   AGE   IP              NODE                    NOMINATED NODE   READINESS GATES
node-exporter-27wdq   1/1     Running   0          57s   172.16.203.66   node03.qytanghost.com   <none>           <none>
node-exporter-gslc9   1/1     Running   0          57s   172.16.202.20   node02.qytanghost.com   <none>           <none>
node-exporter-h5qj6   1/1     Running   0          57s   172.16.201.65   node01.qytanghost.com   <none>           <none>

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