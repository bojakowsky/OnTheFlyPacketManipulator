from impacket.ImpactPacket import TCP
from scapy.all import *


flag = {
    'F': 'FIN',
    'S': 'SYN',
    'R': 'RST',
    'P': 'PSH',
    'A': 'ACK',
    'U': 'URG',
    'E': 'ECE',
    'C': 'CWR'
}

def send_tcp_auto_reply(pkt, flag='PA'):
    # p = IP()/TCP(flags=flag) # for further use - we can get char of the flags instead of hex
    # [flags[x] for x in p.sprintf(flag)]
    if flag == 'SA':
        #handled 3 ways handshake
        print("TCP 3 ways handshake send")
        ip = IP()
        tcp = TCP()
        ip.src = pkt[IP].dst
        ip.dst = pkt[IP].src

        tcp.sport = pkt[TCP].dport
        tcp.dport = pkt[TCP].sport

        tcp.ack = pkt[TCP].seq + 1
        tcp.seq = pkt[TCP].ack
        tcp.flags = flag
        send(ip / tcp)

    else:
        print("Send tcp reply")
        ip = IP()
        tcp = TCP()
        ip.src = pkt[IP].dst
        ip.dst = pkt[IP].src
        tcp.ack = pkt[TCP].seq
        tcp.seq = pkt[TCP].ack
        tcp.sport = pkt[TCP].dport
        tcp.dport = pkt[TCP].sport
        tcp.flags = flag
        data = pkt[TCP].payload
        send(ip / tcp / data)

def send_tcp_fuzzed_reply(pkt):
    ip = IP()
    tcp = TCP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    tcp.sport = pkt[TCP].dport
    tcp.dport = pkt[TCP].sport
    send(ip/fuzz(tcp))

def send_tcp_raw_reply(pkt, handlePorts, handleChksumAndLen):
    if handlePorts:
        dport = pkt[TCP].dport
        pkt[TCP].dport = pkt[TCP].sport
        pkt[TCP].sport = dport
    if handleChksumAndLen:
        del pkt[TCP].chksum
        del pkt.chksum
        del pkt.len
    send(pkt)
