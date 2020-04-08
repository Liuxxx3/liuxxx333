# 隐藏ESSID发现实验

## 实验目的

* 理解隐藏 `ESSID` 发现的基本原理，掌握使用 `scapy` 编程完成 `ESSID` 自动识别和提取的方法；

## 实验环境

- 可以开启监听模式、AP 模式和数据帧注入功能的 USB 无线网卡；
- Kali 虚拟机；
- python scapy；
- aircrack-ng系列软件；
- Wireshark；
- 搭建 **被攻击网络** 所需要使用到的「无线 AP」或「无线路由器」；

## 实验过程

* 首先搭建好自己的无线AP

<img src="image\6.png" />

* 在kali虚拟机中使用舍友的网卡，检查无线网卡配置完成后，使用如下命令将网卡调为监听模式，并开始以channel hopping模式抓包

  ```
  airmon-ng check kill
  airmon-ng start wlan0
  airodump-ng wlan0mon
  ```

<img src="image\3.png" />

* 记录下自己的bssid为`80:1F:02:42:0D:45`

<img src="image\4.png" />

* 使用luci来对openwrt进行管理，将ESSID设置为隐藏ESSID，并提交设置

<img src="image\14.png" />

* 此时在wifi连接界面已无法找到该网络

<img src="image\15.png" />

* 在kali虚拟机中再次以channel hopping模式抓包，发现自己搭建AP的ESSID的lenth变为0，说明实现了隐藏ESSID

<img src="image\16.png" />

* 使用如下命令对指定信道进行抓包，同时使用手机试图连入该网络

```
airodump-ng wlan0mon --beacons -c 10 -w hidden
```

<img src="image\17.png" />

* 无论是否正确输入密码，都可在抓包界面中发现隐藏的ESSID（lsy-openwrt）

<img src="image\18.png" />

* 调用python代码使用scapy对抓到的数据包进行分析，得到隐藏ESSID的有关信息

<img src="image\19.png" />

* 使用pkt.show()查看包具体信息，找到信道所在位置，在老师所给代码上加上一行代码得到信道信息

```python
ap_channel = str(ord(pkt[Dot11Elt:3].info))
ssids_hidden.add(pkt.addr3 + '----' + pkt.getlayer(Dot11Elt).info.decode('utf-8')+'----'+ap_channel)
```

<img src="image\26.png" />

## 遇到的问题

* 使用Mircosoft Edge浏览器无法打开luci进行后台管理

解决方法：使用Google浏览器

## 参考资料

1.https://c4pr1c3.github.io/cuc-mis/chap0x03/scapy.html （**Scapy示例代码阅读理解**）

2.https://blog.csdn.net/cd_xuyue/article/details/48054675 （**自动化WiFI钓鱼工具——WiFiPhisher源码解读**）