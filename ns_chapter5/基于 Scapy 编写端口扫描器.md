# 基于 Scapy 编写端口扫描器

## 实验目的

- 掌握网络扫描之端口状态探测的基本原理

## 实验环境

- python + [scapy](https://scapy.net/)

## 实验要求

- 禁止探测互联网上的 IP ，严格遵守网络安全相关法律法规
- 完成以下扫描技术的编程实现 
  - TCP connect scan / TCP stealth scan
  - TCP Xmas scan / TCP fin scan / TCP null scan
  - UDP scan
- 上述每种扫描技术的实现测试均需要测试端口状态为：`开放`、`关闭` 和 `过滤` 状态时的程序执行结果
- 提供每一次扫描测试的抓包结果并分析与课本中的扫描方法原理是否相符？如果不同，试分析原因；
- 在实验报告中详细说明实验网络环境拓扑、被测试 IP 的端口状态是如何模拟的
- （可选）复刻 `nmap` 的上述扫描技术实现的命令行参数开关

## 代码测试

* 构建如图所示网络拓扑结构，victim1与victim2在同一个内部网络，其中victim1在此充当攻击者，其中网关，攻击者的主机，受害者2的主机ip如图；

<img src="image\1.png" />

<img src="image\2.png" />

<img src="image\3.png" />

<img src="image\4.png" />

### TCP connect scan

（1）首先测试受害者主机关闭80端口时的测试结果，将源地址设为victim1的ip地址，目的地址设为victim2的ip地址

<img src="image\6.png" />

检测结果为端口为关闭状态

<img src="image\5.png" />

分析抓包结果，查看wireshark中捕获的数据包，发现由于是第一次查找此ip地址，故发出ARP请求查找其mac地址；然后再发送tcp数据包，受害者返回RST+ACK，说明受害者主机80端口为关闭状态close(sockfd)，直接丢弃接收缓冲区未读取的数据，并给攻击者主机发一个RST。说明端口处于关闭状态，与课本中一致。

<img src="image\7.png" />

（2）再令受害者主机使用netcat监听80端口，开启端口

```
nc -nvlp 80
```

<img src="image\8.png" />

此时再调用代码，测试结果如下图，检测到端口80为打开状态

<img src="image\9.png" />

查看wireshark中的抓包结果，可以看到发出了一个SYN的请求包，收到了SYN/ACK，然后又发出RST与RST的ACK断开三次握手连接，与课本中描述一致，说明端口处于开启状态

<img src="image\10.png" />

（3）修改victim2的防火墙规则，将80端口接收到的包全部丢弃，则此时victim2主机处于过滤状态

<img src="image\11.png" />

再调用代码，测试结果如下，端口处于closed1（过滤状态）

<img src="image\12.png" />

分析捕获到的数据包，发现发出的TCP包无任何回应，说明端口处于过滤状态，与课本中描写一致。

<img src="image\13.png" />

### TCP stealth scan

（1）修改防火墙规则，允许80端口的数据包输入，由于未开启80端口监听，端口仍未关闭状态

```
iptables -A INPUT -p tcp –dport 80 -j ACCEPT 
```

<img src="image\16.png" />

分析抓包结果与课本描述一致

<img src="image\17.png" />

（2）令受害者主机使用netcat监听80端口，开启端口

<img src="image\8.png" />

代码测试结果为open

<img src="image\18.png" />

分析数据包，发送握手请求后受害者主机返回ACK建立连接，建立连接后攻击者主机立刻发送64741端口与41493端口断开连接的数据包断开连接，与课本描述一致

<img src="image\19.png" />

（3）修改防火墙拒绝ICMP请求包

<img src="image\21.png" />

运行代码，显示端口处于过滤状态

<img src="image\20.png" />

分析数据包，发现防火墙拒绝ICMP包后，攻击者主机试图向受害者主机发送ICMP 数据包,以确定目标 IP 地址是否存活，而受害者主机关闭此端口后，该端口无法抵达，访问失败，受害者主机返回数据包结果为端口不可达，与课本中描述一致

<img src="image\22.png" />

### TCP Xmas scan

（1）端口关闭状态，受害者主机未打开端口

测试结果为关闭

<img src="image\23.png" />

分析包，可看到Xmas 发送一个 TCP 包，并对 TCP 报文头 FIN、URG 和 PUSH 标记进行设置。关闭的端口则响应 RST 报文

<img src="image\24.png" />

（2）端口开启状态

受害者主机开启80端口

<img src="image\25.png" />

调用代码，测试结果为过滤或开启（由于这两个状态均不回复数据包，结果一致）

<img src="image\26.png" />

分析数据包，发现攻击者主机发出TCP请求后没有收到回复，无响应

<img src="image\27.png" />

（3）端口过滤状态

过滤掉80端口的数据包

```
iptables -A INPUT -p tcp --dport 80 -j DROP
```

<img src="image\28.png" />

调用代码，重新捕获数据，结果为打开或过滤

<img src="image\30.png" />

分析捕获到的数据包，发现无回应

<img src="image\29.png" />

### TCP fin scan

（1）端口关闭，测试正确

<img src="image\31.png" />

分析包数据，攻击者主机发出fin包，发现受害者主机返回RST包，与课本无差别

<img src="image\32.png" />

（2）端口开启

测试结果为开启

<img src="image\33.png" />

发出fin数据包，无返回数据包

<img src="image\34.png" />

（3）端口过滤

测试结果为打开或过滤

<img src="image\35.png" />

仅发送 FIN 包，它可以直接通过防火墙，端口是开放或过滤状态则对 FIN 包没有任何响应

<img src="image\36.png" />

### TCP null scan

（1）端口关闭

测试结果正确

<img src="image\37.png" />

发送一个数据包，关闭所有 TCP 报文头标记（<None>)，由于端口关闭，返回RST数据包

<img src="image\38.png" />

（2）端口开启

测试结果正确

<img src="image\39.png" />

发送TCP报头标记为空的数据包后无返回数据包

<img src="image\40.png" />

（3）端口过滤

靶机过滤掉80端口数据包

测试结果正确

<img src="image\41.png" />

分析数据包，无返回数据包

<img src="image\42.png" />

### UDP scan

（1）端口关闭

测试结果为关闭

<img src="image\43.png" />

向靶机发送udp包，发现返回ICMP无法抵达包，无法访问，在大多数情况下，当向一个未开放的 UDP 端口发送数据时,其主机就会返回一个 ICMP 不可到达(ICMP_PORT_UNREACHABLE)的错误，因此大多数 UDP 端口扫描的方法就是向各个被扫描的 UDP 端口发送零字节的 UDP 数据包，如果收到一个 ICMP 不可到达的回应，那么则认为这个端口是关闭的

<img src="image\44.png" />

（2）端口开启

使用 python socket 编程临时开启 udp server，源码如下:

```python
from socket import *
from time import ctime

host = ''
port = 53
bufsize = 1024
addr = (host,port)

udpServer = socket(AF_INET,SOCK_DGRAM)
udpServer.bind(addr)

while True:
	#print('Waiting for connection...')
	data,addr = udpServer.recvfrom(bufsize)
	data  = data.decode(encoding='utf-8').upper()
	#data = "at %s :%s"%(ctime(),data)
	#print('recv', data)
	udpServer.sendto(data.encode(encoding='utf-8'),addr)
	break
udpServer.close()
print("yes")
```

在受害者主机启动UDP53端口服务

<img src="image\45.png" />

重新调用代码，结果如下，打开状态

<img src="image\46.png" />

查看包，向靶机发送一个长度为0的UDP数据包，靶机返回一个长度为0的UDP数据包，然后攻击者主机由于未打开53端口UDP服务，所以会向靶机发送一个ICMP不可达的数据包

<img src="image\47.png" />

（3）端口过滤

```
iptables -A INPUT -p tcp --dport 53 -j DROP
```

<img src="image\48.png" />

重新调用此代码，端口为过滤状态

<img src="image\49.png" />

查看数据包，与closed相同，向靶机发送一个长度为0的UDP数据包，发现返回ICMP无法抵达包，无法访问

<img src="image\50.png" />

### 复刻 `nmap` 的上述扫描技术实现的命令行参数开关

```
nmap ip//nmap 扫描 tcp服务
nmap -sU ip - p 80//nmap 扫描udp服务80
nmap -sU ip - p 53//nmap 扫描udp服务53
nmap  172.16.222.138//扫描该主机端口服务是否开启
nmap -sT -P 80 -T4 -n -vv 172.16.222.138//Tcp connect 
nmap -sS -P 80 -T4 -n -vv 172.16.222.138//TCP stealth scan
nmap -sX -P 80 -T4 -n -vv 172.16.222.138//XMAS scan
nmap -sF -P 80 -T4 -n -vv 172.16.222.138//FIN scan
nmap -sN -P 80 -T4 -n -vv 172.16.222.138//NULL scan
nmap -sU -P 53 -T4 -n -vv 172.16.222.138//UDP scan
```



```
root@bogon:~# nmap -sS -P 22 -T4 -n -vv 10.0.2.6
Warning: The -P option is deprecated. Please use -PE
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-10 15:12 CST
setup_target: failed to determine route to 22 (0.0.0.22)
Initiating ARP Ping Scan at 15:12
Scanning 10.0.2.6 [1 port]
Completed ARP Ping Scan at 15:12, 0.00s elapsed (1 total hosts)
Initiating SYN Stealth Scan at 15:12
Scanning 10.0.2.6 [1000 ports]
Discovered open port 111/tcp on 10.0.2.6
Discovered open port 22/tcp on 10.0.2.6
Completed SYN Stealth Scan at 15:12, 0.06s elapsed (1000 total ports)
Nmap scan report for 10.0.2.6
Host is up, received arp-response (0.00011s latency).
Scanned at 2019-12-10 15:12:15 CST for 0s
Not shown: 998 closed ports
Reason: 998 resets
PORT    STATE SERVICE REASON
22/tcp  open  ssh     syn-ack ttl 64
111/tcp open  rpcbind syn-ack ttl 64
MAC Address: 08:00:27:CE:0A:50 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds
           Raw packets sent: 1001 (44.028KB) | Rcvd: 1001 (40.036KB)
root@bogon:~# nmap -sX -P 22 -T4 -n -vv 10.0.2.6
Warning: The -P option is deprecated. Please use -PE
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-10 15:12 CST
setup_target: failed to determine route to 22 (0.0.0.22)
Initiating ARP Ping Scan at 15:12
Scanning 10.0.2.6 [1 port]
Completed ARP Ping Scan at 15:12, 0.00s elapsed (1 total hosts)
Initiating XMAS Scan at 15:12
Scanning 10.0.2.6 [1000 ports]
Completed XMAS Scan at 15:12, 1.21s elapsed (1000 total ports)
Nmap scan report for 10.0.2.6
Host is up, received arp-response (0.00012s latency).
Scanned at 2019-12-10 15:12:33 CST for 1s
Not shown: 998 closed ports
Reason: 998 resets
PORT    STATE         SERVICE REASON
22/tcp  open|filtered ssh     no-response
111/tcp open|filtered rpcbind no-response
MAC Address: 08:00:27:CE:0A:50 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1.26 seconds
           Raw packets sent: 1003 (40.108KB) | Rcvd: 999 (39.948KB)
root@bogon:~# nmap -sF -P 22 -T4 -n -vv 10.0.2.6
Warning: The -P option is deprecated. Please use -PE
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-10 15:12 CST
setup_target: failed to determine route to 22 (0.0.0.22)
Initiating ARP Ping Scan at 15:12
Scanning 10.0.2.6 [1 port]
Completed ARP Ping Scan at 15:12, 0.00s elapsed (1 total hosts)
Initiating FIN Scan at 15:12
Scanning 10.0.2.6 [1000 ports]
Completed FIN Scan at 15:12, 1.21s elapsed (1000 total ports)
Nmap scan report for 10.0.2.6
Host is up, received arp-response (0.00015s latency).
Scanned at 2019-12-10 15:12:44 CST for 1s
Not shown: 998 closed ports
Reason: 998 resets
PORT    STATE         SERVICE REASON
22/tcp  open|filtered ssh     no-response
111/tcp open|filtered rpcbind no-response
MAC Address: 08:00:27:CE:0A:50 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1.28 seconds
           Raw packets sent: 1003 (40.108KB) | Rcvd: 999 (39.948KB)
root@bogon:~# nmap -sN -P 22 -T4 -n -vv 10.0.2.6
Warning: The -P option is deprecated. Please use -PE
Starting Nmap 7.80 ( https://nmap.org ) at 2019-12-10 15:12 CST
setup_target: failed to determine route to 22 (0.0.0.22)
Initiating ARP Ping Scan at 15:12
Scanning 10.0.2.6 [1 port]
Completed ARP Ping Scan at 15:12, 0.00s elapsed (1 total hosts)
Initiating NULL Scan at 15:12
Scanning 10.0.2.6 [1000 ports]
Completed NULL Scan at 15:12, 1.21s elapsed (1000 total ports)
Nmap scan report for 10.0.2.6
Host is up, received arp-response (0.000094s latency).
Scanned at 2019-12-10 15:12:52 CST for 2s
Not shown: 998 closed ports
Reason: 998 resets
PORT    STATE         SERVICE REASON
22/tcp  open|filtered ssh     no-response
111/tcp open|filtered rpcbind no-response
MAC Address: 08:00:27:CE:0A:50 (Oracle VirtualBox virtual NIC)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1.31 seconds
           Raw packets sent: 1003 (40.108KB) | Rcvd: 999 (39.948KB)
```



## 参考资料

1.https://github.com/CUCCS/2018-NS-Public-DcmTruman/blob/ns_chap5/ns/ns_chap5/实验报告.md

2.https://blog.csdn.net/jackcily/article/details/83117884

3.https://resources.infosecinstitute.com/port-scanning-using-scapy/

4.http://www.doc88.com/p-991971261076.html （**网络安全003ppt**）

5.https://blog.csdn.net/qq_42103479/article/details/90111365 （**Linux kali开启端口、关闭防火墙方法**）

6.https://blog.csdn.net/jrunw/article/details/70339712 （**TCP/IP详解--发送ACK和RST的场景**）

