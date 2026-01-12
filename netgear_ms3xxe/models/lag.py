from dataclasses import dataclass

@dataclass(frozen=True)
class LagConf:
    lag_id: int
    enabled: bool
    status: bool
    static_lacp: bool
    ports: str  # e.g. "1-2" or ""
