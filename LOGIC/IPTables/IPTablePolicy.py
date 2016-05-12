from enum import Enum


class IPTablePolicy(object):
    def __init__(self, tableType, chain, chainTarget):
        self.tableType = tableType
        self.chainTarget = chainTarget
        self.chain = chain

class TableTypeEnum(Enum):
    filter = 'filter' #default table
    nat = 'nat' #for packets that establish connections // not working
    mangle = 'mangle' #for specialized changes in the packets
    raw = 'raw' #highest priority table, packets go to this table first // not working

class ChainEnum(Enum):
    input = 'INPUT' #executed for incoming packets, puprosed for local machine
    forward = 'FORWARD' #executed for packets that are created localy, purposed for packets going out of the local machine
    output = 'OUTPUT' #execute for packets that routed by local machine, but are not purposed for local machine

class ChainTargetEnum(Enum):
    accept = 'ACCEPT' #receive packet
    drop = 'DROP' #drops the packet without informing the sender
    reject = 'REJECT' #drops the packets and informs the sender about error (default ICMP port unreachable)