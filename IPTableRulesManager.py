from enum import Enum
from subprocess import call


def add_rule(tableType, chain, action, event):
    call(["iptables", '-t',tableType.value, action.value, chain.value, '-j', event.value])
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


class TableActionEnum(Enum):
    add_back_to_chain = '-A' #add to the end of the chain
    set_default_chain_policy = '-P' #setting default chain policy
    delete_from_chain = '-D' #deleting from the chain


class TableActionEventEnum(Enum):
    accept = 'ACCEPT' #receive packet
    drop = 'DROP' #drops the packet without informing the sender
    reject = 'REJECT' #drops the packets and informs the sender about error (default ICMP port unreachable)
    nfqueue = 'NFQUEUE' #adds packet to nfqeueue


def main():
    add_rule(TableTypeEnum.filter, ChainEnum.forward, TableActionEnum.add_back_to_chain, TableActionEventEnum.nfqueue)


main()