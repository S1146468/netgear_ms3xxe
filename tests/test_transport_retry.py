import pytest
import requests

from netgear_ms3xxe.transport import Transport


class DummySession:
    def __init__(self, outcomes):
        self._outcomes = list(outcomes)  # list[Exception | object]
        self.calls = 0
        self.headers = {}

    def request(self, method: str, url: str, timeout: float, **kwargs):
        self.calls += 1
        out = self._outcomes.pop(0)
        if isinstance(out, Exception):
            raise out
        return out


def test_transport_retries_get_on_timeout():
    resp = object()
    session = DummySession([requests.exceptions.Timeout(), resp])

    t = Transport("http://example", session=session, retries=2, backoff_s=0.0)
    out = t.request("GET", "/x")
    assert out is resp
    assert session.calls == 2


def test_transport_does_not_retry_non_idempotent_methods():
    session = DummySession([requests.exceptions.ConnectionError("boom")])
    t = Transport("http://example", session=session, retries=10, backoff_s=0.0)

    with pytest.raises(requests.exceptions.ConnectionError):
        t.request("POST", "/x", json={"a": 1})

    assert session.calls == 1


def test_transport_gives_up_after_retries_exhausted():
    session = DummySession(
        [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
        ]
    )
    t = Transport("http://example", session=session, retries=2, backoff_s=0.0)

    with pytest.raises(requests.exceptions.Timeout):
        t.request("GET", "/x")

    assert session.calls == 3
