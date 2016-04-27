#ans, unans = sr(IP(dst="192.168.0.100")/ICMP())
#ans.nsummary()
#ans.nsummary(lambda (s, r): r.sprintf("%IP.src% is alive"))

#a = sniff(count=10)
#a.nsummary()

#res, unans = sr( IP(dst="192.168.0.1")/TCP(dport=(1,100)) )
#res.nsummary( lfilter=lambda (s, r): (r.haslayer(TCP) and (r.getlayer(TCP).flags & 2)))
#ayer(TCP) and (r.getlayer(TCP).flags & 2)))r


#ans, unans = sr(IP(dst="192.168.0.11")/TCP("dsadasdsadsasadsaddasads"))
#print("Answered:")
#ans.nsummary()

#print("Unanswered")
#unans.nsummary()
#an,na = srloop(IP(dst="192.168.0.11")/TCP()/"TestMessage", count=100)
#an.show()
#na.show()
#print("\n")

import os,sys,nfqueue,socket
from IPy import IP
from impacket.ImpactPacket import ICMP, UDP, TCP

from scapy.all import *

import sys
from PyQt4 import QtGui

conf.verbose = 0
conf.L3socket = L3RawSocket


def send_echo_reply(pkt):
    ip = IP()
    icmp = ICMP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    icmp.type = 0
    icmp.code = 0
    icmp.id = pkt[ICMP].id
    icmp.seq = pkt[ICMP].seq
    print("[ICMP] Sending echo reply to %s" % ip.dst)
    data = "Icmp reply"
    send(ip/icmp/data, verbose=0)


def send_udp_reply(pkt):
    ip = IP()
    udp = UDP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    udp.id = pkt[UDP].id
    udp.sport = pkt[UDP].dport
    udp.dport = pkt[UDP].sport
    print("[UDP] Sending UDP reply to %s" % ip.dst)
    data = "Udp reply"
    send(ip / udp / data, verbose=0)


def send_tcp_reply(pkt, flag):
    ip = IP()
    tcp = TCP()
    ip.src = pkt[IP].dst
    ip.dst = pkt[IP].src
    tcp.ack = pkt[TCP].ack
    tcp.sport = pkt[TCP].dport
    tcp.dport = pkt[TCP].sport
    tcp.flags = flag
    print("[UDP] Sending TCP reply to %s" % ip.dst)
    data = "Tcp reply"
    send(ip / tcp / data)


def process(i, payload):
    data = payload.get_data()
    pkt = IP(data)
    proto = pkt.proto

    # Dropping the packet
    payload.set_verdict(nfqueue.NF_DROP)

    # Check if it is a ICMP packet
    if proto is 0x01:
            print("[ICMP] ICMP packet received.")
            # Idea: intercept an echo request and immediately send back an echo reply packet
            if pkt[ICMP].type is 8:
                print("[ICMP] Echo request detected.")
                print("[ICMP] " + str(pkt[ICMP].payload))
                send_echo_reply(pkt)
            else:
                pass
    elif proto is 0x11:
        print ("[UDP] UDP packet received.")
        print ("[UDP] " + str(pkt[UDP].payload))
        send_udp_reply(pkt)
    elif proto is 0x06:
        print ("[TCP] TCP packet received.")
        if pkt[TCP].flags == 0x01: #FIN flag
            pass
        elif pkt[TCP].flags == 0x02: #SYN flag
            print ("[TCP] " + str(pkt[TCP].payload))
            send_tcp_reply(pkt, 0x10)
            pass
        elif pkt[TCP].flags == 0x04: #RST flag
            print("TCP " + str(pkt[TCP].payload))
            send_tcp_reply(pkt, 0x04)
            pass
        elif pkt[TCP].flags == 0x08: #PSH flag
            pass
        elif pkt[TCP].flags == 0x10: #ACK flag
            pass
        elif pkt[TCP].flags == 0x20: #URG flag
            pass
        elif pkt[TCP].flags == 0x40: #ECE flag
            pass
        elif pkt[TCP].flags == 0x80: #CWR flag
            pass
    else:
        print("[Error] Protocol not handled.")
        pass


def main():
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(process)
    q.create_queue(0)

    try:
        q.try_run()
    except KeyboardInterrupt:
        print("[Exit] Closing socket.")
        q.unbind(socket.AF_INET)
        q.close()
        sys.exit(1)

main()


# sudo iptables -L
# sudo iptables -A INPUT -p UDP --dport 60 -j NFQUEUE
# sudo iptables -A INPUT -p ICMP --icmp-type echo-request -j NFQUEUE
#for deleting: sudo iptables -D INPUT 1
# sudo scapy
# ps -aux | grep "Test.py" | grep -v grep | wc -l # testing if process is running


