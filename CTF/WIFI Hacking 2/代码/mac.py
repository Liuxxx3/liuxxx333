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

pkts = rdpcap(pcap)
for pkt in pkts:
    if not pkt.haslayer(Dot11Elt):
        continue
    if pkt.subtype == 5:  
        if pkt.getlayer(Dot11Elt).info.decode('gbk') == 'a101e-guest':
            ssids.add(pkt.addr1)


for essid in ssids:
    print(essid)