# netgear_ms3xxe/transport.py
from __future__ import annotations

import time
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
        retries: int = 2,          # GET-only retries (bounded)
        backoff_s: float = 0.2,    # exponential backoff base
    ):
        self.base = base_url.rstrip("/")
        self.timeout = float(timeout)
        self.session = session or requests.Session()
        if default_headers:
            self.session.headers.update(dict(default_headers))

        self.retries = max(0, int(retries))
        self.backoff_s = float(backoff_s)

    def request(self, method: str, path: str, **kwargs):
        url = self.base + path

        # Conservative: retry only idempotent GETs.
        attempts = 1 + self.retries if method.upper() == "GET" else 1
        delay = self.backoff_s

        for attempt in range(1, attempts + 1):
            try:
                return self.session.request(method, url, timeout=self.timeout, **kwargs)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt >= attempts:
                    raise
                time.sleep(delay)
                delay *= 2
