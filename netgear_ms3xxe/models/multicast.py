from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class MulticastConfRaw:
    """
    Raw multicast payload wrapper.
    """
    payload: Dict[str, Any]


@dataclass(frozen=True)
class MulticastConfs:
    snooping_enable: bool
    vlan_id: int
    static_port: str  # observed: "-" (string)
    validate_header: bool
    block_unknown: bool

    @staticmethod
    def from_api(j: Dict[str, Any]) -> "MulticastConfs":
        c = j["multiConfs"]
        return MulticastConfs(
            snooping_enable=bool(c["snoopingEnable"]),
            vlan_id=int(c["vlanID"]),
            static_port=str(c.get("staticPort", "")),
            validate_header=bool(c["validateHeader"]),
            block_unknown=bool(c["blockUnknown"]),
        )
