from __future__ import annotations

from typing import Any, Mapping, Protocol


class TransportLike(Protocol):
    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any: ...


class RouterLike(Protocol):
    calls: list[str]

    def call(self, endpoint_id: str, payload: Any | None = None) -> Mapping[str, Any]: ...
