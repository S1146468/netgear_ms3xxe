from typing import List
from ..models.lag import LagConf


class LagAPI:
    def __init__(self, router):
        self.router = router

    def get(self) -> List[LagConf]:
        j = self.router.call("lag.get")
        return [
            LagConf(
                lag_id=c["lagID"],
                enabled=bool(c["enable"]),
                status=bool(c["status"]),
                static_lacp=bool(c["staticLACP"]),
                ports=c.get("ports", ""),
            )
            for c in j["lagConfs"]
        ]
