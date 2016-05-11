from enum import Enum
from IPTableRule import *


class IPTableRuleUDP(IPTableRule):
    def __init__(self, sport, dport, payload):
        self.sport = sport
        self.dport = dport
        self.payload = payload