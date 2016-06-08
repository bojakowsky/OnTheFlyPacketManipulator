import nfqueue
from IPy import IP
from LOGIC.Icmp import *
from LOGIC.Tcp import *
from LOGIC.Udp import *
from scapy.all import *

conf.verbose = 0
conf.L3socket = L3RawSocket

from PyQt4.QtCore import QThread

class PacketManager(object):

    def __init__(self, queue, queueRaw):
        print("PacketManager initialized.")
        self.queue = queue
        self.queueRaw = queueRaw

    def run_manager(self):
        q = nfqueue.queue()
        q.open()
        q.bind(socket.AF_INET)
        q.set_callback(self.process)
        q.create_queue(0)
        try:
            print("NFQUEUE ran, socket binded.")
            q.try_run()
        except:
            print(sys.exc_info()[0])
            print("NFQUEUE closed, socket unbinded.")
            q.unbind(socket.AF_INET)
            q.close()

    #def closeQueue(self):
    #    print("NFQUEUE closed, socket unbinded.")
    #    q.unbind(socket.AF_INET)
    #    q.close()


    def process(self, i, payload):
        data = payload.get_data()
        pkt = IP(data)
        proto = pkt.proto

        #print(str(pkt).encode("HEX"))
        # Dropping the packet
        payload.set_verdict(nfqueue.NF_DROP)

        # Some console logging
        print(pkt.summary())

        #Add to multiprocessing queue the data (displayed in table)
        layers = build_packet_layer(pkt)
        dictToDisplay = {}
        for layer in layers:
            dictToDisplay[layer.name] = layer.fields
        self.queue.append(dictToDisplay)

        #Origin not formated data holded in queueRaw, also multiprocess resource
        self.queueRaw.append(data)

        # Check if it is a ICMP packet
        # if proto is 0x01:
        #     if pkt[ICMP].type is 8:
        #         send_echo_reply(pkt)
        #     else:
        #         pass
        # elif proto is 0x11:
        #     send_udp_reply(pkt)
        # elif proto is 0x06:
        #
        #     if pkt[TCP].flags == 0x01:  # FIN flag
        #         pass
        #     elif pkt[TCP].flags == 0x02:  # SYN flag
        #         send_tcp_reply(pkt, 'SA')
        #         pass
        #     elif pkt[TCP].flags == 0x04:  # RST flag
        #         send_tcp_reply(pkt)
        #         pass
        #     elif pkt[TCP].flags == 0x08:  # PSH flag
        #         send_tcp_reply(pkt)
        #         pass
        #     elif pkt[TCP].flags == 0x10:  # ACK flag
        #         send_tcp_reply(pkt)
        #         pass
        #     elif pkt[TCP].flags == 0x20:  # URG flag
        #         send_tcp_reply(pkt)
        #         pass
        #     elif pkt[TCP].flags == 0x40:  # ECE flag
        #         send_tcp_reply(pkt)
        #         pass
        #     elif pkt[TCP].flags == 0x80:  # CWR flag
        #         send_tcp_reply(pkt)
        #         pass
        #     else:
        #         send_tcp_reply(pkt)
        # else:
        #     pass


def build_packet_layer(pkt):
    layers = []
    counter = 0
    while True:
        layer = pkt.getlayer(counter)
        if (layer != None):
            layers.append(layer)
        else:
            break
        counter += 1
    return layers


import sys
from StringIO import StringIO
def get_hexdump_from_packet(pkt):
    s = StringIO()
    sys.stdout = s
    hexdump(pkt)
    hexDump = s.getvalue()
    sys.stdout = sys.__stdout__
    return hexDump


def get_packet_from_raw(raw):
    # strData = raw.decode("HEX")
    pkt = IP(raw)
    return pkt


def send_packet_based_on_layers(layersNew, raw, handleSrcAndDst, handlePorts, handleChksumAndLen):
    pkt = get_packet_from_raw(raw)
    counter = 0
    while True:
        lay = pkt.getlayer(counter)
        if (lay == None):
            send_raw_packet_back(pkt, handleSrcAndDst, handlePorts, handleChksumAndLen)
            break
        else:
            for key, value in lay.fields.iteritems():
                newLay = eval(str(layersNew[counter]))
                lay.fields[key] = newLay[key]
                if "load" in key:
                    pkt[counter - 1].payload = newLay[key]
        counter = counter + 1


def send_auto_packet_back(pkt):
    proto = pkt.proto
    if proto is 0x01:
        if pkt[ICMP].type is 8:
            send_echo_auto_reply(pkt)
        else:
            pass
    elif proto is 0x11:
        send_udp_auto_reply(pkt)
    elif proto is 0x06:
        if pkt[TCP].flags == 0x02:  # SYN flag
            send_tcp_auto_reply(pkt, 'SA')
        else:
            send_tcp_auto_reply(pkt)


def send_fuzzed_packet_back(pkt):
    proto = pkt.proto

    if proto is 0x01:
        send_echo_fuzzed_reply(pkt)
    elif proto is 0x11:
        send_udp_fuzzed_reply(pkt)
    elif proto is 0x06:
        send_tcp_fuzzed_reply(pkt)


def send_raw_packet_back(pkt, handleSrcAndDst, handlePorts, handleChksumAndLen):
    proto = pkt.proto
    if handleSrcAndDst:
        src = pkt[IP].src
        pkt[IP].src = pkt[IP].dst
        pkt[IP].dst = src

    if proto is 0x01:
        send_echo_raw_reply(pkt, handleChksumAndLen)
    elif proto is 0x11:
        send_udp_raw_reply(pkt, handlePorts, handleChksumAndLen)
    elif proto is 0x06:
        send_tcp_raw_reply(pkt, handlePorts, handleChksumAndLen)


