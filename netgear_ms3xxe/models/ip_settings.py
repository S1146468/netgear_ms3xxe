from __future__ import annotations
from dataclasses import dataclass
from ipaddress import IPv4Address

@dataclass(frozen=True)
class IPConfs:
    configuration: str
    ip: str
    submask: str
    default_gateway: str
    dns1_ip: str
    dns2_ip: str

    def validate(self) -> None:
        if self.configuration not in ("static", "dhcp"):
            # don't assume more modes than observed/typical
            raise ValueError(f"Unknown IP configuration mode: {self.configuration}")
        IPv4Address(self.ip)
        IPv4Address(self.submask)          # yes, mask is dotted-quad in your payload
        IPv4Address(self.default_gateway)
        IPv4Address(self.dns1_ip)
        if self.dns2_ip:
            IPv4Address(self.dns2_ip)

@dataclass(frozen=True)
class IPSettings:
    ip_confs: IPConfs

    @staticmethod
    def from_api(j: dict) -> "IPSettings":
        c = j["ipConfs"]
        out = IPSettings(
            ip_confs=IPConfs(
                configuration=str(c.get("configuration", "")),
                ip=str(c.get("IP", "")),
                submask=str(c.get("submask", "")),
                default_gateway=str(c.get("defaultGateway", "")),
                dns1_ip=str(c.get("dns1IP", "")),
                dns2_ip=str(c.get("dns2IP", "")),
            )
        )
        out.ip_confs.validate()
        return out
