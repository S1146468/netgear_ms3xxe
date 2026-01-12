from dataclasses import dataclass

@dataclass(frozen=True)
class QosMode:
    qos_mode: str  # observed: "802.1p/DSCP"
