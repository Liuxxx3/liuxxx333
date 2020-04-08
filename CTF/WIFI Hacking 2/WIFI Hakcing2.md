# WIFI Hacking2

> 分析附件提供的pcap中有多少可用AP？将不重复的SSID提交到以下网址，获取通关flag。

## 测试代码：

* 在Probe response中可找到ssid名为 'a101e-guest'的帧，再输出pkt包中的add1（dst mac）即可

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
```

## 运行结果：

<img src="image\1.png" />