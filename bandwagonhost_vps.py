#!/usr/bin/env python
import yaml
import requests
import sys
import json

# confgureation
config_file = "/etc/zabbix/zabbix_agentd.d/config.yml"
with open(config_file, 'r') as config:
    cfg = yaml.safe_load(config)

# bandwagonhost api url
base_url = 'https://api.64clouds.com/v1/getServiceInfo'

discovery_data = []
for server in cfg:
    discovery_data.append({"{#SERVER}": server})


def get_info(_server, _item):
    try:
        cfg[_server]
    except KeyError:
        print("There is no %s in %s !!!" % (server, config_file))
        exit(1)
    veid = cfg[_server]['veid']
    api_key = cfg[_server]['api_key']
    url = base_url + '&veid=' + str(veid) + '&api_key=' + api_key
    response = requests.get(url).json()
    data_counter = response["data_counter"] * response["monthly_data_multiplier"]
    plan_monthly_data = response["plan_monthly_data"] * response["monthly_data_multiplier"]
    data_next_reset = response["data_next_reset"]
    if _item == "data_counter":
        print(data_counter)
    elif _item == 'plan_monthly_data':
        print(plan_monthly_data)
    elif _item == 'data_next_reset':
        print(data_next_reset)
    else:
        print("%s is not supported!!!" %_item)
        exit(2)


if len(sys.argv) == 1:
    print(json.dumps({"data": discovery_data}, indent=4))
elif len(sys.argv) == 3:
    server = sys.argv[1]
    item = sys.argv[2]
    get_info(server, item)
else:
    print("""Usage:
          # without arguments return all servers
          %s
          # with arguments, support items "data_counter","plan_monthly_data","data_next_reset"
          %s server item""" % (sys.argv[0], sys.argv[0]))
