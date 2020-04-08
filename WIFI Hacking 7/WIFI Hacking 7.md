## WIFI Hacking 7

> 找到WIFI Hacking 4题目附件中哪些AP可能是设置了禁止SSID广播？试列举所有的BSSID？请将这些热点的MAC地址集合填入到以下网址并提交，获得通关flag。

* 禁止了SSID广播的AP即在beacon帧中无法看到广播包，但在response帧中可以找到连接信息

### 代码

```python
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
bssids = set()
locals = set()
pkts = rdpcap(pcap)
for pkt in pkts:
    if not pkt.haslayer(Dot11Elt):
        continue
    if pkt.subtype == 8:
        locals.add(pkt.getlayer(Dot11Elt).info.decode('utf-8'))
for pkt in pkts:
    if pkt.subtype == 5:
        ssid=pkt.getlayer(Dot11Elt).info.decode('utf-8');
        if ssid in locals:
            pass
        else:
            bssids.add(pkt.addr2)

for bssid in bssids:
    print(bssid)
        
```

### 运行结果

<img src="image\运行结果.png" />