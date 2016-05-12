from enum import Enum


class SupportedProtocols(Enum):
    NONE = "NONE" # we choose not to care about the protocol
    ICMP = "ICMP"
    UDP = "UDP"
    TCP = "TCP"