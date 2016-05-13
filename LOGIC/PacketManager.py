import os,sys,nfqueue,socket
from IPy import IP
from impacket.ImpactPacket import ICMP, UDP, TCP
from scapy.all import *

import sys

conf.verbose = 0
conf.L3socket = L3RawSocket

class PacketManager(object):
    def __init__(self):
        q = nfqueue.queue()
        q.open()
        q.bind(socket.AF_INET)
        q.set_callback(self.process)
        q.create_queue(0)
        try:
            q.try_run()
        except:
            print("closing socket")
            q.unbind(socket.AF_INET)
            q.close()

    def send_echo_reply(self, pkt):
        ip = IP()
        icmp = ICMP()
        ip.src = pkt[IP].dst
        ip.dst = pkt[IP].src
        icmp.type = 0
        icmp.code = 0
        icmp.id = pkt[ICMP].id
        icmp.seq = pkt[ICMP].seq
        data = "Icmp reply"
        send(ip/icmp/data, verbose=0)


    def send_udp_reply(self, pkt):
        ip = IP()
        udp = UDP()
        ip.src = pkt[IP].dst
        ip.dst = pkt[IP].src
        udp.id = pkt[UDP].id
        udp.sport = pkt[UDP].dport
        udp.dport = pkt[UDP].sport
        data = "Udp reply"
        send(ip / udp / data, verbose=0)


    def send_tcp_reply(self, pkt, flag):
        ip = IP()
        tcp = TCP()
        ip.src = pkt[IP].dst
        ip.dst = pkt[IP].src
        tcp.ack = pkt[TCP].ack
        tcp.sport = pkt[TCP].dport
        tcp.dport = pkt[TCP].sport
        tcp.flags = flag
        data = "Tcp reply"
        send(ip / tcp / data)


    def process(self, i, payload):
        print("what")
        data = payload.get_data()
        pkt = IP(data)
        proto = pkt.proto

        # Dropping the packet
        payload.set_verdict(nfqueue.NF_DROP)

        # Check if it is a ICMP packet
        if proto is 0x01:
                if pkt[ICMP].type is 8:
                    self.send_echo_reply(pkt)
                else:
                    pass
        elif proto is 0x11:
            self.send_udp_reply(pkt)
        elif proto is 0x06:
            if pkt[TCP].flags == 0x01: #FIN flag
                pass
            elif pkt[TCP].flags == 0x02: #SYN flag
                self.send_tcp_reply(pkt, 0x10)
                pass
            elif pkt[TCP].flags == 0x04: #RST flag
                self.send_tcp_reply(pkt, 0x04)
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
            pass

    def closeQueue(self):
        q.unbind(socket.AF_INET)
        q.close()