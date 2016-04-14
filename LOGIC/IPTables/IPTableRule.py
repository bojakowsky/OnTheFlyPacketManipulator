from enum import Enum
from IPTablePolicy import *


class IPTableRule(IPTablePolicy):
    def __init__(self, tableType, chain, chainTarget):
        self.tableType = tableType
        self.chainTarget = chainTarget
        self.chain = chain


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
