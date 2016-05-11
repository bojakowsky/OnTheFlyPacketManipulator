from enum import Enum
from IPTableRule import *


class IPTableRuleUDP(IPTableRule):
    def __init__(self, sport, dport):
        self.sport = sport
        self.dport = dport