# WIFI Hacking6

> 找到WIFI Hacking 4题目附件中哪些AP支持WPA/WPA2企业级认证方式？请将这些热点的MAC地址集合填入到以下网址并提交，获得通关flag。

## 测试代码：

* 使用wireshark观察AKM type字段，若为1，则表示为WPA2企业级认证方式，若AKM type字段为2，则 

  为WPA2认证方式

<img src="image\RSN.png" />

* 根据此原理在wireshark中输入下行代码，找到所有AP及mac地址

```
   wlan.rsn.akms.type==1
```

## 运行结果：

<img src="image\type为1.png" />

## 
