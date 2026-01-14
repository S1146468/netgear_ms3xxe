import os
import pytest
from netgear_ms3xxe.client import NetgearSwitchClient

def _live_config():
    host = os.getenv("NETGEAR_SWITCH_HOST")
    password = os.getenv("NETGEAR_SWITCH_PASSWORD")
    if not host or not password:
        pytest.skip("Set NETGEAR_SWITCH_HOST and NETGEAR_SWITCH_PASSWORD to run live tests")
    return host, password

@pytest.fixture(scope="session")
def live_client():
    host, password = _live_config()
    client = NetgearSwitchClient(host, password)
    try:
        yield client
    finally:
        client.close()
