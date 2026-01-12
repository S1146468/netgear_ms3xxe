from dataclasses import dataclass

@dataclass(frozen=True)
class PortLedConf:
    enabled: bool
