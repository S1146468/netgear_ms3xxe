# netgear_ms3xxe/backends/registry.py
from __future__ import annotations

from typing import Iterable, Union

from .base import SwitchBackend
from .ms3xxe_react import Ms3xxeReactBackend

# Instantiate known backends here.
_BACKENDS: list[SwitchBackend] = [
    Ms3xxeReactBackend(),
]


def all_backends() -> Iterable[SwitchBackend]:
    return list(_BACKENDS)


def get_backend(backend: Union[str, SwitchBackend]) -> SwitchBackend:
    if not isinstance(backend, str):
        return backend

    key = backend.strip().lower()
    for b in _BACKENDS:
        if b.backend_id.lower() == key:
            return b

    raise ValueError(f"Unknown backend id: {backend!r}. Known: {[b.backend_id for b in _BACKENDS]}")
