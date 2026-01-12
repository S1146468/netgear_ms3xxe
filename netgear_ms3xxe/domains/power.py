from ..models.power_led import PowerLedConf


class PowerAPI:
    def __init__(self, router):
        self.router = router

    def led(self) -> PowerLedConf:
        j = self.router.call("power.led")
        return PowerLedConf(enabled=bool(j["powerLEDConfs"]["enable"]))
