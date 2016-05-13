from IPTableRule import *


class IPTableRuleICMP(IPTableRule):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, protocol, icmpType):
        self.icmpType = icmpType
        super(IPTableRuleICMP, self).__init__(tableType, chain, chainTarget, source, destination, limit, protocol)

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
        rule.append('ICMP')
        if self.icmpType is not None:
            rule.append('--icmp-type')
            rule.append(self.icmpType)  # Hex value
        return rule




