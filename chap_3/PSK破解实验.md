# PSK破解实验

## 实验目的

* 理解 `WPA/WPA2 PSK` 认证方式的认证凭据破解原理并了解使用常见工具进行 `PSK` 口令破解的基本方法；

## 实验环境

- 可以开启监听模式、AP 模式和数据帧注入功能的 USB 无线网卡；
- Kali 虚拟机；
- python scapy；
- aircrack-ng系列软件；
- Wireshark；
- 搭建 **被攻击网络** 所需要使用到的「无线 AP」或「无线路由器」；

## 实验过程

* 在kali虚拟机中使用舍友的网卡，检查无线网卡配置完成后，使用如下命令将网卡调为监听模式，并开始以channel hopping模式抓包

  ```
  airmon-ng check kill
  airmon-ng start wlan0
  airodump-ng wlan0mon
  ```

<img src="image\3.png" />

* 在openwrt中搭建自己的无线网络

<img src="image\6.png" />

<img src="image\8.png" />

* 可查看到附近的ESSID如图所示，找到自己搭建的无线网络，记录BSSID

<img src="image\4.png" />

* 使用`reaver -i wlan0mon -b 80:1F:02:42:0D:45 -vv -S -c 10`对自己搭建的wifi进行暴力破解PIN码，进行等待；

<img src="image\9.png" />

* 使用Pixiewps进行离线破解

根据`pixiewps -e <pke> -r <pkr> -s <e-hash1> -z <e-hash2> -a <authkey> -n <e-nonce>`对reaver抓取到的数据进行分析，从中获取pke pkr 等相关信息

* 当pixiewps破解出PIN码，回到reaver中输入：`reaver -i wlan0mon -b <BSSID MAC> -vv -p <wps PIN>`即可获得密码

* 此处由于使用reaver操作实验时间过长，采用aircrack-ng进行离线破解，输入`airodump-ng -c 10 --bssid 80:1F:02:42:0D:45 -w saved wlan0mon`进行抓包，再在wireshark中将过滤条件改为`eapol`，确认可以抓到四次握手包

<img src="image\11.png" />

* 将此.cap文件使用aircrack-ng破解，使用系统自带的字典与刚刚抓获的数据包saved-01.pacp，得到此ESSID的密码为12345678

```
aircrack-ng -w /usr/share/wordlists/nmap.lst saved-01.pacp
```

<img src="image\12.png" />

<img src="image\13.png" />

## 遇到的问题

* reaver操作一直在运行，但无法得到结果

暴力破解所需时间会由于PIN值复杂程度不同而不同，故reaver操作时间可能很长

## 参考资料

1.https://c4pr1c3.github.io/cuc-mis/chap0x03/main.html （**第三章 无线接入网入侵与防御**）

2.https://www.hackingtutorials.org/wifi-hacking-tutorials/pixie-dust-attack-wps-in-kali-linux-with-reaver/ （**reaver的使用**）