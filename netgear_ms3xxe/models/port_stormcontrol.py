from dataclasses import dataclass

@dataclass(frozen=True)
class PortStormControlConf:
    port_no: int
    limit_kbps: str  # observed: "NONE" or numeric string
