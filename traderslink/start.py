# -*- coding: UTF-8 -*-

# This script will parse puyuan.yml and
# 1. create working directories for each docker.
# 2. generate docker-compose.yml
# 3. generate configure files for each docker instance, e.g. master, routers and gateways

import os
import sys
import yaml
import json
import subprocess

working_dir = 'temp'

docker_compose_obj = yaml.safe_load(
'''
version: '3'
''')
docker_compose_obj['services'] = {}

puyuan_config_file = 'puyuan.yml'
with open(puyuan_config_file) as fin:
    yml = yaml.safe_load(fin)
    for item in yml:
        docker_name = item['docker_name']
        docker_compose_obj['services'][docker_name] = item['docker_compose']
        docker_compose_obj['services'][docker_name]['tty'] = True
        curr_working_dir = os.path.abspath(os.path.join(working_dir, docker_name))
        log_dir = os.path.join(curr_working_dir, 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        cfg_dir = os.path.join(curr_working_dir, 'etc')
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
        cfg_file = os.path.join(cfg_dir, 'config.json')
        with open(cfg_file, 'w') as fout:
            json.dump(item['config'], fout, indent=4)
        docker_compose_obj['services'][docker_name]['volumes'] = [log_dir + ':/shared/log']
        docker_compose_obj['services'][docker_name]['volumes'].append(cfg_file + ':/shared/etc/config.json')

docker_compose_file = 'docker-compose.yml'
with open(docker_compose_file, 'w') as fout:
    yaml.safe_dump(docker_compose_obj, fout, allow_unicode=True, default_flow_style=False)

os.system('docker-compose pull')
os.system('docker-compose up --build -d')