import requests
import json
import sys
import logging

from pprint import pprint


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


def get_checkers(network_name):
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
    return checkers

# def main():
#     check_if_exists(network_name, )


if __name__ == "__main__":
    # network_name = sys.argv[1]
    network_name = 'mainnet'

    preps_dict = get_preps(network_name)['result']['preps']
    checkers = get_checkers(network_name)
    with open('checkup1.json', 'w') as f:
        json.dump(checkers, f)
    print()
    # main()
