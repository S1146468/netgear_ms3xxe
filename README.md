# netgear-ms3xxe

Python client for **NETGEAR Plus / Easy Smart MS3xxE** switches.

This project wraps the switch’s local HTTP API behind a typed, testable client with clear separation of concerns:
- **Transport**: raw HTTP session (requests)
- **Router**: endpoint registry + request encoding/decoding + error handling + call tracing
- **Auth**: login + session/token handling
- **Domains**: small APIs for system/ports/VLAN/LAG/etc.
- **Profiles**: per-model capability metadata (port count, LAG group count)

> Status: early / pre-release (`version = 0.0.0`). Expect breaking changes.

---

## What’s supported (observed)

- Backend: `ms3xxe-react`
- Models with explicit profiles:
  - `MS305E` (5 ports, 2 LAG groups)
  - `MS308E` (8 ports, 4 LAG groups)

Other models may work **only if** their API matches the same backend. Unknown models fall back to a generic profile.

---

## Install

Requires **Python 3.11+**.

### Editable install (recommended for development)

```bash
pip install -e .[dev]
```

### Runtime-only install (from source tree)

```bash
pip install .
```

Dependencies are intentionally minimal: only `requests` at runtime.

---

## Quickstart

```python
from netgear_ms3xxe.client import NetgearSwitchClient

sw = NetgearSwitchClient(
    host="your-switch-ip",       # or "http://your-switch-ip"
    password="your-switch-password",
    timeout=5.0,
    scheme="http",
)

print("backend:", sw.backend_id)
print("model:", sw.profile.display_name)

status = sw.system.status()
print(status.system_info)

ip = sw.system.ip_settings()
print(ip.ip_confs)

ports = sw.ports.get()
stats = sw.ports.statistics()

vlans = sw.vlan.basic1q_vlans()
lag = sw.lag.get()
mc = sw.multicast.get()
```

---

## API surface (domains)

The client exposes domain objects as attributes:

- `sw.system`
  - `status()`
  - `ip_settings()`
  - `qos_mode()`
  - `qos_ports()`
  - `qos_broadcast()`
- `sw.ports`
  - `get()`
  - `statistics()`
  - `pvid()`
  - `ratelimit()`
  - `stormcontrol()`
  - `led()`
- `sw.power`
  - `led()`
- `sw.access_control`
  - `get()`
- `sw.vlan`
  - `mode()`
  - `basic1q_vlans()`
  - `basic_ports()`
  - `basic1q_conf()`
  - `basic1q_mgmt_interface()`
  - `advanced1q()`
  - `advanced_ports()`
  - `advanced1q_oui()`
  - `advanced1q_mgmt_interface()`
- `sw.lag`
  - `get()`
- `sw.multicast`
  - `get()`
  - `get_raw()` (raw payload wrapper)

Return types are dataclasses in `netgear_ms3xxe/models/*` and generally include basic validation.

---

## Architecture notes

### Endpoint registry is the source of truth

All HTTP calls go through `Router.call(endpoint_id, payload)` where `endpoint_id` is declared in `netgear_ms3xxe/endpoints.py`.

This gives you:
- one place to update paths/methods when firmware changes
- call tracing (`router.calls`) for coverage tests
- hard guardrails that prevent domain code from sneaking in raw URLs

### Backends

A backend wires the stack together (transport/router/auth/domains). The current backend is `ms3xxe-react`.

Autodetect is best-effort:
- if you don’t pass `backend=...`, the client tries all registered backends by doing a full login+wiring
- if none match, the error explicitly calls out that **HAR evidence is required** to add a backend

---

## Testing

This repo distinguishes between:
- **normal tests** (fast, no hardware)
- **live tests** (talk to real switch hardware)

By default, pytest excludes live tests.

### Run normal tests

```bash
pytest
```

### Run live tests

Set environment variables:

- `NETGEAR_SWITCH_HOST`
- `NETGEAR_SWITCH_PASSWORD`

Then run:

```bash
pytest -m live -s
```

Live tests include:
- a smoke test that exercises the domain APIs
- an endpoint coverage test that asserts every declared `endpoint_id` was exercised during the run

---

## Adding support for a new model / firmware

If your switch doesn’t work with the existing backend, don’t guess. Capture evidence.

Suggested workflow:
1. Log into the switch web UI in a browser.
2. Capture network traffic (HAR file or “Copy as cURL” of relevant API calls).
3. Compare against `endpoints.py`.
4. Add/adjust endpoint specs and/or implement a new backend.
5. Add a profile (port count / LAG groups) if you can **verify** those constraints.

---

## Project layout

```
netgear_ms3xxe/
  netgear_ms3xxe/
    backends/
    domains/
    models/
    profiles/
    auth.py
    client.py
    endpoints.py
    router.py
    transport.py
  tests/
```

---

## License

No license file was included in the exported snapshot. Add one if you plan to publish this package.
