from IPTableRule import *


class IPTableRuleICMP(IPTableRule):
    def __init__(self, icmpType, payload):
        self.icmpType = icmpType
        self.payload = payload


