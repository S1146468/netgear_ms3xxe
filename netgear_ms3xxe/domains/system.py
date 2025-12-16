class SystemAPI:
    def __init__(self, router):
        self.router = router

    def status(self):
        return self.router.get("/api/system/status")

    def ip_settings(self):
        return self.router.get("/api/system/settings/ip")
