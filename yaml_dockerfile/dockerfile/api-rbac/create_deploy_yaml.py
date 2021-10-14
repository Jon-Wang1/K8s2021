#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# http://www.mingjiao.org:8088/

from kubernetes import client, config, utils
config.load_incluster_config()
k8s_client = client.ApiClient()
yaml_file = 'dp.yaml'
utils.create_from_yaml(k8s_client, yaml_file)
