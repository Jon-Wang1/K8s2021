#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

from kubernetes import client, config


def get_pod(label_selector):
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    ret = v1.list_namespaced_pod("default", label_selector=label_selector, watch=False)
    print(ret.items)


if __name__ == '__main__':
    import sys
    get_pod(sys.argv[1])
    # get_pod("app=api-dp")


