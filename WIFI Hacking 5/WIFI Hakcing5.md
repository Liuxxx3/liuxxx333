# WIFI Hacking5

> 找到WIFI Hacking 4题目附件中哪些AP仅支持使用WPA2 CCMP/AES认证加密模式？请将这些热点的MAC地址集合填入到以下网址并提交，获得通关flag。

## 测试代码：

* 仅含WPA2 CCMP/AES则不含其他加密方式(TKIP)或不加密
* 分析RSN与wireshark中的GCS字段和PCS字段，则PCS和GCS类型都应为CCMP/AES

<img src="image\2.png" />

* wireshark中可看到

加密方式为TKIP,CCMP/AES

<img src="image\3.png" />

加密方式为CCMP/AES

<img src="image\1.png" />

* 根据此原理在wireshark中输入过滤信息

```
(wlan.rsn.pcs.type==4)&&(wlan.rsn.gcs.type==4)
```

## 运行结果：

<img src="image\4.png" />

## 参考资料：

1.[How to use Scapy to determine WPA Encryption?](https://stackoverflow.com/questions/53760266/how-to-use-scapy-to-determine-wpa-encryption)

2.[scapy之ap信息收集](http://www.ijiandao.com/2b/baijia/324266.html)