import pytest
from src.checkup_conf import output_dict, get_preps, get_api_endpoint, get_checkup_dict


def test_github_sync_local_network_config():
    a = output_dict('mainnet')
    b = output_dict('mainnet', pull_remote=False)

    assert a == b


@pytest.mark.parametrize("network", ['mainnet', 'bicon', 'testnet', 'zicon'])
def test_get_api_endpoint(network):
    print(network)
    api = get_api_endpoint(network)
    print(api)


@pytest.mark.parametrize("api_endpoint", ['https://ctz.solidwallet.io'])
def test_get_preps(api_endpoint):
    print(api_endpoint)
    preps = get_preps(api_endpoint)
    print(preps)


@pytest.mark.parametrize("network", ['mainnet', 'bicon', 'zicon', 'testnet'])
def test_get_preps(network):
    print(network)
    output = get_checkup_dict(network)
    print(output)
