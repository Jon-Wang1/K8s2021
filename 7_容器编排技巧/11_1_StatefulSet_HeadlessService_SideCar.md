### 参考文档
#### 基础搭建
https://wiki.shileizcc.com/confluence/pages/viewpage.action?pageId=27000909

#### 无头Headless服务
https://zhuanlan.zhihu.com/p/54153164

#### RBAC权限控制
https://spex.top/archives/kubernetes-mongodb-cluster-mongo-k8s-sidecar.html

### 下载镜像到私有仓库 (mgmtcentos)
```shell script
docker pull mongo:3.4
docker tag mongo:3.4 harbor.qytanghost.com/public/mongo:3.4
docker push harbor.qytanghost.com/public/mongo:3.4

docker pull cvallance/mongo-k8s-sidecar
docker tag cvallance/mongo-k8s-sidecar harbor.qytanghost.com/public/mongo-k8s-sidecar
docker push harbor.qytanghost.com/public/mongo-k8s-sidecar

```

----------------------------------注意此处切换设备--------------------------------------

### 应用资源配置清单 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/stateful_mongodb/svc.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/stateful_mongodb/rbac.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/stateful_mongodb/ss.yaml

```

### 查看StatefulSet (任何一个Master)
[root@master01 ~]# kubectl get statefulset
NAME    READY   AGE
mongo   3/3     8m58s

### 使用下面命令查看整个创建过程 (任何一个Master)
```shell
watch kubectl get pod -l "role=mongo"

```

### 查看Pod, 他们有固定的名字 (任何一个Master)
[root@master01 ~]# kubectl get pod -l "role=mongo"
NAME      READY   STATUS    RESTARTS   AGE
mongo-0   2/2     Running   0          9m39s
mongo-1   2/2     Running   0          8m52s
mongo-2   2/2     Running   0          8m32s


### 查看svc (任何一个Master)
[root@master01 ~]# kubectl describe svc mongo
Name:              mongo
Namespace:         default
Labels:            name=mongo
Annotations:       Selector:  role=mongo
Type:              ClusterIP
IP:                None
Port:              <unset>  27017/TCP
TargetPort:        27017/TCP
Endpoints:         172.16.201.11:27017,172.16.202.2:27017,172.16.203.20:27017
Session Affinity:  None
Events:            <none>

### 测试无头服务的dns解析 (任何一个Master)
#### 进入容器
```shell script
kubectl exec -it $(kubectl get pod -l "app=qyt-lb-dp-label" -o jsonpath='{.items[0].metadata.name}') -- /bin/bash

```

#### 测试dns解析 (任何一个Master)
[root@qyt-lb-dp-7f677cd4cf-wdf8m qytang]# nslookup
> mongo
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   mongo.default.svc.cluster.local
Address: 172.16.203.99
Name:   mongo.default.svc.cluster.local
Address: 172.16.203.101
Name:   mongo.default.svc.cluster.local
Address: 172.16.203.100

> mongo-0.mongo.default.svc.cluster.local
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   mongo-0.mongo.default.svc.cluster.local
Address: 172.16.203.99

> mongo-1.mongo.default.svc.cluster.local
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   mongo-1.mongo.default.svc.cluster.local
Address: 172.16.203.100

> mongo-2.mongo.default.svc.cluster.local
Server:         192.168.0.2
Address:        192.168.0.2#53

Name:   mongo-2.mongo.default.svc.cluster.local
Address: 172.16.203.101
>


### 查看pvc, 每一个pod被固定关联到一个pvc (任何一个Master)
[root@master02 ~]# kubectl get pvc
NAME                               STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
mongo-persistent-storage-mongo-0   Bound    pvc-9a7c6d3c-74f4-4911-bed8-779fa1b8df39   10Gi       RWO            rook-cephfs    10m
mongo-persistent-storage-mongo-1   Bound    pvc-be27ca59-f3d8-4769-9e95-9eeaef3cba84   10Gi       RWO            rook-cephfs    9m20s
mongo-persistent-storage-mongo-2   Bound    pvc-330b9e93-6ccb-4979-85bd-0d326371d27f   10Gi       RWO            rook-cephfs    8m44s

### 查看日志 (任何一个Master)
```shell script
kubectl logs -f -c mongo mongo-0
```

### 进入容器查看集群状态 (任何一个Master)
[root@master01 ~]# kubectl exec -it mongo-0 -- mongo

Defaulting container name to mongo.
Use 'kubectl describe pod/mongo-0 -n default' to see all of the containers in this pod.

MongoDB shell version v3.4.24
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.4.24
Server has startup warnings:
2021-10-14T12:00:36.423+0000 I CONTROL  [initandlisten]
2021-10-14T12:00:36.423+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2021-10-14T12:00:36.423+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2021-10-14T12:00:36.423+0000 I CONTROL  [initandlisten] ** WARNING: You are running this process as the root user, which is not recommended.
2021-10-14T12:00:36.423+0000 I CONTROL  [initandlisten]
2021-10-14T12:00:36.424+0000 I CONTROL  [initandlisten]
2021-10-14T12:00:36.424+0000 I CONTROL  [initandlisten] ** WARNING: /sys/kernel/mm/transparent_hugepage/enabled is 'always'.
2021-10-14T12:00:36.424+0000 I CONTROL  [initandlisten] **        We suggest setting it to 'never'
2021-10-14T12:00:36.424+0000 I CONTROL  [initandlisten]

rs0:PRIMARY> rs.status()
{
        "set" : "rs0",
        "date" : ISODate("2021-10-14T12:12:01.566Z"),
        "myState" : 1,
        "term" : NumberLong(1),
        "syncingTo" : "",
        "syncSourceHost" : "",
        "syncSourceId" : -1,
        "heartbeatIntervalMillis" : NumberLong(2000),
        "optimes" : {
                "lastCommittedOpTime" : {
                        "ts" : Timestamp(1634213514, 1),
                        "t" : NumberLong(1)
                },
                "appliedOpTime" : {
                        "ts" : Timestamp(1634213514, 1),
                        "t" : NumberLong(1)
                },
                "durableOpTime" : {
                        "ts" : Timestamp(1634213514, 1),
                        "t" : NumberLong(1)
                }
        },
        "members" : [
                {
                        "_id" : 0,
                        "name" : "mongo-0.mongo.default.svc.cluster.local:27017",
                        "health" : 1,
                        "state" : 1,
                        "stateStr" : "PRIMARY",
                        "uptime" : 690,
                        "optime" : {
                                "ts" : Timestamp(1634213514, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDate" : ISODate("2021-10-14T12:11:54Z"),
                        "syncingTo" : "",
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "electionTime" : Timestamp(1634212852, 2),
                        "electionDate" : ISODate("2021-10-14T12:00:52Z"),
                        "configVersion" : 7,
                        "self" : true,
                        "lastHeartbeatMessage" : ""
                },
                {
                        "_id" : 1,
                        "name" : "mongo-1.mongo.default.svc.cluster.local:27017",
                        "health" : 1,
                        "state" : 2,
                        "stateStr" : "SECONDARY",
                        "uptime" : 626,
                        "optime" : {
                                "ts" : Timestamp(1634213514, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(1634213514, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDate" : ISODate("2021-10-14T12:11:54Z"),
                        "optimeDurableDate" : ISODate("2021-10-14T12:11:54Z"),
                        "lastHeartbeat" : ISODate("2021-10-14T12:12:00.865Z"),
                        "lastHeartbeatRecv" : ISODate("2021-10-14T12:11:59.983Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "",
                        "syncingTo" : "mongo-0.mongo.default.svc.cluster.local:27017",
                        "syncSourceHost" : "mongo-0.mongo.default.svc.cluster.local:27017",
                        "syncSourceId" : 0,
                        "infoMessage" : "",
                        "configVersion" : 7
                },
                {
                        "_id" : 2,
                        "name" : "mongo-2.mongo.default.svc.cluster.local:27017",
                        "health" : 1,
                        "state" : 2,
                        "stateStr" : "SECONDARY",
                        "uptime" : 585,
                        "optime" : {
                                "ts" : Timestamp(1634213514, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(1634213514, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDate" : ISODate("2021-10-14T12:11:54Z"),
                        "optimeDurableDate" : ISODate("2021-10-14T12:11:54Z"),
                        "lastHeartbeat" : ISODate("2021-10-14T12:12:00.865Z"),
                        "lastHeartbeatRecv" : ISODate("2021-10-14T12:12:00.768Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "",
                        "syncingTo" : "mongo-1.mongo.default.svc.cluster.local:27017",
                        "syncSourceHost" : "mongo-1.mongo.default.svc.cluster.local:27017",
                        "syncSourceId" : 1,
                        "infoMessage" : "",
                        "configVersion" : 7
                }
        ],
        "ok" : 1
}
