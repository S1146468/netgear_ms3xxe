# netgear_ms3xxe/client.py
from __future__ import annotations


from typing import Optional, Union

from .profiles.registry import detect_profile
from .profiles.base import SwitchProfile
from .exceptions import NetgearAPIError

from .backends.registry import get_backend, all_backends
from .backends.base import SwitchBackend, BackendWiring


def _normalize_base_url(host_or_url: str, *, scheme: str = "http") -> str:
    # You cannot “avoid assumptions” here unless you force the caller to pass a URL.
    # This keeps compatibility while allowing overrides.
    if host_or_url.startswith("http://") or host_or_url.startswith("https://"):
        return host_or_url.rstrip("/")
    return f"{scheme}://{host_or_url}".rstrip("/")


class NetgearSwitchClient:
    """
    Facade over a backend implementation.

    The client must NOT bake in backend-specific behaviors besides:
    - selecting a backend (explicit or best-effort autodetect)
    - choosing a profile (capability metadata) from system.status()
    """

    def __init__(
        self,
        host: str,
        password: str,
        *,
        backend: Optional[Union[str, SwitchBackend]] = None,
        profile: Optional[SwitchProfile] = None,
        timeout: float = 5.0,
        scheme: str = "http",
    ):
        self.host = host
        self.base_url = _normalize_base_url(host, scheme=scheme)

        wiring: Optional[BackendWiring] = None
        chosen_backend: Optional[SwitchBackend] = None
        last_err: Optional[Exception] = None

        if backend is not None:
            chosen_backend = get_backend(backend) if isinstance(backend, str) else backend
            wiring = chosen_backend.build(self.base_url, password, timeout=timeout)
        else:
            # Best-effort autodetect: try each backend by attempting a full login+wiring.
            for b in all_backends():
                try:
                    wiring = b.build(self.base_url, password, timeout=timeout)
                    chosen_backend = b
                    break
                except Exception as e:
                    last_err = e

        if wiring is None or chosen_backend is None:
            raise NetgearAPIError(
                f"No compatible backend found for {self.base_url}. "
                f"Last error: {last_err!r}. "
                "Endpoint unknown — HAR evidence required to add a backend."
            )

        self.backend = chosen_backend
        self.transport = wiring.transport
        self.router = wiring.router
        self.auth = wiring.auth

        # Attach domains as first-class attributes
        self.system = wiring.domains["system"]
        self.ports = wiring.domains["ports"]
        self.vlan = wiring.domains["vlan"]
        self.lag = wiring.domains["lag"]
        self.power = wiring.domains["power"]
        self.multicast = wiring.domains["multicast"]
        self.access_control = wiring.domains["access_control"]

        # Profile selection
        if profile is None:
            status = self.system.status()
            self.profile = detect_profile(status.system_info.model_number)
            self._initial_status = status
        else:
            self.profile = profile
            self._initial_status = None

        # Hard sanity check: if profile claims a backend_id, it must match chosen backend.
        if getattr(self.profile, "backend_id", None) not in (None, self.backend.backend_id):
            raise NetgearAPIError(
                f"Profile/backend mismatch: profile.backend_id={self.profile.backend_id!r} "
                f"!= backend.backend_id={self.backend.backend_id!r}"
            )

    @property
    def backend_id(self) -> str:
        return self.backend.backend_id

    def initial_status(self):
        """
        Returns the status captured during __init__ (if profile autodetect was used),
        else None.
        """
        return self._initial_status
