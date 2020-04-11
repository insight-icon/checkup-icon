from src.checkup_conf import get_api_endpoint


def test_github_sync_local_network_config():
    a = get_api_endpoint('mainnet')
    b = get_api_endpoint('mainnet', pull_remote=False)

    assert a == b