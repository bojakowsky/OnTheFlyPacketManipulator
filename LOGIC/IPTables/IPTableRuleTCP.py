from enum import Enum
from IPTableRule import *


class IPTableRuleTCP(IPTableRule):
    def __init__(self, flags, sport, dport, payload):
        self.flags = flags
        self.sport = sport
        self.dport = dport
        self.payload = payload

class TcpFlags(Enum):
    FIN = "FIN"
    SYN = "SYN"
    ACK = "ACK"
    RST = "RST"
    URG = "URG"
    PSH = "PSH"
