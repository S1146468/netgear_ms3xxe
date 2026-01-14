import pytest

from netgear_ms3xxe.router import Router
from netgear_ms3xxe.exceptions import NetgearAPIError


class FakeResponse:
    def __init__(self, status_code: int, json_obj=None, *, text="", headers=None):
        self.status_code = status_code
        self._json_obj = json_obj
        self.text = text
        self.headers = headers or {"content-type": "application/json"}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        if self._json_obj is None:
            raise ValueError("no json")
        return self._json_obj


class FakeTransport:
    def __init__(self, responses):
        self._it = iter(responses)

    def request(self, method: str, path: str, **kwargs):
        return next(self._it)


def test_router_401_triggers_one_relogin_and_single_retry():
    relogins = {"n": 0}

    def on_unauthorized():
        relogins["n"] += 1

    transport = FakeTransport(
        [
            FakeResponse(401, text="unauthorized"),
            FakeResponse(200, json_obj={"ok": True}),
        ]
    )
    router = Router(transport)
    router.set_on_unauthorized(on_unauthorized)

    out = router.call("system.status")
    assert out == {"ok": True}
    assert relogins["n"] == 1
    assert router.calls.count("system.status") == 1


def test_router_401_after_retry_raises():
    relogins = {"n": 0}

    def on_unauthorized():
        relogins["n"] += 1

    transport = FakeTransport(
        [
            FakeResponse(401, text="unauthorized"),
            FakeResponse(401, text="unauthorized again"),
        ]
    )
    router = Router(transport)
    router.set_on_unauthorized(on_unauthorized)

    with pytest.raises(NetgearAPIError):
        router.call("system.status")

    assert relogins["n"] == 1
