from enum import Enum
from IPTableRule import *


class IPTableRuleTCP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, protocol, considerFlags, matchFlags, sport, dport):
        self.considerFlags = considerFlags
        self.matchFlags = matchFlags
        self.sport = sport
        self.dport = dport
        super(self.__class__, self).__init__(tableType, chain, chainTarget, source, destination, limit, protocol)

    def build_add_rule_extended(self):
        addRule = self.build_add_rule()
        addRule = self.build_protocol_specific_rule(addRule)
        return addRule

    def build_remove_rule_extended(self):
        removeRule = self.build_remove_rule()
        removeRule = self.build_protocol_specific_rule(removeRule)
        return removeRule

    def build_protocol_specific_rule(self, rule):
        rule.append('-p')
        rule.append('TCP')
        if self.sport is not None:
            rule.append('--sport')
            rule.append(self.sport)
        if self.dport is not None:
            rule.append('--dport')
            rule.append(self.dport)
        if self.considerFlags is not None:
            if self.matchFlags is not None:
                rule.append('--tcp-flags')
                rule.append(self.considerFlags)
                rule.append(self.matchFlags)
        return rule

class TcpFlags(Enum):
    FIN = "FIN"
    SYN = "SYN"
    ACK = "ACK"
    RST = "RST"
    URG = "URG"
    PSH = "PSH"
