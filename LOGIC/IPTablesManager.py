from enum import Enum
from subprocess import call, check_call
from LOGIC.IPTables.IPTableRule import *
from LOGIC.IPTables.IPTableRuleUDP import *
from LOGIC.IPTables.IPTableRuleTCP import *
from LOGIC.IPTables.IPTableRuleICMP import *
from LOGIC.IPTables.TableActions import *

class IPTablesManager:
    rulesList = []
    policyList = []
    def add_table_rules_manager(self, ipTableRule):
        IPTablesManager.rulesList.append(ipTableRule)

    def add_rule_ICMP(self, ipTableRuleICMP):
        self.add_table_rules_manager(ipTableRuleICMP)
        callBegin = ipTableRuleICMP.build_add_rule_extended()
        check_call(callBegin)

    def add_rule_UDP(self, ipTableRuleUDP):
        self.add_table_rules_manager(ipTableRuleUDP)
        callBegin = ipTableRuleUDP.build_add_rule_extended()
        check_call(callBegin)

    def add_rule_TCP(self, ipTableRuleTCP):
        self.add_table_rules_manager(ipTableRuleTCP)
        callBegin = ipTableRuleTCP.build_add_rule_extended()
        check_call(callBegin)

    def add_rule(self, ipTableRule):
        self.add_table_rules_manager(ipTableRule)
        callBegin = ipTableRule.build_add_rule()
        check_call(callBegin)
        pass

    def remove_rule(self, ruleId):
        objToDelete = IPTablesManager.rulesList[ruleId]
        if objToDelete.protocol is None:
            check_call(objToDelete.build_remove_rule())
        else:
            check_call(objToDelete.build_remove_rule_extended())
        del IPTablesManager.rulesList[ruleId]
        print(len(IPTablesManager.rulesList))

    def set_chain_policy(self, ipTablePolicy):
        call(["iptables", '-t',
              ipTablePolicy.tableType,
              TableActionEnum.set_default_chain_policy.value,
              ipTablePolicy.chain,
              ipTablePolicy.chainTarget])
        IPTablesManager.policyList[ipTablePolicy.chain] = ipTablePolicy.chainTarget

    def return_table_as_string(self, ipTableRule):
        #members = [attr for attr in dir(ipTableRule) if not callable(attr) and not attr.startswith("__")]
        members = dict(ipTableRule)
        returnVal = ''.join(str(m) + ":" + (str(members[m])+"  ") if members[m] is not None else '' for m in members)
        return returnVal