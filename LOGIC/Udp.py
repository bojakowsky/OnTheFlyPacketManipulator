from impacket.ImpactPacket import UDP
from scapy.all import *


def send_udp_auto_reply(pkt):
    print("send udp reply")
    ip = IP()
    udp = UDP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    udp.sport = pkt[UDP].sport
    udp.dport = pkt[UDP].dport+1
    print(pkt[UDP].payload)
    data = pkt[UDP].payload
    send(ip / udp / data)

def send_udp_fuzzed_reply(pkt):
    ip = IP()
    udp = UDP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport
    send(ip / fuzz(udp))

def send_udp_raw_reply(pkt, handlePorts, handleChksumAndLen):

    if handlePorts:
        pkt[UDP].dport = pkt[UDP].dport + 1
    if handleChksumAndLen:
        del pkt[UDP].chksum
        del pkt.chksum
        del pkt.len
        del pkt[UDP].len
    send(pkt)

