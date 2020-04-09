import pytest
from checkup_conf import get_networks_github, get_networks_json

def test_github_sync_local_network_config():
    a = get_networks_json()
    b = get_networks_github()

    assert a == b