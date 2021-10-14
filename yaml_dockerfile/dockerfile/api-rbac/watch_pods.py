#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

from kubernetes import client, config, watch


def watch_pods():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    w = watch.Watch()
    while True:
        for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
            print(f"Event: {event['type']} {event['object'].kind} {event['object'].metadata.name}")


if __name__ == '__main__':
    watch_pods()
