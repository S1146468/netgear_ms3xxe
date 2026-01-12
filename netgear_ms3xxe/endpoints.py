from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

Kind = Literal["json", "textjson"]
Method = Literal["GET", "POST", "PATCH"]


@dataclass(frozen=True)
class EndpointSpec:
    method: Method
    path: str
    kind: Kind


# Alias map: lets old endpoint_ids continue to work while domains migrate to canonical IDs.
ALIASES: Mapping[str, str] = {
    "vlans.basic1q.vlans.get": "vlans.basic1q.vlan.get",
}


# Single source of truth: endpoint_id -> spec
ENDPOINTS: Mapping[str, EndpointSpec] = {
    # Auth
    "auth.login": EndpointSpec("PATCH", "/api/system/login", "textjson"),
    "auth.login_session": EndpointSpec("POST", "/api/login_session", "textjson"),

    # System
    "system.status": EndpointSpec("GET", "/api/system/status", "json"),
    "system.ip_settings": EndpointSpec("GET", "/api/system/settings/ip", "json"),
    "system.qos_mode": EndpointSpec("GET", "/api/system/settings/qos_mode", "json"),
    "system.qos_ports": EndpointSpec("GET", "/api/system/settings/qos/ports", "json"),
    "system.qos_broadcast": EndpointSpec("GET", "/api/system/settings/qos_broadcast", "json"),

    # Ports
    "ports.get": EndpointSpec("GET", "/api/ports", "json"),
    "ports.statistics": EndpointSpec("GET", "/api/ports/statistics", "json"),
    "ports.pvid": EndpointSpec("GET", "/api/ports/pvid", "json"),
    "ports.ratelimit": EndpointSpec("GET", "/api/ports/ratelimit", "json"),
    "ports.stormcontrol": EndpointSpec("GET", "/api/ports/stormcontrol", "json"),
    "ports.led": EndpointSpec("GET", "/api/ports/led", "json"),

    # Power
    "power.led": EndpointSpec("GET", "/api/power/led", "json"),

    # Access control (MS3xxE Plus)
    "access.get": EndpointSpec("GET", "/api/system/settings/accesscontrol", "json"),

    # VLAN
    "vlans.mode.get": EndpointSpec("GET", "/api/vlans/mode", "json"),
    "vlans.basic1q.vlan.get": EndpointSpec("GET", "/api/vlans/basic1q/vlan", "json"),
    "vlans.basicport.get": EndpointSpec("GET", "/api/vlans/basicport", "json"),
    "vlans.basic1q.conf.get": EndpointSpec("GET", "/api/vlans/basic1q/conf", "json"),
    "vlans.basic1q.mgmtinterface.get": EndpointSpec("GET", "/api/vlans/basic1q/mgmtinterface", "json"),
    "vlans.advanced1q.get": EndpointSpec("GET", "/api/vlans/advanced1q", "json"),
    "vlans.advancedport.get": EndpointSpec("GET", "/api/vlans/advancedport", "json"),
    "vlans.advanced1q.oui.get": EndpointSpec("GET", "/api/vlans/advanced1q/oui", "json"),
    "vlans.advanced1q.mgmtinterface.get": EndpointSpec("GET", "/api/vlans/advanced1q/mgmtinterface", "json"),

    # LAG / Multicast
    "lag.get": EndpointSpec("GET", "/api/lag", "json"),
    "multicast.get": EndpointSpec("GET", "/api/multicast", "json"),
}
