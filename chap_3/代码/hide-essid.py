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
ssids_hidden = set()

pkts = rdpcap(pcap)
for pkt in pkts:
    if not pkt.haslayer(Dot11Elt):
        continue
    if pkt.subtype == 8:  # Beacon Frame
        if pkt.getlayer(Dot11Elt).info.decode('utf-8').strip('\x00') == '':
            beacon_null.add(pkt.addr3)
    elif pkt.subtype == 5:  # Probe Response
	    ap_channel = str(ord(pkt[Dot11Elt:3].info))
            if pkt.addr3 in beacon_null:
                ssids_hidden.add(pkt.addr3 + '----' + pkt.getlayer(Dot11Elt).info.decode('utf-8')+'----'+ap_channel)

for essid in ssids_hidden:
    print(essid)