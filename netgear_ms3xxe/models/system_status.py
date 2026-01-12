from __future__ import annotations
from dataclasses import dataclass
from ipaddress import IPv4Address
import re

_MAC_RE = re.compile(r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$")

@dataclass(frozen=True)
class SystemInfo:
    switch_name: str
    mac_addr: str
    serial_number: str
    model_number: str
    firmware_version: str
    language: str

    def validate(self) -> None:
        if not self.switch_name:
            raise ValueError("switch_name is empty")
        if not _MAC_RE.match(self.mac_addr):
            raise ValueError(f"mac_addr is not MAC-like: {self.mac_addr}")
        if not self.serial_number:
            raise ValueError("serial_number is empty")
        if not self.model_number:
            raise ValueError("model_number is empty")
        if not self.firmware_version:
            raise ValueError("firmware_version is empty")
        if not self.language:
            raise ValueError("language is empty")

@dataclass(frozen=True)
class SystemStatus:
    system_info: SystemInfo

    @staticmethod
    def from_api(j: dict) -> "SystemStatus":
        si = j["systemInfo"]
        out = SystemStatus(
            system_info=SystemInfo(
                switch_name=str(si.get("switchName", "")),
                mac_addr=str(si.get("macAddr", "")),
                serial_number=str(si.get("serialNumber", "")),
                model_number=str(si.get("modelNumber", "")),
                firmware_version=str(si.get("firmwareVersion", "")),
                language=str(si.get("language", "")),
            )
        )
        out.system_info.validate()
        return out
