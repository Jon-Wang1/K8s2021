### 标签操作

#### 查看标签
[root@master01 ~]# kubectl get pod mongo-0 --show-labels
NAME      READY   STATUS    RESTARTS   AGE   LABELS
mongo-0   2/2     Running   0          33m   controller-revision-hash=mongo-75b8689ff7,environment=test,role=mongo,statefulset.kubernetes.io/pod-name=mongo-0

#### 打标签
[root@master01 ~]# kubectl label pod mongo-0 versionID=ver0.9
pod/mongo-0 labeled

[root@master01 ~]# kubectl get pod mongo-0 --show-labels
NAME      READY   STATUS    RESTARTS   AGE   LABELS
mongo-0   2/2     Running   0          8h    controller-revision-hash=mongo-95994cbf9,environment=test,role=mongo,statefulset.kubernetes.io/pod-name=mongo-0,versionID=ver0.9

#### 覆盖标签
[root@master01 ~]# kubectl label --overwrite pod mongo-0 versionID=ver10
pod/mongo-0 labeled

[root@master01 ~]# kubectl get pod mongo-0 --show-labels
NAME      READY   STATUS    RESTARTS   AGE   LABELS
mongo-0   2/2     Running   0          34m   controller-revision-hash=mongo-75b8689ff7,environment=test,role=mongo,statefulset.kubernetes.io/pod-name=mongo-0,versionID=ver10


#### 删除标签
[root@master01 ~]# kubectl label pod mongo-0 versionID-
pod/mongo-0 labeled

[root@master01 ~]# kubectl get pod mongo-0 --show-labels
NAME      READY   STATUS    RESTARTS   AGE   LABELS
mongo-0   2/2     Running   0          34m   controller-revision-hash=mongo-75b8689ff7,environment=test,role=mongo,statefulset.kubernetes.io/pod-name=mongo-0

