from enum import Enum
from IPTableRule import *


class IPTableRuleUDP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, sport, dport):
        self.sport = sport
        self.dport = dport
        super(IPTableRuleUDP, self).__init__(tableType, chain, chainTarget, source, destination, limit)