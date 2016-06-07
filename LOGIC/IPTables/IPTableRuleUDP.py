from enum import Enum
from IPTableRule import *


class IPTableRuleUDP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, protocol, sport, dport):
        self.sport = sport
        self.dport = dport
        super(IPTableRuleUDP, self).__init__(tableType, chain, chainTarget, source, destination, limit, protocol)

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
        rule.append('UDP')
        if self.sport is not None:
            rule.append('--sport')
            rule.append(self.sport)
        if self.dport is not None:
            rule.append('--dport')
            rule.append(self.dport)
        return rule
