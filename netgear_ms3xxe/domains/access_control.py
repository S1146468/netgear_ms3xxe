from ..models.access_control import AccessRuleIP


class AccessControlAPI:
    def __init__(self, router):
        self.router = router

    def get(self):
        j = self.router.call("access.get")
        rules = [AccessRuleIP(ip=r["ipAddr"], mask=r["mask"]) for r in j["accessConfs"]]
        for rule in rules:
            rule.validate()
        return rules
