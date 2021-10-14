#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

from kubernetes.client.rest import ApiException
from kubernetes import client, config

config.load_incluster_config()
pod_name = "counter"


def get_pod_log(pod_name):
    try:
        api_instance = client.CoreV1Api()
        api_response = api_instance.read_namespaced_pod_log(name=pod_name, namespace='default')
        print(api_response)
    except ApiException as e:
        print(e)
        print('Found exception in reading the logs')


if __name__ == '__main__':
    import sys
    get_pod_log(sys.argv[1])
