# 基于 VirtualBox 的网络攻防基础环境搭建

---

## 实验目的

- 掌握 VirtualBox 虚拟机的安装与使用；
- 掌握 VirtualBox 的虚拟网络类型和按需配置；
- 掌握 VirtualBox 的虚拟硬盘多重加载；

## 实验环境

以下是本次实验需要使用的网络节点说明和主要软件：

- VirtualBox 虚拟机
- 攻击者主机（Attacker）：Kali Rolling 2019.2
- 网关（Gateway, GW）：Debian Buster
- 靶机（Victim）：From Sqli to shell / xp-sp3 / Kali

## 实验要求

- [x] 靶机可以直接访问攻击者主机
- [x] 攻击者主机无法直接访问靶机
- [x] 网关可以直接访问攻击者主机和靶机
- [x] 靶机的所有对外上下行流量必须经过网关
- [x] 所有节点均可以访问互联网

## 实验过程

* 将虚拟硬盘配置成多重加载，并依次创建靶机（4个，分别是xp-victim1.xp-victim2，kali-victim，debian1），攻击者（kali-attack），网关（debian-gateway）

<img src="image\0.png" />

* 依次进行网络配置，其中靶机均为内部网络，网关有四个网卡，分别是NAT网络，仅主机网络与两个子网（四个靶机分成的两个局域网），攻击者有三个网卡，分别为NAT网络与两个仅主机网络

<img src="image\1.png" />

<img src="image\2.png" />

<img src="image\3.png" />

<img src="image\4.png" />

<img src="image\5.png" />

<img src="image\6.png" />

* 构成如图所示网络拓扑结构，xp-victim1与debian1位于一个网络，xp-victim2与kali-victim2位于一个网络，分别连接到网关上，网关与互联网连接；攻击者与互联网连接，与靶机所在的网络不相连

![img](https://c4pr1c3.github.io/cuc-ns/chap0x01/attach/chap0x01/media/vb-exp-layout.png)

* 分别查看四个靶机，一个网关，一个攻击者的ip地址，观察网络配置是否成功，是否构成如上图所示的拓扑结构，并为后续实验做准备

网关：

<img src="image\7.png" />

四个靶机：

<img src="image\8.png" />

<img src="image\9.png" />

<img src="image\10.png" />

<img src="image\11.png" />

攻击者：

<img src="image\12.png" />

* 由图可得下表，故可知debian1与xp-victim1在同一内部网络，xp-victim2与kali-victim2在同一内部网络

| id           | ip addr           | subnet mask   |
| ------------ | ----------------- | ------------- |
| debian1      | 172.16.111.142/24 | 255.255.255.0 |
| xp-victim1   | 172.16.111.109/24 | 255.255.255.0 |
| kali-victim2 | 172.16.222.138/24 | 255.255.255.0 |
| xp-victim2   | 172.16.222.136/24 | 255.255.255.0 |

网关中包含这两个内部网络，四台靶机分成两个局域网分别连接到网关上，网络拓扑结构正确，可以进行网络连通性实验。

---

## 网络连通性测试

#### 靶机可以直接访问攻击者主机

由于靶机可以经过网关连接到互联网，而攻击者主机也连接到了互联网，靶机可以访问互联网，故可以直接访问攻击者主机。

* xp-victim1可以访问kali-attack

<img src="image\13.png" />

* xp-victim2可以访问kali-attack

<img src="image\14.png" />

* debian1可以访问kali-attack

<img src="image\15.png" />

* kali-victim2可以访问kali-attack

<img src="image\16.png" />

#### 网关可以直接访问攻击者主机和靶机

由于局域网直接连接到网关，故网关可直接访问四台靶机；网关也连接到互联网，攻击者主机也连接到互联网，所以网关可查找到攻击者主机的ip地址，对其进行访问。

* 网关可直接访问攻击者主机

<img src="image\17.png" />

* 网关可以直接访问kali-victim2

<img src="image\18.png" />

* 网关可以直接访问debian1

<img src="image\19.png" />

* 网关可以直接访问xp-victim1

<img src="image\20.png" />

* 网关可以直接访问xp-victim2

<img src="image\21.png" />

#### 攻击者主机无法直接访问靶机

由于攻击者所在主机仅能访问到互联网和互联网所连接的所有机器，而靶机所在网络属于内部网络，连接到网关后才可连接到互联网，所以攻击者主机无法在互联网中找到此ip地址，无法直接访问靶机。

<img src="image\22.png" />

#### 靶机的所有对外上下行流量必须经过网关

由于靶机可以访问互联网，所以在网关中抓取数据包，如果请求数据的包和回复的包可以在网关中被抓到，而**关闭网关所在的虚拟机**以后，所有靶机均无法上网，则说明靶机的所有对外上下行流量必须经过网关。

* xp-victim1

<img src="image\26.png" />

* xp-victim2

<img src="image\27.png" />

由于windows系统与linux系统中ping命令参数不同，查阅资料后得知发一个数据包指令为加后缀`-c `

>https://blog.csdn.net/gechong123/article/details/80609598

>|     参数      | 详解                                                         |
>| :-----------: | :----------------------------------------------------------- |
>|      -a       | Audible ping.                                                |
>|      -A       | 自适应ping，根据ping包往返时间确定ping的速度；               |
>|      -b       | 允许ping一个广播地址；                                       |
>|      -B       | 不允许ping改变包头的源地址；                                 |
>| **-c count**  | ping指定次数后停止ping；                                     |
>|      -d       | 使用Socket的SO_DEBUG功能；                                   |
>| -F flow_label | 为ping回显请求分配一个20位的“flow label”，如果未设置，内核会为ping随机分配； |
>|    **-f**     | 极限检测，快速连续ping一台主机，ping的速度达到100次每秒；    |
>|  -i interval  | 设定间隔几秒发送一个ping包，默认一秒ping一次；               |
>| -I interface  | 指定网卡接口、或指定的本机地址送出数据包；                   |
>|  -l preload   | 设置在送出要求信息之前，先行发出的数据包；                   |
>|      -L       | 抑制组播报文回送，只适用于ping的目标为一个组播地址           |
>|      -n       | 不要将ip地址转换成主机名；                                   |
>|  -p pattern   | 指定填充ping数据包的十六进制内容，在诊断与数据有关的网络错误时这个选项就非常有用，如：“-p ff”； |
>|      -q       | 不显示任何传送封包的信息，只显示最后的结果                   |
>|    -Q tos     | 设置Qos(Quality of Service)，它是ICMP数据报相关位；可以是十进制或十六进制数，详见rfc1349和rfc2474文档； |
>|      -R       | 记录ping的路由过程(IPv4 only)； 注意：由于IP头的限制，最多只能记录9个路由，其他会被忽略； |
>|      -r       | 忽略正常的路由表，直接将数据包送到远端主机上，通常是查看本机的网络接口是否有问题；如果主机不直接连接的网络上，则返回一个错误。 |
>|   -S sndbuf   | Set socket sndbuf. If not specified, it is selected to buffer not more than one packet. |
>| -s packetsize | 指定每次ping发送的数据字节数，默认为“56字节”+“28字节”的ICMP头，一共是84字节； 包头+内容不能大于65535，所以最大值为65507（linux:65507, windows:65500）； |
>|    -t ttl     | 设置TTL(Time To Live)为指定的值。该字段指定IP包被路由器丢弃之前允许通过的最大网段数； |

* debian1

<img src="image\28.png" />

* kali-victim2

<img src="image\29.png" />

#### 所有节点均可以访问互联网

在每个虚拟机中输入指令`ping baidu.com`来查看是否能访问百度网站。由于百度网站的ip地址不存在于主机中，所以需先连接DNS域名服务器，再找到百度网站的ip地址，以此来访问互联网中的百度网站；而如果能访问到，则说明能访问互联网。

* 网关可访问互联网

<img src="image\30.png" />

* xp-victim2可以访问互联网

<img src="image\31.png" />

* xp-victim1可以访问互联网

<img src="image\32.png" />

* kali-victim2可以访问互联网

<img src="image\33.png" />

* debian1可以访问互联网

<img src="image\34.png" />

* kali-attack可以访问互联网

<img src="image\35.png" />

---

## 问题

* 无法多重加载虚拟硬盘

开始时对虚拟机进行了备份，未删除备份，在虚拟介质管理中也无法找到备份文件。删除备份后问题解决，多重加载成功

* 重载后部分虚拟机无法找到系统盘进行启动

由于未重新装载vdi导致，重新装载后可成功运行

* kali无法上网

按老师网站提供代码修改ip文件信息后重启网卡即可

* kali无法解析域名

修改resolv.conf，配置可以使用的DNS server

---

## 参考文献

* https://blog.csdn.net/weixin_42859280/article/details/89281862 （**kali linux解决：ping: www.baidu.com: 未知的名称或服务**） [dream_网络安全](https://me.csdn.net/weixin_42859280)

* https://blog.csdn.net/gechong123/article/details/80609598 （**Linux ping命令详解**）[gechong123](https://me.csdn.net/gechong123)

* http://sec.cuc.edu.cn/ftp/video/MobileInternetSecurity/2019/chap0x01/ **跟着视频操作后发现 Kali 安装完成后无法上网**

* https://www.runoob.com/linux/linux-vim.html **Linux   vi/vim**

  

