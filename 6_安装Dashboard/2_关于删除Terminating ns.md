### 参考文章
https://www.cnblogs.com/xiao987334176/p/13272410.html

### 获取ns
[root@master03 cert]# kubectl get ns
NAME                   STATUS        AGE
calico-apiserver       Active        5h29m
calico-system          Active        5h31m
default                Active        6h47m
kube-node-lease        Active        6h47m
kube-public            Active        6h47m
kube-system            Active        6h47m
kubernetes-dashboard   Terminating   62m
tigera-operator        Active        5h31m

### 查看namespace 中的finalizer, 导出为json
[root@master03 cert]# kubectl get ns kubernetes-dashboard -o json > tmp.json

### 编辑 vi tmp.json
spec部分只保留如下信息:
    "spec": {
    },

### 打开kubectl proxy
[root@master03 cert]# kubectl proxy
Starting to serve on 127.0.0.1:8001

### 在起一个会话
curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json 127.0.0.1:8001/api/v1/namespaces/kubernetes-dashboard/finalize



