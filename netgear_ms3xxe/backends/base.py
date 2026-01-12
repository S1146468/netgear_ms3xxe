# netgear_ms3xxe/backends/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol, Any

from ..router import Router
from ..transport import Transport


@dataclass(frozen=True)
class BackendWiring:
    """
    The backend owns how a switch is wired together (transport/router/auth/domains).
    Client should not know backend-specific details.
    """
    transport: Transport
    router: Router
    auth: Any  # concrete type depends on backend (e.g., AuthManager)
    domains: Dict[str, Any]  # e.g. {"system": SystemAPI(...), "ports": PortsAPI(...)}


class SwitchBackend(Protocol):
    backend_id: str

    def build(self, base_url: str, password: str, *, timeout: float = 5.0) -> BackendWiring:
        """
        Must produce a fully authenticated wiring (login included) or raise.
        """
        ...
