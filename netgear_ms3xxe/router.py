import json
from dataclasses import dataclass
from typing import Any, Dict
from .endpoints import ENDPOINTS, ALIASES
from .exceptions import NetgearAPIError


@dataclass(frozen=True)
class RequestContext:
    method: str
    path: str
    status: int
    content_type: str
    snippet: str


class Router:
    """
    Router owns request encoding/decoding + errors + request tracking.

    Critical: calls are tracked by endpoint_id (not raw path) so tests can detect drift.
    """

    def __init__(self, transport):
        self.transport = transport
        self.calls: list[str] = []  # endpoint_id call trace



    def call(self, endpoint_id: str, payload: Any | None = None) -> Dict[str, Any]:
        # Resolve aliases to canonical IDs
        endpoint_id = ALIASES.get(endpoint_id, endpoint_id)

        spec = ENDPOINTS.get(endpoint_id)
        if spec is None:
            raise NetgearAPIError(f"Unknown endpoint_id: {endpoint_id!r}")

        # Support both legacy tuple specs and the newer EndpointSpec dataclass.
        if hasattr(spec, "method") and hasattr(spec, "path") and hasattr(spec, "kind"):
            method = spec.method
            path = spec.path
            kind = spec.kind
        else:
            # legacy: ("GET", "/api/...", "json")
            method, path, kind = spec

        self.calls.append(endpoint_id)  # track canonical IDs

        if kind == "json":
            return self._request_json(method, path, kind="json")
        if kind == "textjson":
            return self._request_json(method, path, kind="textjson", text_json_body=payload)

        raise NetgearAPIError(f"Unsupported endpoint kind {kind!r} for endpoint_id {endpoint_id!r}")


    # Hard guardrails: prevent domains from sneaking raw paths back in.
    def get(self, path: str) -> Dict[str, Any]:
        raise NetgearAPIError("Router.get(path) is not allowed. Use Router.call(endpoint_id).")

    def post_textjson(self, path: str, obj: Any | None) -> Dict[str, Any]:
        raise NetgearAPIError("Router.post_textjson(path, ...) is not allowed. Use Router.call(endpoint_id, payload).")

    def patch_textjson(self, path: str, obj: Any | None) -> Dict[str, Any]:
        raise NetgearAPIError("Router.patch_textjson(path, ...) is not allowed. Use Router.call(endpoint_id, payload).")

    def post_json(self, path: str, obj: Any | None) -> Dict[str, Any]:
        raise NetgearAPIError("Router.post_json(path, ...) is not allowed. Use Router.call(endpoint_id, payload).")

    def patch_json(self, path: str, obj: Any | None) -> Dict[str, Any]:
        raise NetgearAPIError("Router.patch_json(path, ...) is not allowed. Use Router.call(endpoint_id, payload).")

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        kind: str,
        text_json_body: Any | None = None,
        json_body: Any | None = None,
    ) -> Dict[str, Any]:
        if text_json_body is not None and json_body is not None:
            raise ValueError("Provide only one of text_json_body or json_body")

        headers: Dict[str, str] = {}
        kwargs: Dict[str, Any] = {}

        if text_json_body is not None:
            headers["Content-Type"] = "text/plain;charset=UTF-8"
            kwargs["data"] = json.dumps(text_json_body, separators=(",", ":"))
        elif json_body is not None:
            kwargs["json"] = json_body

        r = self.transport.request(method, path, headers=headers or None, **kwargs)

        ctype = (r.headers.get("content-type") or "").lower()
        snippet = (r.text or "")[:300].replace("\n", " ")
        ctx = RequestContext(method, path, r.status_code, ctype, snippet)

        if r.status_code == 401:
            raise NetgearAPIError(f"Unauthorized (401) for {method} {path}")

        try:
            r.raise_for_status()
        except Exception as e:
            raise NetgearAPIError(f"HTTP {ctx.status} for {ctx.method} {ctx.path}: {ctx.snippet}") from e

        # Detect SPA / HTML fallback early (common when auth/session breaks)
        if "text/html" in ctx.content_type or ctx.snippet.lstrip().lower().startswith(("<!doctype html", "<html")):
            raise NetgearAPIError(
                f"HTML/SPA fallback for {ctx.method} {ctx.path} "
                f"(ctype={ctx.content_type}): {ctx.snippet}"
            )

        try:
            j = r.json()
        except Exception as e:
            raise NetgearAPIError(
                f"Invalid JSON for {ctx.method} {ctx.path} (ctype={ctx.content_type}): {ctx.snippet}"
            ) from e

        if isinstance(j, dict) and "errCode" in j and j["errCode"] not in (0, None):
            raise NetgearAPIError(f"API error for {ctx.method} {ctx.path}: {j}")

        return j
