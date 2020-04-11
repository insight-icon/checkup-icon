import pytest
from src.checkup_conf import get_api_endpoint, get_preps


def test_github_sync_local_network_config():
    a = get_api_endpoint('mainnet')
    b = get_api_endpoint('mainnet', pull_remote=False)

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

