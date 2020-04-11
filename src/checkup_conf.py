import requests
import json
import sys
import logging
import os
import fire

from pprint import pprint

DB_USER = os.getenv('DB_USER', 'postgres')
DB_DBNAME = os.getenv('DB_DBNAME', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

NETWORKS_JSON = 'https://raw.githubusercontent.com/JINWOO-J/icon_network_info/master/conf/all.json'

LOCAL_CONFIG = os.path.join(os.path.curdir, '..', 'configs', 'all.json')


def get_api_endpoint(network_name, pull_remote=True):
    api_endpoint = ""
    if pull_remote:
        nets_conf = requests.get(NETWORKS_JSON).json()
    else:
        print(LOCAL_CONFIG)
        with open(LOCAL_CONFIG, 'r') as f:
            nets_conf = json.load(f)

    for net in nets_conf:
        if net['network_name'] == network_name or net['network_alias'] == network_name:
            api_endpoint = net['api_endpoint']
            # nid = net['nid']
    if api_endpoint == "":
        ValueError('Need to specify network_name -> either mainnet, Euljiro, Yeouido, Pagoda or their alias')

    return api_endpoint


def get_preps(api_endpoint):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": "cx0000000000000000000000000000000000000000",
            "dataType": "call",
            "data": {
                "method": "getPReps",
                "params": {
                    "startRanking": "0x1",
                    "endRanking": "0xffff"
                }
            }
        }
    }

    response = requests.post(api_endpoint + '/api/v3', json=payload).json()
    assert response["jsonrpc"]
    assert response["id"] == 1234
    return response


def get_checkup_dict(network_name, pull_remote=True):
    api_enpoint = get_api_endpoint(network_name, pull_remote=pull_remote)
    response = get_preps(api_enpoint)
    preps = response['result']['preps']
    checkers = []
    for i in range(0, len(preps)):
        endpoint_url = preps[i]['name']
        endpoint_name = "{}:9000".format(preps[i]['p2pEndpoint'].split(':')[0])
        checkers.append({
            "type": "tcp",
            "endpoint_name": endpoint_name,
            "endpoint_url": endpoint_url,
            "attempts": 1
        })

    checkup_conf = {
        'checkers': checkers,
        'storage': {
            "provider": "sql",
            "postgresql": {
                "user": DB_USER,
                "dbname": DB_DBNAME,
                "host": DB_HOST,
                "port": 5432,
                "password": DB_PASSWORD,
                "sslmode": "disable"
            }
        }
    }

    return checkup_conf


def write_checkup_conf(network_name):
    checkup_conf = get_checkup_dict(network_name)

    with open('../checkup1.json', 'w') as f:
        json.dump(checkup_conf, f)


def output_dict(network_name):
    checkup_conf = get_checkup_dict(network_name)
    pprint(checkup_conf)


def main():
    fire.Fire(name='checkup_conf')


if __name__ == "__main__":
    main()
