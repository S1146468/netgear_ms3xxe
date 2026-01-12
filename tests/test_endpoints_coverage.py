import pytest
from netgear_ms3xxe.endpoints import ENDPOINTS


@pytest.mark.live
def test_endpoints_coverage_live(live_client):
    sw = live_client

    # system.status is typically called during client __init__ for profile autodetect.
    # Only call it here if no initial status was captured (e.g. explicit profile passed).
    if sw.initial_status() is None:
        sw.system.status()

    sw.system.ip_settings()
    sw.system.qos_mode()
    sw.system.qos_ports()
    sw.system.qos_broadcast()

    sw.ports.get()
    sw.ports.statistics()
    sw.ports.pvid()
    sw.ports.ratelimit()
    sw.ports.stormcontrol()
    sw.ports.led()

    sw.power.led()
    sw.access_control.get()

    sw.vlan.mode()
    sw.vlan.basic1q_vlans()
    sw.vlan.basic_ports()
    sw.vlan.basic1q_conf()
    sw.vlan.basic1q_mgmt_interface()
    sw.vlan.advanced1q()
    sw.vlan.advanced_ports()
    sw.vlan.advanced1q_oui()
    sw.vlan.advanced1q_mgmt_interface()

    sw.lag.get()
    sw.multicast.get()

    called = set(sw.router.calls)
    declared = set(ENDPOINTS.keys())

    missing = declared - called
    assert not missing, f"Declared endpoint_ids not exercised: {sorted(missing)}"

    extras = called - declared
    assert not extras, f"Endpoint_ids called but not declared: {sorted(extras)}"
