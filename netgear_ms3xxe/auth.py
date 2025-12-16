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
                j = self.router.patch_textjson("/api/system/login", {"password": password})
                self.session_id = j["id"]

                # token is already set as Authorization by your existing logic elsewhere;
                # but we keep it here for reference.
                # If you want Router/Transport to set it, do it in one place.
                tok = j.get("token")
                if not tok:
                    raise NetgearAPIError(f"Login response missing token: {j}")

                self.token = tok
                self.transport.session.headers["Authorization"] = f"Bearer {tok}"

                self.router.post_textjson("/api/login_session", {"id": self.session_id, "status": True})
                return

            except NetgearAPIError as e:
                last_err = e

                # retry once on known flaky server behavior:
                # clear cookies + auth header then re-login
                if attempt == 1:
                    self.transport.session.cookies.clear()
                    self.transport.session.headers.pop("Authorization", None)
                    continue

                raise

        # unreachable, but keeps type checkers happy
        raise last_err or NetgearAPIError("Login failed")
