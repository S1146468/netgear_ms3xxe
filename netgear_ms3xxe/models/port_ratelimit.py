from dataclasses import dataclass

@dataclass(frozen=True)
class PortRateLimitConf:
    port_no: int
    tx_limit_kbps: str  # observed: "NONE" or a number-as-string
    rx_limit_kbps: str
