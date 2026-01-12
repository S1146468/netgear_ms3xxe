from dataclasses import dataclass

@dataclass(frozen=True)
class PortPvidConf:
    port_no: int
    pvid: int
    vlan: str  # observed: "1"
