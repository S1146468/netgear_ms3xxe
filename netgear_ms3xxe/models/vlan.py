from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class VlanMode:
    mode: str  # observed: "none"

@dataclass(frozen=True)
class VlanBasic1qEntry:
    vlan_id: int  # observed: vlanID is int
    vlan_name: str  # observed: vlanName is str

@dataclass(frozen=True)
class VlanBasicPortConf:
    port_no: int
    port_name: str
    vlan_id: int  # observed: vlanID comes back as string "1" -> normalize to int

@dataclass(frozen=True)
class VlanBasic1qPortConf:
    port_no: int
    mode: str   # observed: "Access"
    vlan_id: int  # observed: "1" -> normalize to int

@dataclass(frozen=True)
class VlanMgmtInterface:
    vlan_id: int  # observed: 0

@dataclass(frozen=True)
class VlanAdvanced1qEntry:
    vlan_id: int
    vlan_name: str
    tagged_ports: str        # observed: "1-8" style strings (can be "")
    untagged_ports: str
    excluded_ports: str
    vlan_state: str          # observed: "Disabled"
    voice_cos: int
    camera_cos: int
    wifi_cos: int

@dataclass(frozen=True)
class VlanAdvancedPortEntry:
    vlan_id: int
    vlan_name: str
    member_ports: str        # observed: "1-8"

@dataclass(frozen=True)
class OuiEntry:
    oui_idx: int
    oui_mac: str
    description: str

@dataclass(frozen=True)
class VlanOuiConfs:
    voice: List[OuiEntry]
    camera: List[OuiEntry]
    wifi: List[OuiEntry]
