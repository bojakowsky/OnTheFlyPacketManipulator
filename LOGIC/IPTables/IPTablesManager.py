from enum import Enum
from subprocess import call
from IPTableRule import *

class IPTableRulesManager:
    rulesDict = {}
    policyDict = {}
    ruleId = 0
    def add_table_rules_manager(self, ipTableRule):
        IPTableRulesManager.rulesDict[IPTableRulesManager.ruleId] = ipTableRule;
        IPTableRulesManager.ruleId += 1

    def add_rule_ICMP(self, ipTableRuleICMP):
        add_table_rules_manager(ipTableRuleICMP)
        callBegin = build_rule(ipTableRule)

        call(callBegin)

    def add_rule_UDP(self, ipTableRuleUDP):
        add_table_rules_manager(ipTableRuleUDP)
        callBegin = build_rule(ipTableRule)
        call(callBegin)

    def add_rule_TCP(self, ipTableRuleTCP):
        add_table_rules_manager(ipTableRuleTCP)
        callBegin = build_rule(ipTableRule)
        call(callBegin)

    def add_rule(self, ipTableRule):
        callBegin = build_rule(ipTableRule)
        call(callBegin)

    def build_rule(self, ipTableRule):
        callBegin = ["iptables", '-t',
                     ipTableRule.tableType.value,
                     TableActionEnum.add_back_to_chain.value,
                     ipTableRule.chain.value]

        if ipTableRule.source is not None:
            callBegin.append('-s')
            callBegin.append(ipTableRule.source)
        if ipTableRule.destination is not None:
            callBegin.append('-d')
            callBegin.append(ipTableRule.destination)
        if ipTableRule.limit is not None:
            callBegin.append('-m')
            callBegin.append('limit')
            callBegin.append('--limit')
            callBegin.append(ipTableRule.limit)
        callBegin.append('-j')
        callBegin.append(ipTableRule.chainTarget.value)
        return callBegin

    def remove_rule(self, ruleId):
        objToDelete = IPTableRulesManager.rulesDict[ruleId]
        call(["iptables", '-t',
              objToDelete.tableType.value,
              TableActionEnum.delete_from_chain.value,
              objToDelete.chain.value, '-j', objToDelete.chainTarget.value])
        del IPTableRulesManager.rulesDict[ruleId]
        print(len(IPTableRulesManager.rulesDict))

    def set_chain_policy(self, ipTablePolicy):
        call(["iptables", '-t',
              ipTablePolicy.tableType.value,
              TableActionEnum.set_default_chain_policy.value,
              ipTablePolicy.chain.value,
              ipTablePolicy.chainTarget.value])
        IPTableRulesManager.policyDict[ipTablePolicy.chain.value] = ipTablePolicy.chainTarget.value


class TableActionEnum(Enum):
    add_back_to_chain = '-A'  # add to the end of the chain
    set_default_chain_policy = '-P'  # setting default chain policy
    delete_from_chain = '-D'  # deleting from the chain


def test():
    rulesManager = IPTableRulesManager()
    tableRule = IPTableRule(TableTypeEnum.filter, ChainEnum.output, ChainTargetEnum.drop, None, None, None)
    rulesManager.add_rule(tableRule)
    rulesManager.remove_rule(0)
    tableRule.source = "192.168.111.111"
    tableRule.destination = "192.168.111.112"
    tableRule.limit = "4/m"
    rulesManager.add_rule(tableRule)
    tablePolicy = IPTablePolicy(TableTypeEnum.filter, ChainEnum.input, ChainTargetEnum.accept, )
    rulesManager.set_chain_policy(tablePolicy)
    print(len(IPTableRulesManager.rulesDict))

test()