# WIFI Hacking4

> 找到附件中唯一的一个“乱入”的手机，这部手机没有连接上任何一个热点，但暴漏了它曾经连过很多热点。请将这些热点的SSID集合填入到以下网址并提交，获得通关flag。

## 测试代码：

* 分析：Probe request中找到所有发送含ssid请求但没有发送broadcast连接请求（如下图所示），没有收到Probe response的即为没有连接上任何一个热点的手机，再从该手机发送的Probe request中找到连接过的热点的ssid集合

<img src="image\1.png" />

* 根据此原理编写代码

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
        
```

## 运行结果：

<img src="image\2.png" />

## 参考资料：

1.[**关于python Scapy Dot11(802.11)的关键参数说明(自用)**](https://blog.csdn.net/weixin_43815930/article/details/89489899)

2.[无线WiFi探针](https://wenku.baidu.com/view/6f17efb1ba4cf7ec4afe04a1b0717fd5360cb2cb.html)