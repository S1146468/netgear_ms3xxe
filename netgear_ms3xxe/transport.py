# netgear_ms3xxe/transport.py
from __future__ import annotations

from typing import Mapping, Optional
import requests


class Transport:
    """
    HTTP session only.
    No endpoint knowledge, no body encoding logic, no JSON parsing.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        *,
        session: Optional[requests.Session] = None,
        default_headers: Optional[Mapping[str, str]] = None,
    ):
        self.base = base_url.rstrip("/")
        self.timeout = float(timeout)
        self.session = session or requests.Session()
        if default_headers:
            self.session.headers.update(dict(default_headers))

    def request(self, method: str, path: str, **kwargs):
        url = self.base + path
        return self.session.request(method, url, timeout=self.timeout, **kwargs)
