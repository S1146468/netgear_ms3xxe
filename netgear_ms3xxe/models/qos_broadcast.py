from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class QosBroadcastConfs:
    broadcast_filtering: bool

    @staticmethod
    def from_api(j: Dict[str, Any]) -> "QosBroadcastConfs":
        c = j["qosBrctConfs"]
        return QosBroadcastConfs(
            broadcast_filtering=bool(c["broadcastFiltering"]),
        )
