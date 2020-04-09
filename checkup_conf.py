import requests
import json
import sys
import logging
import os

from pprint import pprint

DB_USER = os.getenv('DB_USER', 'postgres')
DB_DBNAME = os.getenv('DB_DBNAME', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')


def get_url(network_name):
    if network_name not in ['mainnet', 'testnet']:
        return ValueError('Need to specify network_name -> either mainnet or testnet')
    if network_name == 'mainnet':
        url = "https://ctz.solidwallet.io/api/v3"
    elif network_name == 'testnet':
        url = "https://zicon.net.solidwallet.io/api/v3"
    else:
        return ValueError('Need to specify network_name -> either mainnet or testnet')
    return url


def get_preps(network_name):
    url = get_url(network_name)
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

    response = requests.post(url, json=payload).json()
    assert response["jsonrpc"]
    assert response["id"] == 1234
    return response


def get_checkup_dict(network_name):
    response = get_preps(network_name)
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


def write_checkup_conf(checkup_conf):
    with open('checkup1.json', 'w') as f:
        json.dump(checkup_conf, f)


if __name__ == "__main__":
    # network_name = sys.argv[1]
    network_name = 'mainnet'
    checkup_conf = get_checkup_dict(network_name)
    pprint(checkup_conf)
