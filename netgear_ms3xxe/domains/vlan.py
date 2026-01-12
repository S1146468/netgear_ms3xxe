from typing import List

from ..models.vlan import (
    VlanMode,
    VlanBasic1qEntry,
    VlanBasicPortConf,
    VlanBasic1qPortConf,
    VlanMgmtInterface,
    VlanAdvanced1qEntry,
    VlanAdvancedPortEntry,
    OuiEntry,
    VlanOuiConfs,
)


class VlanAPI:
    def __init__(self, router):
        self.router = router

    def mode(self) -> VlanMode:
        j = self.router.call("vlans.mode.get")
        mode = j["vlanModeConfs"]["mode"]
        return VlanMode(mode=mode)

    def basic1q_vlans(self) -> List[VlanBasic1qEntry]:
        j = self.router.call("vlans.basic1q.vlan.get")
        return [
            VlanBasic1qEntry(vlan_id=v["vlanID"], vlan_name=v.get("vlanName", ""))
            for v in j["vlanBasic1qVlan"]
        ]

    def basic_ports(self) -> List[VlanBasicPortConf]:
        j = self.router.call("vlans.basicport.get")
        out: List[VlanBasicPortConf] = []
        for p in j["vlanBasicConfs"]:
            out.append(
                VlanBasicPortConf(
                    port_no=p["portNo"],
                    port_name=p.get("portName", ""),
                    vlan_id=int(p["vlanID"]),  # normalize "1" -> 1
                )
            )
        return out

    def basic1q_conf(self) -> List[VlanBasic1qPortConf]:
        j = self.router.call("vlans.basic1q.conf.get")
        return [
            VlanBasic1qPortConf(
                port_no=p["portNo"],
                mode=p["mode"],
                vlan_id=int(p["vlanID"]),
            )
            for p in j["vlanBasic1qConfs"]
        ]

    def basic1q_mgmt_interface(self) -> VlanMgmtInterface:
        j = self.router.call("vlans.basic1q.mgmtinterface.get")
        return VlanMgmtInterface(vlan_id=int(j["mgmtInterface"]["vlanID"]))

    def advanced1q(self) -> List[VlanAdvanced1qEntry]:
        j = self.router.call("vlans.advanced1q.get")
        return [
            VlanAdvanced1qEntry(
                vlan_id=v["vlanID"],
                vlan_name=v.get("vlanName", ""),
                tagged_ports=v.get("tagged_ports", ""),
                untagged_ports=v.get("untagged_ports", ""),
                excluded_ports=v.get("excluded_ports", ""),
                vlan_state=v.get("vlanState", ""),
                voice_cos=v.get("voiceCos", 0),
                camera_cos=v.get("cameraCos", 0),
                wifi_cos=v.get("wifiCos", 0),
            )
            for v in j["vlanAdv1qConfs"]
        ]

    def advanced_ports(self) -> List[VlanAdvancedPortEntry]:
        j = self.router.call("vlans.advancedport.get")
        return [
            VlanAdvancedPortEntry(
                vlan_id=v["vlanID"],
                vlan_name=v.get("vlanName", ""),
                member_ports=v.get("member_ports", ""),
            )
            for v in j["vlanAdvConfs"]
        ]

    def advanced1q_oui(self) -> VlanOuiConfs:
        j = self.router.call("vlans.advanced1q.oui.get")
        c = j["ouiConfs"]

        def parse_list(key: str) -> List[OuiEntry]:
            return [
                OuiEntry(
                    oui_idx=o["ouiIdx"],
                    oui_mac=o["ouiMacAddr"],
                    description=o.get("ouiDescript", ""),
                )
                for o in c.get(key, [])
            ]

        return VlanOuiConfs(
            voice=parse_list("ouiVoiceConfs"),
            camera=parse_list("ouiCameraConfs"),
            wifi=parse_list("ouiWifiConfs"),
        )

    def advanced1q_mgmt_interface(self) -> VlanMgmtInterface:
        j = self.router.call("vlans.advanced1q.mgmtinterface.get")
        return VlanMgmtInterface(vlan_id=int(j["mgmtInterface"]["vlanID"]))
