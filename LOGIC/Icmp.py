from impacket.ImpactPacket import ICMP
from scapy.all import *


def send_echo_auto_reply(pkt):
    print("send echo reply")
    ip = IP()
    icmp = ICMP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    print(ip.dst)
    icmp.type = 0
    icmp.code = 0
    icmp.id = pkt[ICMP].id
    icmp.seq = pkt[ICMP].seq
    data = pkt[ICMP].payload
    send(ip / icmp / data, verbose=0)

def send_echo_fuzzed_reply(pkt):
    ip = IP()
    icmp = ICMP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    send(ip / fuzz(icmp))

def send_echo_raw_reply(pkt, handleChksumAndLen):
    if handleChksumAndLen:
        del pkt[ICMP].chksum
        del pkt.chksum
        del pkt.len
    send(pkt)