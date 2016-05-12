from IPTableRule import *


class IPTableRuleICMP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, icmpType):
        self.icmpType = icmpType
        super(IPTableRuleICMP, self).__init__(tableType, chain, chainTarget, source, destination, limit)


