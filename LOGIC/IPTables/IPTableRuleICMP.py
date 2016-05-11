from IPTableRule import *


class IPTableRuleICMP(IPTableRule):
    def __init__(self, icmpType):
        self.icmpType = icmpType


