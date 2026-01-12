# netgear_ms3xxe/auth.py
from __future__ import annotations

from .exceptions import NetgearAPIError


class AuthManager:
    def __init__(self, router, transport=None):
        """
        router: Router (preferred)
        transport: only needed if you want to clear cookies on retry
        """
        self.router = router
        self.transport = transport or router.transport
        self.token = None
        self.session_id = None

    def login(self, password: str) -> None:
        last_err = None

        for attempt in (1, 2):
            try:
                j = self.router.call("auth.login", {"password": password})
                self.session_id = j["id"]

                tok = j.get("token")
                if not tok:
                    raise NetgearAPIError(f"Login response missing token: {j}")

                self.token = tok
                self.transport.session.headers["Authorization"] = f"Bearer {tok}"

                self.router.call("auth.login_session", {"id": self.session_id, "status": True})
                return

            except NetgearAPIError as e:
                last_err = e

                if attempt == 1:
                    self.transport.session.cookies.clear()
                    self.transport.session.headers.pop("Authorization", None)
                    continue

                raise

        raise last_err or NetgearAPIError("Login failed")
