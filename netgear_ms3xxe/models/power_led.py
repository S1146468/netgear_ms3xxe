from dataclasses import dataclass

@dataclass(frozen=True)
class PowerLedConf:
    enabled: bool
