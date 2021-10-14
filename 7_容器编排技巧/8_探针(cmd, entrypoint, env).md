### 制作镜像, 并上传到harbor (mgmgcentos)
```shell script
cd /K8S2021/yaml_dockerfile/dockerfile/probes_cmd
docker build -t harbor.qytanghost.com/public/probes:cmd .
docker push harbor.qytanghost.com/public/probes:cmd

cd /K8S2021/yaml_dockerfile/dockerfile/probes_entrypoint/
docker build -t harbor.qytanghost.com/public/probes:entrypoint .
docker push harbor.qytanghost.com/public/probes:entrypoint

cd /K8S2021/yaml_dockerfile/dockerfile/probes_env/
docker build -t harbor.qytanghost.com/public/probes:env .
docker push harbor.qytanghost.com/public/probes:env

```

### 应用资源配置清单 (任何一个Master) [三种传参数方案, 此处只是展示,并不要应用]
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/probes/nginx-curl-probes-cmd.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/probes/nginx-curl-probes-entrypoint.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/probes/nginx-curl-probes-env.yaml

```

### 测试
### 需要提前开三个窗口
#### (窗口1)master01
#### (窗口2)master02
#### (窗口3)node01

--------------------时间点:1--------------------
### (窗口1)master01
#### 应用资源配置清单
```shell
kubectl apply -f http://mgmtcentos.qytanghost.com/probes/nginx-curl-probes-cmd.yaml
```

#### 进入容器nginx-curl-probes-cmd
```shell
kubectl exec -it $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}') -- bash
```

#### 在容器nginx-curl-probes-cmd内, curl测试, 出现故障
```shell
curl 127.0.0.1:8000/startup
```

#### 下面是返回结果
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### (窗口2)master02
#### 查看pod nginx-curl-probes-cmd, 状态并没有ready
```shell
kubectl get pod $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}')
```
#### 下面是输出结果
NAME                                     READY   STATUS    RESTARTS   AGE
nginx-curl-probes-cmd-5bcb7565f6-stbts   0/1     Running   0          30s

#### describe pod了解详情, 发现是startup probe failed
```shell
kubectl describe pod $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}')
```

#### 下面是输出结果
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Warning  Unhealthy  2s (x12 over 35s)  kubelet            Startup probe failed: Get "http://172.16.203.57:8000/startup": context deadline exceeded (Client.Timeout exceede

### (窗口3)Node01
#### 在Node01上测试, 由于并没有startup, 所以流量并没有被导入
```shell
 curl 192.168.68.68:8000/ready
```

#### 下面是返回结果
curl: (7) Failed to connect to 192.168.68.68 port 8000: Connection refused

--------------------时间点:2--------------------
### (窗口1)master01 
#### 容器内测试startup已经正常
[root@nginx-curl-probes-cmd-678bb67789-lrglq qytang]# curl 127.0.0.1:8000/startup
qytang startup 60

### (窗口2)master02 
#### pod已经running与ready
```shell
kubectl get pod $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}')
```

#### 下面是输出结果
NAME                                     READY   STATUS    RESTARTS   AGE
nginx-curl-probes-cmd-5bcb7565f6-stbts   1/1     Running   0          98s

### (窗口3)Node01
#### Node01测试流量已经被正常导入, ready有响应
```shell
curl 192.168.68.68:8000/ready
```

#### 返回结果
qytang ready

#### Node01测试流量已经被正常导入, live有响应
```shell
curl 192.168.68.68:8000/live
```

#### 返回结果
qytang live

--------------------时间点:3--------------------
### (窗口1)Master01
### 容器内测试,ready已经出现故障
```shell
curl 127.0.0.1:8000/ready
```

#### 出现如下报错
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

#### 容器内测试,live依然正常
```shell
curl 127.0.0.1:8000/live
```

#### 下面是返回结果
qytang live

### (窗口2)Master02
#### 查看pod虽然running, 但是并没有ready
```shell
kubectl get pod $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}')
```

#### 下面是输出结果
NAME                                     READY   STATUS    RESTARTS   AGE
nginx-curl-probes-cmd-5bcb7565f6-stbts   0/1     Running   0          2m31s

#### describe pod有Readiness probe failed 故障
```shell
kubectl describe pod $(kubectl get pod -l "app=nginx-curl-probes-cmd" -o jsonpath='{.items[0].metadata.name}')
```

#### 下面是重点的输出结果
  ----     ------     ----                    ----               -------
  Warning  Unhealthy  97s (x20 over 2m34s)  kubelet            Startup probe failed: Get "http://172.16.203.57:8000/startup": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
  Warning  Unhealthy  30s                   kubelet            Readiness probe failed: HTTP probe failed with statuscode: 404

### (窗口3)Node01
#### 流量不再被导入,测试ready失败
```shell
curl 192.168.68.68:8000/ready
```

### 返回结果
curl: (7) Failed to connect to 192.168.68.68 port 8000: Connection refused

#### 流量不再被导入,测试live失败
```shell
curl 192.168.68.68:8000/live
```

#### 返回结果
curl: (7) Failed to connect to 192.168.68.68 port 8000: Connection refused

--------------------时间点:4--------------------
### (窗口1)Master01
### Master01容器内测试, 当live出现故障后(有接近10几秒的时间), pod重启
[root@nginx-curl-probes-cmd-678bb67789-lrglq qytang]# curl 127.0.0.1:8000/live
qytang live
[root@nginx-curl-probes-cmd-678bb67789-lrglq qytang]# curl 127.0.0.1:8000/live
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
[root@nginx-curl-probes-cmd-678bb67789-lrglq qytang]# curl 127.0.0.1:8000/live
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

#### 此时容器被重启
[root@nginx-curl-probes-cmd-678bb67789-lrglq qytang]# command terminated with exit code 137
