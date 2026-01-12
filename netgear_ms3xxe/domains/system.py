from typing import List
from ..models.qos_ports import QosPortPriority
from ..models.qos_mode import QosMode
from ..models.system_status import SystemStatus
from ..models.ip_settings import IPSettings
from ..models.qos_broadcast import QosBroadcastConfs


class SystemAPI:
    def __init__(self, router):
        self.router = router

    def status(self) -> SystemStatus:
        j = self.router.call("system.status")
        return SystemStatus.from_api(j)

    def ip_settings(self) -> IPSettings:
        j = self.router.call("system.ip_settings")
        return IPSettings.from_api(j)

    def qos_mode(self) -> QosMode:
        j = self.router.call("system.qos_mode")
        return QosMode(qos_mode=str(j["qosModeConfs"]["qosMode"]))

    def qos_ports(self) -> List[QosPortPriority]:
        j = self.router.call("system.qos_ports")
        return [
            QosPortPriority(
                port_no=int(p["portNo"]),
                priority=int(p["priority"]),
            )
            for p in j["qosPortConfs"]
        ]

    def qos_broadcast(self) -> QosBroadcastConfs:
        j = self.router.call("system.qos_broadcast")
        return QosBroadcastConfs.from_api(j)
