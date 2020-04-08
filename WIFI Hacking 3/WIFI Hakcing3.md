# WIFI Hacking3

> 找到WIFI Hacking 1题目附件中无线客户端尝试连接过但抓包期间信号覆盖范围内不存在的AP的SSID集合，将结果填入到以下网址并提交，获得通关flag。

## 测试代码：

* 分析：Probe request中找到所有携带SSID发送请求，在beacon帧中无法找到此SSID，说明附近不存在此SSID的即为尝试连接过但抓包期间信号覆盖范围内不存在的AP的SSID集合，下图为Probe request的帧结构

> 无线客户端工作过程中，会定期地搜索周围的无线网络，也就是主动扫描周围的无线网络 根据Probe Request帧（探测请求帧）是否携带SSID，可以将主动扫描分为两种：  客户端发送Probe Request帧（SSID为空）：客户端会定期地在其支持的信道列表中 发送探查请求帧（Probe Request）扫描无线网络。当AP收到探查请求帧后 会回应探查响应帧（Probe Response）通告可以提供的无线网络信息 无线客户端通过主动扫描，可以主动获知可使用的无线服务之后无线客户端可以根据需要选择适当的无线网络接入。  客户端发送Probe Request（Probe Request携带指定的SSID）：当无线客户端配置希望连接的无线网络 或者已经成功连接到一个无线网络情况下，客户端也会定期发送探查请求帧（Probe Request）(该报文携带已经配置或者已经连接的无线网络的SSID)，当能够提供指定SSID无线服务的AP接收到探测请求后回复探查响应。

<img src="image\1.png" />

* 在wireshark中找到一个携带了ssid的Probe request帧进行查看，可以找到ssid

<img src="image\2.png" />

* 在beacon帧中无法找到此ssid，说明附近不存在此ssid

<img src="image\3.png" />

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
    if pkt.subtype == 8:
        locals.add(pkt.getlayer(Dot11Elt).info.decode('gbk'))
    if pkt.subtype == 4:
        ssid=pkt.getlayer(Dot11Elt).info.decode('gbk')
        if ssid in locals:
            pass
        else:
            ssids.add(pkt.getlayer(Dot11Elt).info.decode('gbk'))
        
for essid in ssids:
    print(essid)
        
```

## 运行结果：

<img src="image\4.png" />

## 参考资料：

1.[Probe Request](https://www.codetd.com/article/7636260)

2.[无线WiFi探针](https://wenku.baidu.com/view/6f17efb1ba4cf7ec4afe04a1b0717fd5360cb2cb.html)