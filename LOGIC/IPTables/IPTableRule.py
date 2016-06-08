from enum import Enum
from TableActions import *

class IPTableRule(object):
    def __init__(self, tableType, chain, chainTarget, source, destination, limit, protocol):
        self.tableType = tableType
        self.chainTarget = chainTarget
        self.chain = chain
        self.source = source
        self.destination = destination
        self.limit = limit
        self.protocol = protocol

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def build_add_rule(self):
        addRule = ["iptables", '-t',
                     self.tableType,
                     TableActionEnum.add_back_to_chain.value,
                   self.chain]

        if self.source is not None:
            addRule.append('-s')
            addRule.append(self.source)
        if self.destination is not None:
            addRule.append('-d')
            addRule.append(self.destination)
        if self.limit is not None:
            addRule.append('-m')
            addRule.append('limit')
            addRule.append('--limit')
            addRule.append(self.limit)
        addRule.append('-j')
        addRule.append(self.chainTarget)
        return addRule

    def build_remove_rule(self):
        removeRule = ["iptables", '-t',
              self.tableType,
              TableActionEnum.delete_from_chain.value,
              self.chain, '-j', self.chainTarget]
        return removeRule

    def build_protocol_specific_rule(self, rule):
        pass

class TableTypeEnum(Enum):
    filter = 'filter' #default table
    nat = 'nat' #for packets that establish connections
    mangle = 'mangle' #for specialized changes in the packets
    raw = 'raw' #highest priority table, packets go to this table first

class ChainEnum(Enum):
    input = 'INPUT' #executed for incoming packets, puprosed for local machine
    forward = 'FORWARD' #executed for packets that are created localy, purposed for packets going out of the local machine
    output = 'OUTPUT' #execute for packets that routed by local machine, but are not purposed for local machine
    prerouting = 'PREROUTING' #executed for packets from outside before they're routed
    postrouting = 'POSTROUTING' #executed for packets that are leaving the local machine after being routed


class FilterEnum(Enum):
    input = ChainEnum.input
    forward = ChainEnum.forward
    output = ChainEnum.output


class NatEnum(Enum):
    prerouting = ChainEnum.prerouting
    output = ChainEnum.output
    postrouting = ChainEnum.postrouting


class MangleEnum(Enum):
    prerouting = ChainEnum.prerouting
    output = ChainEnum.output
    input = ChainEnum.input
    forward = ChainEnum.forward
    postrouting = ChainEnum.postrouting


class RawEnum(Enum):
    prerouting = ChainEnum.prerouting
    output = ChainEnum.output

class ChainTargetEnum(Enum):
    accept = 'ACCEPT' #receive packet
    drop = 'DROP' #drops the packet without informing the sender
    reject = 'REJECT' #drops the packets and informs the sender about error (default ICMP port unreachable)
    nfqueue = 'NFQUEUE' #adds packet to nfqeueue