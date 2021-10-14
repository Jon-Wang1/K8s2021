### 进入容器 (任何一个Master)
[root@master01 ~]# kubectl exec -it mongo-0 -- mongo

### 容器内mongo DB操作
#### 切换数据到
rs0:PRIMARY> use admin
switched to db admin

#### 创建用户admin
rs0:PRIMARY> db.createUser({user:"admin",pwd:"Cisc0123",roles:["root"]}) 
Successfully added user: { "user" : "admin", "roles" : [ "root" ] }

#### 使用admin认证登录
rs0:PRIMARY> db.auth('admin','Cisc0123')
1

#### 查看数据库
rs0:PRIMARY> show dbs
admin  0.000GB
local  0.000GB

#### 切换数据库到qytang
rs0:PRIMARY> use qytang
switched to db qytang

#### 创建用户qytangadmin, 授予qytang数据库的dbOwner角色
rs0:PRIMARY> db.createUser({user: "qytangadmin", pwd: "Cisc0123", roles: [{ role: "dbOwner", db: "qytang" }]})
Successfully added user: {
        "user" : "qytangadmin",
        "roles" : [
                {
                        "role" : "dbOwner",
                        "db" : "qytang"
                }
        ]
}

#### 使用qytangadmin登录
rs0:PRIMARY> db.auth('qytangadmin','Cisc0123')
1

#### 查看表
rs0:PRIMARY> show tables

#### 在secie表中插入数据
rs0:PRIMARY> db.secie.insert({'test':123})
WriteResult({ "nInserted" : 1 })

#### 查看表
rs0:PRIMARY> show tables
secie

#### 查看表secie内的数据
rs0:PRIMARY> db.secie.find()
{ "_id" : ObjectId("5f8e437ac7f08b56b24f8c8c"), "test" : 123 }
```