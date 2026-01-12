from dataclasses import dataclass


@dataclass(frozen=True)
class QosPortPriority:
    port_no: int
    priority: int  # observed: 4
