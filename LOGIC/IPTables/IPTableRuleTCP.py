from enum import Enum
from IPTableRule import *


class IPTableRuleTCP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, considerFlags, matchFlags, sport, dport):
        self.considerFlags = considerFlags
        self.matchFlags = matchFlags
        self.sport = sport
        self.dport = dport
        super(self.__class__, self).__init__(tableType, chain, chainTarget, source, destination, limit)


class TcpFlags(Enum):
    FIN = "FIN"
    SYN = "SYN"
    ACK = "ACK"
    RST = "RST"
    URG = "URG"
    PSH = "PSH"
