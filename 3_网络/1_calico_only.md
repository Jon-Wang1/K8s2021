### 前期准备controller manager (不需要配置, 只是回顾)
kube-controller-manager启动参数
  --allocate-node-cidrs=true \
  --cluster-cidr 172.16.0.0/16 \


### 前期的准备kubelet (不需要配置, 只是回顾)
kubelet 启动参数
  --network-plugin=cni : 网络插件使用cni


----------------------------------注意此处切换设备--------------------------------------

### 下载并上传镜像 (任何一个节点，但是需要docker login harbor.qytanghost.com)
```shell script
docker pull quay.io/tigera/operator:v1.20.4
docker pull calico/ctl:v3.20.2
docker tag quay.io/tigera/operator:v1.20.4 harbor.qytanghost.com/public/calico_operator:v1.20.4
docker tag calico/ctl:v3.20.2 harbor.qytanghost.com/public/calico_ctl:v3.20.2
docker push harbor.qytanghost.com/public/calico_operator:v1.20.4
docker push harbor.qytanghost.com/public/calico_ctl:v3.20.2

```

### 下载并tag pause（所有计算节点）
```shell
docker pull harbor.qytanghost.com/public/pause
docker tag harbor.qytanghost.com/public/pause k8s.gcr.io/pause:3.2

```

----------------------------------注意此处切换设备--------------------------------------

### NGINX配置 (mgmtcentos)
```shell script
yum install -y nginx

systemctl start nginx
systemctl enable nginx

cat > /etc/nginx/conf.d/mgmtcentos.qytanghost.com.conf <<'EOF'

server {
        listen          80;
        server_name     mgmtcentos.qytanghost.com;

        location / {
                autoindex       on;
                default_type    text/plain;
                root            /K8S2021/yaml_dockerfile/k8s-yaml;
        }
}
EOF
nginx -s reload

```

----------------------------------注意此处切换设备--------------------------------------

### mgmtwin7上传整个项目到mgmtcentos（可能要新建“/K8S2021”这个目录）

### mgmtwin7测试是否可以打开http://mgmtcentos.qytanghost.com/

----------------------------------注意此处切换设备--------------------------------------
### 应用资源配置清单,安装calico(任何一个Master)
### https://docs.projectcalico.org/getting-started/kubernetes/quickstart
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/calico/tigera-operator.yaml
kubectl apply -f http://mgmtcentos.qytanghost.com/calico/custom-resources.yaml
kubectl delete -f http://mgmtcentos.qytanghost.com/calico/tigera-operator.yaml
kubectl delete -f http://mgmtcentos.qytanghost.com/calico/custom-resources.yaml

```

### 可以使用如下命令，监控pod创建进程
```shell
watch kubectl get pods -n calico-system -o wide

```

### 等待3-5分钟，查看命名空间(任何一个Master)
[root@master01 ~]# kubectl get ns
NAME               STATUS   AGE
calico-apiserver   Active   7m36s
calico-system      Active   9m51s
default            Active   164m
kube-node-lease    Active   164m
kube-public        Active   164m
kube-system        Active   164m
tigera-operator    Active   10m


### 查看命名空间tigera-operator的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n tigera-operator
NAME                               READY   STATUS    RESTARTS   AGE
tigera-operator-59f4845b57-knzgz   1/1     Running   1          10m


### 查看命名空间calico-system的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n calico-system
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-5dc68f7985-tkxp6   1/1     Running   0          10m
calico-node-5dwzm                          1/1     Running   0          10m
calico-node-v9xxh                          1/1     Running   0          10m
calico-node-z5975                          1/1     Running   0          10m
calico-typha-658c5d57d-bxqkz               1/1     Running   0          10m
calico-typha-658c5d57d-fqbnh               1/1     Running   0          10m
calico-typha-658c5d57d-xvgkh               1/1     Running   0          10m

### 查看命名空间calico-apiserver的pods(任何一个Master)
[root@master01 ~]# kubectl get pod -n calico-apiserver
NAME                                READY   STATUS    RESTARTS   AGE
calico-apiserver-6bb8d7579f-dc8s7   1/1     Running   0          8m11s

### 安装calicoctl (node01, node02, node03)
#### 确认秘钥(node01, node02, node03)
```shell
ssh root@master01.qytanghost.com

```
注意:一定要退出

#### 下载kube.config(node01, node02, node03)
```shell
mkdir ~/.kube
cd ~/.kube/
sshpass -p "Cisc0123" scp master01.qytanghost.com:~/.kube/config .

```

#### 下载calicoctl(node01, node02, node03)
```shell
curl -O -L  https://github.com/projectcalico/calicoctl/releases/download/v3.20.2/calicoctl
chmod +x calicoctl
export DATASTORE_TYPE=kubernetes
export KUBECONFIG=~/.kube/config

./calicoctl get node

```

## 如果希望预留地址(推荐)(任何一个Master)

### 给node打标签(任何一个Master)
```shell
kubectl label nodes node01.qytanghost.com rack=1
kubectl label nodes node02.qytanghost.com rack=2
kubectl label nodes node03.qytanghost.com rack=3

```

### 查看地址池(任何一个Node)
```shell
./calicoctl get ippool -o wide

```
### 删除默认的地址池(任何一个Node)
```shell
./calicoctl delete ippools default-ipv4-ippool

```

### 下载资源配置清单(任何一个Node)
```shell
wget http://mgmtcentos.qytanghost.com/calico/node01.yaml
wget http://mgmtcentos.qytanghost.com/calico/node02.yaml
wget http://mgmtcentos.qytanghost.com/calico/node03.yaml

```
### 应用资源配置清单(任何一个Node)
```shell
./calicoctl create -f - < node01.yaml
./calicoctl create -f - < node02.yaml
./calicoctl create -f - < node03.yaml

```

### 查看地址池(任何一个Node)
[root@node01 ~]# ./calicoctl get ippool -o wide
NAME            CIDR              NAT    IPIPMODE   VXLANMODE   DISABLED   SELECTOR
rack-1-ippool   172.16.201.0/24   true   Never      Always      false      rack == "1"
rack-2-ippool   172.16.202.0/24   true   Never      Always      false      rack == "2"
rack-3-ippool   172.16.203.0/24   true   Never      Always      false      rack == "3"

### 查看node状态（已经Ready了）(任何一个Master)
[root@master01 ~]# kubectl get node
NAME                    STATUS   ROLES   AGE   VERSION
node01.qytanghost.com   Ready    node    75m   v1.20.11
node02.qytanghost.com   Ready    node    75m   v1.20.11
node03.qytanghost.com   Ready    node    75m   v1.20.11

### 默认BGP是full mesh状态(任何一个Node)
[root@node01 .kube]# ./calicoctl node status
Calico process is running.

IPv4 BGP status
+--------------+-------------------+-------+----------+-------------+
| PEER ADDRESS |     PEER TYPE     | STATE |  SINCE   |    INFO     |
+--------------+-------------------+-------+----------+-------------+
| 10.1.1.202   | node-to-node mesh | up    | 06:53:20 | Established |
| 10.1.1.203   | node-to-node mesh | up    | 06:53:29 | Established |
+--------------+-------------------+-------+----------+-------------+

IPv6 BGP status
No IPv6 peers found.

### 思科路由器BGP配置(CSR)
```shell
router bgp 63400
 bgp log-neighbor-changes
 bgp listen range 10.1.1.0/24 peer-group calico
 neighbor calico peer-group
 neighbor calico remote-as 63400
 neighbor calico route-reflector-client

```

### 切换到路由反射器(任何一个Node)
```shell
rm -f bgp-config-off-mesh.yaml
wget http://mgmtcentos.qytanghost.com/calico/bgp-config-off-mesh.yaml
./calicoctl apply -f - < bgp-config-off-mesh.yaml

rm -f node01-bgp.yaml
rm -f node02-bgp.yaml
rm -f node02-bgp.yaml

wget http://mgmtcentos.qytanghost.com/calico/node01-bgp.yaml
wget http://mgmtcentos.qytanghost.com/calico/node02-bgp.yaml
wget http://mgmtcentos.qytanghost.com/calico/node03-bgp.yaml

./calicoctl apply -f - < node01-bgp.yaml
./calicoctl apply -f - < node02-bgp.yaml
./calicoctl apply -f - < node03-bgp.yaml

```

### 查看节点BGP状态(任何一个Node)
[root@node01 ~]# ./calicoctl node status
Calico process is running.

IPv4 BGP status
+--------------+---------------+-------+----------+-------------+
| PEER ADDRESS |   PEER TYPE   | STATE |  SINCE   |    INFO     |
+--------------+---------------+-------+----------+-------------+
| 10.1.1.16    | node specific | up    | 07:00:01 | Established |
+--------------+---------------+-------+----------+-------------+

IPv6 BGP status
No IPv6 peers found.

[root@node02 .kube]# ./calicoctl node status
Calico process is running.


IPv4 BGP status
+--------------+---------------+-------+----------+-------------+
| PEER ADDRESS |   PEER TYPE   | STATE |  SINCE   |    INFO     |
+--------------+---------------+-------+----------+-------------+
| 10.1.1.16    | node specific | up    | 07:00:00 | Established |
+--------------+---------------+-------+----------+-------------+

IPv6 BGP status
No IPv6 peers found.

[root@node03 .kube]# ./calicoctl node status
Calico process is running.

IPv4 BGP status
+--------------+---------------+-------+----------+-------------+
| PEER ADDRESS |   PEER TYPE   | STATE |  SINCE   |    INFO     |
+--------------+---------------+-------+----------+-------------+
| 10.1.1.16    | node specific | up    | 07:00:00 | Established |
+--------------+---------------+-------+----------+-------------+

IPv6 BGP status
No IPv6 peers found.

###路由器上查看邻居(CSR)
CSR1#show ip bgp summary
BGP router identifier 10.1.1.16, local AS number 63400
BGP table version is 4, main routing table version 4
3 network entries using 744 bytes of memory
3 path entries using 408 bytes of memory
1/1 BGP path/bestpath attribute entries using 288 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 1440 total bytes of memory
BGP activity 3/0 prefixes, 9/6 paths, scan interval 60 secs
3 networks peaked at 07:00:01 Oct 26 2021 UTC (00:16:34.683 ago)

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
*10.1.1.201     4        63400      27      25        4    0    0 00:16:34        1
*10.1.1.202     4        63400      26      28        4    0    0 00:16:33        1
*10.1.1.203     4        63400      26      25        4    0    0 00:16:34        1
* Dynamically created based on a listen range command
Dynamically created neighbors: 3, Subnet ranges: 1

BGP peergroup calico listen range group members:
  10.1.1.0/24


Total dynamically created neighbors: 3/(100 max), Subnet ranges: 1

###路由器上查看路由(CSR)
CSR1#show ip route bgp
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      172.16.0.0/24 is subnetted, 3 subnets
B        172.16.201.0 [200/0] via 10.1.1.201, 00:17:15
B        172.16.202.0 [200/0] via 10.1.1.202, 00:17:15
B        172.16.203.0 [200/0] via 10.1.1.203, 00:17:15
