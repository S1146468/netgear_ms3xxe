# netgear_ms3xxe/backends/ms3xxe_react.py
from __future__ import annotations

from typing import Dict, Any

from .base import SwitchBackend, BackendWiring
from ..transport import Transport
from ..router import Router
from ..auth import AuthManager

from ..domains.system import SystemAPI
from ..domains.ports import PortsAPI
from ..domains.vlan import VlanAPI
from ..domains.lag import LagAPI
from ..domains.power import PowerAPI
from ..domains.multicast import MulticastAPI
from ..domains.access_control import AccessControlAPI


class Ms3xxeReactBackend:
    backend_id = "ms3xxe-react"

    def build(self, base_url: str, password: str, *, timeout: float = 5.0) -> BackendWiring:
        # Backend-specific default headers belong HERE (not in domains).
        # Keep transport generic; configure session defaults via backend.
        default_headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": base_url.rstrip("/") + "/",
            "Origin": base_url.rstrip("/"),
        }

        transport = Transport(base_url, timeout=timeout, default_headers=default_headers)
        router = Router(transport)

        auth = AuthManager(router, transport)
        auth.login(password)

        def _relogin() -> None:
            # Make refresh deterministic: clear cookies + auth header, then login again.
            transport.session.cookies.clear()
            transport.session.headers.pop("Authorization", None)
            auth.login(password)

        router.set_on_unauthorized(_relogin)

        domains: Dict[str, Any] = {
            "system": SystemAPI(router),
            "ports": PortsAPI(router),
            "vlan": VlanAPI(router),
            "lag": LagAPI(router),
            "power": PowerAPI(router),
            "multicast": MulticastAPI(router),
            "access_control": AccessControlAPI(router),
        }

        return BackendWiring(transport=transport, router=router, auth=auth, domains=domains)
