from ..models.multicast import MulticastConfs, MulticastConfRaw


class MulticastAPI:
    def __init__(self, router):
        self.router = router

    def get(self) -> MulticastConfs:
        j = self.router.call("multicast.get")
        return MulticastConfs.from_api(j)

    def get_raw(self) -> MulticastConfRaw:
        j = self.router.call("multicast.get")
        return MulticastConfRaw(payload=j)
