### 进入容器qyt-lb-dp
```shell script
kubectl exec -it $(kubectl get pod -l "app=qyt-lb-dp-label" -o jsonpath='{.items[0].metadata.name}') -- /bin/bash
```

#### 安装Python3
```shell script
yum install -y python3
```

#### 安装pymongo模块
```shell script
pip3 install pymongo
```

#### 交互式界面测试mongo集群
[root@qyt-lb-dp-7f677cd4cf-wdf8m qytang]# python3

>>> from pymongo import *

>>> client = MongoClient('mongodb://mongo-0.mongo.default.svc.cluster.local:27017,mongo-1.mongo.default.svc.cluster.local:27017,mongo-2.mongo.mongo.svc.cluster.local:27017/?replicaSet=rs0')

>>> db = client['qytang']

>>> for obj in db.secie.find():
...   print(obj)
... 
{'_id': ObjectId('5f8e437ac7f08b56b24f8c8c'), 'test': 123.0}
```