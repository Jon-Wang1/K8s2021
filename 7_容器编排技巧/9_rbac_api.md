### 产生Python api测试的镜像 (mgmtcentos)
```shell script
cd /K8S2021/yaml_dockerfile/dockerfile/api-rbac/
docker build -t harbor.qytanghost.com/public/api-rbac .
docker push harbor.qytanghost.com/public/api-rbac

```

----------------------------------注意此处切换设备--------------------------------------

### 查看当前k8s cluster中的api资源 （任何一个Master）
[root@master01 ~]# kubectl api-resources -o wide
NAME                              SHORTNAMES        APIGROUP                       NAMESPACED   KIND                             VERBS
bindings                                                                           true         Binding                          [create]
componentstatuses                 cs                                               false        ComponentStatus                  [get list]
configmaps                        cm                                               true         ConfigMap                        [create delete deletecollection get list patch update watch]
endpoints                         ep                                               true         Endpoints                        [create delete deletecollection get list patch update watch]
events                            ev                                               true         Event                            [create delete deletecollection get list patch update watch]
limitranges                       limits                                           true         LimitRange                       [create delete deletecollection get list patch update watch]
namespaces                        ns                                               false        Namespace                        [create delete get list patch update watch]
nodes                             no                                               false        Node                             [create delete deletecollection get list patch update watch]
persistentvolumeclaims            pvc                                              true         PersistentVolumeClaim            [create delete deletecollection get list patch update watch]
persistentvolumes                 pv                                               false        PersistentVolume                 [create delete deletecollection get list patch update watch]
pods                              po                                               true         Pod                              [create delete deletecollection get list patch update watch]
podtemplates                                                                       true         PodTemplate                      [create delete deletecollection get list patch update watch]
replicationcontrollers            rc                                               true         ReplicationController            [create delete deletecollection get list patch update watch]
resourcequotas                    quota                                            true         ResourceQuota                    [create delete deletecollection get list patch update watch]
secrets                                                                            true         Secret                           [create delete deletecollection get list patch update watch]
serviceaccounts                   sa                                               true         ServiceAccount                   [create delete deletecollection get list patch update watch]
services                          svc                                              true         Service                          [create delete get list patch update watch]
mutatingwebhookconfigurations                       admissionregistration.k8s.io   false        MutatingWebhookConfiguration     [create delete deletecollection get list patch update watch]
validatingwebhookconfigurations                     admissionregistration.k8s.io   false        ValidatingWebhookConfiguration   [create delete deletecollection get list patch update watch]
customresourcedefinitions         crd,crds          apiextensions.k8s.io           false        CustomResourceDefinition         [create delete deletecollection get list patch update watch]
apiservices                                         apiregistration.k8s.io         false        APIService                       [create delete deletecollection get list patch update watch]
controllerrevisions                                 apps                           true         ControllerRevision               [create delete deletecollection get list patch update watch]
daemonsets                        ds                apps                           true         DaemonSet                        [create delete deletecollection get list patch update watch]
deployments                       deploy            apps                           true         Deployment                       [create delete deletecollection get list patch update watch]
replicasets                       rs                apps                           true         ReplicaSet                       [create delete deletecollection get list patch update watch]
statefulsets                      sts               apps                           true         StatefulSet                      [create delete deletecollection get list patch update watch]
tokenreviews                                        authentication.k8s.io          false        TokenReview                      [create]
localsubjectaccessreviews                           authorization.k8s.io           true         LocalSubjectAccessReview         [create]
selfsubjectaccessreviews                            authorization.k8s.io           false        SelfSubjectAccessReview          [create]
selfsubjectrulesreviews                             authorization.k8s.io           false        SelfSubjectRulesReview           [create]
subjectaccessreviews                                authorization.k8s.io           false        SubjectAccessReview              [create]
horizontalpodautoscalers          hpa               autoscaling                    true         HorizontalPodAutoscaler          [create delete deletecollection get list patch update watch]
cronjobs                          cj                batch                          true         CronJob                          [create delete deletecollection get list patch update watch]
jobs                                                batch                          true         Job                              [create delete deletecollection get list patch update watch]
cephblockpools                                      ceph.rook.io                   true         CephBlockPool                    [delete deletecollection get list patch create update watch]
cephclients                                         ceph.rook.io                   true         CephClient                       [delete deletecollection get list patch create update watch]
cephclusters                                        ceph.rook.io                   true         CephCluster                      [delete deletecollection get list patch create update watch]
cephfilesystems                                     ceph.rook.io                   true         CephFilesystem                   [delete deletecollection get list patch create update watch]
cephnfses                         nfs               ceph.rook.io                   true         CephNFS                          [delete deletecollection get list patch create update watch]
cephobjectstores                                    ceph.rook.io                   true         CephObjectStore                  [delete deletecollection get list patch create update watch]
cephobjectstoreusers              rcou,objectuser   ceph.rook.io                   true         CephObjectStoreUser              [delete deletecollection get list patch create update watch]
certificatesigningrequests        csr               certificates.k8s.io            false        CertificateSigningRequest        [create delete deletecollection get list patch update watch]
leases                                              coordination.k8s.io            true         Lease                            [create delete deletecollection get list patch update watch]
endpointslices                                      discovery.k8s.io               true         EndpointSlice                    [create delete deletecollection get list patch update watch]
events                            ev                events.k8s.io                  true         Event                            [create delete deletecollection get list patch update watch]
ingresses                         ing               extensions                     true         Ingress                          [create delete deletecollection get list patch update watch]
ingressclasses                                      networking.k8s.io              false        IngressClass                     [create delete deletecollection get list patch update watch]
ingresses                         ing               networking.k8s.io              true         Ingress                          [create delete deletecollection get list patch update watch]
networkpolicies                   netpol            networking.k8s.io              true         NetworkPolicy                    [create delete deletecollection get list patch update watch]
runtimeclasses                                      node.k8s.io                    false        RuntimeClass                     [create delete deletecollection get list patch update watch]
objectbucketclaims                obc,obcs          objectbucket.io                true         ObjectBucketClaim                [delete deletecollection get list patch create update watch]
objectbuckets                     ob,obs            objectbucket.io                false        ObjectBucket                     [delete deletecollection get list patch create update watch]
poddisruptionbudgets              pdb               policy                         true         PodDisruptionBudget              [create delete deletecollection get list patch update watch]
podsecuritypolicies               psp               policy                         false        PodSecurityPolicy                [create delete deletecollection get list patch update watch]
clusterrolebindings                                 rbac.authorization.k8s.io      false        ClusterRoleBinding               [create delete deletecollection get list patch update watch]
clusterroles                                        rbac.authorization.k8s.io      false        ClusterRole                      [create delete deletecollection get list patch update watch]
rolebindings                                        rbac.authorization.k8s.io      true         RoleBinding                      [create delete deletecollection get list patch update watch]
roles                                               rbac.authorization.k8s.io      true         Role                             [create delete deletecollection get list patch update watch]
volumes                           rv                rook.io                        true         Volume                           [delete deletecollection get list patch create update watch]
priorityclasses                   pc                scheduling.k8s.io              false        PriorityClass                    [create delete deletecollection get list patch update watch]
volumesnapshotclasses                               snapshot.storage.k8s.io        false        VolumeSnapshotClass              [delete deletecollection get list patch create update watch]
volumesnapshotcontents                              snapshot.storage.k8s.io        false        VolumeSnapshotContent            [delete deletecollection get list patch create update watch]
volumesnapshots                                     snapshot.storage.k8s.io        true         VolumeSnapshot                   [delete deletecollection get list patch create update watch]
csidrivers                                          storage.k8s.io                 false        CSIDriver                        [create delete deletecollection get list patch update watch]
csinodes                                            storage.k8s.io                 false        CSINode                          [create delete deletecollection get list patch update watch]
storageclasses                    sc                storage.k8s.io                 false        StorageClass                     [create delete deletecollection get list patch update watch]
volumeattachments                                   storage.k8s.io                 false        VolumeAttachment                 [create delete deletecollection get list patch update watch]

### 查看特定的api资源 （任何一个Master）
[root@master02 ~]# kubectl api-resources -o wide | grep -i pods
NAME                              SHORTNAMES        APIGROUP                       NAMESPACED   KIND                             VERBS
pods                              po                v1                             true         Pod                              [create delete deletecollection get list patch update watch]
podsecuritypolicies               psp               policy/v1beta1                 false        PodSecurityPolicy                [create delete deletecollection get list patch update watch]

[root@master02 ~]# kubectl api-resources -o wide | grep -i deployment
NAME                              SHORTNAMES        APIGROUP                       NAMESPACED   KIND                             VERBS
deployments                       deploy            apps/v1                        true         Deployment                       [create delete deletecollection get list patch update watch]

[root@master01 ~]# kubectl api-resources -o wide | grep -i services
NAME                              SHORTNAMES        APIGROUP                       NAMESPACED   KIND                             VERBS
services                          svc               v1                             true         Service                          [create delete get list patch update watch]

[root@master01 ~]# kubectl api-resources -o wide | grep -i traefik
NAME                              SHORTNAMES        APIGROUP                       NAMESPACED   KIND                             VERBS
ingressroutes                                       traefik.containo.us/v1alpha1   true         IngressRoute                     [delete deletecollection get list patch create update watch]

### api实例 （任何一个Master）
https://github.com/kubernetes-client/python/tree/master/examples

### 应用rbac资源配置清单 （任何一个Master）
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/api/rbac.yaml

```

### 应用deployment资源配置清单 （任何一个Master）
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/api/api-dp.yaml

```

### 查看pod （任何一个Master）
```shell script
kubectl get pod $(kubectl get pod -l "app=api-dp" -o jsonpath='{.items[0].metadata.name}')

```

#### 返回结果 （任何一个Master）
NAME                      READY   STATUS    RESTARTS   AGE
api-dp-54d8649bfb-4q4tm   1/1     Running   0          82s

### 进入pod （任何一个Master）
```shell script
kubectl exec -it $(kubectl get pod -l "app=api-dp" -o jsonpath='{.items[0].metadata.name}')  -- /bin/bash

```

#### 容器内查看文件 （任何一个Master）
[root@api-dp-54d8649bfb-4q4tm qytang]# ls -an
total 36
drwxr-xr-x 1 0 0   30 Oct 14 19:15 .
drwxr-xr-x 1 0 0   28 Oct 14 19:19 ..
-rwxr-xr-x 1 0 0 1795 Oct 14 19:15 create_deploy.py
-rwxr-xr-x 1 0 0  437 Oct 14 19:15 create_deploy_yaml.py
-rwxr-xr-x 1 0 0  832 Oct 14 19:15 delete_deploy.py
-rw-r--r-- 1 0 0  586 Oct 14 19:15 dp.yaml
-rwxr-xr-x 1 0 0  602 Oct 14 19:15 get_pod_detail.py
-rwxr-xr-x 1 0 0  777 Oct 14 19:15 get_pod_logs.py
-rwxr-xr-x 1 0 0  626 Oct 14 19:15 get_pods.py
-rwxr-xr-x 1 0 0  901 Oct 14 19:15 update_deploy.py
-rwxr-xr-x 1 0 0  657 Oct 14 19:15 watch_pods.py

### 容器内测试list pods （任何一个Master）
```shell script
python3 get_pods.py 

```

### 容器内测试watch pods,能实时显示pod操作 （任何一个Master）
```shell script
python3 watch_pods.py 

```

### 创建一个pod测试 (任何一个Master)
```shell script
kubectl apply -f http://mgmtcentos.qytanghost.com/qyt-lb/qyt-lb-dp.yaml

```

### 容器内get特定pod详情 （任何一个Master）
```shell script
python3 get_pod_detail.py app=api-dp

```

### 容器内get pod/log （任何一个Master）
```shell script
python3 get_pod_logs.py qyt-lb-dp-7f677cd4cf-8869j

```

### 容器内create deploy （任何一个Master）
```shell script
python3 create_deploy.py 

```

### 查看创建的pods(任何一个Master)
[root@master02 ~]# kubectl get pod
NAME                                         READY   STATUS    RESTARTS   AGE
nginx-deployment-5dd6f4f544-f4s2s            1/1     Running   0          5m38s
nginx-deployment-5dd6f4f544-nq7lr            1/1     Running   0          5m38s
nginx-deployment-5dd6f4f544-xsbdp            1/1     Running   0          5m38s

### 容器内create deploy从yaml （任何一个Master）
```shell script
python3 create_deploy_yaml.py

```

### 查看创建的pods(任何一个Master)
[root@master02 ~]# kubectl get pod
NAME                                         READY   STATUS    RESTARTS   AGE
nginx-pod-api-from-yaml-9db56fff6-dcfmr      1/1     Running   0          31s

### 容器内update deploy (api 为 patch) （任何一个Master）
```shell script
python3 update_deploy.py 

```

### 容器内delete deploy （任何一个Master）
```shell script
python3 delete_deploy.py 

```