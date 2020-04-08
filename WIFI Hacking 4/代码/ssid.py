#!/usr/bin/env python
from __future__ import unicode_literals
import os
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import Dot11Elt, rdpcap
pcap = sys.argv[1]
if not os.path.isfile(pcap):
    print('input file does not exist')
    exit(1)
beacon_null = set()
ssids = set()
locals = set()
pkts = rdpcap(pcap)
for pkt in pkts:
    if not pkt.haslayer(Dot11Elt):
        continue
    if pkt.subtype == 5:
        locals.add(pkt.addr1)
    if pkt.subtype == 4:
        if (pkt.addr2 in locals) or (pkt.getlayer(Dot11Elt).info.decode('gbk') == ''):
            pass
        else:
            mac=pkt.addr2
for pkt in pkts:
    if not pkt.haslayer(Dot11Elt):
        continue
    if pkt.subtype == 8:
        locals.add(pkt.getlayer(Dot11Elt).info.decode('gbk'))
    if pkt.subtype == 4:
        ssid=pkt.getlayer(Dot11Elt).info.decode('gbk')
        if (ssid in locals) or (pkt.addr2 !=mac):
            pass
        else:
            ssids.add(pkt.getlayer(Dot11Elt).info.decode('utf-8'))
for essid in ssids:
    print(essid)
        