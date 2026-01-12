import pytest


@pytest.mark.live
def test_smoke_live(live_client):
    sw = live_client
    assert sw.backend_id == "ms3xxe-react"
    assert sw.profile.backend_id == sw.backend_id


    # NEW: avoid a second /api/system/status call if the client already fetched it for profile autodetect
    status = sw.initial_status() or sw.system.status()
    print("status:", status)
    assert sw.profile is not None
    assert status.system_info.model_number in sw.profile.model_numbers
    assert sw.profile.backend_id == "ms3xxe-react"

    ip = sw.system.ip_settings()
    print("ip:", ip)
    assert ip.ip_confs.ip
    assert ip.ip_confs.default_gateway

    qos_mode = sw.system.qos_mode()
    print("qos mode:", qos_mode)
    assert qos_mode.qos_mode

    qos_ports = sw.system.qos_ports()
    print("qos ports:", qos_ports)
    assert qos_ports
    assert qos_ports[0].port_no >= 1
    assert 0 <= qos_ports[0].priority <= 7  # don't assume more than "priority is PCP-like"

    qos_bc = sw.system.qos_broadcast()
    print("qos broadcast:", qos_bc)
    assert isinstance(qos_bc.broadcast_filtering, bool)

    ports = sw.ports.get()
    print("ports:", ports)
    assert ports, "No ports returned"

    # If we have a known model with a known constraint, enforce it
    if sw.profile.expected_port_count is not None:
        assert len(ports) == sw.profile.expected_port_count

    stats = sw.ports.statistics()
    print("port stats:", stats)
    assert stats
    assert stats[0].port_no >= 1
    assert stats[0].bytes_recv >= 0
    assert stats[0].bytes_send >= 0

    pvid = sw.ports.pvid()
    print("pvid:", pvid)
    assert pvid
    assert pvid[0].port_no >= 1
    assert pvid[0].pvid >= 1

    rl = sw.ports.ratelimit()
    print("ratelimit:", rl)
    assert rl
    assert rl[0].port_no >= 1
    assert rl[0].tx_limit_kbps  # "NONE" is still truthy
    assert rl[0].rx_limit_kbps

    storm = sw.ports.stormcontrol()
    print("stormcontrol:", storm)
    assert storm
    assert storm[0].port_no >= 1
    assert storm[0].limit_kbps  # "NONE" is truthy

    pled = sw.ports.led()
    print("ports led:", pled)
    assert isinstance(pled.enabled, bool)

    pow_led = sw.power.led()
    print("power led:", pow_led)
    assert isinstance(pow_led.enabled, bool)

    acl = sw.access_control.get()
    print("acl:", acl)
    assert isinstance(acl, list)

    mode = sw.vlan.mode()
    print("vlan mode:", mode)
    assert mode.mode in ("none", "basic", "advanced")  # don't over-assume

    vlans = sw.vlan.basic1q_vlans()
    print("basic1q vlans:", vlans)
    assert vlans
    assert vlans[0].vlan_id >= 1

    vports = sw.vlan.basic_ports()
    print("basic vlan ports:", vports)
    assert vports
    assert vports[0].port_no >= 1

    conf = sw.vlan.basic1q_conf()
    print("basic1q conf:", conf)
    assert conf
    assert conf[0].port_no >= 1
    assert conf[0].mode in ("Access", "Trunk")  # don't assume more than we saw

    mgmt = sw.vlan.basic1q_mgmt_interface()
    print("basic1q mgmtinterface:", mgmt)
    assert isinstance(mgmt.vlan_id, int)
    assert mgmt.vlan_id >= 0

    adv = sw.vlan.advanced1q()
    print("advanced1q:", adv)
    assert adv
    assert adv[0].vlan_id >= 1

    advp = sw.vlan.advanced_ports()
    print("advanced ports:", advp)
    assert advp
    assert advp[0].vlan_id >= 1

    oui = sw.vlan.advanced1q_oui()
    print("advanced1q oui:", oui)
    assert oui.voice  # should have Siemens/Cisco/etc on your box

    amgmt = sw.vlan.advanced1q_mgmt_interface()
    print("advanced1q mgmtinterface:", amgmt)
    assert isinstance(amgmt.vlan_id, int)
    assert amgmt.vlan_id >= 0

    lag = sw.lag.get()
    print("lag:", lag)

    if sw.profile.expected_lag_group_count is not None:
        assert len(lag) == sw.profile.expected_lag_group_count

    mc = sw.multicast.get()
    print("multicast:", mc)
    assert isinstance(mc.snooping_enable, bool)
    assert mc.vlan_id >= 1
    assert isinstance(mc.static_port, str)

    mc_raw = sw.multicast.get_raw()
    assert isinstance(mc_raw.payload, dict)










