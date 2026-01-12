from typing import List

from ..models.ports import PortConf
from ..models.port_statistics import PortStatistics
from ..models.port_pvid import PortPvidConf
from ..models.port_ratelimit import PortRateLimitConf
from ..models.port_stormcontrol import PortStormControlConf
from ..models.port_led import PortLedConf


class PortsAPI:
    def __init__(self, router):
        self.router = router

    def get(self):
        j = self.router.call("ports.get")
        return [
            PortConf(
                port_no=p["portNo"],
                name=p.get("portName", ""),
                link_speed_conf=p["linkSpeedConf"],
                link_speed=p["linkSpeed"],
                flow_control=p["flowControl"],
            )
            for p in j["portConfs"]
        ]

    def statistics(self) -> List[PortStatistics]:
        j = self.router.call("ports.statistics")
        return [
            PortStatistics(
                port_no=s["portNo"],
                port_name=s.get("portName", ""),
                bytes_recv=int(s.get("bytesRecv", 0)),
                bytes_send=int(s.get("bytesSend", 0)),
                crc_packets=int(s.get("crcPackets", 0)),
            )
            for s in j["portStatistics"]
        ]

    def pvid(self) -> List[PortPvidConf]:
        j = self.router.call("ports.pvid")
        return [
            PortPvidConf(
                port_no=p["portNo"],
                pvid=int(p["pvid"]),
                vlan=str(p.get("vlan", "")),
            )
            for p in j["pvidConfs"]
        ]

    def ratelimit(self) -> List[PortRateLimitConf]:
        j = self.router.call("ports.ratelimit")
        return [
            PortRateLimitConf(
                port_no=p["portNo"],
                tx_limit_kbps=str(p.get("txLimit_kbps", "")),
                rx_limit_kbps=str(p.get("rxLimit_kbps", "")),
            )
            for p in j["portRateLimitConfs"]
        ]

    def stormcontrol(self) -> List[PortStormControlConf]:
        j = self.router.call("ports.stormcontrol")
        return [
            PortStormControlConf(
                port_no=p["portNo"],
                limit_kbps=str(p.get("limit_kbps", "")),
            )
            for p in j["stormCtrlConfs"]
        ]

    def led(self) -> PortLedConf:
        j = self.router.call("ports.led")
        return PortLedConf(enabled=bool(j["portLEDConfs"]["enable"]))
