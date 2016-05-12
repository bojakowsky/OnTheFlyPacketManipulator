from enum import Enum
from subprocess import call, check_call
from IPTableRule import *

class IPTablesManager:
    rulesDict = {}
    policyDict = {}
    ruleId = 0
    def add_table_rules_manager(self, ipTableRule):
        IPTablesManager.rulesDict[IPTablesManager.ruleId] = ipTableRule;
        IPTablesManager.ruleId += 1

    def add_rule_ICMP(self, ipTableRuleICMP):
        self.add_table_rules_manager(ipTableRuleICMP)
        callBegin = self.build_rule(ipTableRuleICMP)
        callBegin.append('-p')
        callBegin.append('ICMP')
        if ipTableRuleICMP.icmpType is not None:
            callBegin.append('--icmp-type')
            callBegin.append(ipTableRuleICMP.icmpType) #Hex value
        check_call(callBegin)

    def add_rule_UDP(self, ipTableRuleUDP):
        self.add_table_rules_manager(ipTableRuleUDP)
        callBegin = self.build_rule(ipTableRuleUDP)
        callBegin.append('-p')
        callBegin.append('UDP')
        if ipTableRuleUDP.sport is not None:
            callBegin.append('--dport')
            callBegin.append(ipTableRuleUDP.dport)
        if ipTableRuleUDP.dport is not None:
            callBegin.append('--sport')
            callBegin.append(ipTableRuleUDP.sport)
        check_call(callBegin)

    def add_rule_TCP(self, ipTableRuleTCP):
        self.add_table_rules_manager(ipTableRuleTCP)
        callBegin = self.build_rule(ipTableRuleTCP)
        callBegin.append('-p')
        callBegin.append('TCP')
        if ipTableRuleTCP.sport is not None:
            callBegin.append('--dport')
            callBegin.append(ipTableRuleTCP.dport)
        if ipTableRuleTCP.dport is not None:
            callBegin.append('--sport')
            callBegin.append(ipTableRuleTCP.sport)
        if ipTableRuleTCP.considerFlags is not None:
            if ipTableRuleTCP.matchFlags is not None:
                callBegin.append('--tcp-flags')
                callBegin.append(ipTableRuleTCP.considerFlags)
                callBegin.append(ipTableRuleTCP.matchFlags)
        check_call(callBegin)

    def add_rule(self, ipTableRule):
        self.add_table_rules_manager(ipTableRule)
        callBegin = self.build_rule(ipTableRule)
        check_call(callBegin)
        pass

    def build_rule(self, ipTableRule):
        callBegin = ["iptables", '-t',
                     ipTableRule.tableType,
                     TableActionEnum.add_back_to_chain.value,
                     ipTableRule.chain]

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
        callBegin.append(ipTableRule.chainTarget)
        return callBegin

    def remove_rule(self, ruleId):
        objToDelete = IPTablesManager.rulesDict[ruleId]
        call(["iptables", '-t',
              objToDelete.tableType,
              TableActionEnum.delete_from_chain.value,
              objToDelete.chain, '-j', objToDelete.chainTarget])
        del IPTablesManager.rulesDict[ruleId]
        print(len(IPTablesManager.rulesDict))

    def set_chain_policy(self, ipTablePolicy):
        call(["iptables", '-t',
              ipTablePolicy.tableType,
              TableActionEnum.set_default_chain_policy.value,
              ipTablePolicy.chain,
              ipTablePolicy.chainTarget])
        IPTablesManager.policyDict[ipTablePolicy.chain] = ipTablePolicy.chainTarget

    def return_table_as_string(self, ipTableRule):
        #members = [attr for attr in dir(ipTableRule) if not callable(attr) and not attr.startswith("__")]
        members = dict(ipTableRule)
        returnVal = ''.join(str(m) + ":" + (str(members[m])+"  ") if members[m] is not None else '' for m in members)
        return returnVal


class TableActionEnum(Enum):
    add_back_to_chain = '-A'  # add to the end of the chain
    set_default_chain_policy = '-P'  # setting default chain policy
    delete_from_chain = '-D'  # deleting from the chain